from bs4 import BeautifulSoup
import requests
import re
from urlextract import URLExtract




def getImageLinks(url):

    # Load intermediate google ads website
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.content, 'html.parser')
    scripts = soup.findAll("script")

    # Extract actual link to website
    text = scripts[len(scripts) - 1].get_text()
    extractor = URLExtract()
    urls = extractor.find_urls(text)
    actualURL = urls[0]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(actualURL, headers=headers)
    soup = BeautifulSoup(result.content, 'html.parser')

    returnLink = list()

    for link in soup.findAll("a", {"class": "action-expand"}):
        returnLink.append(link.get('href'))
    return(returnLink)


