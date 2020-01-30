from tkinter import *
from connect import *
import tkinter.ttk as ttk
import tkinter as tk
from calls import *
from proc import *

objects=[]

db_connect = {'port': 5432,
              'host': 'localhost',
              'user': "postgres",
              'dbname': 'test', }



counter = 0

def get_appointments_call():
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('get_appointments', ())
    return view(tree, cur.fetchall())

def add_appointment():
    list_enters=[e1, e2, e3, comboExample, e5, e6]
    values = tuple([e.get() for e in list_enters])
    if not all([True if value!='' else False for value in values]):
        new_window = Toplevel(window)
        label = Label(new_window, text='Please, enter the data')
        label.grid(row=0, column=0)
        return

    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('insert_appointment', values)
    cur.close()
    conn.commit()
    get_appointments_call()
    for enter in list_enters:
        enter.delete(0, END)


def view(tree, records):
    tree.delete(*tree.get_children())
    for record in records:
        output_text = []
        for item in record:
            output_text.append(str(item))
        tree.insert('', 'end', text=output_text[0],
                    values=tuple(output_text[1:]))


def all_patients_view():
    new_window = Toplevel(window)
    tree = ttk.Treeview(new_window,
                        columns=('First name', 'Second name',
                                 'Age', 'Weight'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Name')
    tree.heading('#2', text='Date of birth')
    tree.heading('#3', text='Sex')

    tree.column('#0', stretch=YES, width=30)
    tree.column('#1', stretch=YES, width=150)
    tree.column('#2', stretch=YES, width=150)
    tree.column('#3', stretch=YES, width=100)
    tree.grid(row=2, columnspan=4, sticky='nsew')

    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    records = cur.fetchall()
    conn.close()
    view(tree, records)

def all_doctors_view():
    new_window = Toplevel(window)
    tree = ttk.Treeview(new_window,
                        columns=('Name', 'Profession',
                                 'Experience'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Name')
    tree.heading('#2', text='Profession')
    tree.heading('#3', text='Experience')

    tree.column('#0', stretch=YES, width=30)
    tree.column('#1', stretch=YES, width=150)
    tree.column('#2', stretch=YES, width=80)
    tree.column('#3', stretch=YES, width=80)
    tree.grid(row=2, columnspan=4, sticky='nsew')

    conn = psycopg2.connect(**db_connect)

    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors")
    records = cur.fetchall()
    conn.close()
    view(tree, records)

def new_doctor_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, add a new doctor")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)
    l2 = Label(new_window, text='Profession')
    l2.grid(row=1, column=2)
    l3 = Label(new_window, text='Experience')
    l3.grid(row=3, column=0)

    name = StringVar()
    e1 = Entry(new_window, textvariable=name)
    e1.grid(row=1, column=1)
    profession = StringVar()
    e2 = Entry(new_window, textvariable=profession)
    e2.grid(row=1, column=3)
    experience = StringVar()
    e3 = Entry(new_window, textvariable=experience)
    e3.grid(row=3, column=1)

    add_doctor_to_datebase = Button(new_window, text='Add', width=12,
                                    command=lambda: insert_doctor_call(e1.get(), e2.get(), e3.get(), new_window))
    add_doctor_to_datebase.grid(row=4, column=3)
    new_window.mainloop()

def delete_patient_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, delete a patient")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)
    l2 = Label(new_window, text='Date of birth')
    l2.grid(row=1, column=2)

    e1 = Entry(new_window, textvariable=StringVar())
    e1.grid(row=1, column=1)

    e2 = Entry(new_window, textvariable=StringVar())
    e2.grid(row=1, column=3)

    del_patient_from_datebase = Button(new_window, text='Delete', width=12,
                                    command=lambda: delete_patient_call(e1.get(), e2.get(), new_window))
    del_patient_from_datebase.grid(row=4, column=3)
    new_window.mainloop()

#new
def delete_doctor_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, delete a doctor")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)

    e1 = Entry(new_window, textvariable=StringVar())
    e1.grid(row=1, column=1)

    del_doctor_from_datebase = Button(new_window, text='Delete', width=12,
                                    command=lambda: delete_doctor_call(e1.get(), new_window))
    del_doctor_from_datebase.grid(row=4, column=3)
    new_window.mainloop()


def new_patient_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, add a new patient")
    display.grid(row=0)
    l1 = Label(new_window, text='Name')
    l1.grid(row=1, column=0)
    l2 = Label(new_window, text='Date of birth')
    l2.grid(row=1, column=2)
    l3 = Label(new_window, text='Sex')
    l3.grid(row=2, column=0)

    name = StringVar()
    e1 = Entry(new_window, textvariable=name)
    e1.grid(row=1, column=1)
    datebirth = StringVar()
    e2 = Entry(new_window, textvariable=datebirth)
    e2.grid(row=1, column=3)
    sex = StringVar()
    e3 = Entry(new_window, textvariable=sex)
    e3.grid(row=2, column=1)

    add_patient_to_datebase = Button(new_window, text='Add patient', width=12,
                                     command=lambda: insert_patient_call(e1.get(), e2.get(), e3.get(), new_window))
    add_patient_to_datebase.grid(row=2, column=3)
    new_window.mainloop()


def clear_table_window():
    new_window = Toplevel(window)
    display = Label(new_window, text="Please, enter title of the table")
    display.grid(row=0)
    l1 = Label(new_window, text='Table')
    l1.grid(row=1, column=0)

    title = StringVar()
    e1 = Entry(new_window, textvariable=title)
    e1.grid(row=1, column=1)


    clear_this = Button(new_window, text='Clear the table', width=12,
                                     command=lambda: clear_table_call(e1.get(), new_window))
    clear_this.grid(row=2, column=3)
    new_window.mainloop()


def delete():
    curItem = tree.focus()
    conn = psycopg2.connect(
        port=5432,
        host='localhost',
        user="postgres",
        dbname='test',
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE first_name=? OR "
                "sec_name=? OR age=? OR weight=?;", (e1.get(), e2.get(), e3.get(), e4.get()))
    records = cur.fetchall()
    conn.close()


def delete_all():
    global counter
    counter = 0
    tree.delete(*tree.get_children())
    conn = psycopg2.connect(**db_connect)

    cur = conn.cursor()
    cur.execute("DELETE FROM book;")
    conn.commit()
    conn.close()

def delete_db2():
    delete_database()
    window.destroy()

def delete_db1():
    new_window = Toplevel(window)
    del_button = Button(new_window, text='Delete the database?', height=4,
                                     command=delete_db2)
    del_button.grid(row=1, column=1)
    new_window.mainloop()



window = Tk()

l1 = Label(window, text='Name')
l1.grid(row=0, column=0)
objects.append(l1)

l2 = Label(window, text='Date of birth')
l2.grid(row=0, column=2)
objects.append(l2)

l3 = Label(window, text='Service')
l3.grid(row=0, column=4)
objects.append(l3)

l4 = Label(window, text='Doctors')
l4.grid(row=1, column=0)
objects.append(l4)

l5 = Label(window, text='Price')
l5.grid(row=1, column=2)
objects.append(l5)

l6 = Label(window, text='Time')
l6.grid(row=1, column=4)
objects.append(l6)

## =====================================

e1 = Entry(window, textvariable=StringVar())
e1.grid(row=0, column=1)
objects.append(e1)

e2 = Entry(window, textvariable=StringVar())
e2.grid(row=0, column=3)
objects.append(e2)

e3 = Entry(window, textvariable=StringVar())
e3.grid(row=0, column=5)
objects.append(e3)

e5 = Entry(window, textvariable=StringVar())
e5.grid(row=1, column=3)
objects.append(e5)

e6 = Entry(window, textvariable=StringVar())
e6.grid(row=1, column=5)
objects.append(e6)

## =====================================

list1 = Listbox(window, height=8, width=35)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)
objects.append(list1)

## =====================================
scr = Scrollbar(window)
scr.grid(row=2, column=2, rowspan=6, )
objects.append(scr)

list1.configure(yscrollcommand=scr.set)
scr.configure(command=list1.yview)

## =====================================

submit_button = Button(window, text='Add patient', width=12, command=new_patient_window)
submit_button.grid(row=2, column=5)
objects.append(submit_button)

view_patients_button = Button(window, text='View patients', width=12, command=all_patients_view)
view_patients_button.grid(row=3, column=5)
objects.append(view_patients_button)

add_doctor_button = Button(window, text='Add doctor', width=12, command=new_doctor_window)
add_doctor_button.grid(row=4, column=5)
objects.append(add_doctor_button)

view_doctors_button = Button(window, text='View doctors', width=12, command=all_doctors_view)
view_doctors_button.grid(row=5, column=5)
objects.append(view_doctors_button)

add_appo = Button(window, text='New appointment', width=12, command=add_appointment)
add_appo.grid(row=2, column=3)
objects.append(add_appo)

refresh_appo = Button(window, text='Apps', width=12, command=get_appointments_call)
refresh_appo.grid(row=2, column=4)
objects.append(refresh_appo)

delete_patient_button = Button(window, text='Del patient', width=12, command=delete_patient_window)
delete_patient_button.grid(row=2, column=6)
objects.append(delete_patient_button)

#new
delete_doctor_button = Button(window, text='Del doctor', width=12, command=delete_doctor_window)
delete_doctor_button.grid(row=3, column=6)
objects.append(delete_doctor_button)

delete_database_button = Button(window, text='Del database', width=12, command=delete_db1)
delete_database_button.grid(row=4, column=6)
objects.append(delete_database_button)

clear_all_tables_button = Button(window, text='Clear all', width=12, command=clear_all_tables_call)
clear_all_tables_button.grid(row=3, column=4)

clear_table_button = Button(window, text='Clear table', width=12, command=clear_table_window)
clear_table_button.grid(row=4, column=4)

tree = ttk.Treeview(window,
                    columns=('id', 'Patient',
                             'Service', 'Doctor', 'Price', 'Time' ))
tree.heading('#0', text='id')
tree.heading('#1', text='Patient')
tree.heading('#2', text='Service')
tree.heading('#3', text='Doctor')
tree.heading('#4', text='Price')
tree.heading('#5', text='Time')

tree.column('#0', stretch=YES, width=30)
tree.column('#1', stretch=YES, width=150)
tree.column('#2', stretch=YES, width=150)
tree.column('#3', stretch=YES, width=150)
tree.column('#4', stretch=YES, width=90)
tree.column('#5', stretch=YES, width=90)

tree.grid(row=8, columnspan=10,)
treeview = tree


comboExample = ttk.Combobox(window,
                            values=get_docnames_call())

comboExample.grid(row=1, column=1)


# connect()

entry_list = [children for children in window.children.values() if 'entry' in str(children)]
window.mainloop()


"""1) Идем в proc.py и создаем новую процедуру
2) стоит проверить её работу через bash (select * func_name(...) )
3) Создаём в calls.py вызов этой функции
4) Делаем кнопку, которая будет вызывать нашу процедуру
5) Если нужен вызов нового окна, то делаем def ..._new_window()
6) В этом новом окне создаём кнопку, которая уже и будет выполнять вызов функции call из шага 3
7) всё
"""