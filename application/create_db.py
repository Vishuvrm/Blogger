# pip install mysql-connector
# pip install mysql-connector-python
# pip install mysql-connector-python-rf
import mysql.connector

def create_db(host="localhost", user="root", passwd="passwd", db="users"):
    mydb = mysql.connector.connect(host="localhost",
                                   user="root",
                                   passwd="")
    cur = mydb.cursor()
    cur.execute(f"""CREATE DATABASE IF NOT EXISTS {db}""")
    cur.execute("SHOW DATABASES")
    print("Create database users")

if __name__ == "__main__":
    create_db()