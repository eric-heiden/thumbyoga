import requests
from bs4 import BeautifulSoup

r = requests.post('http://www.saidwhat.co.uk/quotes/search/', data = {'search':'grass person ball outdoor player'})
soup = BeautifulSoup(r.text, "html5lib")
quotes = soup.find('body').find('div', id="middle").p.find_next_siblings("p")[1].contents[2:]

arrayQuotes = []

for i in range(2, len(quotes)):
	if (len(str(quotes[i])) > 0):
		if (str(quotes[i])[0].isalnum() == True):
			arrayQuotes.append(str(quotes[i]).strip())

print (arrayQuotes)