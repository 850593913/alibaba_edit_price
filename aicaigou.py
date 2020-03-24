import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

option = webdriver.ChromeOptions()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
browser = webdriver.Chrome(chrome_driver, chrome_options=option)
wait = WebDriverWait(browser, 10)

# 产品标题
def title(row):
    title = row[0]
    if len(title) >=50:
        title = title[:50]

    title_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#title')))
    title_input.send_keys(title)

# 百度类目
def sort():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loadcat > option:nth-child(2)'))).click()

# 型号
def model(row):
    for column in row:
        if '型号:' in column:
            result = re.match('型号:(.*)', column)

            model_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#keyword')))
            model_input.send_keys(result.group(1))

# 产品类型
def product_type():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#type_box > select > option:nth-child(2)'))).click()



# 品牌
def brand(row):
    for column in row:
        if '品牌:' in column:
            result = re.match('品牌.*?([\u4E00-\u9FA5]+)', column)

            brand_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#brand')))
            brand_input.send_keys(result.group(1))

# 产品主图
def main_img():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#showthumb'))).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.layui-layer-btn.layui-layer-btn- > a.layui-layer-btn0'))).click()
    browser.switch_to_frame(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.layui-layer-content iframe"))))
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.row > div > div > div > a > div > img'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="checkbox"]')))
    lis = browser.find_elements_by_xpath('//input[@type="checkbox"]')
    for i in lis[:3]:
        i.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.btn-group > a.btn-d.use-image'))).click()

#关键词
def keyword(row):
    for column in row:
        if '型号:' in column:
            result = re.match('型号:(.*)', column)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#keyword1'))).send_keys(result.group(1))
        if '品牌:' in column:
            result = re.match('品牌.*?([\u4E00-\u9FA5]+)', column)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#keyword2'))).send_keys(result.group(1))

#产品描述
def description():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#select_desc'))).click()
    browser.switch_to_frame(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#Dtop iframe"))))
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > table > tbody > tr:nth-child(2) > td:nth-child(3) > a.use'))).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#addparam')))
    
# 参数
def argument(row):
    data = []
    for column in row[1:]:
        if '价格:' not in column and '￥' not in column and column != ':':
            result = re.match('(.*?):', column)
            if result != None:
                data.append(result.group(1))
            result = re.match('.*?:(.*)', column)
            if result != None:
                parameter = result.group(1)
                if len(result.group(1)) <= 30:
                    data.append(parameter)  
                else:
                    parameter = result.group(1)[:30]
                    data.append(parameter)

    if len(data) > 10:
        click_count = int((len(data) - 10)/2)
        params_add_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#addparam')))
        ActionChains(browser).move_to_element(params_add_button).perform()
        for i in range(click_count):
            params_add_button.click()
    
    params_inputs = browser.find_elements_by_css_selector('#params > tbody input')
    del params_inputs[len(data):]
    for i in range(len(data)):
        params_inputs[i].clear()
        params_inputs[i].send_keys(data[i])
    


# 价格_最小起订量
def price_amount(row):

    #计量单位
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#u0'))).send_keys('pcs')
    #供货总量
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#amount'))).send_keys('200000')

    data = []
    for i in [column for column in row if '￥' in column]:
        result = re.match('.*?(\d+\.\d+).*?', i)
        price = result.group(1)
        data.append(price)
        result = re.match('.*?:.*?(\d+).*?', i)
        amount = result.group(1)
        data.append(amount)
    if data == []:
        data = ['0.5', '1000']
    
    price_amount_inputs = browser.find_elements_by_css_selector('#dform > table > tbody > tr:nth-child(12) > td.tr > div input')
    del price_amount_inputs[:3]
    for i in range(len(data)):
        price_amount_inputs[i].clear()
        price_amount_inputs[i].send_keys(data[i])
#提交
def submit():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#dform > table > tbody > tr:nth-child(14) > td.tr > input.btn_g'))).click()

#添加新产品
def new_product():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#serch-b > div:nth-child(4) > a:nth-child(2)'))).click()

#上传失败处理
def exception(row):
    title = row[0]
    error = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.layui-layer-content.layui-layer-padding')))
    print(title+':'+error.text)
    with open('exception.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([title,error.text])
    browser.get('https://www.bjweizhifu.com/member/my.php?mid=5&action=add')

if __name__ == "__main__":
    with open('data_remain.csv','r', encoding='gbk') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                title(row)
                sort()
                model(row)
                product_type()
                brand(row)
                main_img()
                keyword(row)
                description()
                argument(row)
                price_amount(row)
                submit()
                time.sleep(6)
                try:
                    new_product()
                except:
                    exception(row)
            except Exception as e:
                name = row[0]
                with open('exception.csv', 'a', newline='', encoding='gbk') as f:
                    writer = csv.writer(f)
                    writer.writerow([name,e])
                    browser.get('https://www.bjweizhifu.com/member/my.php?mid=5&action=add')