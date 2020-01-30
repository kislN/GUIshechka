import psycopg2

db_connect = {'port': 5432,
              'host': "localhost",
              'user': "postgres",
              'dbname': "test"}



# db_connect = {'port': 5432,
#               'host': "localhost",
#               'user': "postgres"}
#
#
# def create_database_proc():
#     conn = psycopg2.connect(**db_connect, database="postgres")
#     cur = conn.cursor()
#
#     cur.execute(
#         "CREATE OR REPLACE FUNCTION create_database(dbname varchar(50))"
#         " RETURNS VOID AS $$ "
#         "BEGIN "
#         "CREATE DATABASE dbname;"
#         "END;"
#         "$$ LANGUAGE plpgsql;",
#     )
#
#     cur.close()
#     conn.commit()
#
#
# def create_database_procc():
#     conn = psycopg2.connect(**db_connect, database="postgres")
#     cur = conn.cursor()
#
#     cur.execute(
#         "CREATE PROCEDURE create_database(IN dbname varchar(50))"
#         "AS $$ "
#         "BEGIN "
#         "CREATE DATABASE dbname;"
#         "END;"
#         "$$ LANGUAGE plpgsql;",
#     )
#
#     cur.close()
#     conn.commit()




def create_all_tables_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.execute(
        "CREATE OR REPLACE PROCEDURE create_all_tables() AS $$ "
        "BEGIN "
        "CREATE TABLE if not exists patients (patient_id SERIAL PRIMARY KEY , name varchar(50),"
        "datebirth date, sex varchar(5));"
        "CREATE TABLE if not exists pinfo (pinfo_id SERIAL PRIMARY KEY, weight integer, "
        "height integer, allergy varchar(50)); "
        "CREATE TABLE if not exists ps_map (ps_id SERIAL PRIMARY KEY, patient_id integer, pinfo_id integer); "
        "CREATE TABLE if not exists appointment (app_id SERIAL PRIMARY KEY, person_id integer, service_name varchar(50), "
        "doctor_id integer, price integer, time varchar(50), diagnosis varchar(50)); "
        "CREATE TABLE if not exists doctors (doctor_id SERIAL PRIMARY KEY, doctor_name varchar(50),"
        "profession varchar(50), experience integer);"
        "END;"
        "$$ LANGUAGE plpgsql;")

    cur.close()
    conn.commit()


def insert_doctor_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION insert_doctor(doc_name varchar(50), profession varchar(50), experience integer) "
        "RETURNS VOID AS $$ "
        "BEGIN "
            "INSERT INTO doctors(doctor_name , profession, experience) VALUES (doc_name, profession, experience);"
        "END;"
        "$$ LANGUAGE plpgsql;",
        )

    cur.close()
    conn.commit()

def insert_patient_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION insert_patient(name varchar(50), datebirth date, sex varchar(5)) "
        "RETURNS VOID AS $$  "
        "BEGIN "
            "INSERT INTO patients(name, datebirth, sex) VALUES (name, datebirth, sex);"
        "END;"
        "$$ LANGUAGE plpgsql;",
        )

    cur.close()
    conn.commit()

def view_patient_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION veiw_patients() "
        "RETURNS VOID AS $$ "
        "BEGIN "
            "SELECT * FROM patients; "
        "END;"
        "$$ LANGUAGE plpgsql;",
        )

    cur.close()
    conn.commit()



def insert_appointment_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION insert_appointment(_person_name varchar(50), _birthdate date, "
            "_service varchar(50), _doc_name varchar(50), _price integer, _app_time varchar(50)) "
        "RETURNS VOID AS $$ "
        "BEGIN "
            "INSERT INTO patients(name, datebirth)" 
            "SELECT _person_name, _birthdate "
            "WHERE NOT EXISTS ("
            "SELECT 1 FROM patients WHERE name=_person_name and datebirth=_birthdate); "
            " INSERT INTO appointment(person_id, service_name , doctor_id, price, time) "
                "VALUES ((SELECT patient_id from patients where name=_person_name and datebirth=_birthdate),"
                        "_service, "
                        "(SELECT doctor_id from doctors where doctor_name=_doc_name), "
                        "_price, _app_time);"
        "END;"
        "$$ LANGUAGE plpgsql;",
        )

    cur.close()
    conn.commit()


