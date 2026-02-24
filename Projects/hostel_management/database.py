import sqlite3

class DB:
    def __init__(self):
        # Database connection
        self.conn = sqlite3.connect('hostel.db')
        self.cur = self.conn.cursor()
        self.create_tables()

    # =========================
    # ✅ CREATE ALL TABLES HERE
    # =========================
    def create_tables(self):
        # Students Table
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                room TEXT,
                contact TEXT
            )
        ''')

        # Rooms Table
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_no TEXT NOT NULL,
                capacity INTEGER DEFAULT 1,
                occupied INTEGER DEFAULT 0
            )
        ''')

        # Fees Table
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS fees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                amount REAL,
                date TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        ''')

        # Mess Table
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS mess (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                month TEXT,
                bill_amount REAL,
                paid INTEGER DEFAULT 0,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        ''')

        self.conn.commit()

    # =========================
    # ✅ COMMON DATABASE ACTIONS
    # =========================
    def execute(self, query, params=()):
        """Run INSERT, UPDATE, DELETE queries"""
        self.cur.execute(query, params)
        self.conn.commit()

    def fetch(self, query, params=()):
        """Run SELECT queries"""
        self.cur.execute(query, params)
        return self.cur.fetchall()

    # =========================
    # ✅ STUDENT RELATED METHODS
    # =========================
    def get_students(self):
        return self.fetch("SELECT * FROM students")

    # =========================
    # ✅ ROOM RELATED METHODS
    # =========================
    def get_rooms(self):
        self.cur.execute("SELECT * FROM rooms")
        return self.cur.fetchall()

    def add_room(self, room_no, capacity):
        self.execute("INSERT INTO rooms (room_no, capacity, occupied) VALUES (?, ?, ?)",
                     (room_no, capacity, 0))

    # =========================
    # ✅ FEES RELATED METHODS
    # =========================
    def get_fees(self):
        return self.fetch("SELECT * FROM fees")

    # =========================
    # ✅ MESS RELATED METHODS
    # =========================
    def get_mess_records(self):
        return self.fetch("SELECT * FROM mess")

    # =========================
    # ✅ CLOSE CONNECTION
    # =========================
    def close(self):
        self.conn.close()


# =========================
# ✅ RUN ONCE TO TEST
# =========================
if __name__ == "__main__":
    db = DB()
    print("Database initialized successfully ✅")
