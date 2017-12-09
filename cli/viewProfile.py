from mysql.connector import MySQLConnection, Error
import util
import home

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()


# View a profile go back to where were previously
def view_profile(own, viewing):
    if own == viewing:
        print("-------------------Welcome to your Profile-----------------")
    else:
        print("--------------Veiwing the profile of " + viewing + "---------------")
    while True:
        print("Options: \n1. Main profile\n2. Co-ops\n3. Courses\n4. Study Abroad\n5. Research\n6. Majors and Minors")
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
        elif option == '6':
            majors_and_minors(own, viewing)
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
                if split[2] == "":
                    print("Need a new value")
                    continue
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
                about = raw_input("Enter a descrpition of the co-op:\n")
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
                start = row[0]
                end = row[1]
                company = row[2]
                desc = row[3]
                changed = False
                while True:
                    option = raw_input("Enter a command")
                    if (option == 'back') or (option == 'next'):
                        if changed:
                            cursor.callproc("del_co_op", [viewing, old_time])
                            cnx.commit()
                            cursor.callproc("add_co_op", [viewing, start, end, company, desc])
                            cnx.commit()
                        if option == 'back':
                            return
                        break
                    elif option == 'delete':
                        cursor.callproc("del_co_op", [viewing, old_time])
                        cnx.commit()
                        break
                    elif option == 'start':
                        changed = True
                        start = raw_input("Enter the new start date yyyy-mm-dd:\n")
                    elif option == 'end':
                        changed = True
                        end = raw_input("Enter the new end date yyyy-mm-dd:\n")
                    elif option == "company":
                        changed = True
                        company = raw_input("Enter the company name:\n")
                    elif option == "description":
                        changed = True
                        desc = raw_input("Enter the description:\n")
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
                cursor.callproc("add_course", [viewing, title, sem, prof])
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
                sem = row[3]
                name = row[1]
                prof = row[2]
                while True:
                    option = raw_input("Enter a command")
                    if (option == 'back') or (option == 'next'):
                        if changed:
                            cursor.callproc("del_courses", [row[0]])
                            cnx.commit()
                            cursor.callproc("add_course", [viewing, name, sem, prof])
                            cnx.commit()
                        if option == 'back':
                            return
                        break
                    elif option == 'delete':
                        cursor.callproc("del_courses", [row[0]])
                        cnx.commit()
                        break
                    elif option == 'semester':
                        changed = True
                        sem = raw_input("Enter the new semester start date yyyy-mm-dd:\n")
                    elif option == "course-name":
                        changed = True
                        name = raw_input("Enter the course name:\n")
                    elif option == "professor":
                        changed = True
                        prof = raw_input("Enter the professor's name:\n")
                    else:
                        print("Command not recognized")
            row = result.fetchone()
        print("There are no other courses")
        return


