import search
import login
import delete
import viewProfile
import connections
import groups


# Landing Page all things come back to here, other than logging out/deleting account
def landing(user):
    print("------------------Home------------------")
    print("Options\n1.Search Users\n2. View/Edit Profile\n3. View/Remove Connections\n"
          + "4. View Groups\n5. Search Groups\n6. Logout\n7. Delete Account")
    while True:
        option = raw_input("Please enter an option (e.g. 1):\n")
        if option == "1":
            search.search_users(user)
        elif option == "2":
            viewProfile.view_profile(user, user)
        elif option == "3":
            connections.main(user)
        elif option == "4":
            search.search_groups(user)
        elif option == "5":
            groups.view_groups(user)
        elif option == "6":
            print("You are now logged out of your account")
            return login.start()
        elif option == "7":
            return delete.delete_account(user)
        else:
            print("Command not recognized. Enter a number from 1-7")