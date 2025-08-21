import tkinter as tk
from tkinter import ttk
from Phidget22.Devices.DigitalOutput import *
import time


class RelayController:
    def __init__(self, channel):
        self.relay = DigitalOutput()
        self.relay.setChannel(channel)
        self.relay.openWaitForAttachment(5000)

        self.state = False  # False = OFF, True = ON
        self.toggle_count = 0
        self.on_time = 1000   # ms
        self.off_time = 1000  # ms
        self.running = False

        # Time tracking
        self.total_on_time = 0.0
        self.total_off_time = 0.0
        self.last_state_change_timestamp = None
        self.started = False  # Becomes True after first ON

    def toggle(self, force_on=False):
        """Toggle relay ON/OFF and update timers"""
        now = time.time()

        if self.last_state_change_timestamp is not None:
            elapsed = now - self.last_state_change_timestamp
            if self.state:
                self.total_on_time += elapsed
            elif self.started:  # Count OFF only after first ON
                self.total_off_time += elapsed

        # Switch state
        if force_on:
            self.state = True
        else:
            self.state = not self.state

        if self.state:
            self.relay.setDutyCycle(1.0)
            self.started = True  # Now OFF timer can start later
        else:
            self.relay.setDutyCycle(0.0)

        self.toggle_count += 1
        self.last_state_change_timestamp = now

        return self.state, self.toggle_count

    def stop(self):
        """Stop and turn relay OFF, update timers"""
        now = time.time()
        if self.last_state_change_timestamp is not None:
            elapsed = now - self.last_state_change_timestamp
            if self.state:
                self.total_on_time += elapsed
            elif self.started:
                self.total_off_time += elapsed

        self.running = False
        self.relay.setDutyCycle(0.0)
        self.state = False
        self.last_state_change_timestamp = now

    def reset(self):
        """Reset counters and timers"""
        self.toggle_count = 0
        self.total_on_time = 0.0
        self.total_off_time = 0.0
        self.last_state_change_timestamp = None
        self.started = False

    def close(self):
        self.stop()
        self.relay.close()


class PhidgetRelayGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PhidgetInterfaceKit 0/0/4 Control with Timer")
        self.root.geometry("700x470")

        self.controllers = [RelayController(i) for i in range(4)]
        self.widgets = []

        for i in range(4):
            frame = ttk.LabelFrame(root, text=f"Relay {i}", padding=10)
            frame.pack(fill="x", padx=10, pady=5)

            btn = tk.Button(frame, text="OFF", width=12, bg="red", fg="white",
                            command=lambda idx=i: self.manual_toggle(idx))
            btn.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

            tk.Label(frame, text="ON Time (s):").grid(row=0, column=1, sticky="e")
            on_entry = tk.Entry(frame, width=5)
            on_entry.insert(0, "1")
            on_entry.grid(row=0, column=2, padx=5)

            tk.Label(frame, text="OFF Time (s):").grid(row=1, column=1, sticky="e")
            off_entry = tk.Entry(frame, width=5)
            off_entry.insert(0, "1")
            off_entry.grid(row=1, column=2, padx=5)

            start_btn = tk.Button(frame, text="Start Timer", width=12,
                                  command=lambda idx=i: self.start_timer(idx))
            start_btn.grid(row=0, column=3, padx=5)

            stop_btn = tk.Button(frame, text="Stop Timer", width=12,
                                 command=lambda idx=i: self.stop_timer(idx))
            stop_btn.grid(row=1, column=3, padx=5)

            reset_btn = tk.Button(frame, text="Reset Counter", width=12,
                                  command=lambda idx=i: self.reset_counter(idx))
            reset_btn.grid(row=0, column=4, padx=5, rowspan=2)

            counter_lbl = tk.Label(frame, text="Toggles: 0")
            counter_lbl.grid(row=0, column=5, rowspan=2, padx=10)

            time_lbl = tk.Label(frame, text="ON: 0.0s | OFF: 0.0s")
            time_lbl.grid(row=0, column=6, rowspan=2, padx=10)

            self.widgets.append({
                "button": btn,
                "on_entry": on_entry,
                "off_entry": off_entry,
                "counter": counter_lbl,
                "time": time_lbl
            })

        tk.Button(root, text="Exit", width=20, height=2, command=self.cleanup).pack(pady=10)

        # Update timers every 1s
        self.update_timers()

    def manual_toggle(self, idx):
        controller = self.controllers[idx]
        state, count = controller.toggle()
        btn = self.widgets[idx]["button"]
        btn.config(text="ON" if state else "OFF", bg="green" if state else "red")
        self.widgets[idx]["counter"].config(text=f"Toggles: {count}")

    def start_timer(self, idx):
        controller = self.controllers[idx]
        try:
            controller.on_time = int(float(self.widgets[idx]["on_entry"].get()) * 1000)
            controller.off_time = int(float(self.widgets[idx]["off_entry"].get()) * 1000)
        except ValueError:
            return

        controller.running = True
        # Force first state to ON
        controller.toggle(force_on=True)
        self.widgets[idx]["button"].config(text="ON", bg="green")
        self.run_timer(idx)

    def run_timer(self, idx):
        controller = self.controllers[idx]
        if not controller.running:
            return

        state, count = controller.toggle()
        btn = self.widgets[idx]["button"]
        btn.config(text="ON" if state else "OFF", bg="green" if state else "red")
        self.widgets[idx]["counter"].config(text=f"Toggles: {count}")

        delay = controller.on_time if state else controller.off_time
        self.root.after(delay, lambda: self.run_timer(idx))

    def stop_timer(self, idx):
        self.controllers[idx].stop()
        btn = self.widgets[idx]["button"]
        btn.config(text="OFF", bg="red")
        self.widgets[idx]["counter"].config(text=f"Toggles: {self.controllers[idx].toggle_count}")

    def reset_counter(self, idx):
        controller = self.controllers[idx]
        controller.reset()
        self.widgets[idx]["counter"].config(text="Toggles: 0")
        self.widgets[idx]["time"].config(text="ON: 0.0s | OFF: 0.0s")

    def update_timers(self):
        """Update total ON/OFF time display"""
        now = time.time()
        for i, controller in enumerate(self.controllers):
            if controller.last_state_change_timestamp is None:
                continue

            elapsed = now - controller.last_state_change_timestamp
            total_on = controller.total_on_time + (elapsed if controller.state else 0)
            total_off = controller.total_off_time + (elapsed if (not controller.state and controller.started) else 0)
            self.widgets[i]["time"].config(
                text=f"ON: {total_on:.1f}s | OFF: {total_off:.1f}s"
            )
        self.root.after(1000, self.update_timers)

    def cleanup(self):
        for controller in self.controllers:
            controller.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PhidgetRelayGUI(root)
    root.mainloop()
