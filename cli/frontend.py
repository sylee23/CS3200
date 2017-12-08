from mysql.connector import MySQLConnection, Error
import login

cnx = MySQLConnection(user='project', password='project', database='project')
cursor = cnx.cursor()



# main function
def main():
    login.start()
    print("Exiting...")
    return 0


# Edit profile
if __name__ == '__main__':
    main()
