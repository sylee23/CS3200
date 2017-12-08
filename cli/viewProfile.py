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
                  + "\nEmail: " + util.xstr(row[3]) + "\nPhone: " + util.xstr(row[4]))
            row = result.fetchone()
        # Check for connection update?
        if own != viewing:
            is_found = False
            cursor.callproc("check_connection", [own, viewing, is_found])
            if is_found:
                while True:
                    connection_option = raw_input("Would you like to remove" + viewing + " as a connection? (y/n)\n")
                    if connection_option == 'y':
                        cursor.callproc("add_connection", [own, viewing])
                        cnx.commit()
                        print("Connection removed")
                        break
                    elif connection_option == 'n':
                        print("Connection not removed")
                        break
                    else:
                        print("Command not recognized")
            else:
                while True:
                    connection_option = raw_input("Would you like to add " + viewing + "as a connection? (y/n)\n")
                    if connection_option == 'y':
                        cursor.callproc("drop_connection", [own, viewing])
                        cnx.commit()
                        print("Connection added")
                        break
                    elif connection_option == 'n':
                        print("Connection not added")
                        break
                    else:
                        print("Command not recognized")
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
    # Add a co-op
    if own == viewing:
        while True:
            add_co_op = raw_input("Add a co-op (y/n):\n")
            if add_co_op == 'n':
                break
            elif add_co_op == 'y':
                start = raw_input("Enter a start date yyyy-mm-dd:\n")
                end = raw_input("Enter an end date yyyy-mm-dd:\n")
                comp = raw_input("Enter a company:\n")
                about = raw_input("Enter a descrpition of the co-op")
                cursor.callproc("add_co_op", [viewing, start, end, comp, about])
                cnx.commit()
            else:
                print("Valid options are y or n")
    # Go through all co-ops
    print("-----------Viewing Co-ops------------")
    cursor.callproc("get_co_ops", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no co-ops for " + viewing + ".")
            return
        while row is not None:
            print("----------------CO-OP------------------")
            print("start: " + util.xstr(row[0]) + "\nend: " + util.xstr(row[1])
                  + "\ncompany: " + util.xstr(row[2]) + "\ndescription: " + util.xstr(row[3]))

            # Change a co-op if own account
            if own == viewing:
                print("You can edit this co-op with the name of the field multiple fields can be changed,"
                      " 'delete' it, go to the next co-op with 'next', or go 'back'")
                old_time = row[0]
                changed = False
                while True:
                    option = raw_input("Enter a command")
                    if (option == 'back') or (option == 'next'):
                        if changed:
                            cursor.callproc("del_co_op", [viewing, old_time])
                            cnx.commit()
                            cursor.callproc("add_co_op", [viewing, row[0], row[1], row[2], row[3]])
                            cnx.commit()
                        if option == 'back':
                            return
                        break
                    elif option == 'delete':
                        cursor.callproc("del_co_op", [viewing, row[0]])
                        cnx.commit()
                        break
                    elif option == 'start':
                        changed = True
                        row[0] = raw_input("Enter the new start date yyyy-mm-dd:\n")
                    elif option == 'end':
                        changed = True
                        row[1] = raw_input("Enter the new end date yyyy-mm-dd:\n")
                    elif option == "company":
                        changed = True
                        row[2] = raw_input("Enter the company name:\n")
                    elif option == "dectription":
                        changed = True
                        row[3] = raw_input("Enter the description:\n")
                    else:
                        print("Command not recognized")
                row = result.fetchone()
        print("There are no other Co-ops")
        return


def courses(own, viewing):
    print("---------------Courses-----------------")
    # Add a course
    if own == viewing:
        while True:
            add_course = raw_input("Add a course? (y/n):\n")
            if add_course == 'n':
                break
            elif add_course == 'y':
                sem = raw_input("Enter a semester start date yyyy-mm-dd:\n")
                title = raw_input("Enter a course name:\n")
                prof = raw_input("Enter a professor's name:\n")
                cursor.callproc("add_co_op", [viewing, title, sem, prof])
                cnx.commit()
            else:
                print("Valid options are y or n")
    # Go through all courses
    print("-----------Viewing Courses------------")
    cursor.callproc("get_courses", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no courses for " + viewing + ".")
            return
        while row is not None:
            print("----------------Course------------------")
            print("course-name: " + util.xstr(row[1]) + "\nprofessor: " + util.xstr(row[2])
                  + "\nsemester: " + util.xstr(row[3]))

            # Change a course if own account
            if own == viewing:
                print("You can edit this course with the name of the field multiple fields can be changed,"
                      " 'delete' it, go to the next course with 'next', or go 'back'")
                changed = False
                while True:
                    option = raw_input("Enter a command")
                    if (option == 'back') or (option == 'next'):
                        if changed:
                            cursor.callproc("del_course", [row[0]])
                            cnx.commit()
                            cursor.callproc("add_course", [viewing, row[1], row[3], row[2]])
                            cnx.commit()
                        if option == 'back':
                            return
                        break
                    elif option == 'delete':
                        cursor.callproc("del_course", [row[0]])
                        cnx.commit()
                        break
                    elif option == 'semester':
                        changed = True
                        row[3] = raw_input("Enter the new semester start date yyyy-mm-dd:\n")
                    elif option == "course-name":
                        changed = True
                        row[1] = raw_input("Enter the course name:\n")
                    elif option == "professor":
                        changed = True
                        row[3] = raw_input("Enter the proffessor's name:\n")
                    else:
                        print("Command not recognized")
                row = result.fetchone()
        print("There are no other courses")
        return


def study_abroad(own, viewing):
    print("study_abroad")


def research(own, viewing):
    print("---------------Co-ops-----------------")
    # Add a co-op
    if own == viewing:
        while True:
            add_co_op = raw_input("Add a co-op (y/n):\n")
            if add_co_op == 'n':
                break
            elif add_co_op == 'y':
                start = raw_input("Enter a start date yyyy-mm-dd:\n")
                end = raw_input("Enter an end date yyyy-mm-dd:\n")
                comp = raw_input("Enter a company:\n")
                about = raw_input("Enter a descrpition of the co-op")
                cursor.callproc("add_co_op", [viewing, start, end, comp, about])
                cnx.commit()
            else:
                print("Valid options are y or n")
    # Go through all co-ops
    print("-----------Viewing Co-ops------------")
    cursor.callproc("get_co_ops", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no co-ops for " + viewing + ".")
            return
        while row is not None:
            print("----------------CO-OP------------------")
            print("start: " + util.xstr(row[0]) + "\nend: " + util.xstr(row[1])
                  + "\ncompany: " + util.xstr(row[2]) + "\ndescription: " + util.xstr(row[3]))

            # Change a co-op if own account
            if own == viewing:
                print("You can edit this co-op with the name of the field multiple fields can be changed,"
                      " 'delete' it, go to the next co-op with 'next', or go 'back'")
                old_time = row[0]
                changed = False
                while True:
                    option = raw_input("Enter a command")
                    if (option == 'back') or (option == 'next'):
                        if changed:
                            cursor.callproc("del_co_op", [viewing, old_time])
                            cnx.commit()
                            cursor.callproc("add_co_op", [viewing, row[0], row[1], row[2], row[3]])
                            cnx.commit()
                        if option == 'back':
                            return
                        break
                    elif option == 'delete':
                        cursor.callproc("del_co_op", [viewing, row[0]])
                        cnx.commit()
                        break
                    elif option == 'start':
                        changed = True
                        row[0] = raw_input("Enter the new start date yyyy-mm-dd:\n")
                    elif option == 'end':
                        changed = True
                        row[1] = raw_input("Enter the new end date yyyy-mm-dd:\n")
                    elif option == "company":
                        changed = True
                        row[2] = raw_input("Enter the company name:\n")
                    elif option == "dectription":
                        changed = True
                        row[3] = raw_input("Enter the description:\n")
                    else:
                        print("Command not recognized")
                row = result.fetchone()
        print("There are no other Co-ops")
        return
