"""
Slot Booking Web Application — FastAPI Backend
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from mysql.connector import pooling

# ── Load .env ────────────────────────────────────────────────
load_dotenv()

# ── App & Templates ──────────────────────────────────────────
app = FastAPI(title="Slot Booking System")
templates = Jinja2Templates(directory="templates")

# ── MySQL Connection Pool (lazy init) ────────────────────────
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "booking_system"),
}

_pool = None


def _get_pool():
    """Create the connection pool on first use (lazy)."""
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="booking_pool",
            pool_size=5,
            **DB_CONFIG,
        )
    return _pool


def get_db():
    """Grab a connection from the pool."""
    return _get_pool().get_connection()


# ── Routes ───────────────────────────────────────────────────

@app.get("/")
def index(request: Request, msg: str = "", error: str = ""):
    """Dashboard — show every slot, color-coded by availability."""
    slots = []
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT s.id, s.start_time, s.end_time, s.is_booked,
                   b.user_name, b.user_email
            FROM   slots s
            LEFT JOIN bookings b ON b.slot_id = s.id
            ORDER  BY s.start_time
            """
        )
        slots = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        import traceback
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
        error = error or f"Could not connect to the database. Error: {str(e)}"

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "slots": slots, "msg": msg, "error": error},
    )



@app.post("/book/{slot_id}")
def book_slot(
    slot_id: int,
    user_name: str = Form(...),
    user_email: str = Form(...),
):
    """Book a slot — wrapped in a transaction with SELECT … FOR UPDATE."""
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        # Lock the row to prevent double-booking
        cursor.execute(
            "SELECT id, is_booked FROM slots WHERE id = %s FOR UPDATE",
            (slot_id,),
        )
        slot = cursor.fetchone()

        if slot is None:
            conn.rollback()
            return RedirectResponse(
                url="/?error=Slot+not+found", status_code=303
            )

        if slot["is_booked"]:
            conn.rollback()
            return RedirectResponse(
                url="/?error=This+slot+is+already+booked", status_code=303
            )

        # Mark as booked
        cursor.execute(
            "UPDATE slots SET is_booked = TRUE WHERE id = %s", (slot_id,)
        )

        # Create booking record
        cursor.execute(
            """
            INSERT INTO bookings (slot_id, user_name, user_email)
            VALUES (%s, %s, %s)
            """,
            (slot_id, user_name, user_email),
        )

        conn.commit()
        return RedirectResponse(
            url="/?msg=Slot+booked+successfully!", status_code=303
        )

    except Exception:
        conn.rollback()
        return RedirectResponse(
            url="/?error=Something+went+wrong.+Please+try+again.",
            status_code=303,
        )
    finally:
        cursor.close()
        conn.close()
