from mysql.connector import MySQLConnection, Error
import home

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()

# Search for accounts
def search_users(user):
    print("-----------------Search-----------------")
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
            print("------------------------------------------------")
    while True:
        option = raw_input("View a profile with: 'view-user Username', "
                           + "search again with 'search-users', or go back to home with 'home'\n")
        split = option.split(" ", 1)
        if option == "home":
            return home.landing(user)
        elif option == "search-users":
            return search_users(user)
        elif split[0] == "view-user":
            view_other_user(split[1])
        else:
            print("Command not recognized")
