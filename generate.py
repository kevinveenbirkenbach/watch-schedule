import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
from ics import Calendar, Event, DisplayAlarm

class ShiftPlanner:
    def __init__(self, json_file):
        with open(json_file) as f:
            data = json.load(f)

        self.crew = data['crew']
        self.start_date = datetime.strptime(data['start_date'], "%Y-%m-%d %H:%M")
        self.end_date = datetime.strptime(data['end_date'], "%Y-%m-%d %H:%M")
        hours, minutes = map(int, data['shiftduration'].split(':'))
        self.delta = timedelta(hours=hours, minutes=minutes)
        self.description = data['description']
        self.depature_location = data['depature_location']
        self.arrival_location = data['arrival_location']
        self.ship_name = data['ship_name']

    def top_most_experienced_sailors(self, n=4):
        return sorted(self.crew, key=lambda k: int(k['experience']), reverse=True)[:n]

    def least_experienced_sailors(self, n=4):
        return sorted(self.crew, key=lambda k: int(k['experience']))[:n]

    def sailor_with_min_watch_count(self, watch_staff):
        return min(watch_staff, key=lambda sailor: sailor['watch_count'])

    def second_lowest_watch_count(self, watch_staff):
        return sorted(watch_staff, key=lambda sailor: sailor['watch_count'])[1]

    def create_plan(self):
        data = []
        current_date = self.start_date

        while current_date <= self.end_date:
            experienced_watch_staff = self.top_most_experienced_sailors()
            watch1 = self.sailor_with_min_watch_count(experienced_watch_staff)
            inexperienced_watch_staff = self.least_experienced_sailors()
            watch2 = self.sailor_with_min_watch_count(inexperienced_watch_staff)
            if watch1 == watch2: 
                watch2 = self.second_lowest_watch_count(inexperienced_watch_staff)
            data.append(
                [
                    current_date,
                    current_date.astimezone(pytz.timezone('Europe/Lisbon')),
                    current_date.astimezone(pytz.timezone('Europe/Berlin')),
                    watch1["name"],
                    watch2["name"]
                ]
            )
            watch1["watch_count"] += 1
            watch2["watch_count"] += 1
            current_date += self.delta
        return data

    def save_csv(self, data):
        df = pd.DataFrame(data, columns=["UTC","WEST","CEST","Watch I", "Watch II"])
        df.to_csv("shift_plan.csv", index=False)
    
    def create_ical(self, data):
        for person in self.crew:
            c = Calendar()
            name = person['name']
            alert_time = person['alert_time']
            for datum in data:
                if name in datum[3:5]:
                    watch_num = "Watch I" if name == datum[3] else "Watch II"
                    e = Event()
                    e.name = f"{watch_num}({name}) on {self.ship_name}"
                    e.begin = datum[0].strftime("%Y%m%d %H%M%S")
                    e.description = f"\nDescription: {self.description}\n"
                    e.location = f"{self.depature_location} to {self.arrival_location}"
                    e.duration = timedelta(hours=3, minutes=30)
                    alarm = DisplayAlarm(trigger=timedelta(seconds=-alert_time))
                    e.alarms.append(alarm)
                    c.events.add(e)
            with open(f'{name}.ics', 'w') as my_file:
                my_file.writelines(c)

if __name__ == "__main__":
    shift_planner = ShiftPlanner("description.json")
    data = shift_planner.create_plan()
    shift_planner.save_csv(data)
    shift_planner.create_ical(data)
    print(shift_planner.crew)
