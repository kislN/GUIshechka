from proc import *

db_connect = {'port': 5432,
              'host': 'localhost',
              'user': "postgres",
              'dbname': 'test'}



def insert_doctor_call(doc_name, profession, experience, win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('insert_doctor', [doc_name, profession, experience])
    cur.close()
    conn.commit()
    win.destroy()

def get_docnames_call():
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('get_docnames', ())
    return cur.fetchall()

def search_patient_call(name, date, sex):
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('search_patient', (name, date, sex))
    return cur.fetchall()

def search_doctor_call(name, prof, exp):
    conn = psycopg2.connect(**db_connect)
    cur=conn.cursor()
    cur.callproc('search_doctor', (name, prof, exp))
    return cur.fetchall()

def insert_patient_call(name, datebirth, sex, win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('insert_patient', [name, datebirth, sex])
    cur.close()
    conn.commit()
    win.destroy()


def delete_patient_call(name, datebirth,win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('delete_patient', [name, datebirth])
    cur.close()
    conn.commit()
    win.destroy()

#new
def delete_doctor_call(name, win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('delete_doctor', [name])
    cur.close()
    conn.commit()
    win.destroy()

def clear_all_tables_call():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('clear_all_tables')
    cur.close()
    conn.commit()

def clear_table_call(title, win):
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.callproc('clear_table', [title])
    cur.close()
    conn.commit()
    win.destroy()