import datetime, time


class AlarmScheduler:
    def __init__(self):
        self.alarms = []

    def get_alarm_times(self):
        return self.alarms

    def set_alarm(self, alarm_time: str, label: str = ""):
        try:
            alarm_dt = datetime.datetime.strptime(alarm_time, "%Y-%m-%d %H:%M:%S")
            self.alarms.append([alarm_dt, label])
            print(f"Alarm set for {alarm_dt} with label '{label}'")
        except ValueError:
            print("❌ Invalid time format. Use YYYY-MM-DD HH:MM:SS")

    def remove_alarm(self, alarm_time: datetime.datetime):
        for i in self.alarms:
            if i[0] == alarm_time:
                self.alarms.remove(i)
                print(f"✅ Alarm for {alarm_time} removed")
                return
        print(f"⚠️ No alarm found for {alarm_time}")

    def check_alarm(self):
        current_time = datetime.datetime.now()
        for i in self.alarms:
            if current_time >= i[0]:
                print(f"🔔 Alarm! {i[1]}")
                time.sleep(5)  # simulate ringing
                self.remove_alarm(i[0])
                return True
        return False


if __name__ == "__main__":
    alarm = AlarmScheduler()
    alarm.set_alarm("2025-07-03 19:00:00", "Meeting")

    while True:
        if alarm.check_alarm():
            break
        time.sleep(1)
