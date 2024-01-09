"""import csv
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
    time.sleep(5)

    kaynak = browser.page_source
    bs = BeautifulSoup(kaynak, "html.parser")
    urunYorumlar = bs.find("div", attrs={"class": "comment-section"})

    yorumlar = urunYorumlar.find_all("div", attrs={"class": "comment"})
    rank = urunYorumlar.find_all("div", attrs={"class": "wrapper-comments commetPrd"})
    isimler = urunYorumlar.find_all("div", attrs={"class": "comment-name"})
    tarihler = urunYorumlar.find_all("span", attrs={"class": "replaced-date"})

    print(isimler[0].text)
    print(tarihler[0].text)

    print(yorumlar[0].text)
    rank[0].get('data-rank')

    time.sleep(300)
"""

import sqlite3

con = sqlite3.connect("urun.db")

cursor = con.cursor()


def tabloyaurunekleme():
    cursor.execute("INSERT INTO urun VALUES { 'iphone1','iphone',12,'saddsa',4,'cok iyii',1}")
    con.commit()
    con.close()


tabloyaurunekleme()
