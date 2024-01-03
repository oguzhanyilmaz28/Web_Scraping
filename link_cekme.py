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

    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[1]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[2]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[3]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[4]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[5]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[6]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[7]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[8]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[9]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[10]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[11]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[12]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[13]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[14]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[15]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[16]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[17]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[18]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[19]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[20]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[21]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[22]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[23]/div[1]/a').get_attribute('href'))
    urun_url_liste.append(browser.find_element(By.XPATH,'//*[@id="productsLoad"]/div[24]/div[1]/a').get_attribute('href'))



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
