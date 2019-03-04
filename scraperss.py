import feedparser
import urllib
import tldextract
import csv
from bs4 import BeautifulSoup
from newspaper import Article

class ArticleData:
    def __init__(self, publication, title, arttext, pubyear, pubmonth, pubday, url):
        self.publication = publication
        self.title = title
        self.arttext = arttext
        self.pubyear = pubyear
        self.pubmonth = pubmonth
        self.pubday = pubday
        self.url = url
   
def extract_data(link):
    article = Article(link)
    
    try:
        article.download()
        try:
            article.parse()
            
            publication = tldextract.extract(link).domain
            title = article.title
            arttext = article.text
            
            url = link
            
            if article.publish_date is None:
                pubyear = 0
                pubmonth = 0
                pubday = 0
            else:
                pubyear = article.publish_date.strftime('%Y')
                pubmonth = article.publish_date.strftime('%m')
                pubday = article.publish_date.strftime('%d')
            
            print(link)
            
            return ArticleData(publication, title, arttext, pubyear, pubmonth, pubday, url)
        except:
            print('oop parse fail')
            return ArticleData(0,0,0,0,0,0,0)
    except:
        print('oop download fail')
        return ArticleData(0,0,0,0,0,0,0)


# Get a list of search terms
query = input('Comma delimited search terms: ')
query_list = query.split(',')

for query in query_list:
    filename = query + '.csv'
    # Converts search term text into something compatible with a URL
    query = urllib.parse.quote_plus(query)
    feed_url = 'https://news.google.com/rss/search?q={' + query + '}'
    
    # Convert RSS feed into objects
    results = feedparser.parse(feed_url)
    
    # Pull a list of URLs from the parsed results and extract data from each link
    links = [entry.link for entry in results.entries]
    full_data = [extract_data(link) for link in links]
    
    # Write object hierarchy as a csv file
    with open(filename, 'w+', ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Publication', 'Title', 'Text', 'Year', 'Month', 'Day', 'URL'])
        for article in full_data:
            writer.writerow([article.publication, article.title, article.arttext, article.pubyear, article.pubmonth, article.pubday, article.url])