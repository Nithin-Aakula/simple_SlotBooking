import traceback
from dotenv import load_dotenv
load_dotenv()
try:
    import main
    conn = main.get_db()
    cur = conn.cursor()
    cur.execute('SELECT 1')
    print('OK')
except Exception as e:
    traceback.print_exc()
