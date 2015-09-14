import nltk
import pandas as pd
from urllib import urlopen
from bs4 import BeautifulSoup

# We start by parsing Sasha's first paper in Cerebral Cortex

url = "http://cercor.oxfordjournals.org/content/24/2/281.full"

# Open and import into Beautiful Soup
html = urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')
soupArticle = soup.find(class_="article")
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