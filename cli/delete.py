from mysql.connector import MySQLConnection, Error
import home
import login

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()

# delete account and all info related to it
def delete_account(user):
    print("-----------------------------------------------")
    option = raw_input("Are you sure you want to permanently delete your acount"
                       + "and all information related to it (y/n):\n")
    while True:
        if option == 'y':
            cursor.callproc('del_user', [user])
            cnx.commit()
            print("Your account has been deleted")
            return login.start()
        elif option == 'n':
            print("Account deletion has been canceled")
            return home.landing(user)
        else:
            option = raw_input("command not recognized. Enter 'y' or 'n'\n")
