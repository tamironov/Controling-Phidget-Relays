import tkinter as tk
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalOutput import *

class PhidgetRelayGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PhidgetInterfaceKit 0/0/4 Control")
        self.root.geometry("400x250")

        # Store relay objects and states
        self.relays = [DigitalOutput() for _ in range(4)]
        self.relay_states = [False, False, False, False]

        # Configure each relay
        for i in range(4):
            self.relays[i].setChannel(i)
            self.relays[i].openWaitForAttachment(5000)

        # Create buttons
        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text=f"Relay {i} OFF", width=20, height=2,
                            bg="red", fg="white",
                            command=lambda idx=i: self.toggle_relay(idx))
            btn.pack(pady=5)
            self.buttons.append(btn)

        # Exit button
        tk.Button(root, text="Exit", width=20, height=2, command=self.cleanup).pack(pady=10)

    def toggle_relay(self, idx):
        """Toggle a relay ON/OFF"""
        self.relay_states[idx] = not self.relay_states[idx]
        if self.relay_states[idx]:
            self.relays[idx].setDutyCycle(1.0)  # ON
            self.buttons[idx].config(text=f"Relay {idx} ON", bg="green")
        else:
            self.relays[idx].setDutyCycle(0.0)  # OFF
            self.buttons[idx].config(text=f"Relay {idx} OFF", bg="red")

    def cleanup(self):
        """Turn off and close relays before exiting"""
        for i in range(4):
            self.relays[i].setDutyCycle(0.0)
            self.relays[i].close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhidgetRelayGUI(root)
    root.mainloop()
