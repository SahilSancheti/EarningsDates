from bs4 import BeautifulSoup
import requests
import csv


def getFinvizDate(symbol):
    page = requests.get("https://finviz.com/quote.ashx?t={}".format(symbol))
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.content, 'html.parser')
    finviz = [tag.string for tag in soup.find_all('td')]
    return finviz[finviz.index('Earnings')+1]

def getEarningsWhispersDate(symbol):
    page = requests.get('https://www.earningswhispers.com/stocks/{}'.format(symbol))
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find("div",{'id': 'datebox'}).find('div',{'class':'mainitem'}).string

# def getEarningsTDAmeritrade(symbol):
#     # headers = requests.utils.default_headers()
#     # headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
#     page = urlopen('https://research.tdameritrade.com/grid/public/research/stocks/earnings?symbol={}'.format(symbol))
#     soup = BeautifulSoup(page.content, 'html.parser')
#     text_file = open("output.html", "w")
#     text_file.write(soup.prettify())
#     text_file.close()
#     print(soup.find_all('td', {'class':'value week-of'}))

# getEarningsTDAmeritrade('fb')
#https://research.tdameritrade.com/grid/public/research/stocks/earnings?symbol=FB

def getEarningsZacks(symbol):
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    page = requests.get('https://www.zacks.com/stock/quote/{}?q={}'.format(symbol.upper(),symbol), headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    tds = soup.find('section',{'id':'stock_key_earnings'}).find_all('td')
    tds = tds[[tag.string for tag in tds].index('Exp Earnings Date')+1]
    tds.find('sup').replaceWith('')
    return str(tds)[4:-5]

def generateCSV(fileName='stocklist.csv'):
    symbolList = []
    with open(fileName, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader, None)
        for row in spamreader:
            symbolList += [row[0]]
    
    with open('earnings.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        row = ['Symbol','Finviz', 'EarningsWhisper', 'Zacks']
        spamwriter.writerow(row)
        print(row)
        for symbol in symbolList:
            row = [symbol, getFinvizDate(symbol), getEarningsWhispersDate(symbol), getEarningsZacks(symbol)]
            spamwriter.writerow(row)
            print(row)
generateCSV()