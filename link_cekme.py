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

    artan = 1
    for x in range(24):
        urun_url_liste.append( browser.find_elements(By.XPATH, '/ html / body / main / div[1] / div / div / div[4] / div[1] / div['+str(x)+'] / div[1] / a'))
        artan+=1

    print(urun_url_liste)


    f = open('link.csv', 'w', encoding="utf-8")
    baslik = ["link"]
    writer = csv.writer(f)
    writer.writerow(baslik)
    for row in urun_url_liste:
        writer.writerow(row)
    f.close()
for x in range(1):
    scrape_link(sayfa_url_liste[x])
