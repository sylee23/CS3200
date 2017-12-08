from mysql.connector import MySQLConnection, Error
from util import xstr

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()


def view_groups(user):
    print("-----------------Viewing Your Groups------------------")
    cursor.callproc("get_groups", [user])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("You are not a member of any groups")
        else:
            while row is not None:
                print("group-id: " + row[0])
                print("group-name: " + row[1])
                print("Description: " + row[2])
                print("---------------------------------------------------")
                row = result.fetchone()
            print("You are not a member of any other groups")
            print("------------------------------------------------")
            break
    while True:
        print("Options:\n1.Go back to home\n2.View group page\n3.Suggest groups\n4.Create a group")
        option = raw_input("Enter a number:\n")
        if option == '1':
            return
        elif option == '2':
            group_id = raw_input("What group's page do you want to view?\n")
            view_specific_group(user, group_id)
        elif option == '3':
            suggest_groups(user)
        elif option == '4':
            create_group(user)
        else:
            print("Invalid Option")


def create_group(user):
    print("---------------------Group Creation--------------------")
    name = raw_input("Enter a name for the group:\n")
    about = raw_input("Enter a description for the group:\n")
    result_args = cursor.callproc("new_group", [name, about, -1])
    cnx.commit()
    cursor.callproc("add_admin", [user, result_args[2]])
    cursor.callproc("join_group", [user, result_args[2]])
    cnx.commit()
    print("Your are now an admin/member of the newly created group")
    return

def view_specific_group(user, group):
    print("-----------------Viewing Group with group-id: " + group + "---------------")
    cursor.callproc("group_from_id", [group])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("You are not a member of any groups")
        else:
                print("group-id: " + row[0])
                print("group-name: " + row[1])
                print("Description: " + row[2])
                print("---------------------------------------------------")
                break
    admin_args = cursor.callproc("check_admin", [user, group, False])
    joined_args = cursor.callproc("check_joined", [user, group, False])
    if admin_args[2]:
        while True:
            admin_mode = raw_input("Enter admin mode for group (y/n)\n")
            if admin_mode == 'y':
                admin_group_page(user, group)
                break
            elif admin_mode == 'n':
                break
            else:
                print("Command not recognized, valid options are y or n")
    if joined_args[2]:
        while True:
            options = raw_input("Options:\n1. Get Member information\n2. Back\n3. Leave group\n")
            if options == '1':
                get_group_members(group)
            elif options == '2':
                return
            elif options == '3':
                print("You have left the group")
                cursor.callproc("leave_group", [user, group])
    else:
        while True:
            is_joining = raw_input("Would you like to join this group? (y/n):\n")
            if is_joining == 'y':
                cursor.callproc("join_group", [user, group])
                cnx.commit()
                print("You have joined the group")
                return
            if is_joining == 'n':
                print("Leaving group page, as no other options")
                return
            print("Not a recognized command, options are y or n")


def suggest_groups(user):
    print("--------------Suggesting Groups----------------")
    cursor.callproc("suggested_groups", [user])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no suggested groups for you.")
            print("--------------------------------------")
            return
        else:
            while row is not None:
                print("group-id: " + row[0])
                print("group-name: " + row[1])
                print("Description: " + row[2])
                print("---------------------------------------------------")
                row = result.fetchone()
            print("There are no more suggestions")
            print("------------------------------------------------")
            break
    while True:
        print("Options:\n1. View a suggested group\n2. Go back")
        option = raw_input("Select an option:\n")
        if option == '1':
            group_id = raw_input("Enter the group-id to view:\n")
            view_specific_group(user, group_id)
        elif option == '2':
            return
        else:
            print("Not a recognized command, options are 1 or 2.")


def get_group_members(group):
    cursor.callproc("group_emails", [group])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no members.")
            print("--------------------------------------")
            return
        else:
            while row is not None:
                print("Username: " + row[0] + "Name: " + row[1] + ", email: " + row[2])
                row = result.fetchone()
            print("There are no more members")
            print("------------------------------------------------")
            return


def admin_group_page(user, group):
    print("---------------Admin Page for" + group + "---------------------")
    while True:
        option = raw_input("Options:\n1. Step down as admin\n2.Add admin\n3.Edit group information\n4. Back")
        if option == '4':
            return
        if option == '3':
            cursor.callproc("rm_admin", [user, group])
            cnx.commit()
            return
        if option == '2':
            new_admin = raw_input("Enter the username of the new admin")
            cursor.callproc("add_admin", [new_admin, group])
        if option == '1':
            name = raw_input("Enter the new name for the group")
            desc = raw_input("Enter the new description for the group")
            cursor.callproc("update_group", [group, name, desc])
            cnx.commit()
            print("group updated")
        else:
            print("Not a valid command.")
