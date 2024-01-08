import csv
import time
import sqlite3 as sql
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

con = sql.connect("urun.db")
cursor = con.cursor()

def tabloOlustur():
    cursor.execute("CREATE TABLE IF NOT EXISTS urun (urunId INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "adi TEXT NOT NULL,"
                   "marka TEXT NOT NULL,"
                   "fiyat INTEGER,"
                   "link TEXT NOT NULL UNIQUE,"
                   "ort_yildiz INTEGER,"
                   "yorum_sayisi INTEGER)")

    cursor.execute("CREATE TABLE IF NOT EXISTS yorum (yorumId INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "isim TEXT NOT NULL,"
                    "yorum TEXT NOT NULL,"
                    "tarih TEXT NOT NULL,"
                    "yildiz INTEGER NOT NULL,"
                    "urunId INTEGER NOT NULL,"
                    "FOREIGN KEY (urunId) REFERENCES urun(urunId))")


tabloOlustur()
yas = ["abc", "avs", 5545, "tfj", 4, 55]
cursor.execute('INSERT INTO urun (adi, marka, fiyat, link, ort_yildiz, yorum_sayisi) VALUES (?, ?, ?, ?, ?, ?)', yas)
cursor.close()

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
    urunBilgi = bs.findAll("a", attrs={"class": "bradcrumb-item"})
    urunMarka = urunBilgi[3].text
    urunModel = urunBilgi[4].text
    toplamYorum = (bs.find("a", attrs={"class": "comment-count"}).text).replace("(", "").replace(")", "")
    urunYildiz = (bs.find('span', attrs={"class": "score"})).get("style")

    yorumlar_linki = browser.find_element(By.CSS_SELECTOR, 'a[href="#yorumlar"]')
    yorumlar_linki.click()
    time.sleep(5)

    kaynak = browser.page_source
    bs = BeautifulSoup(kaynak, "html.parser")
    ortalamaRank = bs.find("strong", attrs={"id": "averageRankNum"}).text
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
