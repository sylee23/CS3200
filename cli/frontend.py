from mysql.connector import MySQLConnection, Error

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()


# Login Function
def login():
    print("Login:")
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
            return name
        else:
            print("Incorrect username or password. Go back to start with 'back'")


# Account Creation Function
def new_user():
    while True:
        username = raw_input("Enter a username for the account:\n")
        if password == 'back':
            return start()
        password = raw_input("Enter a password for the account:\n")
        if password == 'back':
            return start()
        name = raw_input("Enter your name to be used on the account:\n")
        if password == 'back':
            return start()
        result_args = cursor.callproc('new_user', [username, password, name, 0])
        if result_args[3]:
            print("Account Successfully Created")
            cnx.commit()
            return username
        else:
            print("The username entered is unavailable")


# Startup login or create account
def start():
    print("Student Organization Database")
    while True:
        option = raw_input("Please login with 'login' or create an account with 'create'.\n")
        if option == "login":
            return login()
        elif option == "create":
            return new_user()
        else:
            print("Command not recognized.")


# Landing Page
def landing(user):
    print("---Home---")
    print("Search for users with: 'search-users'")
    print("View and edit your profile with 'profile'")
    print("Delete your account with 'delete-account'")
    print("Logout of your account with logout")
    while True:
        option = raw_input("Please enter a command:\n")
        if option == "search-users":
            search_users(user)
        elif option == "profile":
            return view_own_profile(user)
        elif option == "delete-account":
            return delete_account(user)
        elif option == "logout":
            print("You are now logged out of your account")
            return start()
        else:
            print("Command not recognized. Valid commands are: search-users,"
                  + " profile, delete-account, logout")


# Search for accounts
def search_users(user):
    tag = raw_input("Enter a tag to search users with:\n")
    cursor.callproc("search_user_tag", [tag])
    print("Users are listed in descending order of relevance")
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no results")
        else:
            while row is not None:
                print("Username: " + row[0] + ", Name: " + row[1])
                row = result.fetchone()
            print("There are no additional results")
    while True:
        option = raw_input("View a profile with: 'view-user Username', "
                           + "search again with 'search-users', or go back to home with 'home'\n")
        split = option.split(" ", 1)
        if option == "home":
            return landing(user)
        elif option == "search":
            return search_users(user)
        elif split[0] == "view-user":
            view_other_user(split[1])
        else:
            print("Command not recognized")


def xstr(s):
    if s is None:
        return ''
    return str(s)


# View another users profile
def view_other_user(viewing):
    print("Veiwing the profile of " + viewing)
    cursor.callproc("view_user", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("Profile not found.")
        else:
            while row is not None:
                print("Name: " + xstr(row[0]) + "\nDescription: "
                      + xstr(row[1]) + "\nYear-of-Graduation: " + xstr(row[2]) + "\nEmail: "
                      + xstr(row[3]) + "\nPhone: " + xstr(row[4]))
                row = result.fetchone()
            # print("For Additional Information use 'view research'")
            # Also do co-ops, courses, research, study-abroad etc
            print("Go back to search results with 'back'")
            while True:
                option = raw_input("Enter a command:\n")
                split = option.split(" ", 1)
                if option == "back":
                    return
                # elif split[0] == "view":
                #    if split[1] == "research":
                #       view_research(viewing)
                else:
                    # Fix this in final version
                    print("Valid command is: 'back'")  # and 'view research'")


# View another users research not including this for demo
def view_research(viewing):
    print("Implement research")


# View own profile
def view_own_profile(user):
    print("Welcome to your Profile")
    cursor.callproc("view_user", [user])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("Profile not found.")
        else:
            while row is not None:
                print("Username: " + user + "\nName: " + xstr(row[0]) + "\nDescription: "
                      + xstr(row[1]) + "\nYear of Graduation: " + xstr(row[2]) + "\nEmail Address: "
                      + xstr(row[3]) + "\nPhone: " + xstr(row[4]))
                row = result.fetchone()
            # print("For Additional Information use 'view research'")
            # Also do co-ops, courses, research, study-abroad etc
            while True:
                print("Go back to home with 'back' or edit profile with"
                      + " 'edit' and the field-name and value. For example edit year-of-graduation 2014")
                option = raw_input("Enter a command:\n")
                split = option.split(" ", 2)
                if option == "back":
                    return landing(user)
                elif split[0] == "edit":
                    if split[1] == "name":
                        cursor.execute("UPDATE users SET real_name=%s WHERE username=%s", (split[2], user))

                    elif split[1] == "description":
                        cursor.execute("UPDATE users SET Description=%s WHERE username=%s", (split[2], user))
                    elif split[1] == "year-of-graduation":
                        cursor.execute("UPDATE users SET gradYear=%s WHERE username=%s", (split[2], user))
                    elif split[1] == "email":
                        cursor.execute("UPDATE users SET email=%s WHERE username=%s", (split[2], user))
                    elif split[1] == "phone":
                        cursor.execute("UPDATE users SET phone=%s WHERE username=%s", (split[2], user))
                    else:
                        print("Invalid Command")
                        continue
                    cnx.commit()
                    return view_own_profile(user)
                else:
                    # Fix this in final version
                    print("Invalid Command")  # and 'view research'")


# delete account and all info related to it
def delete_account(user):
    option = raw_input("Are you sure you want to permanently delete your acount"
                       + "and all information related to it: y/n\n")
    while True:
        if option == 'y':
            cursor.callproc('del_user', [user])
            cnx.commit()
            print("Your account has been deleted")
            return start()
        elif option == 'n':
            print("Account deletion has been canceled")
            return landing(user)
        else:
            option = raw_input("command not recognized. Enter 'y' or 'n'\n")


# main function
def main():
    user = start()
    landing(user)
    print("Exiting...")
    return 0


# Edit profile

if __name__ == '__main__':
    main()
