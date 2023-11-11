import MySQLdb
from MySQLdb import DatabaseError
from flask_mysqldb import MySQL
from decouple import config


def getConnection():
    try:
        return MySQLdb.connect(
            host=config('MYSQL_HOST'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            database=config('MYSQL_DATABASE')
        )
    except DatabaseError as ex:
        raise ex
    

