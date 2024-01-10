import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time

anaurl = "https://www.vatanbilgisayar.com/"
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
browser.get(anaurl)
bar = browser.find_element(By.XPATH, '/html/body/header/nav/div[3]/div[1]/div/div/div[1]/button')
bar.click()
time.sleep(1)
telefon = browser.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[1]/a')
telefon.click()
time.sleep(1)
tümtelefon = browser.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[1]/div/div/div[1]/ul[2]/div[1]/li[1]/a')
tümtelefon.click()
current_url = browser.current_url


sayfa_url_liste = []
urun_url_liste=[]
sayac = 1

for a in range(9):
    sayfa_url_liste.append(str(current_url)+"?page=" + str(sayac))
    sayac += 1

#tarayıcı günlüklerini devre dışı bırakır, gereksiz log çıktılarından kaçınır
options = webdriver.ChromeOptions();
options.add_experimental_option('excludeSwitches', ['enable-logging']);


def scrape_link(url):
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.get(url)

    time.sleep(3)

    for c in range(1,25) :
        urun_url_liste.append(
            browser.find_element(By.XPATH, '//*[@id="productsLoad"]/div['+str(c)+']/div[1]/a').get_attribute('href'))
        c+=1

    f = open('link.csv', 'w', newline='', encoding="utf-8")
    baslik = ["link"]
    writer = csv.writer(f)
    writer.writerow(baslik)
    for row in urun_url_liste:
        writer.writerow(row)
    f.close()

    with open('link.csv', 'r') as dosya:
        veri = dosya.read()

    temiz_veri = veri.replace(',', '')

    with open('link.csv', 'w') as temizlenmis_dosya:
        temizlenmis_dosya.write(temiz_veri)


#kac sayfa gezecek o belirtilir
for x in range(9):
    scrape_link(sayfa_url_liste[x])
