import pymysql as sql
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pymysql.cursors import DictCursor


def create_database():
    conn = psycopg2.connect(port=5432,
              host="localhost",
              user="postgres",
              dbname="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur=conn.cursor()
    # cur.execute("DROP DATABASE IF EXISTS test")
    cur.execute("CREATE DATABASE test")
    cur.close()
    conn.close()

def delete_database():
    conn = psycopg2.connect(port=5432,
              host="localhost",
              user="postgres",
              dbname="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS test")
    cur.close()
    conn.close()

try:
    create_database()
except psycopg2.errors.DuplicateDatabase:
    print('db already exists')
else:
    from proc import *
    new_start()



#new
# db_connect = {'port': 5432,
#               'host': "localhost",
#               'user': "postgres"}
#
#
#
# con = psycopg2.connect(
#     **db_connect,
#     database="postgres")

