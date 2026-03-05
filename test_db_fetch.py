import sys
import traceback
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

import main

try:
    print("Fetching slots from PostgreSQL...")
    conn = main.get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT s.id, s.start_time, s.end_time, s.is_booked,
               b.user_name, b.user_email
        FROM   slots s
        LEFT JOIN bookings b ON b.slot_id = s.id
        ORDER  BY s.start_time
    """)
    slots = cursor.fetchall()
    print('Slots count:', len(slots))
    if len(slots) > 0:
        print('First slot:', slots[0])
    cursor.close()
    main._pool.putconn(conn)
except Exception as e:
    traceback.print_exc()
