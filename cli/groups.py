from mysql.connector import MySQLConnection, Error

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()


def view_groups(user):
    print("Viewing groups")
    return


def create_group(user):
    print("creating group")
    return

def view_specific_group(user, group):
    print("Viewing a specific group")
    return