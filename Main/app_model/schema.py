import sqlite3
#create connection to project_data database
conn = sqlite3.connect("DATA/project_data.db")
cur = conn.cursor()
#create SQL table 'user'
def create_user_table(conn):
    cur = conn.cursor()
    #fields in the table
    sql = '''CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    roles TEXT NOT NULL,
    phone_num TEXT NOT NULL);
    '''
    cur.execute(sql)
    conn.commit()

