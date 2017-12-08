from mysql.connector import MySQLConnection, Error
import home

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()


def main(user):
    print("add connections")
    return home.landing(user)