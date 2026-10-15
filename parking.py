import tkinter as tk
from tkinter import ttk
import csv
import datetime

def save_record(name, car, checkin, checkout):
    with open("report.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, car, checkin, checkout])

def start_app():
    root = tk.Tk()
    root.title("Parking Management System")

    columns = ("Name", "Car Number", "Check-in Time", "Check-out Time")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)

    def check_in():
        name = entry_name.get()
        car = entry_car.get()
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tree.insert("", "end", values=(name, car, time, ""))
        entry_name.delete(0, tk.END)
        entry_car.delete(0, tk.END)

    def check_out():
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            values = list(item["values"])
            values[3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tree.item(selected[0], values=values)
            save_record(values[0], values[1], values[2], values[3])

    tk.Label(root, text="Name").pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text="Car Number").pack()
    entry_car = tk.Entry(root)
    entry_car.pack()

    tk.Button(root, text="Check In", command=check_in).pack()
    tk.Button(root, text="Check Out", command=check_out).pack()

    root.mainloop()

if __name__ == "__main__":
    start_app()
    
