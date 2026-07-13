#file contains method to retrive data from created SQL table and move this table into the project_data database
import pandas as pd
#moves the SQL table into project_data database
def migrate_it_tickets(conn):  
    data = pd.read_csv('DATA/it_tickets.csv')
    data.to_sql('it_tickets',conn)

#gets all the information in the table
def get_all_it_tickets(conn):
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql,conn)
    conn.close()
    return data 

