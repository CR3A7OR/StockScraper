#pip install requests
#pip install beautifulsoup
import requests
from bs4 import BeautifulSoup
import re
import sys
import termplot

try:
        code = sys.argv[1]
        URL = "https://www.marketwatch.com/investing/stock/" + code
        graphURL = "https://finance.yahoo.com/quote/" + code + "/history?period1=1604534400&period2=1612483200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
except:
        #Scrapes a search relative to input
        print("What Stonk you want")
        stock = input()
        searchURL = "https://www.marketwatch.com/tools/quotes/lookup.asp?lookup=" + stock
        searchPage = requests.get(searchURL)
        searchSoup = BeautifulSoup(searchPage.content, "html.parser")
        searchResults = searchSoup.findAll("div", {'class': 'results'})
        searchResults = str(searchResults)

        scanSoup = BeautifulSoup(searchResults, "html.parser")
        search = [[]]
        counter = 0
        counted = 1
        temp = ""
        for link in scanSoup.find_all('td'):
            if link.has_attr("class"):
                if counted < 3:
                    temp = link.get("class", "bottomborder"), link.text
                    search[counter].append(temp[1])
                    if counted == 2:
                        search.append([])
                        counter += 1
                    counted += 1
                else:
                    counted = 1

        search.pop()
        counter = 0
        for stonk in search:
            print("NUM: "+ str(counter) +" CODE: "+ stonk[0] + " TITLE: " + stonk[1])
            counter += 1

        print("Select Code")
        code = input()
        code = int(code)
        stonk = search[code]
        URL = "https://www.marketwatch.com/investing/stock/" + stonk[0]
        graphURL = "https://finance.yahoo.com/quote/" + stonk[0] + "/history?period1=1604534400&period2=1612483200&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"

#Scrapes all information about stock
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.findAll("h3", {'class': 'intraday__price'})[0].find('bg-quote').text
keyResults = soup.findAll("ul", {'class': 'list list--kv list--col50'})

detailResults = []
strkeyResults = str(keyResults)
soup2 = BeautifulSoup(strkeyResults, "html.parser")
for link in soup2.find_all('li'):
    if link.has_attr("class"):
        temp = link.get("class", ""), link.text
        test = temp[1]
        test = test[1:-2]
        test = test.replace('\n', ': ')
        detailResults.append(test + "\n")


print(*detailResults)
print("Current Stonk Price: $" + str(results) + "\n")

#Scrapes graph for selected stock
gpage = requests.get(graphURL)
gsoup = BeautifulSoup(gpage.content, "html.parser")
graphResults = gsoup.findAll("tr", {'class': 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})

finalGraphResults = []
graphcounter = 1
graphResults = str(graphResults)
gsoup2 = BeautifulSoup(graphResults, "html.parser")
for link in gsoup2.find_all('td'):
    if link.has_attr("class"):
        if graphcounter == 6:
            temp = link.get("class", "Py(10px) Pstart(10px)"), link.text
            test = temp[1]
            test = str(test.replace(',',''))
            test = int(float(test))
            finalGraphResults.append(test)
        elif graphcounter == 7:
            graphcounter = 0
        graphcounter += 1

finalGraphResults = finalGraphResults[::-1]
#print(finalGraphResults)
termplot.plot(finalGraphResults, plot_height=70, plot_char='/')
