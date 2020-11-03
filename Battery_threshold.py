#!/usr/bin/env python
import os
import sys
from tkinter import messagebox
import tkinter

class Battery:
    """This is a Battery Threshold Changer for Linux Ubuntu 20.04.01,
    tested with Asus UX534FTC, made it to change quickly for optimal battery threshold.
    """
    def __init__(self):
        if self.get_super_user_access():
            return
        self.window = tkinter.Tk()
        self.window.title("Battery Threshold Changer")
        self.frame1 = tkinter.Frame(
            master = self.window,
            relief=tkinter.RAISED,
            borderwidth=1
        )
        self.file = "/sys/class/power_supply/BAT0/charge_control_end_threshold"
        self.frame1.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        self.label = tkinter.Label(master=self.frame1, width=40, height=5)
        self.get_battery_threshold()
        self.label.pack()
        for y in range(0, 4):
            self.frame2 = tkinter.Frame(
                master=self.window,
                relief=tkinter.RAISED,
                borderwidth=1
            )
            self.frame2.grid(row=1, column=y, padx=5, pady=5)
            self.button = tkinter.Button(master=self.frame2, text=f"Change battery \nthreshold to {int((y + 1.5) * 20 // 1)}", command=lambda y = y: self.change_threshold_to(str(int((y + 1.5) * 20 // 1))))
            self.button.pack()
        self.window.mainloop()
        
    def get_super_user_access(self):
        euid = os.geteuid()
        if euid != 0:
            print("Script not started as root. Running sudo..")
            args = ['sudo', sys.executable] + sys.argv + [os.environ]
            # the next line replaces the currently-running process with the sudo
            os.execlpe('sudo', *args)
            return True
    
    def get_battery_threshold(self):
        with open(self.file, 'r') as file:
            self.label['text'] = "Battery threshold is set now at:\n " + file.readline()
    
    def change_threshold_to(self, to_what):
        try:
            with open(self.file, 'w') as file:
                file.write(to_what)
            self.get_battery_threshold()
        except Exception as excep:
            messagebox.showerror("Encountered a problem while writing to a file", excep)

if __name__ == "__main__":
    Battery()