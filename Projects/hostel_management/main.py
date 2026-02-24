# main.py
from tkinter import *
from tkinter import ttk, messagebox
from database import DB
from student_module import StudentModule
from room_module import RoomModule
from fee_module import FeeModule
# future modules: mess_module, complaint_module, report_module

ADMIN_PASSWORD = 'admin123'

class App:
    def __init__(self, root):
        self.root = root
        self.db = DB()
        self.root.title("🏠 Hostel Management System")
        self.root.geometry("900x600")
        self.root.config(bg="#f5f6fa")
        self.create_login_screen()

    # ----------------------------------------------------------------
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ----------------------------------------------------------------
    def create_login_screen(self):
        self.clear_window()
        frame = Frame(self.root, bg="white", padx=40, pady=40, relief=GROOVE, bd=2)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(frame, text="Hostel Management Login", font=("Segoe UI", 16, "bold"), bg="white", fg="#0078D7").pack(pady=10)
        Label(frame, text="Enter Admin Password", font=("Segoe UI", 11), bg="white").pack(pady=5)

        self.password_entry = Entry(frame, show="*", width=25, font=("Segoe UI", 12), relief=SOLID, bd=1)
        self.password_entry.pack(pady=5)
        self.password_entry.focus()

        Button(frame, text="Login", font=("Segoe UI", 11, "bold"), bg="#0078D7", fg="white",
               padx=15, pady=5, relief=FLAT, command=self.check_login).pack(pady=15)

    # ----------------------------------------------------------------
    def check_login(self):
        if self.password_entry.get() == ADMIN_PASSWORD:
            self.create_dashboard()
        else:
            messagebox.showerror("Error", "❌ Wrong Password! Try again.")

    # ----------------------------------------------------------------
    def create_dashboard(self):
        self.clear_window()

        # Header
        header = Frame(self.root, bg="#0078D7", height=60)
        header.pack(fill=X)
        Label(header, text="🏠 Hostel Management Dashboard", fg="white", bg="#0078D7",
              font=("Segoe UI", 16, "bold")).pack(pady=10)

        # Button Grid
        body = Frame(self.root, bg="#f5f6fa")
        body.pack(fill=BOTH, expand=True, pady=40)

        buttons = [
            ("Students", self.open_students),
            ("Rooms", self.open_rooms),
            ("Fees", self.open_fees),
            ("Mess", self.open_mess),
            ("Complaints", self.open_complaints),
            ("Reports", self.open_reports)
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = Button(body, text=text, width=20, height=2, bg="#0078D7", fg="white",
                         font=("Segoe UI", 12, "bold"), relief=FLAT, activebackground="#005a9e",
                         activeforeground="white", command=cmd)
            btn.grid(row=i//2, column=i%2, padx=40, pady=20)

    # ----------------------------------------------------------------
    def open_students(self):
        new = Toplevel(self.root)
        new.title("Students Management")
        new.geometry("900x600")
        StudentModule(new, self.db)

    def open_rooms(self):
        new = Toplevel(self.root)
        new.title("Room Management")
        new.geometry("900x600")
        RoomModule(new, self.db)

    def open_fees(self):
        new = Toplevel(self.root)
        new.title("Fees Management")
        new.geometry("900x600")
        FeeModule(new, self.db)

    def open_mess(self):
        new = Toplevel(self.root)
        new.title("Mess Management")
        new.geometry("900x600")
        Label(new, text="🍽️ Mess Management Section", font=("Segoe UI", 14, "bold")).pack(pady=20)

    def open_complaints(self):
        new = Toplevel(self.root)
        new.title("Complaints")
        new.geometry("900x600")
        Label(new, text="📩 Complaints Section", font=("Segoe UI", 14, "bold")).pack(pady=20)

    def open_reports(self):
        new = Toplevel(self.root)
        new.title("Reports")
        new.geometry("900x600")
        Label(new, text="📊 Reports Section", font=("Segoe UI", 14, "bold")).pack(pady=20)


# ----------------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
