#file contains method to retrive data from created SQL table and move this table into the project_data database
import pandas as pd
#used to move table to created database
def migrate_datasets_metadata(conn):  
    data = pd.read_csv('DATA/datasets_metadata.csv')
    data.to_sql('datasets_metadata',conn)

#used to get all information from table 
def get_all_datasets_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql,conn)
    conn.close()
    return data 