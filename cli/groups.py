from mysql.connector import MySQLConnection, Error
import home

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()

def view_groups(user):
    print("Viewing groups")
    return home.landing(user)