import urllib.request
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
import html2text

# Setting the path and driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window()
div = '1'  # For concatenate and set a div loop
cdiv = 1  # For count divs
n = 1

# Open olx page
while n != 55:  # change this value according to numbers of pages you want to scrape
    ns = str(n)
    # You need to find the page pattern and concatenate with 'ns' to set the loop
    page = driver.get("https://ba.olx.com.br/grande-salvador/imoveis/venda/apartamentos?f=p&o="+ns+"&pe=200000&sf=1")
    print(driver.title)
    og = driver.window_handles[0]
    sleep(5)
    # Going to first ad
    while cdiv != 55:
        try:
            sleep(4)
            driver.switch_to.window(og)
            xp = "//li["+div+"]/a/div/div[2]/div[1]/div[1]/h2"
            WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, f"{xp}"))).click()
            sleep(5)
        except:
            cdiv += 1
            div = str(cdiv)
            print(cdiv)
            continue
        # Clicking on 'show description' and 'show number'
        try:
            driver.switch_to.window(driver.window_handles[1])
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div[1]/div[13]/div/div[2]/div/a"))).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, "//div[2]/div/div[2]/div[1]/div[13]/div/div[2]/div/p/span/a"))).click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div[1]/div[13]/div/div[2]/div/p/span/a"))).click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div[1]/div[13]/div/div[2]/div/p/span/a"))).click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[2]/div/div[2]/div[1]/div[13]/div/div[2]/div/p/span/a"))).click()
        except:
            pass
        sleep(5)
        # Changing driver focus to the ad window with phone number loaded
        driver.switch_to.window(driver.window_handles[1])
        my_url = driver.current_url

        # Making a text from HTML
        my_url_HTML = driver.page_source
        text_maker = html2text.HTML2Text()
        text_maker.ignore_images = True
        text_maker.ignore_links = True
        text = text_maker.handle(my_url_HTML)

        # Some REGEX to find and organize phone number into a list
        phone_ddd = re.compile(r'\d\d[-]\d\d\d\d\d\d\d\d\d')
        phone_3ddd = re.compile(r'\d\d\d[-]\d\d\d\d\d\d\d\d\d')
        phone_ddd_dash = re.compile(r'\d\d\d\d\d\d\d[-]\d\d\d\d')
        phone_ddd_doubledash = re.compile(r'\d\d[-]\d\d\d\d\d[-]\d\d\d\d')
        phone_ddd_nodash = re.compile(r'\d\d\d\d\d\d\d\d\d\d\d')
        phone_comma_dash = re.compile(r'\d\d\d\d\d[-]\d\d\d\d[,.]')
        phone_comma = re.compile(r'[9]\d\d\d\d\d\d\d\d[,.]')
        phone_nodash = re.compile(r'[9]\d\d\d\d\d\d\d\d')
        phone_dash = re.compile(r'[9]\d\d\d\d[-]\d\d\d\d')
        if phone_comma_dash == phone_dash:
            phone_comma_dash = ' '

        # Organizing phone numbers in a list
        pn = [phone_ddd.findall(text), phone_comma.findall(text), phone_nodash.findall(text), phone_dash.findall(text),
              phone_comma_dash.findall(text), phone_ddd_doubledash.findall(text), phone_3ddd.findall(text),
              phone_ddd_dash.findall(text), phone_ddd_nodash.findall(text)]
        pns = str(pn)
        pns = pns.replace(']', '').replace('[', '').replace(',', '')

        # Writing phone numbers on txt file and saving it
        if pns == str('        '):
            with open('phone&url.txt', 'a') as saving:
                saving.write(str(my_url) + '\n' + ' folder without number ' + '\n')
                saving.write('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=' + '\n')
        else:
            with open('phone.txt', 'a') as onlyphone:
                onlyphone.write(pns.replace("'", "") + '\n')
            with open('phone&url.txt', 'a') as saving:
                saving.write(str(my_url) + '\n' + pns + '\n')
                saving.write('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=' + '\n')
                print(pns)
        # Changing driver focus to ad window and closing it
        driver.switch_to.window(driver.window_handles[1])
        cdiv += 1
        div = str(cdiv)
        print(div)
        driver.close()