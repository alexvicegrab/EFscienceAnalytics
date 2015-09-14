import nltk
from urllib import urlopen
from bs4 import BeautifulSoup

# We start by parsing Sasha's first paper in Cerebral Cortex

url = "http://cercor.oxfordjournals.org/content/24/2/281.full"

# Open and import into Beautiful Soup
html = urlopen(url).read()
soup = BeautifulSoup(html, 'lxml')
soupArticle = soup.find(class_="article")
citations = soup.find_all(class_='xref-bibr')

# Print all citations to the display
for c in citations:
    print c.text + ' : ' + c['href']
    
    cLinks = soup.find_all(id=c['href'][1:])
    
    # Get citation text with DOI link
    # For Cerebral Cortex this is located in the next element
    e = cLinks[0].next_sibling()
    print ' '.join(nltk.word_tokenize(e[0].text))
    
    print ''