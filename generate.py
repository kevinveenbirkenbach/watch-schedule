import pandas as pd
from datetime import datetime, timedelta
import pytz
from ics import Calendar, Event

class ShiftPlanner:
    def __init__(self, crew, start_date, end_date, delta):
        self.crew = crew
        self.start_date = start_date
        self.end_date = end_date
        self.delta = delta

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
        for name in [person['name'] for person in self.crew]:
            c = Calendar()
            for datum in data:
                if name in datum[3:5]:  
                    e = Event()
                    e.name = "Watch"
                    e.begin = datum[0].strftime("%Y%m%d %H%M%S")  
                    e.duration = timedelta(hours=3, minutes=30)
                    c.events.add(e)
            with open(f'{name}.ics', 'w') as my_file:
                my_file.writelines(c)

if __name__ == "__main__":
    crew = [
        {"name":"Dirk","experience":"10","watch_count":0},
        {"name":"Thomas","experience":"8","watch_count":0},
        {"name":"Kevin","experience":"8","watch_count":0},
        {"name":"Detlef","experience":"6","watch_count":0},
        {"name":"Steve","experience":"2","watch_count":0},
        {"name":"Lasse","experience":"4","watch_count":0},
        {"name":"Stefan","experience":"5","watch_count":0}
    ]
    start_date = datetime(2023, 7, 15, 14, 0)
    end_date = datetime(2023, 7, 26, 22, 0)
    delta = timedelta(hours=3, minutes=30)

    shift_planner = ShiftPlanner(crew, start_date, end_date, delta)
    data = shift_planner.create_plan()
    shift_planner.save_csv(data)
    shift_planner.create_ical(data)
    print(shift_planner.crew)
