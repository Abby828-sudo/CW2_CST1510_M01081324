#file contains method to retrive data from created SQL table and move this table into the project_data database
import pandas as pd
#moves the SQL table to the project_data database
def migrate_cyber_incidents(conn):  
    data = pd.read_csv('DATA/cyber_incidents.csv')
    data.to_sql('cyber_incidents',conn)

#retrives all information from the table
def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql,conn)
    conn.close()
    return data 
