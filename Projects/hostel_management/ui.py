# ui.py
# Modern-ish Tkinter UI with Dashboard -> opens separate windows for each module
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from database import DB
from datetime import datetime

# ----------------- small UI helpers -----------------
def make_hover(btn, bg='#0066cc', fg='white'):
    def on_enter(e):
        btn['background'] = bg
        btn['foreground'] = fg
    def on_leave(e):
        btn['background'] = btn._orig_bg
        btn['foreground'] = btn._orig_fg
    btn._orig_bg = btn['background']
    btn._orig_fg = btn['foreground']
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

def center_window(win, w, h):
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

# ----------------- Main App UI -----------------
class HostelUI:
    def __init__(self, root, db: DB):
        self.root = root
        self.db = db
        self.root.title("Hostel Management - Dashboard")
        center_window(self.root, 900, 600)
        self.root.configure(bg="#f3f6fb")
        self.setup_styles()
        self.build_header()
        self.build_dashboard()

        # ensure mess table exists (simple local table)
        self.ensure_mess_table()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", font=("Segoe UI", 10))

    def build_header(self):
        # blue gradient-like header (two tones)
        header = Frame(self.root, bg="#0b61a4", height=80)
        header.pack(fill=X)
        header.pack_propagate(False)
        title = Label(header, text="🏠 Hostel Management System", bg="#0b61a4", fg="white",
                      font=("Segoe UI", 20, "bold"))
        title.pack(side=LEFT, padx=20)
        subtitle = Label(header, text="Dashboard", bg="#0b61a4", fg="#e6f2ff", font=("Segoe UI", 12))
        subtitle.pack(side=LEFT, padx=10, pady=28)

        # small info on right
        nowlbl = Label(header, text=datetime.now().strftime("%d %b %Y — %H:%M"), bg="#0b61a4", fg="#dfeffd")
        nowlbl.pack(side=RIGHT, padx=20)

    def build_dashboard(self):
        body = Frame(self.root, bg="#f3f6fb")
        body.pack(fill=BOTH, expand=True, padx=20, pady=20)

        Label(body, text="Open a module", font=("Segoe UI", 14, "bold"), bg="#f3f6fb").pack(anchor=W)

        grid = Frame(body, bg="#f3f6fb")
        grid.pack(pady=18)

        btn_cfg = {
            'width':20, 'height':2, 'bd':0, 'relief':RIDGE,
            'bg':'#e9f4ff', 'fg':'#003366', 'font':("Segoe UI", 11, "bold")
        }

        # Buttons: Student, Room, Fee, Mess, Complaint, Report
        btn_student = Button(grid, text="👨‍🎓  Students", command=self.open_students_window, **btn_cfg)
        btn_room    = Button(grid, text="🏘️  Rooms", command=self.open_rooms_window, **btn_cfg)
        btn_fee     = Button(grid, text="💰  Fees", command=self.open_fees_window, **btn_cfg)
        btn_mess    = Button(grid, text="🍽️  Mess", command=self.open_mess_window, **btn_cfg)
        btn_comp    = Button(grid, text="📝  Complaints", command=self.open_complaints_window, **btn_cfg)
        btn_report  = Button(grid, text="📊  Reports", command=self.open_reports_window, **btn_cfg)

        buttons = [btn_student, btn_room, btn_fee, btn_mess, btn_comp, btn_report]
        for i,b in enumerate(buttons):
            r = i//3; c = i%3
            b.grid(row=r, column=c, padx=20, pady=12)
            make_hover(b)

        # quick tip box
        tip = Frame(body, bg="white", bd=1, relief=SOLID)
        tip.pack(fill=X, pady=12)
        Label(tip, text="Tip: Click any module to open a separate window. Use 'Backup Database' from Reports to save DB copy.",
              bg="white", font=("Segoe UI", 10)).pack(padx=10, pady=8)

    # ---------------- Window Openers ----------------
    def open_students_window(self):
        win = Toplevel(self.root)
        win.title("Students")
        center_window(win, 900, 520)
        StudentsWindow(win, self.db)

    def open_rooms_window(self):
        win = Toplevel(self.root)
        win.title("Rooms")
        center_window(win, 700, 450)
        RoomsWindow(win, self.db)

    def open_fees_window(self):
        win = Toplevel(self.root)
        win.title("Fees")
        center_window(win, 760, 500)
        FeesWindow(win, self.db)

    def open_mess_window(self):
        win = Toplevel(self.root)
        win.title("Mess")
        center_window(win, 650, 420)
        MessWindow(win, self.db)

    def open_complaints_window(self):
        win = Toplevel(self.root)
        win.title("Complaints")
        center_window(win, 760, 480)
        ComplaintsWindow(win, self.db)

    def open_reports_window(self):
        win = Toplevel(self.root)
        win.title("Reports")
        center_window(win, 820, 520)
        ReportsWindow(win, self.db)

    # ---------------- Mess table ensure ----------------
    def ensure_mess_table(self):
        cur = self.db.conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS mess_records(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            meal TEXT,
            student_id INTEGER,
            attended INTEGER DEFAULT 0
        )''')
        self.db.conn.commit()

# ---------------- Students Window ----------------
class StudentsWindow:
    def __init__(self, root, db: DB):
        self.root = root
        self.db = db
        self.build_ui()

    def build_ui(self):
        frm_top = Frame(self.root)
        frm_top.pack(fill=X, pady=8, padx=8)

        Label(frm_top, text="Name").grid(row=0,column=0, padx=6, pady=6)
        self.e_name = Entry(frm_top, width=30); self.e_name.grid(row=0,column=1, padx=6)
        Label(frm_top, text="Roll No").grid(row=0,column=2, padx=6)
        self.e_roll = Entry(frm_top, width=20); self.e_roll.grid(row=0,column=3, padx=6)
        Label(frm_top, text="Room No").grid(row=0,column=4, padx=6)
        self.e_room = Entry(frm_top, width=12); self.e_room.grid(row=0,column=5, padx=6)
        Label(frm_top, text="Contact").grid(row=1,column=0, padx=6)
        self.e_contact = Entry(frm_top, width=20); self.e_contact.grid(row=1,column=1, padx=6)

        Button(frm_top, text="Add Student", command=self.add_student).grid(row=1,column=3, padx=6)
        Button(frm_top, text="Update Selected", command=self.update_student).grid(row=1,column=4, padx=6)
        Button(frm_top, text="Delete Selected", command=self.delete_student).grid(row=1,column=5, padx=6)

        # Treeview
        cols = ('id','name','roll','branch','room','contact','joined_on')
        self.tree = ttk.Treeview(self.root, columns=cols, show='headings', height=18)
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=110)
        self.tree.pack(fill=BOTH, expand=True, padx=8, pady=8)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.load_students()

    def load_students(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        rows = self.db.find_students('')
        for row in rows:
            self.tree.insert('', END, values=row)

    def add_student(self):
        name = self.e_name.get().strip()
        roll = self.e_roll.get().strip()
        room = self.e_room.get().strip()
        contact = self.e_contact.get().strip()
        if not name or not roll:
            messagebox.showwarning("Input", "Name and Roll required")
            return
        try:
            sid = self.db.add_student(name, roll, '', room, contact)
            messagebox.showinfo("OK", f"Student added (ID: {sid})")
            self.clear_inputs(); self.load_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student(self):
        sel = self.tree.selection()
        if not sel:
            return
        sid = int(self.tree.item(sel[0])['values'][0])
        try:
            self.db.update_student(sid, self.e_name.get(), self.e_roll.get(), '', self.e_room.get(), self.e_contact.get())
            messagebox.showinfo("OK", "Updated")
            self.load_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student(self):
        sel = self.tree.selection()
        if not sel: return
        if not messagebox.askyesno("Confirm", "Delete selected student?"): return
        sid = int(self.tree.item(sel[0])['values'][0])
        self.db.delete_student(sid)
        self.load_students()

    def on_select(self, e):
        sel = self.tree.selection()
        if not sel: return
        v = self.tree.item(sel[0])['values']
        # id,name,roll,branch,room,contact,joined_on
        self.e_name.delete(0,END); self.e_name.insert(0, v[1])
        self.e_roll.delete(0,END); self.e_roll.insert(0, v[2])
        self.e_room.delete(0,END); self.e_room.insert(0, v[4])
        self.e_contact.delete(0,END); self.e_contact.insert(0, v[5])

    def clear_inputs(self):
        self.e_name.delete(0,END); self.e_roll.delete(0,END); self.e_room.delete(0,END); self.e_contact.delete(0,END)

# ---------------- Rooms Window ----------------
class RoomsWindow:
    def __init__(self, root, db: DB):
        self.root = root
        self.db = db
        self.build_ui()

    def build_ui(self):
        top = Frame(self.root)
        top.pack(fill=X, padx=8, pady=8)
        Label(top, text="Room No").grid(row=0,column=0, padx=6)
        self.e_rno = Entry(top); self.e_rno.grid(row=0,column=1, padx=6)
        Label(top, text="Capacity").grid(row=0,column=2, padx=6)
        self.e_cap = Entry(top); self.e_cap.grid(row=0,column=3, padx=6); self.e_cap.insert(0,'1')
        Button(top, text="Add Room", command=self.add_room).grid(row=0,column=4, padx=6)

        cols = ('room_no','capacity','occupied')
        self.tree = ttk.Treeview(self.root, columns=cols, show='headings', height=16)
        for c in cols:
            self.tree.heading(c, text=c.title()); self.tree.column(c, width=150)
        self.tree.pack(fill=BOTH, expand=True, padx=8, pady=8)
        self.load_rooms()

    def add_room(self):
        rn = self.e_rno.get().strip()
        try:
            cap = int(self.e_cap.get().strip() or 1)
        except:
            cap = 1
        if not rn:
            messagebox.showwarning("Input","Enter Room No")
            return
        ok = self.db.add_room(rn,cap)
        if ok:
            messagebox.showinfo("OK","Room added")
            self.e_rno.delete(0,END); self.e_cap.delete(0,END); self.e_cap.insert(0,'1')
            self.load_rooms()
        else:
            messagebox.showwarning("Exists","Room already exists")

    def load_rooms(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        rows = self.db.get_rooms()
        for row in rows:
            self.tree.insert('', END, values=row)

# ---------------- Fees Window ----------------
class FeesWindow:
    def __init__(self, root, db: DB):
        self.root = root
        self.db = db
        self.build_ui()

    def build_ui(self):
        top = Frame(self.root)
        top.pack(fill=X, padx=8, pady=8)
        Label(top, text="Student ID").grid(row=0,column=0, padx=6)
        self.e_sid = Entry(top); self.e_sid.grid(row=0,column=1, padx=6)
        Label(top, text="Month (YYYY-MM)").grid(row=0,column=2, padx=6)
        self.e_month = Entry(top); self.e_month.grid(row=0,column=3, padx=6); self.e_month.insert(0, datetime.now().strftime("%Y-%m"))
        Label(top, text="Amount").grid(row=1,column=0, padx=6)
        self.e_amount = Entry(top); self.e_amount.grid(row=1,column=1, padx=6); self.e_amount.insert(0,'0')
        Button(top, text="Add Fee (Paid)", command=self.add_fee).grid(row=1,column=3, padx=6)

        cols = ('id','student_id','month','amount','status','paid_on')
        self.tree = ttk.Treeview(self.root, columns=cols, show='headings', height=16)
        for c in cols:
            self.tree.heading(c, text=c.title()); self.tree.column(c, width=110)
        self.tree.pack(fill=BOTH, expand=True, padx=8, pady=8)

    def add_fee(self):
        try:
            sid = int(self.e_sid.get().strip())
            month = self.e_month.get().strip() or datetime.now().strftime("%Y-%m")
            amount = float(self.e_amount.get().strip() or 0)
        except Exception as e:
            messagebox.showerror("Error","Invalid input")
            return
        self.db.add_fee(sid, month, amount, 'Paid')
        messagebox.showinfo("OK","Fee recorded")
        self.load_fees()

    def load_fees(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        try:
            sid = int(self.e_sid.get().strip())
        except:
            return
        rows = self.db.get_fees_for_student(sid)
        for row in rows:
            self.tree.insert('', END, values=row)

# ---------------- Mess Window ----------------
class MessWindow:
    def __init__(self, root, db: DB):
        self.root = root
        self.db = db
        self.build_ui()

    def build_ui(self):
        top = Frame(self.root); top.pack(fill=X, padx=8, pady=8)
        Label(top, text="Student ID").grid(row=0,column=0, padx=6)
        self.e_sid = Entry(top); self.e_sid.grid(row=0,column=1, padx=6)
        Label(top, text="Meal").grid(row=0,column=2, padx=6)
        self.cmb = ttk.Combobox(top, values=["Breakfast","Lunch","Dinner"], width=12); self.cmb.grid(row=0,column=3, padx=6); self.cmb.current(0)
        Button(top, text="Mark Attendance", command=self.mark_att).grid(row=1,column=1, padx=6)
        Button(top, text="View Today Summary", command=self.load_summary).grid(row=1,column=3, padx=6)

        cols = ('meal','count')
        self.tree = ttk.Treeview(self.root, columns=cols, show='headings', height=12)
        for c in cols:
            self.tree.heading(c, text=c.title()); self.tree.column(c, width=140)
        self.tree.pack(fill=BOTH, expand=True, padx=8, pady=8)

    def mark_att(self):
        try:
            sid = int(self.e_sid.get().strip())
        except:
            messagebox.showwarning("Input","Enter valid Student ID")
            return
        meal = self.cmb.get()
        date = datetime.now().strftime("%Y-%m-%d")
        cur = self.db.conn.cursor()
        cur.execute("INSERT INTO mess_records(date,meal,student_id,attended) VALUES(?,?,?,1)", (date, meal, sid))
        self.db.conn.commit()
        messagebox.showinfo("OK", f"Marked {meal} for student {sid}")

    def load_summary(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        date = datetime.now().strftime("%Y-%m-%d")
        cur = self.db.conn.cursor()
        cur.execute("SELECT meal, COUNT(*) FROM mess_records WHERE date=? GROUP BY meal", (date,))
        rows = cur.fetchall()
        for row in rows:
            self.tree.insert('', END, values=row)

# ---------------- Complaints Window ----------------
class ComplaintsWindow:
    def __init__(self, root, db: DB):
        self.root = root
        self.db = db
        self.build_ui()

    def build_ui(self):
        top = Frame(self.root); top.pack(fill=X, padx=8, pady=8)
        Label(top, text="Student ID").grid(row=0,column=0, padx=6)
        self.e_sid = Entry(top); self.e_sid.grid(row=0,column=1, padx=6)
        Label(top, text="Details").grid(row=0,column=2, padx=6)
        self.e_det = Entry(top, width=40); self.e_det.grid(row=0,column=3, padx=6)
        Button(top, text="Add Complaint", command=self.add_comp).grid(row=0,column=4, padx=6)
        Button(top, text="Refresh", command=self.load_complaints).grid(row=0,column=5, padx=6)

        cols = ('id','student','roll','details','status','raised_on')
        self.tree = ttk.Treeview(self.root, columns=cols, show='headings', height=16)
        for c in cols:
            self.tree.heading(c, text=c.title()); self.tree.column(c, width=120)
        self.tree.pack(fill=BOTH, expand=True, padx=8, pady=8)
        self.tree.bind("<Double-1>", self.on_double)
        self.load_complaints()

    def add_comp(self):
        try:
            sid = int(self.e_sid.get().strip())
        except:
            messagebox.showwarning("Input","Enter valid Student ID"); return
        details = self.e_det.get().strip()
        if not details: return
        self.db.add_complaint(sid, details)
        messagebox.showinfo("OK","Complaint added")
        self.load_complaints()

    def load_complaints(self):
        for r in self.tree.get_children(): self.tree.delete(r)
        rows = self.db.get_complaints()
        for r in rows:
            self.tree.insert('', END, values=r)

    def on_double(self, e):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])['values']
        cid = vals[0]; cur_status = vals[4]
        new = simpledialog.askstring("Update Status", f"Current: {cur_status}\nEnter new status:")
        if new:
            self.db.update_complaint_status(cid, new)
            self.load_complaints()

# ---------------- Reports Window ----------------
class ReportsWindow:
    def __init__(self, root, db: DB):
        self.root = root
        self.db = db
        self.build_ui()

    def build_ui(self):
        top = Frame(self.root); top.pack(fill=X, padx=8, pady=8)
        Button(top, text="Room Occupancy Report", command=self.report_rooms).grid(row=0,column=0, padx=6)
        Button(top, text="Fee Summary", command=self.report_fees).grid(row=0,column=1, padx=6)
        Button(top, text="Backup Database", command=self.backup_db).grid(row=0,column=2, padx=6)

        self.txt = Text(self.root, height=22)
        self.txt.pack(fill=BOTH, expand=True, padx=8, pady=8)

    def report_rooms(self):
        rows = self.db.room_occupancy_report()
        self.txt.delete("1.0", END)
        self.txt.insert(END, "Room No\tCapacity\tOccupied\n")
        for r in rows:
            self.txt.insert(END, f"{r[0]}\t{r[1]}\t{r[2]}\n")

    def report_fees(self):
        rows = self.db.fee_summary()
        self.txt.delete("1.0", END)
        self.txt.insert(END, "ID\tName\tRoll\tTotalPaid\n")
        for r in rows:
            self.txt.insert(END, f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\n")

    def backup_db(self):
        backup_name = f'hostel_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
        self.db.conn.commit()
        self.db.conn.close()
        import shutil
        shutil.copy(DB_FILE, backup_name)  # DB_FILE comes from database.py
        # reopen DB connection
        self.db = DB()
        messagebox.showinfo("Backup", f"Backup created: {backup_name}")

# ---------------- Run as standalone UI ----------------
if __name__ == "__main__":
    root = Tk()
    db = DB()
    app = HostelUI(root, db)
    root.mainloop()
