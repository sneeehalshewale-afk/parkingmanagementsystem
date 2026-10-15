import sqlite3

def init_db():
    conn = sqlite3.connect("parking.db")
    c = conn.cursor()

    # Drop table if exists (clean reset during development)
    # ⚠️ WARNING: This will wipe old data each time you restart
    c.execute("DROP TABLE IF EXISTS parking")

    # Create table fresh
    c.execute('''
        CREATE TABLE parking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            floor INTEGER NOT NULL,
            slot INTEGER NOT NULL,
            status TEXT DEFAULT 'available',
            vehicle TEXT,
            owner TEXT
        )
    ''')

    # Insert slots (3 floors × 10 slots each)
    for floor in range(1, 4):  # Floor 1, 2, 3
        for slot in range(1, 11):  # Slots 1 → 10
            c.execute(
                "INSERT INTO parking (floor, slot, status) VALUES (?, ?, ?)",
                (floor, slot, "available")
            )

    # ✅ NEW CODE (added safely at the end)
    # Create problems table to store user problem queries
    c.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            floor INTEGER,
            slot INTEGER,
            description TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized with 3 floors × 10 slots each + problems table added")

if __name__ == "__main__":
    init_db()
