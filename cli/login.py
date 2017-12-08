from mysql.connector import MySQLConnection, Error
import home

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()


# Startup login or create account
def start():
    print("--------------Student Organization Database----------------")
    while True:
        option = raw_input("Please login with 'login' or create an account with 'create'.\n")
        if option == "login":
            return login()
        elif option == "create":
            return new_user()
        else:
            print("Command not recognized.")


# Login Function
def login():
    print("----------------Login---------------\n Go back with back")
    while True:
        name = raw_input("Enter your username:\n")
        if name == 'back':
            return start()
        password = raw_input("Enter your password:\n")
        if password == 'back':
            return start()
        result_args = cursor.callproc('login', [name, password, 0])
        if result_args[2]:
            print("Login Successful: You are logged in as " + name)
            return home.landing(name)
        else:
            print("Incorrect username or password. Go back to start with 'back'")


# Account Creation Function
def new_user():
    print("----------------Account Creation-----------------\n go back with 'back'")
    while True:
        username = raw_input("Enter a username for the account:\n")
        if username == 'back':
            return start()
        password = raw_input("Enter a password for the account:\n")
        if password == 'back':
            return start()
        name = raw_input("Enter your name to be used on the account:\n")
        if name == 'back':
            return start()
        result_args = cursor.callproc('new_user', [username, password, name, 0])
        if result_args[3]:
            print("Account Successfully Created")
            cnx.commit()
            return home.landing(username)
        else:
            print("The username entered is unavailable")
