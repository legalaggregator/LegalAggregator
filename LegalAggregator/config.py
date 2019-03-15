import pymysql

def get_conn():
    return pymysql.connect(host="localhost", user="username", passwd="password", database="database")


