import nltk
import pandas as pd
from urllib import urlopen
from urllib import FancyURLopener
from bs4 import BeautifulSoup
#from selenium import webdriver

# Custom url opener for Google Scholar, which detects bots
class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
openurl = MyOpener().open

# We start by parsing Sasha's first paper in Cerebral Cortex

url = "http://cercor.oxfordjournals.org/content/24/2/281.full"

# Open and import into Beautiful Soup
html = urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')
soupArticle = soup.find(class_="article")

# Find the article's DOI (in Cerebral Cortex)
articleDOI = soup.find(class_='slug-doi').text

# Query google scholar for citations
urlQ = 'http://scholar.google.com/scholar?q=' + articleDOI
htmlQ = openurl(urlQ).read()
soupQ = BeautifulSoup(htmlQ, 'lxml')

urlC = "http://scholar.google.com" + soupQ.find(class_='gs_ri').find(class_='gs_fl').a.get('href')
htmlC = openurl(urlC).read()
soupC = BeautifulSoup(html, 'lxml')

for t in soupC.find_all(class_='gs_md_wp'):
    if t.find(class_='gs_ctg2').text == '[HTML]':
        print t.a.get('href')



citations = soup.find_all(class_='xref-bibr')

DOIs = list()

# Print all citations to the display
for c in citations:
    print c.text + ' : ' + c['href']
    
    cRef = soup.find_all(id=c['href'][1:])
    
    # Get citation text with DOI link
    # For Cerebral Cortex this is located in the next element
    cText = cRef[0].next_sibling()
    print ' '.join(nltk.word_tokenize(cText[0].text))
    
    # Get HTML links
    try:
        doi = cText[0].find('a')['href']
        DOIs.append(doi)
    except:
        print '<***> NO HREF for' + c.text + ' <***>'
        
    print ''

print 'DOIs:'
print DOIs