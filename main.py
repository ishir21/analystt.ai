from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from csv import writer



s = HTMLSession()
a=[]


def extract_text(x,y,z):
    try:
        return x.find(y,class_=z).text
    except AttributeError as err:
        return None

url = 'https://www.amazon.in/s?k=bags'
list=[]
list.append(url)
def getdata(url):
    r = s.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def getnextpage(soup):
    # this will return the next page URL
    pages = soup.find('span', {'class': 's-pagination-strip'})
    try:
        if not pages.find('li', {'class': 's-pagination-next s-pagination-disabled'}):
            url = 'https://www.amazon.in' + str(pages.find('a', {'class': 's-pagination-next'})['href'])
            return url
        else:
            return
    except AttributeError as err:
        return None

i=1
while i<=19:
    data = getdata(url)
    url = getnextpage(data)
    list.append(url)
    i=i+1
# print(list)
# list has the url's of all pages
for url in list:
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    url_list = soup.find_all('div',class_="s-asin")
    # print(url_list)
# print(len(lists))
with open('amazon.csv','w',encoding='utf8',newline='') as f:
    thewriter = writer(f)
    header=['Product URL','Title','Price','Rating','Number of reviews']
    thewriter.writerow(header)
    for x in url_list:
        product_url = "https://www.amazon.in"+str(x.find('a')['href'])
        title=x.find('span',class_="a-text-normal").text
        price = "Rs." + str(extract_text(x,'span','a-price-whole'))
        rating=extract_text(x,'span','a-icon-alt')
        reviews=extract_text(x,'span','a-size-base')
        info = [product_url,title,price,rating,reviews]
        thewriter.writerow(info)



