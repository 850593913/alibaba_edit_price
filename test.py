from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from tkinter import * #窗口
from tkinter import messagebox

import time
import re
import threading
import os

option = webdriver.ChromeOptions()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_driver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
chrome_driver = os.environ.get('CHROME_DRIVER')
browser = webdriver.Chrome(chrome_driver, chrome_options=option)
wait = WebDriverWait(browser, 10)


# 查找型号
def search(model):
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ballon-container > div.posting-manage > div > div > div > div:nth-child(1) > div > form > div > div:nth-child(1) > span > input')))
    search_input.send_keys(Keys.CONTROL,'a')
    search_input.send_keys(model)
    search_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ballon-container > div.posting-manage > div > div > div > div:nth-child(1) > div > form > div > div:nth-child(4) > button.next-btn.next-medium.next-btn-primary.custom-component-mr-12')))
    search_button.click()
    time.sleep(2)

def get_one_page_product_count():
    items = browser.find_elements_by_css_selector('#ballon-container > div.posting-manage > div > div > div > div.next-loading.next-loading-inline.list-loading > div > div > div > div > div > div:nth-child(4) i')
    return len(items)

def get_page_count():
    page_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ballon-container > div.posting-manage > div > div > div > div.next-pagination.next-medium.next-normal.component-list-pagination > div.next-pagination-pages > div > button')))
    page_num = re.match('.*?共(\d+).*', page_button.get_attribute('aria-label'))
    return int(page_num.group(1))
        


# 修改价格
def editPice(normal_price, num):
    
    edit_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ballon-container > div.posting-manage > div > div > div > div.next-loading.next-loading-inline.list-loading > div > div > div:nth-child(' + str(num+1) + ') > div > div > div:nth-child(4) > div > button > i')))
    edit_button.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.next-overlay-wrapper.opened > div.next-dialog.next-closeable.next-overlay-inner.posting-price-dialog > div.next-dialog-body > div > header > span')))
    price_amount_inputs = browser.find_elements_by_css_selector('body > div.next-overlay-wrapper.opened > div.next-dialog.next-closeable.next-overlay-inner.posting-price-dialog > div.next-dialog-body > div > div > div > div:nth-child(1) > div > div.next-table.next-table-medium.ladder-price-table.only-bottom-border > table > tbody input')
    for i in range(len(price_amount_inputs)):
        if i%2 == 0:
            if int(price_amount_inputs[i].get_attribute('value')) == 100:
                price_amount_inputs[i+1].send_keys(Keys.CONTROL,'a')
                price = round(normal_price + 0.02, 2)
                print(price)
                price_amount_inputs[i+1].send_keys(str(price))
                
            elif int(price_amount_inputs[i].get_attribute('value')) == 1000:
                price_amount_inputs[i+1].send_keys(Keys.CONTROL,'a')
                price = round(normal_price + 0.01, 2)
                print(price)

                price_amount_inputs[i+1].send_keys(str(price))

            elif int(price_amount_inputs[i].get_attribute('value')) == 3000:
                price_amount_inputs[i+1].send_keys(Keys.CONTROL,'a')
                price_amount_inputs[i+1].send_keys(str(normal_price))

            elif int(price_amount_inputs[i].get_attribute('value')) == 30000:
                price_amount_inputs[i+1].send_keys(Keys.CONTROL,'a')
                price = round(normal_price - 0.01, 2)
                print(price)

                price_amount_inputs[i+1].send_keys(str(price))
                
            elif int(price_amount_inputs[i].get_attribute('value')) == 300000:
                price_amount_inputs[i+1].send_keys(Keys.CONTROL,'a')
                price = round(normal_price - 0.02, 2)
                print(price)

                price_amount_inputs[i+1].send_keys(str(price))

    time.sleep(1)

    confirm_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.next-overlay-wrapper.opened > div.next-dialog.next-closeable.next-overlay-inner.posting-price-dialog > div.next-dialog-footer.next-align-right > button.next-btn.next-medium.next-btn-primary.next-dialog-btn'))) 
    confirm_button.click()

    time.sleep(1)


def main():
    #建立窗口
    root = Tk()
    root.resizable(0,0)
    # 型号
    Label(root,text = "型号:").grid(row = 1, column = 0)
    model=Entry(root)
    model.grid(row = 1, column = 1)
    Button(root, text = "搜索", width=5).grid(row = 1, column = 2)
    # 底价
    Label(root,text = "底价:").grid(row = 2, column = 0)
    price=Entry(root)
    price.grid(row = 2, column = 1)
    # 利润率
    Label(root,text = "利润率:").grid(row = 3, column = 0)
    profit=Entry(root)
    profit.grid(row = 3, column = 1)
    # 汇率
    Label(root,text = "汇率:").grid(row = 4, column = 0)
    parities=Entry(root)
    parities.grid(row = 4, column = 1)

    model_str=''
    print_str=''
    profit_str = ''
    parities_str = ''

    def doit():
        try:
            model_str = model.get()
            print_str = price.get()
            profit_str = profit.get()
            parities_str = parities.get()

            normal_price = round(float(print_str)*(1+float(profit_str))/float(parities_str), 2)
            print(normal_price)

            search(model_str)
            for i in range(get_page_count()):
                for j in range(get_one_page_product_count()):
                    editPice(normal_price, j)
                if i+1 != get_page_count():
                    nextpage_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ballon-container > div.posting-manage > div > div > div > div.next-pagination.next-medium.next-normal.component-list-pagination > div.next-pagination-pages > button.next-btn.next-medium.next-btn-normal.next-pagination-item.next-next')))
                    nextpage_button.click()
                    # time.sleep(2)
                else:
                    messagebox.showinfo('结束', '程序结束')
                    break
        except Exception as e:
            messagebox.showinfo('出错', e)
            messagebox.showinfo('结束', '程序结束')
    
    def doit_thread():
        global th
        th=threading.Thread(target=doit)  
        # th.setDaemon(True)#守护线程
        th.start()
    
    def term_thread():
        # 强制结束线程
        import os
        if os.name == "nt":
            # windows 系统
            # 注意：线程结束后 threading.Thread 没有任何提示。
            import ctypes
            h = ctypes.windll.kernel32.OpenThread(1, 0, th.ident)
            assert h != 0
            r = ctypes.windll.kernel32.TerminateThread(h, 0xff)
            assert r != 0
        else:
            raise NotImplementedError

    

    Button(root, text = "执行", width=20, command=doit_thread).grid(row = 5, column = 1)
    Button(root, text = "停止", width=20, command=term_thread).grid(row = 6, column = 1)

    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        messagebox.showinfo('出错', e)
