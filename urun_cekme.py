import csv
import time
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# Programın başlangıç zamanını al
start_time = time.time()

con = sqlite3.connect("ceptelefon.db")
cursor = con.cursor()

# Tablo varsa silme kodu
cursor.execute("DROP TABLE IF EXISTS urun")
cursor.execute("DROP TABLE IF EXISTS yorum")

def tabloOlustur():

    cursor.execute("CREATE TABLE IF NOT EXISTS Urun (urunID INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "adi TEXT NOT NULL,"
                       "marka TEXT NOT NULL,"
                       "kategori TEXT NOT NULL,"
                       "stok TEXT NOT NULL,"
                       "fiyat INTEGER,"
                       "link TEXT NOT NULL,"
                       "ort_yildiz REAL,"
                       "yorum_sayisi INTEGER)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Yorum (yorumID INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "isim TEXT,"
                       "yorum TEXT,"
                       "tarih TEXT,"
                       "yildiz INTEGER ,"
                       "urunID INTEGER ,"
                       "FOREIGN KEY (urunID) REFERENCES Urun(urunID))")


tabloOlustur()

linkler = []

# CSV dosyasinin yolu
link_yolu = "link.csv"

with open(link_yolu, encoding="utf-8") as csvfile:
    linklerCSV = csv.reader(csvfile)

    for link in linklerCSV:
        linkler.append(link[0])

# Ilk indeksdeki 'link' kelimesini silme
del linkler[0]
browser = webdriver.Chrome()

for i in range(len(linkler)):
    browser.get(linkler[i])
    kaynak = browser.page_source
    bs = BeautifulSoup(kaynak, "html.parser")

    urunBilgi = bs.findAll("a", attrs={"class": "bradcrumb-item"})
    urunKategori = urunBilgi[2].text
    urunMarka = urunBilgi[3].text
    urunModel = urunBilgi[4].text
    toplamYorum = int((bs.find("a", attrs={"class": "comment-count"}).text).replace("(", "").replace(")", ""))
    stokBilgi = bs.find("div", attrs={"class": "d-cell product-button--cell"}).text

    if stokBilgi == "\n\nTükendi\n\n":
        stokDurum = "Yok"
        urunFiyat = 0
    else:
        stokDurum = "Var"
        urunFiyat = bs.find("span", attrs={"class": "product-list__price"}).text

    try:
        yorumlar_linki = browser.find_element(By.CSS_SELECTOR, 'a[id="allCommentBtn"]')
        yorumlar_linki.click()
        time.sleep(3)
    except:
        print("Yorum Yok")

    kaynak = browser.page_source
    bs = BeautifulSoup(kaynak, "html.parser")
    ortalamaRank = float(bs.find("strong", attrs={"id": "averageRankNum"}).text)

    sql_sorgu = "INSERT INTO urun (adi,marka, kategori, stok, fiyat,link,ort_yildiz,yorum_sayisi) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?)"
    veri = (urunModel, urunMarka,  urunKategori, stokDurum, urunFiyat, linkler[i], ortalamaRank, toplamYorum)

    # Veritabanına ekleme işlemi
    cursor.execute(sql_sorgu, veri)
    con.commit()

    urunYorumlar = bs.find("div", attrs={"class": "comment-section"})

    isimler = urunYorumlar.find_all("div", attrs={"class": "comment-name"})
    yorumlar = urunYorumlar.find_all("div", attrs={"class": "comment"})
    tarihler = urunYorumlar.find_all("span", attrs={"class": "replaced-date"})
    rank = urunYorumlar.find_all("div", attrs={"class": "wrapper-comments commetPrd"})

    #ilk 100 yorumu alması için
    yorumlar = yorumlar[0:100]

    for a in range(len(yorumlar)):
        sql_sorgu = "INSERT INTO yorum (isim, yorum, tarih, yildiz,urunId) VALUES ( ?, ?, ?, ?, ?)"
        veri = (isimler[a].text, yorumlar[a].text, tarihler[a].text, rank[a].get('data-rank'), i+1)
        # Veritabanına ekleme işlemi
        cursor.execute(sql_sorgu, veri)

    # Değişiklikleri kaydet
    con.commit()

# Veritabanin kapatilmasi
con.close()

# Programın bitiş zamanını al
end_time = time.time()
# Geçen süreyi hesapla
elapsed_time = end_time - start_time

print(f"Programın çalışma süresi: {elapsed_time} saniye")
