from mysql.connector import MySQLConnection, Error

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()


def main(user):
    cursor.callproc("view_connections", [user])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no results")
        else:
            while row is not None:
                print("Username: " + row[0])
                row = result.fetchone()
            print("There are no additional users you are connected to.")
            print("------------------------------------------------")
            break
    print("To remove a user from your connections enter remove and their user name"
          "Like remove user. Go back with 'back'")
    while True:
        option = raw_input("Enter a command:\n")
        split = option.split(" ", 1)
        if option == 'back':
            return
        elif split[0] == 'remove':
            cursor.callproc("drop_connection", [user, split[1]])
            cnx.commit()

