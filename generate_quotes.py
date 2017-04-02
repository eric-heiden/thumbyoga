import requests
from bs4 import BeautifulSoup

LIFE_QUOTES = [
    'The secret of life is to have a task, something you devote your entire life to, something you bring everything to, every minute of the day for the rest of your life.',
    'I find that when you have a real interest in life and a curious life, that sleep is not the most important thing.',
    'Every experience in life, everything with which we have come in contact in life, is a chisel which has been cutting away at our life statue, molding, modifying, shaping it. We are part of all we have met. Everything we have seen, heard, felt or thought has had its hand in molding us, shaping us.',
]

# TODO make it more stable
def generate_quotes(tags):
    arrayQuotes = []
    try:
        r = requests.post(
            'http://www.saidwhat.co.uk/quotes/search/',
            data = {'search': tags}
        )
        soup = BeautifulSoup(r.text, 'html5lib')
        # print(r.text)
        # print(soup.find('body').find('div', id="middle").p)
        quotes = soup.find('body').find('div', id="middle").p.find_next_siblings("p")[1].contents[2:]
        # print("quotes0", quotes)
        for i in range(2, len(quotes)):
            if len(str(quotes[i])) > 0 and str(quotes[i])[0].isalnum():
                arrayQuotes.append(str(quotes[i]).strip())

        return arrayQuotes if len(arrayQuotes) > 0 else LIFE_QUOTES
    except:
        print("Resorting to life quotes :(")
        return LIFE_QUOTES
