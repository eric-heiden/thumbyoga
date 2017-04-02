import requests
from bs4 import BeautifulSoup

def generate_quotes(tags):
    r = requests.post(
        'http://www.saidwhat.co.uk/quotes/search/',
        data = {'search': tags}
    )
    soup = BeautifulSoup(r.text, 'html5lib')
    # print(r.text)
    # print(soup.find('body').find('div', id="middle").p)
    quotes = soup.find('body').find('div', id="middle").p.find_next_siblings("p")[1].contents[2:]
    # print("quotes0", quotes)
    arrayQuotes = []
    for i in range(2, len(quotes)):
        if len(str(quotes[i])) > 0 and str(quotes[i])[0].isalnum():
            arrayQuotes.append(str(quotes[i]).strip())

    return arrayQuotes
