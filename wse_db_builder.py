#!/usr/bin/python3
#
# author: a5892731
# version: 1.0
# date: 2021-06-16
# lat update: 2021-06-30
#
# Description:
# Ths is a script that connects to server and builds a database
# It can be run directly from linux console
#
# Upgrade:
# Script is upgraded for Warsaw Stock Exchange data storage purpose
# ---------------------------------------------------------------------------------------------------------------------
#

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print(">>> " + "No module: Install mysql.connector")

    import pip
    packages = [package.project_name for package in pip.get_installed_distributions()]
    if 'mysql.connector' not in packages:
        pip.main(['install', 'mysql.connector'])

class DBdata:  # <-------------------------------------------DATA FOR DATABASE------------------------------------------
    def __init__(self):
        self.db_name = "WSE_database"
        self.host_address = "127.0.0.1"
        self.user_name = "root"
        self.user_password = ""

        self.status = "" # class information status

        #self.settings() # default settings only in GPW_collector

    def settings(self):
        user_choice = input(">>> >>> " + "Retrieve default settings (y/n/e)?: ")
        if user_choice.capitalize() == "Y":
            pass
        elif user_choice.capitalize() == "N":
            self.data_from_user()
        elif user_choice.capitalize() == "E":
            print(">>> " + "Exit program")
            exit()
        else:
            self.settings()

        self.status = "Database connection data collected"

    def data_from_user(self):

        self.db_name = input(">>> >>> " + "Input a database name: ")
        print(">>> " + "Your database name is {}".format(self.db_name))

        self.host_address = input(">>> >>> " + "Input a database address: ")
        print(">>> " + "Your database address is {}".format(self.host_address))

        self.user_name = input(">>> >>> " + "Input a user name: ")
        print(">>> " + "Your user name is {}".format(self.user_name))

        self.password_verify()

    def password_verify(self):
        password = input(">>> >>> " + "Input a user password: ")
        repeated_password = input(">>> >>> " + "Repeat a user password: ")

        if password == repeated_password:
            self.user_password = password
        else:
            print(">>> " + "Error! Try again")
            self.password_verify()

#-----------------------------------------------------------------------------------------------------------------------

class DatabaseBuilder:
    def __init__(self, db_name, host_address, user_name, user_password):
        self.db_name = db_name
        self.host_address = host_address
        self.user_name = user_name
        self.user_password = user_password
        self.status = ""  # error status of DB

    def create_connection_to_server(self):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.host_address,
                user=self.user_name,
                passwd=self.user_password
            )
            self.status = "Connection to MySQL server successful"
        except Error as e:
            self.status = f"The error '{e}' occurred"
        return connection


    def create_database(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            self.status = "Database created successfully"

        except Error as e:
            if "1007 (HY000)" in f"{e}":
                self.status = "Database exists"
            else:
                self.status = f"The error '{e}' occurred"


if __name__ == "__main__":
    print(">>> " + "db_builder is starting")

    connection_data = DBdata()
    print(">>> " + connection_data.status)

    db = DatabaseBuilder(connection_data.db_name, connection_data.host_address,
                         connection_data.user_name, connection_data.user_password)

    connection = db.create_connection_to_server()
    print(">>> " + db.status)
    create_database_query = "CREATE DATABASE {} CHARSET=utf8".format(connection_data.db_name)
    db.create_database(connection, create_database_query)
    print(">>> " + db.status)
