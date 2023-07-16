import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import pytz
from ics import Calendar, Event

class ShiftPlanner:
    def __init__(self):

        self.crew   = [
            {"name":"Dirk","experience":"10","watch_count":0},
            {"name":"Thomas","experience":"8","watch_count":0},
            {"name":"Kevin","experience":"8","watch_count":0},
            {"name":"Detlef","experience":"6","watch_count":0},
            {"name":"Steve","experience":"2","watch_count":0},
            {"name":"Lasse","experience":"4","watch_count":0},
            {"name":"Stefan","experience":"5","watch_count":0}
        ]

        # Shift change every 3:30 hours, set start time and end time
        self.start_date = datetime(2023, 7, 15, 14, 0)
        self.end_date = datetime(2023, 7, 26, 22, 0)
        self.delta = timedelta(hours=3, minutes=30)

    def top_most_experienced_sailors(self, n=4):
        self.crew = sorted(self.crew, key=lambda k: int(k['experience']), reverse=True)
        return self.crew[:n]

    def least_experienced_sailors(self, n=4):
        self.crew.sort(key=lambda sailor: int(sailor['experience']))
        return self.crew[:n]

    def sailor_with_min_watch_count(self,watch_staff):
        return min(watch_staff, key=lambda sailor: sailor['watch_count'])

    def second_lowest_watch_count(self,watch_staff):
        watch_staff.sort(key=lambda sailor: sailor['watch_count'])
        return watch_staff[1]

    def create_plan(self):
        # Create empty list for data
        data = []
        
        # This variable is used to keep start_date further as a unique variable
        current_date = self.start_date

        # Iterate from start_date to end_date
        while current_date <= self.end_date:
            experienced_watch_staff=self.top_most_experienced_sailors()
            watch1=self.sailor_with_min_watch_count(experienced_watch_staff)
            inexperienced_watch_staff=self.least_experienced_sailors()
            watch2=self.sailor_with_min_watch_count(inexperienced_watch_staff)
            if watch1 == watch2: 
                watch2=self.second_lowest_watch_count(inexperienced_watch_staff)
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
        # Create DataFrame and save as CSV
        df = pd.DataFrame(data, columns=["UTC","WEST","CEST","Watch I", "Watch II"])
        df.to_csv("shift_plan.csv", index=False)
    
    def create_ical(self, data):
        # Create an ics calendar for each person
        crew_names = [person['name'] for person in self.crew]
        for name in crew_names:
            c = Calendar()
            for datum in data:
                if name in datum[3:5]:  # Watch I or Watch II
                    e = Event()
                    e.name = "Watch"
                    e.begin = datum[0].strftime("%Y%m%d %H%M%S")  # Format date and time
                    e.duration = timedelta(hours=3, minutes=30)
                    c.events.add(e)
            # Save the ics file with the person's name
            with open(f'{name}.ics', 'w') as my_file:
                my_file.writelines(c)

if __name__ == "__main__":
    shift_planner = ShiftPlanner()
    data = shift_planner.create_plan()
    shift_planner.save_csv(data)
    shift_planner.create_ical(data)
    print(shift_planner.crew)
