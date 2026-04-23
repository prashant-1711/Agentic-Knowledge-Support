from db import engine

try:
    conn = engine.connect()
    print("✅ DB Connected successfully")
    conn.close()
except Exception as e:
    print(" Connection failed:", e)