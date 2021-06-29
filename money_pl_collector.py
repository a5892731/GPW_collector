#!/bin/python3
'''

author: a5892731
date: 2021-06-29
actualization date: 2021-06-29
version: 1.0

description: this script gets data from https://www.money.pl/gielda/spolki-gpw/ end extract it to table

'''

import requests
from bs4 import BeautifulSoup



url = 'https://www.money.pl/gielda/spolki-gpw/'
r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser") # "html.parser" is for get rid of warnings > https://stackoverflow.com/questions/33511544/how-to-get-rid-of-beautifulsoup-user-warning
headline_data = soup.find_all("div") # <div>This is heading 2</div> #div style="text-overflow:ellipsis;overflow:hidden



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

    if len(row) == 9:

        table.append(row)

        #print("Walor Kurs(PLN) Zmiana(%) Otwarcie Min Max Obrót (szt.) Obrót(PLN) Czas_aktualizacji")
        #print(row) # this is data test printer two for comtaration

        row = []

    if column_number == 9:
        column_number = 0
    column_number += 1

print(["Walor", "Kurs(PLN)", "Zmiana(%)", "Otwarcie","Min","Max", "Obrót(szt.)", "Obrót(PLN)", "Czas_aktualizacji"])
for row in table:
    print(row)

print("\nTable size: {} elements".format(len(table)))