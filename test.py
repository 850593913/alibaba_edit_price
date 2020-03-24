from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tkinter import * #窗口
from tkinter.filedialog import askdirectory #选择文件夹
from tkinter.filedialog import askopenfilename #选择文件

# option = webdriver.ChromeOptions()
# option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# chrome_driver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
# browser = webdriver.Chrome(chrome_driver, chrome_options=option)
# wait = WebDriverWait(browser, 10)

def getText():
    tex


if __name__ == "__main__":
    # model=StringVar()
    # price=StringVar()
    #建立窗口
    root = Tk()
    root.resizable(0,0)
    Label(root,text = "型号:").grid(row = 1, column = 0)
    text_1 = Entry(root, textvariable = 'model').grid(row = 1, column = 1)
    Label(root,text = "底价:").grid(row = 2, column = 0)
    text_2 = Entry(root, textvariable = 'price').grid(row = 2, column = 1)
    Button(root, text = "执行", width=20, command=getText).grid(row = 3, column = 1)

    root.mainloop()

    prin


