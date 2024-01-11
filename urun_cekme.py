import csv
import time
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


con = sqlite3.connect("urun.db")
cursor = con.cursor()

def tabloOlustur():

    cursor.execute("CREATE TABLE IF NOT EXISTS urun (urunId INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "adi TEXT NOT NULL,"
                       "marka TEXT NOT NULL,"
                       "fiyat INTEGER,"
                       "link TEXT NOT NULL,"
                       "ort_yildiz INTEGER,"
                       "yorum_sayisi INTEGER)")

    cursor.execute("CREATE TABLE IF NOT EXISTS yorum (yorumId INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "isim TEXT,"
                       "yorum TEXT,"
                       "tarih TEXT,"
                       "yildiz INTEGER ,"
                       "urunId INTEGER ,"
                       "FOREIGN KEY (urunId) REFERENCES urun(urunId))")


tabloOlustur()

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
    #stokBilgi = bs.find("span", attrs={"class": "icon-shopping-card"}).text
    """    if stokBilgi == "Sepete Ekle":
        urunFiyat = bs.find("span", attrs={"class": "product-list__price"}).text
    else:
        urunFiyat = 0"""
    urunBilgi = bs.findAll("a", attrs={"class": "bradcrumb-item"})
    urunMarka = urunBilgi[3].text
    urunModel = urunBilgi[4].text
    toplamYorum = (bs.find("a", attrs={"class": "comment-count"}).text).replace("(", "").replace(")", "")
    urunYildiz = (bs.find('span', attrs={"class": "score"})).get("style")

    connection = sqlite3.connect("urun.db")
    cursor = connection.cursor()

    sql_sorgu = "INSERT INTO urun (adi,marka,fiyat,link,ort_yildiz,yorum_sayisi) VALUES ( ?, ?, ?, ?, ?, ?)"
    veri = ("urunModel", "urunMarka", 0, "linkler", 0, 0)

    # Veritabanına ekleme işlemi
    cursor.execute(sql_sorgu, veri)
    connection.commit()
    connection.close()


"""
    try:
        yorumlar_linki = browser.find_element(By.CSS_SELECTOR, 'a[id="allCommentBtn"]')
        time.sleep(1)
        yorumlar_linki.click()
        time.sleep(2)
    except:
        print("yorumyok")


    kaynak = browser.page_source
    bs = BeautifulSoup(kaynak, "html.parser")
    ortalamaRank = bs.find("strong", attrs={"id": "averageRankNum"}).text
    urunYorumlar = bs.find("div", attrs={"class": "comment-section"})

    isimler = urunYorumlar.find_all("div", attrs={"class": "comment-name"})
    yorumlar = urunYorumlar.find_all("div", attrs={"class": "comment"})
    tarihler = urunYorumlar.find_all("span", attrs={"class": "replaced-date"})
    rank = urunYorumlar.find_all("div", attrs={"class": "wrapper-comments commetPrd"})

    #ilk 100 yorumu alması için
    yorumlar = yorumlar[0:100]

    connection = sqlite3.connect("urun.db")
    cursor = connection.cursor()

    for a in range(len(yorumlar)):
        sql_sorgu = "INSERT INTO yorum (isim, yorum, tarih, yildiz,urunId) VALUES ( ?, ?, ?, ?, ?)"
        veri = (isimler[a].text, yorumlar[a].text, tarihler[a].text, rank[a].get('data-rank'), i)
        # Veritabanına ekleme işlemi
        cursor.execute(sql_sorgu, veri)

    # Değişiklikleri kaydet ve bağlantıyı kapat
    connection.commit()
    connection.close()
"""
