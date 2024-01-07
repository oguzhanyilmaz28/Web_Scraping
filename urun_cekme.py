import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

linkler = []

# CSV dosyasinin yolu
link_yolu = "link.csv"

with open(link_yolu, encoding="utf-8") as csvfile:
    linklerCSV = csv.reader(csvfile)

    for link in linklerCSV:
        linkler.append(link)

# Ilk indeksdeki 'link' kelimesini silme
del linkler[0]

browser = webdriver.Chrome()

for i in range(len(linkler)):
    browser.get(linkler[i][0])
    kaynak = browser.page_source
    bs = BeautifulSoup(kaynak, "html.parser")
    urunFiyat = bs.find("span", attrs={"class": "product-list__price"}).text
    urunMarka = bs.find("h1", attrs={"class": "product-list__product-name"}).text
    urunYildiz = (bs.find('span', attrs={"class": "score"})).get("style")

    yorumlar_linki = browser.find_element(By.CSS_SELECTOR, 'a[href="#yorumlar"]')
    yorumlar_linki.click()
    time.sleep(3)
    #urunYorumlar = bs.find("div", attrs={"class": "col-md-12 ds-table comment-items"})
    #yorum = urunYorumlar.find_all("span")
    #text = bs.find('div', class_='comment-section')
    #print(yorum)