import datetime
import time
import sqlite3

class Alarm:
    def __init__(self, time_str, label=""):
        # Store as a datetime object, not a string
        self.time = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        self.label = label

# Class responsible for interacting with the SQLite alarm database
class AlarmScheduler:
    def __init__(self):
        # Connect to (or create) the database file
        conn = sqlite3.connect("alarms.db")

        # Create a cursor object
        cursor = conn.cursor()

        # Create the alarms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alarms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT NOT NULL,
                label TEXT,
                triggered INTEGER DEFAULT 0
            )
        ''')

        # Commit and close
        conn.commit()
        conn.close() # Always close DB connection after use

    def get_alarm_times(self):
        conn = sqlite3.connect("alarms.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM alarms")
        res = cursor.fetchall()
        
        conn.commit() # Save changes to the DB
        conn.close()
        
        return res

    def add_alarm(self, alarm: Alarm):
        conn = sqlite3.connect("alarms.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM alarms WHERE time = ? AND label = ?", (alarm.time, alarm.label))
        if cursor.fetchone():
            print("⚠️ Alarm already exists.")
        else:
            cursor.execute("INSERT INTO alarms (time, label) VALUES (?, ?)", (alarm.time, alarm.label))
            print(f"✅ Alarm set for {alarm.time} with label '{alarm.label}'")


        conn.commit()
        conn.close()


    def remove_alarm(self, time=None, label=None):
        conn = sqlite3.connect("alarms.db")
        cursor = conn.cursor()

        if time and label:
            query = "DELETE FROM alarms WHERE time = ? AND label = ?"
            cursor.execute(query, (time, label))
        elif time:
            query = "DELETE FROM alarms WHERE time = ?"
            cursor.execute(query, (time,))
        elif label:
            query = "DELETE FROM alarms WHERE label = ?"
            cursor.execute(query, (label,))
        else:
            print("⚠️ You must provide at least a time or a label to delete.")
            return
        
        conn.commit()
        conn.close()



    def check_alarms(self):
        conn = sqlite3.connect("alarms.db")
        cursor = conn.cursor()

        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            SELECT id, time, label FROM alarms
            WHERE time <= ? AND triggered = 0
        ''', (now,))

        due_alarms = cursor.fetchall()

        for alarm_id, alarm_time, label in due_alarms:
            print(f"🔔 Alarm! {label} at {alarm_time}")
        
            # cursor.execute("UPDATE alarms SET triggered = 1 where id = ?", (alarm_id,))
        
        # cursor.execute("DELETE FROM alarms WHERE triggered = 1")
        conn.commit()
        conn.close()



if __name__ == "__main__":
    # You could replace this with input(), voice command, or GUI later
    alarm = Alarm(time_str="2025-07-03 19:00:00", label="Meeting")
    clock = AlarmScheduler()
    clock.add_alarm(alarm)

    print(clock.get_alarm_times())

    i = 0
    while True:
        clock.check_alarms()
        time.sleep(5)
        if i == 4:
            clock.remove_alarm(label="Meeting")
            break
        i += 1
