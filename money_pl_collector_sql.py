#!/usr/bin/python3
'''

author: a5892731
date: 2021-06-29
actualization date: 2021-07-04
version: 1.0

description: This script collects data from Warsaw Stock Exchange (WSE) --- Giełda Papierów Wartościowych w Warszawie (GPW)
             and saves it in swe_database.
source: https://www.money.pl/gielda/spolki-gpw/

'''

import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from time import gmtime, strftime

class Data:  # <-------------------------------------------------------------------------------------GENERAL GLOBAL DATA
    url = 'https://www.money.pl/gielda/spolki-gpw/'
    header_oryginal = ["Walor", "Kurs_PLN", "Zmiana_PROC", "Otwarcie", "Min", "Max",
                       "Obrót_SZT", "Obrót_PLN", "Czas_aktualizacji", "Data"]
    header_eng = ["Value", "Rate_(PLN)", "Change_(PROC)", "Opening", "Min", "Max",
                  "Turnover_(pcs.)", "Turnover_(PLN)", "Update_time", "Date"]

    header = header_oryginal

class DBdata:  # <-------------------------------------------------------------------------------------DATA FOR DATABASE
    def __init__(self):
        self.db_name = "WSE_database"
        self.host_address = "127.0.0.1"
        self.user_name = "root"
        self.user_password = ""

class WSE_Data_Collector(Data): # <--------------THIS IS MODIFICATED SCRIPT FROM https://github.com/a5892731/SQL_handler

    def __init__(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser") # "html.parser" is for get rid of warnings > https://stackoverflow.com/questions/33511544/how-to-get-rid-of-beautifulsoup-user-warning
        headline_data = soup.find_all("div") # <div>This is heading</div>
        self.table = self.translate_data(headline_data)

    def translate_data(self, headline_data):
        number_of_headline = 1
        table = []
        row = []
        column_number = 1

        for item in headline_data:  # item is headline with attributes <div>
            if number_of_headline < 121 or item.text == "" or len(item.text) > 40 \
                    or "Loading" in item.text or "MONEY.PL" in item.text\
                    or number_of_headline % 2 == 0 or "——————" in item.text:  # trash filter
                number_of_headline += 1
                continue
            if column_number == 1 and "," in item.text: # trash filter two
                continue
            #print("{}) >>> {}".format(number_of_headline, item.text)) #  this is data test printer

            number_of_headline += 1
            row.append("{}".format(item.text.replace("\xa0","")))

            if len(row) == 9:  # create row in table
                table.append(row)
                #print(row) # this is data test printer two for comtaration
                row = []

            if column_number == 9:
                column_number = 0
            column_number += 1

        return table

class TableBuilder(Data): # <--------------------THIS IS MODIFICATED SCRIPT FROM https://github.com/a5892731/SQL_handler
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
        self.table_SQL = ""

    def create_table(self):

        def create_columns(table):
            columns = ""

            for column in table:
                columns += column + ", "
            columns += "PRIMARY KEY ({})".format(columns.split(" ")[0]) # add to the end "PRIMARY KEY (first_column_name)"

            return columns

        create_table = """
        CREATE TABLE {} (
          {}
        ) ENGINE = InnoDB 
        """.format(self.table_name.replace(".", "_").replace("!", "_").replace("&", "_").
                   replace("-", "_").replace("/", "_"),
                   create_columns(self.table))

        #self.execute_query(self.connection, create_table, "DB {} table created successfully".format(self.table_name))

        self.table_SQL = create_table

class SQL_Creator(TableBuilder): # <------------------------------------------THIS IS A QUERY BUILDER FOR TABLE CREATION

    def __init__(self, table_name):
        self.table_name = table_name
        self.table = ["Lp"]
        for column in self.header:
            self.table.append(column)
        self.table_SQL = ""

        self.define_table_variables()
        self.create_table()

    def define_table_variables(self):
        self.table[0] = "{} INT AUTO_INCREMENT".format(self.table[0]) # ID
        self.table[1] = "{} CHAR(40)".format(self.table[1])
        for column_nr in range(2, 9):
            self.table[column_nr] = "{} CHAR(10)".format(self.table[column_nr])  # numeric data
        for column_nr in range(9, 11):
            self.table[column_nr] = "{} CHAR(10)".format(self.table[column_nr])

class DatabaseConnector(DBdata): # <-------------THIS IS MODIFICATED SCRIPT FROM https://github.com/a5892731/SQL_handler
    def __init__(self):
        super().__init__() #<- DBdata variables

        self.status = ""  # error status of DB
        self.connection = None

    def create_connection_to_server(self):

        try:
            self.connection = mysql.connector.connect(
                host=self.host_address,
                user=self.user_name,
                passwd=self.user_password,
                database=self.db_name
            )
            self.status = "Connection to MySQL server successful"
        except Error as e:
            self.status = f"The error '{e}' occurred"

    def execute_query(self, query, message):

        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            self.status = "{}".format(message)
        except Error as e:
            self.status = f"The error '{e}' occurred"

class Insert_QUERY(Data):

    def __init__(self, table_name, row):

        self.current_date = strftime("%Y-%m-%d", gmtime())
        self.row = row
        self.row.append(self.current_date)
        self.time_corrector()
        for i in range(len(row)):
            self.row[i] = self.row[i].replace(",", ".")

        table_columns= "({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
            self.header[0], self.header[1], self.header[2], self.header[3], self.header[4], self.header[5],
            self.header[6], self.header[7], self.header[8], self.header[9]
        )
        values = "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            self.row[0], self.row[1], self.row[2].replace("+", ""),
            self.row[3], self.row[4], self.row[5],
            self.row[6], self.row[7], self.row[8], self.row[9])

        self.table_data = "INSERT INTO {} {} VALUES {}".format(
            table_name, table_columns, values)

    def time_corrector(self):
        if ":" in self.row[8]:  # Czas_aktualizacji / Update_time
            self.row[9] = self.current_date  # Data / Date
        else:
            self.row[9] = self.row[8]
            self.row[8] = "—"
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    GPW = WSE_Data_Collector()

    DB = DatabaseConnector()
    DB.create_connection_to_server()

    for row in GPW.table:
        table = SQL_Creator(row[0].replace(" ", "_"))
        table_name = row[0].replace(" ", "_").replace("-", "_").replace(".", "_").replace("/", "_").replace("&", "_").\
            replace("!", "_")

        DB.execute_query(table.table_SQL, "table {} created".format(row[0].replace(" ", "_")))



        if "error" in DB.status and "already exists" not in DB.status:
            print(DB.status)
            print(table.table_SQL)
        elif "error" not in DB.status or "already exists" in DB.status:
            insert = Insert_QUERY(table_name, row)
            DB.execute_query(insert.table_data, "data inserted to table {}".format(table_name))
            print(DB.status)
            if "error" in DB.status:
                print(insert.table_data)
        else:
            print(DB.status)