def study_abroad(own, viewing):
    print("---------------Study Abroad-----------------")
    # Add a study abroad
    if own == viewing:
        while True:
            add_study_abroad = raw_input("Add a Study Abroad Experience? (y/n):\n")
            if add_study_abroad == 'n':
                break
            elif add_study_abroad == 'y':
                start = raw_input("Enter a start date yyyy-mm-dd:\n")
                end = raw_input("Enter an end date yyyy-mm-dd:\n")
                uni = raw_input("Enter the University:\n")
                loc = raw_input("Enter the country:\n")
                cursor.callproc("add_study_abroad", [viewing, start, end, uni, loc])
                cnx.commit()
            else:
                print("Valid options are y or n")
    # Go through all co-ops
    print("-----------Viewing Study Abroad------------")
    cursor.callproc("get_study_abroad", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no study abroad experiences for " + viewing + ".")
            return
        while row is not None:
            print("----------------Study Abroad------------------")
            print("start: " + util.xstr(row[0]) + "\nend: " + util.xstr(row[1])
                  + "\nuniversity: " + util.xstr(row[2]) + "\ncountry: " + util.xstr(row[3]))

            # Change a co-op if own account
            if own == viewing:
                print("You can edit this study abroad with the name of the field multiple fields can be changed,"
                      " 'delete' it, go to the next co-op with 'next', or go 'back'")
                old_time = row[0]
                start = row[0]
                end = row[1]
                uni = row[2]
                loc = row[3]
                changed = False
                while True:
                    option = raw_input("Enter a command")
                    if (option == 'back') or (option == 'next'):
                        if changed:
                            cursor.callproc("del_study_abroad", [viewing, old_time])
                            cnx.commit()
                            cursor.callproc("add_study_abroad", [viewing, start, end, uni, loc])
                            cnx.commit()
                        if option == 'back':
                            return
                        break
                    elif option == 'delete':
                        cursor.callproc("del_study_abroad", [viewing, old_time])
                        cnx.commit()
                        break
                    elif option == 'start':
                        changed = True
                        start = raw_input("Enter the new start date yyyy-mm-dd:\n")
                    elif option == 'end':
                        changed = True
                        end = raw_input("Enter the new end date yyyy-mm-dd:\n")
                    elif option == "university":
                        changed = True
                        uni = raw_input("Enter the University:\n")
                    elif option == "country":
                        changed = True
                        loc = raw_input("Enter the country:\n")
                    else:
                        print("Command not recognized")
            row = result.fetchone()
        print("There are no other Study Abroad experiences.")
        return


def research(own, viewing):
    print("---------------Research Experience-----------------")
    # Add a research
    if own == viewing:
        while True:
            add_research = raw_input("Add a Research Experience (y/n):\n")
            if add_research == 'n':
                break
            elif add_research == 'y':
                start = raw_input("Enter a start date yyyy-mm-dd:\n")
                end = raw_input("Enter an end date yyyy-mm-dd:\n")
                prof = raw_input("Enter a professor:\n")
                about = raw_input("Enter a description of the research:\n")
                cursor.callproc("add_research", [viewing, start, end, prof, about])
                cnx.commit()
            else:
                print("Valid options are y or n")
    # Go through all co-ops
    print("-----------Viewing Research------------")
    cursor.callproc("get_research", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no research experiences for " + viewing + ".")
            return
        while row is not None:
            print("----------------Research------------------")
            print("start: " + util.xstr(row[0]) + "\nend: " + util.xstr(row[1])
                  + "\nprofessor: " + util.xstr(row[2]) + "\ndescription: " + util.xstr(row[3]))

            # Change a co-op if own account
            if own == viewing:
                print("You can edit this research with the name of the field multiple fields can be changed,"
                      " 'delete' it, go to the next co-op with 'next', or go 'back'")
                old_time = row[0]
                start = row[0]
                end = row[1]
                prof = row[2]
                desc = row[3]
                changed = False
                while True:
                    option = raw_input("Enter a command")
                    if (option == 'back') or (option == 'next'):
                        if changed:
                            cursor.callproc("del_research", [viewing, old_time])
                            cnx.commit()
                            cursor.callproc("add_research", [viewing, start, end, prof, desc])
                            cnx.commit()
                        if option == 'back':
                            return
                        break
                    elif option == 'delete':
                        cursor.callproc("del_research", [viewing, row[0]])
                        cnx.commit()
                        break
                    elif option == 'start':
                        changed = True
                        start = raw_input("Enter the new start date yyyy-mm-dd:\n")
                    elif option == 'end':
                        changed = True
                        end = raw_input("Enter the new end date yyyy-mm-dd:\n")
                    elif option == "professor":
                        changed = True
                        prof = raw_input("Enter the professor's name:\n")
                    elif option == "dectription":
                        changed = True
                        desc = raw_input("Enter the description:\n")
                    else:
                        print("Command not recognized")
            row = result.fetchone()
        print("There are no other Research experiences.")
        return


def majors_and_minors(own, viewing):
    print("Add majors or Minors.")
    if own == viewing:
        while True:
            add_m = raw_input("Select:\n1. Add a Major\n2. Add a Minor\n3. View Majors/Minors\n4.Back\n")
            if add_m == '3':
                break
            elif add_m =='4':
                return
            elif add_m == '1':
                major = raw_input('Enter the name of the major:\n')
                cursor.callproc("add_major", [viewing, major])
                cnx.commit()
            elif add_m == '2':
                minor = raw_input('Enter the name of the minor:\n')
                cursor.callproc("add_minor", [viewing, minor])
                cnx.commit()
            else:
                print("Valid options are 1, 2, 3, 4")
    # Go through all Majors
    print("-----------Viewing Majors------------")
    cursor.callproc("get_major", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no majors for " + viewing + ".")
            return
        while row is not None:
            print(util.xstr(row[0]))
            # Delete major if own account
            if own == viewing:
                print("You can delete this major with 'delete', go to the 'next' major, or "
                      " 'delete' it, go to the next co-op with 'next', or go 'back'")
                while True:
                    option = raw_input("Enter a command")
                    if option == 'back':
                        return
                    if option == 'next':
                        break
                    elif option == 'delete':
                        cursor.callproc("del_major", [viewing, row[0]])
                        cnx.commit()
                        break
                    else:
                        print("Command not recognized")
            row = result.fetchone()
        print("There are no other majors")
        break
    # Go through all Minors
    print("-----------Viewing Minors------------")
    cursor.callproc("get_minors", [viewing])
    for result in cursor.stored_results():
        row = result.fetchone()
        if row is None:
            print("There are no minors for " + viewing + ".")
            return
        while row is not None:
            print(util.xstr(row[0]))
            # Delete major if own account
            if own == viewing:
                print("You can delete this mino with 'delete', go to the 'next' major, or "
                      " 'delete' it, go to the next co-op with 'next', or go 'back'")
                while True:
                    option = raw_input("Enter a command")
                    if option == 'back':
                        return
                    if option == 'next':
                        break
                    elif option == 'delete':
                        cursor.callproc("del_minor", [viewing, row[0]])
                        cnx.commit()
                        break
                    else:
                        print("Command not recognized")
            row = result.fetchone()
        print("There are no other minors")
        return
