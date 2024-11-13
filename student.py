import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Initialize the main window
window = tk.Tk()
window.geometry("1300x700")
window.title("Student Management System")

# Database Functions
def create_table():
    con = sqlite3.connect('student_management.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS students (
                    rollno TEXT PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    gender TEXT,
                    class TEXT,
                    contact TEXT,
                    dob TEXT,
                    address TEXT)''')
    con.commit()
    con.close()

def get_data():
    con = sqlite3.connect('student_management.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM students')
    rows = cur.fetchall()
    Student_table.delete(*Student_table.get_children())
    for row in rows:
        Student_table.insert('', tk.END, values=row)
    con.close()

def add_data():
    if rollno.get() == "" or name.get() == "" or class_var.get() == "":
        messagebox.showerror('Error', 'All fields are required')
    else:
        con = sqlite3.connect('student_management.db')
        cur = con.cursor()
        cur.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (rollno.get(), name.get(), email.get(), gender.get(), class_var.get(), contact.get(), dob.get(), address.get()))
        con.commit()
        con.close()
        get_data()
        clear()
        messagebox.showinfo("Success", "Record saved successfully")

def update_data():
    con = sqlite3.connect('student_management.db')
    cur = con.cursor()
    cur.execute('''UPDATE students SET name=?, email=?, gender=?, class=?, contact=?, dob=?, address=?
                   WHERE rollno=?''', (name.get(), email.get(), gender.get(), class_var.get(), contact.get(), dob.get(), address.get(), rollno.get()))
    con.commit()
    con.close()
    get_data()
    clear()

def delete_data():
    con = sqlite3.connect('student_management.db')
    cur = con.cursor()
    cur.execute('DELETE FROM students WHERE rollno=?', (rollno.get(),))
    con.commit()
    con.close()
    get_data()
    clear()
    messagebox.showinfo('Success', 'Record deleted')

def clear():
    rollno.set("")
    name.set("")
    email.set("")
    gender.set("")
    class_var.set("")
    contact.set("")
    dob.set("")
    address.set("")

def on_focus(event):
    cursor = Student_table.focus()
    content = Student_table.item(cursor)
    row = content['values']
    if row:
        rollno.set(row[0])
        name.set(row[1])
        email.set(row[2])
        gender.set(row[3])
        class_var.set(row[4])
        contact.set(row[5])
        dob.set(row[6])
        address.set(row[7])

# UI Setup
Label_Heading = tk.Label(window, text="Student Management System", font=("Times New Roman", 35, "bold"), bg="blue", fg="pink", border=12, relief=tk.GROOVE)
Label_Heading.pack(side=tk.TOP, fill=tk.X)

Frame_Details = tk.LabelFrame(window, text="Enter details", font=("Times New Roman", 22, "bold"), bd=12, relief=tk.GROOVE, bg="#e3f4f1")
Frame_Details.place(x=20, y=100, width=400, height=575)

Frame_Data = tk.Frame(window, bd=12, relief=tk.GROOVE, bg="#e3f4f1")
Frame_Data.place(x=440, y=100, width=890, height=575)

# Variable Declarations
rollno, name, email, gender, class_var, contact, dob, address, search_box = (tk.StringVar() for _ in range(9))

# Entry widgets and labels in the details frame
labels = ["Roll No", "Name", "Email", "Gender", "Class", "Contact No", "D.O.B", "Address"]
variables = [rollno, name, email, gender, class_var, contact, dob, address]
for i, (label_text, var) in enumerate(zip(labels, variables)):
    tk.Label(Frame_Details, text=label_text, font=("Times New Roman", 17), bg="#e3f4f1").grid(row=i, column=0, padx=2, pady=2)
    tk.Entry(Frame_Details, bd=7, font=("Times New Roman", 17), width=17, textvariable=var).grid(row=i, column=1, padx=2, pady=2)

# Button frame and buttons
Frame_Btn = tk.Frame(Frame_Details, bg="#e3f4f1", bd=7, relief=tk.GROOVE)
Frame_Btn.place(x=15, y=390, width=348, height=120)

buttons = [("Add", add_data), ("Delete", delete_data), ("Update", update_data), ("Clear", clear)]
for i, (text, cmd) in enumerate(buttons):
    tk.Button(Frame_Btn, text=text, bg="#00FFFF", bd=7, font=("Times New Roman", 15), width=13, command=cmd).grid(row=i//2, column=i % 2, padx=2, pady=2)

# Search Frame
Frame_Search = tk.Frame(Frame_Data, bg="#1E90FF", bd=10, relief=tk.GROOVE)
Frame_Search.pack(side=tk.TOP, fill=tk.X)

tk.Label(Frame_Search, text="Search", bg="#e3f4f1", font=("Times New Roman", 16)).grid(row=0, column=0, padx=12, pady=2)
Search_Box = ttk.Combobox(Frame_Search, font=("Times New Roman", 16), state="readonly", textvariable=search_box)
Search_Box['values'] = ("Name", "Roll No", "Email", "Class", "Contact No", "D.O.B")
Search_Box.grid(row=0, column=1, padx=12, pady=2)
tk.Button(Frame_Search, text="Search", bg="#e3f4f1", bd=7, font=("Times New Roman", 15), width=14).grid(row=0, column=2, padx=12, pady=2)
tk.Button(Frame_Search, text="Show All", bg="#76EE00", bd=7, font=("Times New Roman", 15), width=14, command=get_data).grid(row=0, column=3, padx=12, pady=2)

# Database Table Frame
Frame_Database = tk.Frame(Frame_Data, bg="#0000FF", bd=11, relief=tk.GROOVE)
Frame_Database.pack(fill=tk.BOTH, expand=True)

Scroll_X = tk.Scrollbar(Frame_Database, orient=tk.HORIZONTAL)
Scroll_Y = tk.Scrollbar(Frame_Database, orient=tk.VERTICAL)

columns = ["Roll No", "Name", "Email", "Gender", "Class", "Contact No", "D.O.B", "Address"]
Student_table = ttk.Treeview(Frame_Database, columns=columns, xscrollcommand=Scroll_X.set, yscrollcommand=Scroll_Y.set)

Scroll_X.config(command=Student_table.xview)
Scroll_Y.config(command=Student_table.yview)
Scroll_X.pack(side=tk.BOTTOM, fill=tk.X)
Scroll_Y.pack(side=tk.RIGHT, fill=tk.Y)

for col in columns:
    Student_table.heading(col, text=col)
    Student_table.column(col, width=100)
Student_table['show'] = 'headings'
Student_table.pack(fill=tk.BOTH, expand=True)
Student_table.bind("<ButtonRelease-1>", on_focus)

# Initialize database table
create_table()

# Run the application
window.mainloop()
