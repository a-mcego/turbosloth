import tkinter as tk
from tkinter import simpledialog
import csv
from datetime import datetime

def start_timer():
    global start_time, running
    if running:
        stop_timer()
    running = True
    start_time = datetime.now()
    entry_name.config(state=tk.NORMAL)
    log_time("start", 0.0, entry_name.get())
    update_status("Timer started...")
    update_timer()

def stop_timer():
    global running
    if not running:
        start_timer()
    running = False
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    log_time("end", duration, entry_name.get())
    update_status("Timer stopped.")
    timer_label.config(text="00:00:00")

def update_timer():
    if running:
        elapsed_time = datetime.now() - start_time
        hours, remainder = divmod(int(elapsed_time.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        timer_label.config(text="{:02}:{:02}:{:02}".format(hours, minutes, seconds))
        root.after(1000, update_timer)  # Schedule the next update in 1 second.

def update_status(message):
    status_label.config(text=message)

def log_time(timetype, duration, name, extra=""):
    timevalue = datetime.now()
    timestamp = datetime.now().timestamp()
    with open('timer_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timetype, timevalue, timestamp, duration, name, extra])

def on_closing():
    if running:
        stop_timer()
    root.destroy()

root = tk.Tk()
root.title("TurboSloth")

running = False
start_time = None

button_frame = tk.Frame(root)
start_button = tk.Button(button_frame, text="Start", command=start_timer, font=("", 48))
stop_button = tk.Button(button_frame, text="Stop", command=stop_timer, font=("", 48))
entry_name = tk.Entry(root, state=tk.NORMAL, font=("", 48), justify='center')
timer_label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
status_label = tk.Label(root, text="Ready")

start_button.pack(side=tk.LEFT)
stop_button.pack(side=tk.LEFT)
button_frame.pack()
entry_name.pack()
timer_label.pack()
status_label.pack()

root.wm_protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
