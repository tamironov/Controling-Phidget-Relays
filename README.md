PhidgetInterfaceKit 0/0/4 Relay Controller with Timer

A Python GUI application (Tkinter) for controlling the PhidgetInterfaceKit 0/0/4 relay board.
This tool provides both manual relay toggling and automated on/off timing control with counters and time tracking.
<img width="403" height="283" alt="GUI1" src="https://github.com/user-attachments/assets/196cd2c9-4c48-4b4d-b18a-7564309ddcb1" />

**Features**
- Control up to 4 relays from a single window.
- Manual toggle: switch any relay ON/OFF with a button.
- Timer mode:
- Set independent ON time and OFF time for each relay.
- Automatic toggling between ON and OFF.
- Counters to track how many times each relay toggled.
- ON/OFF runtime statistics (total active/inactive time per relay).
- OFF-time counting starts only after the first ON cycle, ensuring accurate timing.
- Reset counters per relay.
- Safe shutdown: all relays switch OFF on exit.

<img width="704" height="503" alt="GUI3" src="https://github.com/user-attachments/assets/a30f07df-9e2a-40ef-80fe-c391b8842156" />

**GUI Layout**
Each relay has:
- ON/OFF button with color status (🟢 ON / 🔴 OFF).
- Input fields for ON/OFF time (in seconds).
- Start Timer / Stop Timer buttons.
- Reset Counter button.
- Labels showing:
- Number of toggles.
- Total ON and OFF time.

  **Requirements**
- Python 3.8+
- Phidget22 Python library (pip install Phidget22)
- Tkinter (included with most Python installations)

- 
