# room_module.py
from tkinter import *
from tkinter import ttk, messagebox

class RoomModule:
    def __init__(self, parent, db):
        self.db = db
        self.frame = Frame(parent, padx=10, pady=10)
        self.build_ui()

    def build_ui(self):
        top = Frame(self.frame)
        top.pack(fill=X)
        Label(top, text='Room No').grid(row=0,column=0)
        self.r_no = Entry(top); self.r_no.grid(row=0,column=1)
        Label(top, text='Capacity').grid(row=1,column=0)
        self.r_cap = Entry(top); self.r_cap.insert(0,'1'); self.r_cap.grid(row=1,column=1)
        Button(top, text='Add', command=self.add_room).grid(row=2,column=0,columnspan=2)

        cols=('room_no','capacity','occupied')
        self.tree = ttk.Treeview(self.frame, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c,text=c.title()); self.tree.column(c,width=120)
        self.tree.pack(fill=BOTH, expand=1)
        self.load_rooms()

    def add_room(self):
        rn = self.r_no.get().strip()
        cap = int(self.r_cap.get() or 1)
        if self.db.add_room(rn,cap):
            messagebox.showinfo('Added','Room added')
            self.load_rooms()
        else:
            messagebox.showerror('Exists','Room already exists')

    def load_rooms(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for r in self.db.get_rooms():
            self.tree.insert('',END,values=r)
