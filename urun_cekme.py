import csv
import time
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# Programın başlangıç zamanını al
start_time = time.time()

con = sqlite3.connect("urun.db")
cursor = con.cursor()

# Tablo varsa silme kodu
cursor.execute("DROP TABLE IF EXISTS urun")
cursor.execute("DROP TABLE IF EXISTS yorum")

def tabloOlustur():

    cursor.execute("CREATE TABLE IF NOT EXISTS urun (urunId INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "adi TEXT NOT NULL,"
                       "marka TEXT NOT NULL,"
                       "stok TEXT NOT NULL,"
                       "fiyat INTEGER,"
                       "link TEXT NOT NULL,"
                       "ort_yildiz REAL,"
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
        linkler.append(link[0])

# Ilk indeksdeki 'link' kelimesini silme
del linkler[0]
browser = webdriver.Chrome()

for i in range(len(linkler)):
    browser.get(linkler[i])
    kaynak = browser.page_source
    bs = BeautifulSoup(kaynak, "html.parser")

    urunBilgi = bs.findAll("a", attrs={"class": "bradcrumb-item"})
    urunMarka = urunBilgi[3].text
    urunModel = urunBilgi[4].text
    toplamYorum = int((bs.find("a", attrs={"class": "comment-count"}).text).replace("(", "").replace(")", ""))
    stokBilgi = bs.find("div", attrs={"class": "d-cell product-button--cell"}).text  #class="btn btn-success detail-cart-button btn-nonstock"

    if stokBilgi == "\n\nTükendi\n\n":
        stokDurum = "Yok"
        urunFiyat = 0
    else:
        stokDurum = "Var"
        urunFiyat = bs.find("span", attrs={"class": "product-list__price"}).text

    print(urunFiyat)
    try:
        yorumlar_linki = browser.find_element(By.CSS_SELECTOR, 'a[id="allCommentBtn"]')
        yorumlar_linki.click()
        time.sleep(1)
    except:
        print("Yorum Yok")

    kaynak = browser.page_source
    bs = BeautifulSoup(kaynak, "html.parser")
    ortalamaRank = float(bs.find("strong", attrs={"id": "averageRankNum"}).text)

    connection = sqlite3.connect("urun.db")
    cursor = connection.cursor()

    sql_sorgu = "INSERT INTO urun (adi,marka,stok, fiyat,link,ort_yildiz,yorum_sayisi) VALUES ( ?, ?, ?, ?, ?, ?, ?)"
    veri = (urunModel, urunMarka, stokDurum, urunFiyat, linkler[i], ortalamaRank, toplamYorum)

    # Veritabanına ekleme işlemi
    cursor.execute(sql_sorgu, veri)
    connection.commit()
    connection.close()

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

# Programın bitiş zamanını al
end_time = time.time()
# Geçen süreyi hesapla
elapsed_time = end_time - start_time

print(f"Programın çalışma süresi: {elapsed_time} saniye")
