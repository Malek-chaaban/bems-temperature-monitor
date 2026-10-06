"""
generate_data.py
Creates sample temperature readings, like data a BEMS would log from room sensors.
Run this first. It makes a file called readings.csv.
"""
import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # same "random" data every run, so results are repeatable

ROOMS = {
    # room name: normal temperature (degrees C)
    "Office": 22.0,
    "Server Room": 20.0,
    "Meeting Room": 21.0,
}

start = datetime(2026, 10, 12, 0, 0)  # midnight
readings = []

# One reading every 15 minutes for 24 hours = 96 readings per room
for i in range(96):
    time = start + timedelta(minutes=15 * i)
    for room, normal in ROOMS.items():
        temp = normal + random.uniform(-0.6, 0.6)  # small natural variation

        # Fault 1: server room cooling fails between 13:00 and 15:00
        if room == "Server Room" and 13 <= time.hour < 15:
            temp += 8

        # Fault 2: meeting room heating is off early in the morning
        if room == "Meeting Room" and 4 <= time.hour < 7:
            temp -= 4

        readings.append([time.strftime("%Y-%m-%d %H:%M"), room, round(temp, 1)])

with open("readings.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "room", "temperature"])
    writer.writerows(readings)

print(f"Created readings.csv with {len(readings)} readings.")