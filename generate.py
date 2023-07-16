import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
import pytz
from ics import Calendar, Event

class Schichtplaner:
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

        # Wachwechsel alle 3:30 Stunden, Startzeit und Endzeit festlegen
        self.startdatum = datetime(2023, 7, 15, 14, 0)
        self.enddatum = datetime(2023, 7, 26, 22, 0)
        self.delta = timedelta(hours=3, minutes=30)

    def top_erfahrensten_segler(self, n=4):
        self.crew = sorted(self.crew, key=lambda k: int(k['experience']), reverse=True)
        return self.crew[:n]

    def mindest_erfahrenen_segler(self, n=4):
        self.crew.sort(key=lambda segler: int(segler['experience']))
        return self.crew[:n]

    def segler_mit_min_watch_count(self,wachpersonal):
        return min(wachpersonal, key=lambda segler: segler['watch_count'])

    def zweit_geringsten_watch_count(self,wachpersonal):
        wachpersonal.sort(key=lambda segler: segler['watch_count'])
        return wachpersonal[1]

    def erstellen_plan(self):
        # Leere Liste für Daten erstellen
        data = []
        
        # Diese Variable wird genutzt um startdatum weiter als eindeutige Variable zu haben
        current_datum = self.startdatum

        # Iterriere von Startdatum bis Enddatum
        while current_datum <= self.enddatum:
            erfahrenes_wachpersonal=self.top_erfahrensten_segler()
            wache1=self.segler_mit_min_watch_count(erfahrenes_wachpersonal)
            unerfahrenes_wachpersonal=self.mindest_erfahrenen_segler()
            wache2=self.segler_mit_min_watch_count(unerfahrenes_wachpersonal)
            if wache1 == wache2: 
                wache2=self.zweit_geringsten_watch_count(unerfahrenes_wachpersonal)
            data.append(
                [
                    current_datum,
                    current_datum.astimezone(pytz.timezone('Europe/Lisbon')),
                    current_datum.astimezone(pytz.timezone('Europe/Berlin')),
                    wache1["name"],
                    wache2["name"]
                ]
            )
            wache1["watch_count"] += 1
            wache2["watch_count"] += 1
            current_datum += self.delta
        return data

    def speichern_csv(self, data):
        # DataFrame erstellen und als CSV speichern
        df = pd.DataFrame(data, columns=["UTC","WEST","CEST","Wache I", "Wache II"])
        df.to_csv("schichtplan.csv", index=False)
    
    def erstellen_ical(self, data):
        # Ein ics-Kalender für jede Person erstellen
        crew_names = [person['name'] for person in self.crew]
        for name in crew_names:
            c = Calendar()
            for datum in data:
                if name in datum[3:5]:  # Wache I oder Wache II
                    e = Event()
                    e.name = "Wache"
                    e.begin = datum[0].strftime("%Y%m%d %H%M%S")  # Datum und Uhrzeit formatieren
                    e.duration = timedelta(hours=3, minutes=30)
                    c.events.add(e)
            # Speichern Sie die ics-Datei mit dem Namen der Person
            with open(f'{name}.ics', 'w') as my_file:
                my_file.writelines(c)

if __name__ == "__main__":
    schichtplaner = Schichtplaner()
    data = schichtplaner.erstellen_plan()
    schichtplaner.speichern_csv(data)
    schichtplaner.erstellen_ical(data)
    print(schichtplaner.crew)
