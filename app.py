import os
import sqlite3
import logging
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

# ---------------- Flask Setup ----------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- Paths ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "parking.db")

# ---------------- Logger ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ParkingSystem")

# ---------------- Database Initialization ----------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create all tables
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS parking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        floor INTEGER,
        slot INTEGER,
        status TEXT,
        vehicle TEXT UNIQUE,
        owner TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT,
        vehicle TEXT,
        checkin_time TEXT,
        checkout_time TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        floor INTEGER,
        slot INTEGER,
        description TEXT,
        status TEXT
    )""")

    # Initialize parking slots (3 floors × 10 slots)
    c.execute("SELECT COUNT(*) FROM parking")
    if c.fetchone()[0] == 0:
        for floor in range(1, 4):
            for slot in range(1, 11):
                c.execute(
                    "INSERT INTO parking (floor, slot, status) VALUES (?, ?, 'available')",
                    (floor, slot)
                )

    # Insert sample problems if none exist
    c.execute("SELECT COUNT(*) FROM problems")
    if c.fetchone()[0] == 0:
        sample_problems = [
            (1, 3, "Slot sensor not working", "Pending"),
            (2, 5, "Slot display shows wrong status", "Resolved"),
            (3, 2, "Check-in button not responding", "Pending")
        ]
        for floor, slot, desc, status in sample_problems:
            c.execute(
                "INSERT INTO problems (floor, slot, description, status) VALUES (?, ?, ?, ?)",
                (floor, slot, desc, status)
            )

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

# ---------------- Routes ----------------

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect(url_for("index"))
        elif user:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match!")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("signup.html", error="Username already exists!")

    return render_template("signup.html")

@app.route("/index")
def index():
    if 'user' not in session:
        return redirect(url_for("login"))
    floors = get_parking_data()
    return render_template("index.html", floors=floors)

@app.route("/book", methods=["POST"])
def book_slot():
    slot_id = int(request.json.get("slot_id"))
    vehicle = request.json.get("vehicle")
    owner = request.json.get("owner")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM parking WHERE vehicle=?", (vehicle,))
    existing_vehicle = c.fetchone()
    if existing_vehicle:
        conn.close()
        return jsonify({"success": False, "message": "This vehicle is already parked!"})

    c.execute("SELECT status FROM parking WHERE id=?", (slot_id,))
    result = c.fetchone()

    if result and result[0] == "available":
        checkin_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("UPDATE parking SET status='booked', vehicle=?, owner=? WHERE id=?", (vehicle, owner, slot_id))
        c.execute("INSERT INTO reports (owner, vehicle, checkin_time) VALUES (?, ?, ?)", (owner, vehicle, checkin_time))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": f"Slot {slot_id} booked!"})
    else:
        conn.close()
        return jsonify({"success": False, "message": "Slot already booked!"})

@app.route("/checkout", methods=["POST"])
def checkout_slot():
    slot_id = int(request.json.get("slot_id"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT vehicle, owner FROM parking WHERE id=?", (slot_id,))
    record = c.fetchone()

    if record:
        vehicle, owner = record
        checkout_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("UPDATE parking SET status='available', vehicle=NULL, owner=NULL WHERE id=?", (slot_id,))
        c.execute("UPDATE reports SET checkout_time=? WHERE vehicle=? AND owner=? AND checkout_time IS NULL",
                  (checkout_time, vehicle, owner))
        conn.commit()

    conn.close()
    return jsonify({"success": True, "message": f"Slot {slot_id} is now available"})

@app.route("/report")
def report():
    if 'user' not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT owner, vehicle, checkin_time, checkout_time FROM reports ORDER BY id DESC")
    records = c.fetchall()
    conn.close()
    return render_template("report.html", records=records)

@app.route("/permission")
def permission():
    if 'user' not in session:
        return redirect(url_for("login"))
    return render_template("permission.html")

@app.route("/problem")
def problem():
    if 'user' not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM problems ORDER BY id DESC")
    problems = c.fetchall()
    conn.close()
    return render_template("problem.html", problems=problems)


# ---------------- Helper ----------------
def get_parking_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, floor, slot, status, vehicle, owner FROM parking ORDER BY floor, slot")
    rows = c.fetchall()
    conn.close()

    data = []
    for floor_num in range(1, 4):
        floor_slots = [
            {
                "id": row[0],
                "slot": row[2],
                "occupied": row[3] == "booked",
                "vehicle": row[4] or "",
                "owner": row[5] or ""
            }
            for row in rows if row[1] == floor_num
        ]
        data.append({"number": floor_num, "slots": floor_slots})
    return data

# ---------------- Main ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
