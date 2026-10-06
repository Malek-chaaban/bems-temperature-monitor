BEMS Temperature Monitor

I made this to learn a bit about how fault detection works in a BEMS.
It's a small Python program that makes up temperature readings for a
few rooms in a building and checks if any of them go out of range.

I used AI to help me get started and to understand how the code works.

What it does:
- Makes a day of fake temperature readings (one every 15 minutes) for
  3 rooms: Office, Server Room and Meeting Room
- Checks each reading against that room's min and max temperature
- Flags a sustained fault if a room stays out of range for an hour or more
- Prints a report with the min, max and average temperature for each
  room, how many readings were out of range, and any faults found

How to run it:
1. Run generate_data.py (this makes readings.csv)
2. Run monitor.py (this prints the report and saves it as report.txt)

You just need Python 3, nothing else to install.

What you should see:
I put two faults into the fake data to check the monitor catches them:
- Server Room goes too hot from 13:00 to 14:45 (like a cooling failure)
- Meeting Room goes too cold from 04:00 to 06:45 (like the heating being off)

The Office stays in range, so it shows as OK.

Things I learned:
- How to read a CSV file and group the data by room
- Using loops and functions to check readings against limits
- Why you'd only flag a fault after a few bad readings in a row, so a
  single odd reading doesn't set off an alarm

Things I want to add:
- Graphs of the temperatures
- Email alerts when there's a fault
- Try reading real data from controllers (BACnet or Modbus)
