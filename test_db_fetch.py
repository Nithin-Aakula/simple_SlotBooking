import sys
import traceback

try:
    import main
    conn = main.get_db()
    cursor = conn.cursor(dictionary=True)
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
        print('First slot start_time:', type(slots[0]['start_time']), slots[0]['start_time'])
    cursor.close()
    conn.close()
except Exception as e:
    traceback.print_exc()
