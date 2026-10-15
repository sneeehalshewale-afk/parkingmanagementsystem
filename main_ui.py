import tkinter as tk
from tkinter import messagebox, ttk
import csv
import datetime
import logging
import os

# ---------------- Logger Setup ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ParkingSystem")

# ---------------- Users / Signup ----------------
def register_user(username, password):
    with open("users.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([username, password])
    logger.info(f"New user registered: {username}")

def signup():
    def save_user():
        uname = entry_username.get()
        pwd = entry_password.get()
        if uname == "" or pwd == "":
            messagebox.showerror("Error", "All fields are required!")
        else:
            register_user(uname, pwd)
            messagebox.showinfo("Success", "User Registered Successfully!")
            root.destroy()
            login()  # back to login

    root = tk.Tk()
    root.title("Signup")

    tk.Label(root, text="Username").pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    tk.Label(root, text="Password").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    tk.Button(root, text="Register", command=save_user).pack()
    root.mainloop()

# ---------------- Parking Management ----------------
REPORT_FILE = "report.csv"
if not os.path.exists(REPORT_FILE):
    with open(REPORT_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Car Number", "Check-in Time", "Check-out Time"])

def save_record(name, car, checkin, checkout):
    with open(REPORT_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, car, checkin, checkout])
    logger.info(f"Record saved: {name} - {car} - {checkin} - {checkout}")

def start_parking_ui():
    root = tk.Tk()
    root.title("Parking Management System")

    columns = ("Name", "Car Number", "Check-in Time", "Check-out Time")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)

    # Entry fields
    tk.Label(root, text="Name").pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text="Car Number").pack()
    entry_car = tk.Entry(root)
    entry_car.pack()

    # Buttons
    def check_in():
        name = entry_name.get()
        car = entry_car.get()
        if not name or not car:
            messagebox.showerror("Error", "Name and Car Number required!")
            return
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tree.insert("", "end", values=(name, car, time, ""))
        entry_name.delete(0, tk.END)
        entry_car.delete(0, tk.END)
        logger.info(f"Check-in: {name} - {car} at {time}")

    def check_out():
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            values = list(item["values"])
            values[3] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tree.item(selected[0], values=values)
            save_record(values[0], values[1], values[2], values[3])
            logger.info(f"Check-out: {values[0]} - {values[1]} at {values[3]}")
        else:
            messagebox.showerror("Error", "No record selected for checkout!")

    tk.Button(root, text="Check In", command=check_in).pack()
    tk.Button(root, text="Check Out", command=check_out).pack()

    root.mainloop()

# ---------------- Login UI ----------------
def login():
    def validate_login():
        uname = entry_username.get()
        pwd = entry_password.get()

        if not os.path.exists("users.csv"):
            messagebox.showerror("Error", "No users found! Please sign up first.")
            root.destroy()
            signup()
            return

        with open("users.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == uname and row[1] == pwd:
                    messagebox.showinfo("Success", "Login Successful!")
                    logger.info(f"User '{uname}' logged in successfully")
                    root.destroy()
                    start_parking_ui()  # open parking UI
                    return

        # Login failed
        messagebox.showerror("Error", "Invalid Username or Password")
        logger.warning(f"Login failed for user '{uname}'")

    def open_signup():
        root.destroy()
        signup()

    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Username").grid(row=0, column=0)
    tk.Label(root, text="Password").grid(row=1, column=0)

    entry_username = tk.Entry(root)
    entry_password = tk.Entry(root, show="*")

    entry_username.grid(row=0, column=1)
    entry_password.grid(row=1, column=1)

    tk.Button(root, text="Login", command=validate_login).grid(row=2, column=0, columnspan=2)
    tk.Button(root, text="Signup", command=open_signup).grid(row=3, column=0, columnspan=2)

    root.mainloop()

# ---------------- Main ----------------
if __name__ == "__main__":
    login()
