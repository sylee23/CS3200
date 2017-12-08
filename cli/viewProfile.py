from mysql.connector import MySQLConnection, Error
import util

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()


# View a profile
def view_profile(own, viewing):
    if own == viewing:
        print("-------------------Welcome to your Profile-----------------")
    else:
        print("--------------Veiwing the profile of " + viewing + "---------------")
    while True:
        print("Options: \n1. Main profile\n2. Co-ops\n3. Courses\n4. Study Abroad\n5. Research")
        print("Go back with: back")
        option = raw_input("Enter a number:\n")
        if option == '1':
            main_profile(own, viewing)
        elif option == '2':
            co_ops(own, viewing)
        elif option == '3':
            courses(own, viewing)
        elif option == '4':
            study_abroad(own, viewing)
        elif option == '5':
            research(own, viewing)
        elif option == 'back':
            return
        else:
            print("not a valid command")


def main_profile(own, viewing):
    print("----------------Main profile-----------------")
    cursor.callproc("view_user", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("Profile not found.")
            return
        while row is not None:
            print("Name: " + util.xstr(row[0]) + "\nDescription: "
                  + util.xstr(row[1]) + "\nYear-of-Graduation: " + util.xstr(row[2])
                  + "\nEmail: "+ util.xstr(row[3]) + "\nPhone: " + util.xstr(row[4]))
            row = result.fetchone()
        if own != viewing:
            return
        # is the user's profile they can edit
        while True:
            print("Go back with 'back' or edit profile with"
                  + " 'edit' and the field-name and value. For example edit year-of-graduation 2014")
            option = raw_input("Enter a command:\n")
            split = option.split(" ", 2)
            if option == "back":
                return
            elif split[0] == "edit":
                if split[1] == "name":
                    cursor.execute("UPDATE users SET real_name=%s WHERE username=%s", (split[2], own))
                elif split[1] == "description":
                    cursor.execute("UPDATE users SET Description=%s WHERE username=%s", (split[2], own))
                elif split[1] == "year-of-graduation":
                    cursor.execute("UPDATE users SET gradYear=%s WHERE username=%s", (split[2], own))
                elif split[1] == "email":
                    cursor.execute("UPDATE users SET email=%s WHERE username=%s", (split[2], own))
                elif split[1] == "phone":
                    cursor.execute("UPDATE users SET phone=%s WHERE username=%s", (split[2], own))
                else:
                    print("Invalid field")
                    continue
                cnx.commit()
                print("---------------------Updated-------------------")
                return main_profile(own, viewing)
            else:
                # Fix this in final version
                print("Invalid Command")  # and 'view research'")


def co_ops(own, viewing):
    print("---------------Co-ops-----------------")
    cursor.callproc("view_user", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("Profile not found.")
            return
        while row is not None:
            print("Name: " + util.xstr(row[0]) + "\nDescription: "
                  + util.xstr(row[1]) + "\nYear-of-Graduation: " + util.xstr(row[2])
                  + "\nEmail: " + util.xstr(row[3]) + "\nPhone: " + util.xstr(row[4]))
            row = result.fetchone()
        if own != viewing:
            return


def courses(own, viewing):
    print("courses")


def study_abroad(own, viewing):
    print("study_abroad")


def research(own, viewing):
    print("research")
