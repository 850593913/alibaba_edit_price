from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import csv
import time
from random import random
from selenium.webdriver.common.keys import Keys

option = webdriver.ChromeOptions()
# option.add_experimental_option('prefs', {"profile.managed_default_content_settings.images": 2}) #不加载图片
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
# option.add_experimental_option('excludeSwitches', ['enable-automation']) #开发者模式
# option.add_argument('--headless') #无窗口模式
browser = webdriver.Chrome(chrome_driver, chrome_options=option)
browser.maximize_window() #窗口最大化
wait = WebDriverWait(browser, 10)
browser.set_page_load_timeout(3) #设置页面加载超时
browser.set_script_timeout(3) #设置脚本加载超时

def parse_one_product():
    one_product = []

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mod-detail-title > h1')))
    doc = pq(browser.page_source)

    # 标题
    title = doc('#mod-detail-title > h1')
    one_product.append(title.text())
    
    # 价格
    price_all = []
    price = doc('#mod-detail-price > div > table > tbody > tr.price').items()
    for item in price:
        for value in item.find('td').items():
            price_all.append(value.text())
    # 批量
    amout_all = []
    amounts = doc('#mod-detail-price > div > table > tbody > tr.amount').items()
    for item in amounts:
        for amount in item.find('td').items():
            amout_all.append(amount.text())
    
    # 价格+批量
    for i in range(len(price_all)):
        price_amount = price_all[i] + ':' + amout_all[i]
        one_product.append(price_amount)
    
    # 详细信息
    detail_all = []
    detail = doc('#mod-detail-attributes > div.obj-content > table > tbody').items()
    for tr in detail:
        for td in tr.find('td').items():
            detail_all.append(td.text())

    for i in range(len(detail_all)):
        if i%2 == 0:
            try:
                detail_pair = detail_all[i] + ':' + detail_all[i+1]
                one_product.append(detail_pair)
            except:
                pass
    print(one_product)
    
    with open('data.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(one_product)

def parse_one_page():
    product_amount = []
    doc = pq(browser.page_source)
    products = doc('#search-bar > div.wp-offerlist-windows.should-get-async-price > div > div > div > ul').items()
    for item in products:
        for li in item.find('.title-new').items():
            product_amount.append(li)
    for i in range(len(product_amount)):
        product_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#search-bar > div.wp-offerlist-windows.should-get-async-price > div > div > div > ul > li:nth-child(' + str(i+1) + ') > div.image > a')))
        if i >= 7:
            browser.execute_script("window.scrollTo(0,1500)")
        product_link.click()
        windows = browser.window_handles
        browser.switch_to.window(windows[-1])
        
        #如果加载超过3秒
        try:
            parse_one_product() #解析
        except:
            browser.execute_script("window.stop()") #停止加载
            parse_one_product() #重新解析

        browser.close()
        browser.switch_to.window(windows[0])
        time.sleep(random()*10)

def next_page(pagenumber):

    page_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#site_content > div.grid-main > div > div.mod.mod-offerColumnNew.app-offerColumnNew.app-type-default.mod-ui-not-show-title.mod-offerColumnNew.mod-ui-not-show-title > div > div.m-content > div.mod.wp-all-offer-column.wp-all-offer-column-new > div.app-paginator.app-type-default > div > ul > li.pagination > a.next')))
    try:
        page_button.click()
    except:
        browser.execute_script("window.stop()") #停止加载

if __name__ == "__main__":
    for pagenumber in range(70,72):
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#search-bar > div.wp-offerlist-windows.should-get-async-price > div > div > div > ul')))
        try:
            parse_one_page()
        except:
            browser.execute_script("window.stop()") #停止加载
            parse_one_page()
        next_page(pagenumber)
        
 

        

