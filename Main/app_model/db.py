import sqlite3
#creates a function that other files will use to connect to the created database 
def get_conn():
    conn = sqlite3.connect('DATA/project_data.db', check_same_thread=False)
    return conn