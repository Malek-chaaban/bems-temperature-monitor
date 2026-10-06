"""
monitor.py
A simple BEMS-style temperature monitor.

It reads sensor logs from readings.csv, checks each room against its
allowed temperature range, and reports:
  - every reading that is out of range (alarms)
  - sustained faults (out of range for 4+ readings in a row, i.e. 1 hour+)
  - min / max / average temperature for each room
The results are printed and saved to report.txt.
"""
import csv
from collections import defaultdict

# Allowed temperature range for each room: (minimum, maximum) in degrees C
LIMITS = {
    "Office": (20.0, 24.0),
    "Server Room": (18.0, 24.0),
    "Meeting Room": (19.0, 24.0),
}

# How many bad readings in a row count as a sustained fault (4 x 15 min = 1 hour)
SUSTAINED_COUNT = 4


def load_readings(filename):
    """Read the CSV and group the readings by room."""
    data = defaultdict(list)
    with open(filename, newline="") as f:
        for row in csv.DictReader(f):
            data[row["room"]].append((row["timestamp"], float(row["temperature"])))
    return data


def check_room(room, readings):
    """Return (alarms, sustained_faults) for one room."""
    low, high = LIMITS[room]
    alarms = []
    faults = []
    run = []  # current run of consecutive out-of-range readings

    for timestamp, temp in readings:
        if temp < low or temp > high:
            reason = "TOO COLD" if temp < low else "TOO HOT"
            alarms.append((timestamp, temp, reason))
            run.append((timestamp, temp, reason))
        else:
            # Reading is normal, so the run has ended. Was it long enough to be a fault?
            if len(run) >= SUSTAINED_COUNT:
                faults.append(run)
            run = []

    if len(run) >= SUSTAINED_COUNT:  # run that lasted until the end of the data
        faults.append(run)

    return alarms, faults


def build_report(data):
    """Create the report as a list of text lines."""
    lines = ["BEMS TEMPERATURE REPORT", "=" * 40]

    for room, readings in data.items():
        temps = [t for _, t in readings]
        low, high = LIMITS[room]
        alarms, faults = check_room(room, readings)

        lines.append(f"\n{room} (allowed {low}-{high} C)")
        lines.append(
            f"  Min {min(temps):.1f} C | Max {max(temps):.1f} C | "
            f"Average {sum(temps) / len(temps):.1f} C"
        )
        lines.append(f"  Out-of-range readings: {len(alarms)}")

        for run in faults:
            start, end = run[0][0], run[-1][0]
            lines.append(
                f"  SUSTAINED FAULT: {run[0][2]} from {start} to {end} "
                f"({len(run)} readings)"
            )

        if not alarms:
            lines.append("  Status: OK")

    return lines


if __name__ == "__main__":
    data = load_readings("readings.csv")
    report = build_report(data)

    print("\n".join(report))

    with open("report.txt", "w") as f:
        f.write("\n".join(report))
    print("\nReport saved to report.txt")