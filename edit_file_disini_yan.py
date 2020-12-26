import time
import undetected_chromedriver as UC
import pyfiglet as pf
import matplotlib.pyplot as plt

from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait as wd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

UC.TARGET_VERSION = 87

class ScrapeData:

    def __init__(self):
        opsi = UC.ChromeOptions()
        print("----- Opsi Chrome -----\n")
        set_gui = input("Headless / Normal : ")
        if set_gui == "headless":
            opsi.headless = True
            opsi.add_argument('--headless')
        else:
            opsi.headless = False
            opsi.add_argument('start-maximized')
            
        set_server = input("Proxy / Socks5 / None : ")
        if set_server.lower == "proxy":
            proxy_server = input("Masukan proxy : ")
            opsi.add_argument(f"--proxy-server={proxy_server}")
        elif set_server.lower == "socks5":
            socks5_server = input("Masukan socks5 : ")
            opsi.add_argument(f"--proxy-server=socks5://{socks5_server}")
        else:
            pass
        opsi.add_argument('--disable-extensions')
        prefs = {"profile.default_content_setting_values.notifications": False,
        "credentials_enable_service": False, 
        "profile.password_manager_enabled" : False}
        self.browser = UC.Chrome(options=opsi, enable_console_log=True)
        self.browser.get("https://lazada.co.id")
        
    def filter_produk(self, harga, harga_max):
        self.harga = harga
        self.harga_max = harga_max
        try:
            filter = wd(self.browser, 60).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div[6]/div[2]/div/input[1]')))
            self.browser.execute_script("arguments[0].click();", filter)
            filter.send_keys(harga)
            filter2 = wd(self.browser, 60).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div[6]/div[2]/div/input[2]')))
            self.browser.execute_script("arguments[0].click();", filter2)
            filter2.send_keys(harga_max)
            click = wd(self.browser, 60).until(EC.element_to_be_clickable((
                By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[2]/div/div[6]/div[2]/div/button')))
            self.browser.execute_script("arguments[0].click();", click)
        except NoSuchElementException as e:
            print(e)
    
    def search_produk(self, nama_barang):
        try:
            produk = wd(self.browser, 60).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="q"]')))
        except NoSuchElementException as e:
            print(e)
        self.browser.execute_script("arguments[0].click();", produk)
        produk.send_keys(nama_barang, Keys.RETURN)

    def scraping_element_list(self):
        try:
            self.nama_produk = self.browser.find_elements(By.CLASS_NAME, 'c16H9d')
            time.sleep(5)
            self.harga_produk = self.browser.find_elements(By.CLASS_NAME, 'c3gUW0')
        except NoSuchElementException as e:
            print(e)
        
    def list_manipulating(self, jumlah):
        self.jumlah = jumlah
        list_nama = []
        list_harga = []
        print("\n")
        for nama in self.nama_produk:
            list_nama.append(nama.text)
            a = len(list_nama)
            if a == self.jumlah:
                break
            continue
        
        for harga in self.harga_produk:
            list_harga.append(harga.text)
            b = len(list_harga)
            if b == self.jumlah:
                break
            continue

        self.a = list_nama
        self.b = list_harga
        
        #.replace('p', '')     
    def output_list(self):
        self.b = [i.replace('Rp', '').replace('.', '') for i in self.b]
        print("----- List Nama Produk -----")
        y = 0
        for x in self.a:
            print("-", self.a[y])
            y += 1
        print("\n")
        print("----- List Harga Produk -----")
        z = 0
        for x in self.b:
            print("-", self.b[z])
            z += 1
        
#         print("\n")
#         print(a)
#         print("\n")
#         print(b)
        
    def apaya(self):
        a = pf.figlet_format("UAS DAA 100")
        print(a)
        
    def main(self):
        self.apaya()
        print("\n-------------------------------\n")
        nama_barang = input("Masukan barang yang dicari : ")
        harga = input("Input rentang harga terendah : ")
        harga_max = input("Input rentang harga tertinggi :")
        jumlah = int(input("Input jumlah barang untuk di sorting : "))
        self.search_produk(nama_barang)
        self.filter_produk(harga, harga_max)
        self.scraping_element_list()
        self.list_manipulating(jumlah)
        self.output_list()
        
if __name__ == "__main__":
    a = ScrapeData()
    a.main()