def search_patient_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION search_patient(patient_name varchar(50), birthdate date, _sex varchar(10))"
        " RETURNS TABLE (search_id integer, search_name varchar(50), search_datebirth date, search_sex varchar(10)) AS $$ "
        "BEGIN "
            "RETURN QUERY "
                "SELECT patient_id, name, datebirth, sex FROM patients WHERE name=patient_name AND datebirth=birthdate AND "
                "sex=_sex; "
        "END; "
        "$$ LANGUAGE plpgsql;",
        )
    cur.close()
    conn.commit()


def get_docnames_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION get_docnames()"
        " RETURNS TABLE (search_name varchar(50)) AS $$ "
        "BEGIN "
            "RETURN QUERY "
                "SELECT doctor_name FROM doctors; "
        "END; "
        "$$ LANGUAGE plpgsql;",
        )
    cur.close()
    conn.commit()




def get_appointments_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION get_appointments()"
        " RETURNS TABLE (id integer, patient varchar(50), serv varchar(50), doctor varchar(50),"
        "_price integer, _time_app varchar(50)) AS $$ "
        "BEGIN "
            "RETURN QUERY "
                "SELECT app_id, name, service_name, doctor_name, price, time FROM appointment inner join doctors on "
                "appointment.doctor_id = doctors.doctor_id inner join patients on person_id=patient_id; "
        "END; "
        "$$ LANGUAGE plpgsql;",
        )
    cur.close()
    conn.commit()




def search_doctor_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION search_doctor(doc_name varchar(50), prof varchar(50), exp integer)"
        " RETURNS TABLE (search_id integer, search_name varchar(50), search_prof varchar(50), exper varchar(10)) AS $$ "
        "BEGIN "
            "RETURN QUERY "
                "SELECT doctor_id, doctor_name, profession, experience FROM patients "
                "WHERE doctor_name=doc_name AND profession=prof AND experience=exp; "
        "END; "
        "$$ LANGUAGE plpgsql;",
        )
    cur.close()
    conn.commit()

def delete_patient_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION delete_patient(_name varchar(50), _datebirth date) "
        "RETURNS VOID AS $$ "
        "BEGIN "
            "DELETE FROM patients where name=_name and datebirth=_datebirth; "
        "END;"
        "$$ LANGUAGE plpgsql;"
    )
    cur.close()
    conn.commit()

#new
def delete_doctor_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    cur.execute(
        "CREATE OR REPLACE FUNCTION  delete_doctor(_name varchar(50)) "
        "RETURNS VOID AS $$ "
        "BEGIN "
            "DELETE FROM doctors where doctor_name=_name; "
        "END;"
        "$$ LANGUAGE plpgsql;"
    )
    cur.close()
    conn.commit()

def clear_all_tables_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION clear_all_tables() "
        "RETURNS VOID AS $$ "
        "BEGIN "
        "DELETE FROM patients; "
        "DELETE FROM pinfo; "
        "DELETE FROM ps_map; "
        "DELETE FROM appointment; "
        "DELETE FROM doctors; "
        "END;"
        "$$ LANGUAGE plpgsql;"
    )
    cur.close()
    conn.commit()

def clear_table_proc():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()

    cur.execute(
        "CREATE OR REPLACE FUNCTION clear_table(title varchar(50)) "
        "RETURNS VOID AS $$ "
        "BEGIN "
        "IF (title = 'patients') THEN "
        "DELETE FROM patients; "
        "END IF;"
        "IF (title = 'pinfo') THEN "
        "DELETE FROM pinfo; "
        "END IF;"
        "IF (title = 'ps_map') THEN "
        "DELETE FROM ps_map; "
        "END IF;"
        "IF (title = 'appointment') THEN "
        "DELETE FROM appointment; "
        "END IF;"
        "IF (title = 'doctors') THEN "
        "DELETE FROM doctors; "
        "END IF;"
        "END;"
        "$$ LANGUAGE plpgsql;"
    )
    cur.close()
    conn.commit()

def insert():
    conn = psycopg2.connect(**db_connect)
    cur = conn.cursor()
    # cur.callproc('create_all_tables')
    cur.execute("CALL create_all_tables();")
    cur.close()
    conn.commit()

def new_start():
    create_all_tables_proc()
    insert_doctor_proc()
    insert_patient_proc()
    view_patient_proc()
    insert_appointment_proc()
    search_patient_proc()
    get_docnames_proc()
    get_appointments_proc()
    search_doctor_proc()
    delete_patient_proc()
    delete_doctor_proc()
    clear_all_tables_proc()
    clear_table_proc()
    insert()

