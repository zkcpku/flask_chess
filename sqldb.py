import sqlite3
import os
import hashlib

USER_HASH = True

def get_md5(data):
    obj = hashlib.md5("to make md5 more difficult".encode('utf-8'))
    obj.update(data.encode('utf-8'))
    result = obj.hexdigest()
    return result

def init_db(path = 'data/user.db'):
    dbConn=sqlite3.connect(path,check_same_thread=False)
    create_tb_cmd = '''
        CREATE TABLE IF NOT EXISTS USER
        (USERNAME TEXT,
        PASSWD TEXT);
    '''
    try:
        dbConn.execute(create_tb_cmd)
    except:
        print("create db error")
        assert(False)    
    return dbConn

dbConn = init_db()

def search_user(username,sql = dbConn):
    rst = sql.execute("SELECT * FROM USER WHERE USERNAME='%s'" % str(username))
    data = rst.fetchall()
    rst.close()
    return data


def create_user(username,passwd,use_hash = USER_HASH):
    if use_hash:
        passwd = get_md5(passwd)

    users = search_user(username)
    if len(users) != 0:
        return False


    cmd = "INSERT INTO USER(USERNAME,PASSWD) VALUES (?,?)"
    rst = dbConn.execute(cmd,(str(username),str(passwd)))
    print(rst.fetchall())
    rst.close()
    dbConn.commit()
    return True

def login_user(username,passwd,use_hash = USER_HASH, sql = dbConn):
    if use_hash:
        passwd = get_md5(passwd)
    rst = sql.execute("SELECT * FROM USER WHERE USERNAME='%s'" % str(username))
    data = rst.fetchall()
    rst.close()

    if len(data) == 0:
        return False,None
    else:
        return data[0][1] == passwd, username


def showalldata(sql = dbConn):
    rst = sql.execute("SELECT * FROM USER")
    data = rst.fetchall()
    rst.close()
    return data


if __name__ == '__main__':
    print(showalldata())
    # print(login_user('root','123456789abc'))
    print(create_user('root','123456789abc'))
    print(showalldata())
    print(login_user('root','123'))
    print(login_user('root','123456789abc'))