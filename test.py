from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from tkinter import * #窗口

option = webdriver.ChromeOptions()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
browser = webdriver.Chrome(chrome_driver, chrome_options=option)
wait = WebDriverWait(browser, 10)

# 查找型号
def search(model):
    search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ballon-container > div.posting-manage > div > div > div > div:nth-child(1) > div > form > div > div:nth-child(1) > span > input')))
    search_input.send_keys(Keys.CONTROL,'a')
    search_input.send_keys(model)
    search_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ballon-container > div.posting-manage > div > div > div > div:nth-child(1) > div > form > div > div:nth-child(4) > button.next-btn.next-medium.next-btn-primary.custom-component-mr-12')))
    search_button.click()

# 修改价格
def editPice(price):
    edit_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ballon-container > div.posting-manage > div > div > div > div.next-loading.next-loading-inline.list-loading > div > div > div:nth-child(1) > div > div > div:nth-child(4) > div > button > i')))
    edit_button.click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.next-overlay-wrapper.opened > div.next-dialog.next-closeable.next-overlay-inner.posting-price-dialog > div.next-dialog-body > div > header > span')))
    price_amount_inputs = browser.find_elements_by_css_selector('body > div.next-overlay-wrapper.opened > div.next-dialog.next-closeable.next-overlay-inner.posting-price-dialog > div.next-dialog-body > div > div > div > div:nth-child(1) > div > div.next-table.next-table-medium.ladder-price-table.only-bottom-border > table > tbody input')
    for i in range(len(price_amount_inputs)):
        if i%2 == 0:
            if int(price_amount_inputs[i].get_attribute('value')) <= 1000:
                price_amount_inputs[i+1].send_keys(Keys.CONTROL,'a')
                price_amount_inputs[i+1].send_keys(price*3)
            elif int(price_amount_inputs[i].get_attribute('value')) <= 3000:
                price_amount_inputs[i+1].send_keys(Keys.CONTROL,'a')
                price_amount_inputs[i+1].send_keys(price*2)
            elif int(price_amount_inputs[i].get_attribute('value')) >= 30000:
                price_amount_inputs[i+1].send_keys(Keys.CONTROL,'a')
                price_amount_inputs[i+1].send_keys(price*1)

def main():
    #建立窗口
    root = Tk()
    root.resizable(0,0)
    Label(root,text = "型号:").grid(row = 1, column = 0)
    model=Entry(root)
    model.grid(row = 1, column = 1)
    Label(root,text = "底价:").grid(row = 2, column = 0)
    price=Entry(root)
    price.grid(row = 2, column = 1)

    model_str=''
    print_str=''

    def getText():
        model_str = model.get()
        print_str = price.get()
        search(model_str)
        editPice(int(print_str))

    Button(root, text = "执行", width=20, command=getText).grid(row = 3, column = 1)

    root.mainloop()


if __name__ == "__main__":

    main()



