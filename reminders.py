import threading
import os
from datetime import datetime
from time import sleep
from tkinter import *
from backports.datetime_fromisoformat import MonkeyPatch
import calendar

'''
icons:
dialog-information (i)
dialog-error (!)
'''
MonkeyPatch.patch_fromisoformat()
curr_time = datetime.now()
months=('01','02','03','04','05','06','07','08','09','10','11','12')


def send_reminder(title, message, importance, icon):
    os.system('notify-send -u {} -i {} \"{}\" \"{}\"'.format(importance, icon, title, message))


def string_to_dt(month, day, year, hour, minute):
    dt = datetime.fromisoformat('{}-{}-{}T{}:{}:00'.format(year, month, day, hour, minute))
    return dt


def get_days():
    try:
        month = int(monthBox.get())
        year = int(yearBox.get())
    except NameError:
        month = int(datetime.now().strftime('%m'))
        year = int(datetime.now().strftime('%Y'))

    days_list = [x+1 for x in range(calendar.monthrange(year,month)[1])]

    try:
        dayBox.config(values=tuple(days_list))
    except NameError:
        hello = 1

    return tuple(days_list)


def submit_data(hour, minute, month, day, year, msg):
    timestamp = string_to_dt(month, day, year, hour, minute)
    with open('reminders.txt','a') as out_file:
        out_file.write("{};{}".format(timestamp, msg))
        out_file.write("\n")
    background()
    print(timestamp)
    print(msg)


def background():
    with open('reminders.txt', 'r') as reminders:
        while True:
            for line in reminders.readlines():
                if line.split(';')[0] == datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                    send_reminder(line.split(';')[0], line.split(';')[1], "critical", "dialog-information")
                else:
                    print(line)
            continue

##b = threading.Thread(name = "background", target = background)
##f = threading.Thread(name = "foreground", target = foreground)
##
##f.start()
##b.start()

root = Tk()
root.title("Reminders")

timeLabel = Label(root, text="Time:").grid(row=0,column=0)
hoursBox = Spinbox(root, from_=0, to=23, width=4)
hoursBox.grid(row=0,column=1)
hoursBox.delete(0,2)
hoursBox.insert(0, datetime.now().strftime('%H'))

minutesBox = Spinbox(root, from_=0, to=59, width=4)
minutesBox.grid(row=0,column=2)
minutesBox.delete(0,2)
minutesBox.insert(0, datetime.now().strftime('%M'))
timeLabel2 = Label(root, text="(HH:MM)").grid(row=0,column=4,sticky=W)

dateLabel = Label(root, text="Date:").grid(row=1,column=0)
monthBox = Spinbox(root, width=4, values=months, command=get_days)
monthBox.grid(row=1,column=1)
monthBox.delete(0,2)
monthBox.insert(0, datetime.now().strftime('%m'))

dayBox = Spinbox(root, width=4, values=get_days())
dayBox.grid(row=1,column=2)
dayBox.delete(0,2)
dayBox.insert(0, datetime.now().strftime('%d'))

yearBox = Spinbox(root, width=4, from_=int(datetime.now().strftime('%Y')), to=9999)
yearBox.grid(row=1,column=3)
yearBox.delete(0,4)
yearBox.insert(0, datetime.now().strftime('%Y'))
dateLabel2 = Label(root, text="(MM/DD/YYYY)").grid(row=1,column=4)

msgLabel = Label(root, text="Reminder Text:").grid(columnspan=6)
msgBox = Text(root, height=4, width=25, wrap=WORD)
msgBox.grid(columnspan=6)

submitButton = Button(root, text="Submit", command=lambda: submit_data(hoursBox.get(), minutesBox.get(), monthBox.get(), dayBox.get(), yearBox.get(), msgBox.get("1.0", "end-1c"))).grid(row=8,pady=5,columnspan=6)

root.update_idletasks()
root.mainloop()
