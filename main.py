import webbrowser
import schedule
import tkinter as tk
from tkinter import ttk
import sys
from ttkthemes import themed_tk as tttk
from tkinter import messagebox

root = tttk.ThemedTk()
root.get_themes()
root.set_theme("breeze")
root.title("Meeting Attender")


class Meeting:
    def __init__(self, time, link, name):
        self.time = time
        self.link = link
        self.name = name

    def get_time(self):
        return self.time

    def get_link(self):
        return self.link

    def get_name(self):
        return self.name

def open_meeting(url):
    webbrowser.open_new_tab(url);

def add_meeting():
    if name_var.get() == "":
        messagebox.showerror(title="Blank Meeting Name", message="Please enter a meeting name")
        return
    elif link_var.get() == "":
        messagebox.showerror(title="Blank Link URL", message="Please enter a url")
        return
    elif time_var.get() == "":
        messagebox.showerror(title="Blank Time", message="Please enter a time")
        return

    meeting_name = name_var.get()
    meeting_link = link_var.get()
    meeting_time = convert24(time_var.get())
    if meeting_time == None:
        messagebox.showerror(title="Time Error", message="The time you entered was invalid")
        return
    print(meeting_time)
    meetings.append(Meeting(meeting_time, meeting_link, meeting_name))
    c = meeting_name + " at " + time_var.get()
    meeting_listbox.insert(tk.END, c)
    a1.delete(0, tk.END)
    b1.delete(0, tk.END)
    c1.delete(0, tk.END)
    schedule.clear()
    for meeting in meetings:
        try:
            schedule.every().day.at(meeting.get_time()).do(open_meeting, url=meeting.get_link())
        except:
            messagebox.showerror(title="Time Error", message="The time you entered was invalid")
            return
        print("Added", meeting.get_name(), "to schedule for", meeting.get_time())
        print(schedule.jobs)

def delete_meeting():
    try:
        selection = meeting_listbox.curselection()[0]
        meeting_listbox.delete(selection)
    except:
        messagebox.showerror(title="Meeting needs to be selected", message="A meeting needs to be selected in order to delete")
    else:
        del schedule.jobs[selection]
        del meetings[selection]

def how_to_use():
    messagebox.showinfo(title="How to use", message=
"""
/* Add and Delete Meetings */
To add a meeting to your schedule, fill out all of the information in the entry fields, and click the \"Add\" button.
To delete a meeting from your scheule, click on it in the Meeting Box and press the \"Delete\" button.

/* Filling out Entry Fields */
Enter the name of meeting in the \"Name:\" entry field.
Enter the link of the meeting in the \"Link:\" entry field.
Enter the time you want to join the meeting in the \"Time:\" entry field with AM or PM. Ex: 03:00PM
"""
)
def convert24(str1):
    try:
       y = str(int(str1[:2]) + 12) + str1[2:5]
    except:
        return
    else:
        if str1[-2:] == "AM" and str1[:2] == "12":
            return "00" + str1[2:-2]

        # remove the AM
        elif str1[-2:] == "AM":
            return str1[:-2]

        # Checking if last two elements of time
        # is PM and first two elements are 12
        elif str1[-2:] == "PM" and str1[:2] == "12":
            return str1[:-2]

        else:
            # add 12 to hours and remove PM
            return str(int(str1[:2]) + 12) + str1[2:5]


name_var=tk.StringVar()
link_var=tk.StringVar()
time_var=tk.StringVar()

frame_meetings = tk.Frame(root, padx=15, pady=15)
frame_meetings.pack()

meeting_listbox = tk.Listbox(frame_meetings, height=10, width=50)
meeting_listbox.pack(side="left")

scrollbar_meetings = ttk.Scrollbar(frame_meetings)
scrollbar_meetings.pack(side="right", fill=tk.Y)

meeting_listbox.config(yscrollcommand=scrollbar_meetings.set)
scrollbar_meetings.config(command=meeting_listbox.yview)

frame1 = tk.Frame(root)
frame1.pack()
frame2 = tk.Frame(root)
frame2.pack()
frame3 = tk.Frame(root)
frame3.pack()

a = tk.Label(frame1 ,text = "Name:", width=5)
a.pack(side="left")
a1 = ttk.Entry(frame1, textvariable=name_var, width=40)
a1.pack(side="left")

b = tk.Label(frame2 ,text = "Link:", width=5)
b.pack(side="left")
b1 = ttk.Entry(frame2, textvariable=link_var, width=40)
b1.pack(side="left")

c = tk.Label(frame3 ,text = "Time:", width=5)
c.pack(side="left")
c1 = ttk.Entry(frame3, textvariable=time_var, width=40)
c1.pack(side="left")

meetings = []

add_btn = ttk.Button(root, text="Add Meeting to Schedule", command=add_meeting)
add_btn.pack(pady=(4, 4))

del_btn = ttk.Button(root, text="Delete", command=delete_meeting)
del_btn.pack(pady=(0, 4))

how_btn = ttk.Button(root, text="How to use", command=how_to_use)
how_btn.pack(pady=(0, 4))


while True:
    try:
        root.update_idletasks()
        root.update()
        schedule.run_pending()
    except:
        sys.exit()
