from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import time

sayfa_url_liste = []
urun_url_liste=[]
sayac = 1

for a in range(9):
    sayfa_url_liste.append("https://www.vatanbilgisayar.com/arama/Cep%20telefonu/?page=" + str(sayac))
    sayac += 1

options = webdriver.ChromeOptions();
options.add_experimental_option('excludeSwitches', ['enable-logging']);


def scrape_link(url):
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.get(url)

    time.sleep(3)

    bs = BeautifulSoup(browser.page_source, "html.parser")
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

for x in range(9):
    scrape_link(sayfa_url_liste[x])
