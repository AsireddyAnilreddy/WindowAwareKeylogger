import sqlite3


def view_logs():
    conn = sqlite3.connect("keylogs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, window_title, sentence FROM logs ORDER BY id DESC")
    rows = cursor.fetchall()

    print("📝 Keylogger Logs:\n")
    for row in rows:
        timestamp, window_title, sentence = row
        print(f"[{timestamp}] ({window_title}): {sentence}")

    conn.close()


if __name__ == "__main__":
    view_logs()
