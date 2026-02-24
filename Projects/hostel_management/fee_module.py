# fee_module.py
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

class FeeModule:
    def __init__(self, parent, db):
        self.db = db
        self.frame = Frame(parent, padx=10, pady=10)
        self.build_ui()

    def build_ui(self):
        top = Frame(self.frame)
        top.pack(fill=X)
        Label(top,text='Student ID').grid(row=0,column=0)
        self.sid=Entry(top);self.sid.grid(row=0,column=1)
        Label(top,text='Month').grid(row=1,column=0)
        self.month=Entry(top);self.month.insert(0,datetime.now().strftime('%Y-%m'));self.month.grid(row=1,column=1)
        Label(top,text='Amount').grid(row=2,column=0)
        self.amount=Entry(top);self.amount.insert(0,'0');self.amount.grid(row=2,column=1)
        Button(top,text='Add Fee',command=self.add_fee).grid(row=3,column=0,columnspan=2)

        cols=('id','student_id','month','amount','status','paid_on')
        self.tree=ttk.Treeview(self.frame,columns=cols,show='headings')
        for c in cols:
            self.tree.heading(c,text=c.title());self.tree.column(c,width=100)
        self.tree.pack(fill=BOTH,expand=1)

    def add_fee(self):
        try:
            sid=int(self.sid.get())
            self.db.add_fee(sid,self.month.get(),float(self.amount.get()),'Paid')
            messagebox.showinfo('Success','Fee added')
            self.load_fees()
        except Exception as e:
            messagebox.showerror('Error',str(e))

    def load_fees(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        sid=int(self.sid.get())
        for f in self.db.get_fees_for_student(sid):
            self.tree.insert('',END,values=f)
