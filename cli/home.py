import search
import login
import delete
import viewProfile


# Landing Page
def landing(user):
    print("------------------Home------------------")
    print("Search for users with: 'search-users'")
    print("View and edit your profile with 'profile'")
    print("Delete your account with 'delete-account'")
    print("Logout of your account with logout")
    while True:
        option = raw_input("Please enter a command:\n")
        if option == "search-users":
            search.search_users(user)
        elif option == "profile":
            return viewProfile.view_profile(user, user)
        elif option == "delete-account":
            return delete.delete_account(user)
        elif option == "logout":
            print("You are now logged out of your account")
            return login.start()
        else:
            print("Command not recognized. Valid commands are: search-users,"
                  + " profile, delete-account, logout")