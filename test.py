'''




'''

import requests
from bs4 import BeautifulSoup



url = 'https://www.money.pl/gielda/spolki-gpw/'
r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser") # "html.parser" is for get rid of warnings > https://stackoverflow.com/questions/33511544/how-to-get-rid-of-beautifulsoup-user-warning

number_of_headline = 1
for i in range(1000):  # item is headline with atributs <div>

    item = soup.div
    print("{}) >>> {}".format(number_of_headline, item.text)) # item.text is our headline with out atributes <h2>
