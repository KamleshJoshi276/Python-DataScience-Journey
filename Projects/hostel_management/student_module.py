# student_module.py
from tkinter import *
from tkinter import ttk, messagebox

class StudentModule:
    def __init__(self, root, db):
        self.root = root
        self.db = db

        # Title
        Label(self.root, text="🎓 Student Management", font=("Segoe UI", 16, "bold"), fg="#0078D7").pack(pady=10)

        # Frame for form
        form = Frame(self.root, bg="white", bd=2, relief=GROOVE)
        form.pack(padx=20, pady=10, fill=X)

        Label(form, text="Student Name:", bg="white").grid(row=0, column=0, padx=10, pady=5)
        self.name = Entry(form, width=25)
        self.name.grid(row=0, column=1, padx=10, pady=5)

        Label(form, text="Room No:", bg="white").grid(row=0, column=2, padx=10, pady=5)
        self.room = Entry(form, width=15)
        self.room.grid(row=0, column=3, padx=10, pady=5)

        Label(form, text="Contact:", bg="white").grid(row=1, column=0, padx=10, pady=5)
        self.contact = Entry(form, width=25)
        self.contact.grid(row=1, column=1, padx=10, pady=5)

        Button(form, text="Add Student", bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"),
               command=self.add_student).grid(row=1, column=3, padx=10, pady=5)

        # Table
        self.tree = ttk.Treeview(self.root, columns=("id", "name", "room", "contact"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("room", text="Room No")
        self.tree.heading("contact", text="Contact")
        self.tree.pack(padx=20, pady=10, fill=BOTH, expand=True)

        self.load_students()

    # -----------------------------
    def add_student(self):
        name = self.name.get().strip()
        room = self.room.get().strip()
        contact = self.contact.get().strip()
        if name == "" or room == "" or contact == "":
            messagebox.showwarning("Warning", "All fields are required!")
            return
        self.db.execute("INSERT INTO students (name, room, contact) VALUES (?, ?, ?)", (name, room, contact))
        self.db.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        self.load_students()

    # -----------------------------
    def load_students(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = self.db.fetchall("SELECT * FROM students")
        for row in rows:
            self.tree.insert("", END, values=row)
