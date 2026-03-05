import traceback
from dotenv import load_dotenv
import os
import main

load_dotenv()

try:
    print("Attempting to connect to database...")
    conn = main.get_db()
    cur = conn.cursor()
    cur.execute('SELECT 1')
    result = cur.fetchone()
    print(f'Connection OK! Result: {result}')
    cur.close()
    main._pool.putconn(conn)
except Exception as e:
    print("Connection FAILED!")
    traceback.print_exc()
