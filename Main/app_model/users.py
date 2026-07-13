#'''file contains information about a created SQL table with user's information 
# and methods to get or move information from and to it. All this information is stored in the project_data database'''
#function to add the user into the table
def add_user(conn,username,password_hash,roles,phone_num):
    cur = conn.cursor()
    sql = '''INSERT INTO user(username,password_hash,roles,phone_num) VALUES (?,?,?,?)'''
    pm =  (username,password_hash,roles,phone_num)
    cur.execute(sql,pm)
    conn.commit()

#moves user into database
def migrate_user(conn):
    with open('DATA/user.txt','r')as f:
        users = f.readlines()
    for user in users:
        username,password_hash,roles,phone_num = user.strip().split(',')
        add_user(conn,username,password_hash,roles,phone_num)


#reads data from user
def get_all_users(conn):
    cur = conn.cursor()
    sql = '''SELECT * FROM user'''
    cur.execute(sql)
    users = cur.fetchall()
    return users

#reads just one user based on their name
def get_user(conn,username):
    cur = conn.cursor()
    sql = '''SELECT username, password_hash, roles FROM user WHERE username = ?'''
    parm = (username,)
    cur.execute(sql,parm)
    user = cur.fetchone()
    return user

#reads one user based on their phone number
def get_user_by_phone_num(conn,phone_num):
    cur = conn.cursor()
    sql = '''SELECT username, password_hash,roles,phone_num FROM user WHERE phone_num = ?'''
    parm = (phone_num,)
    cur.execute(sql,parm)
    user = cur.fetchone()
    return user

#updates user information
def update_user(conn,phone_num,password_hash):
    sql = 'UPDATE user SET password_hash = ? WHERE phone_num = ?'
    cur = conn.cursor()
    param = (password_hash,phone_num)
    cur.execute(sql,param)
    conn.commit() 

#deletes field in a user's row
def delete_user(conn,user_n):
    sql = 'DELETE FROM user WHERE username = ?'
    cur = conn.cursor()
    param = (user_n,)
    cur.execute(sql,param)
    conn.commit() 