import pandas as pd
from datetime import datetime, timedelta

class Schichtplaner:
    def __init__(self):

        # Klassifizieren der Personen
        self.expert = ["Dirk", "Thomas", "Kevin", "Detlef"]
        self.springer = ["Detlef"]
        self.unerfahren = ["Steve", "Lasse", "Stefan"]

        # Wachwechsel alle 3:30 Stunden, Startzeit und Endzeit festlegen
        self.start = datetime(2023, 7, 15, 13, 0)
        self.end = datetime(2023, 7, 26, 22, 0)
        self.delta = timedelta(hours=3, minutes=30)

    def erstellen_plan(self):
        # Leere Liste für Daten erstellen
        data = []

        # Zuordnung der Wachen
        while self.start <= self.end:
            if len(self.expert) > 0:
                expert1 = self.expert.pop(0)
                if len(self.springer) > 0 and expert1 == "Detlef":
                    unerf1 = self.unerfahren.pop(0)
                    data.append([self.start, expert1, unerf1])
                    self.unerfahren.append(unerf1)
                else:
                    spring1 = self.springer.pop(0)
                    data.append([self.start, expert1, spring1])
                    self.springer.append(spring1)
                self.expert.append(expert1)
            self.start += self.delta

        return data

    def speichern_csv(self, data):
        # DataFrame erstellen und als CSV speichern
        df = pd.DataFrame(data, columns=["Schichtbeginn", "Wachperson I", "Wachperson II"])
        df.to_csv("schichtplan.csv", index=False)

if __name__ == "__main__":
    schichtplaner = Schichtplaner()
    data = schichtplaner.erstellen_plan()
    schichtplaner.speichern_csv(data)
