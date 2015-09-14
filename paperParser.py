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

def url_to_soup(url):
    html = openurl(url).read()
    soup = BeautifulSoup(html, 'lxml')
    #[x.extract() for x in soup(['script','style'])]
    return soup

# We start by parsing Sasha's first paper in Cerebral Cortex

url = "http://cercor.oxfordjournals.org/content/24/2/281.full"

# Open and import into Beautiful Soup
soup = url_to_soup(url)

soupArticle = soup.find(class_="article")

# Find the article's DOI (in Cerebral Cortex)
articleDOI = soup.find(class_='slug-doi').text

# Query google scholar for citations
urlQ = 'http://scholar.google.com/scholar?q=' + articleDOI

soupQ = url_to_soup(urlQ)

urlC = "http://scholar.google.com" + soupQ.find(class_='gs_ri').find(class_='gs_fl').a.get('href')

soupC = url_to_soup(urlC)

citers = list()

for t in soupC.find_all(class_='gs_md_wp'):
    if t.find(class_='gs_ctg2').text == '[HTML]':
        citers.append( t.a.get('href') )

print citers

# Get first cited paper
urlL = citers[0]

soupL = url_to_soup(urlL)


# Get ID of reference
for c in soupL.find_all(class_='ref-cit'):
    if c.get('data-doi') == articleDOI:
        ref = c.parent.find(class_="rev-xref-ref").get("href")

for c in soupL.find_all(class_="xref-bibr"):
    if c.get('id') == ref[1:]:
        print c.parent.text
        

##############################################

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