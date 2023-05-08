from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tkinter import *
import tkinter as tk
import tkinter.font
import time



chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://danawa.com")
time.sleep(2)
'''
window = Tk()
window.title("다나와 최저가 검색")
window.geometry("1280x720+100+100")
window.configure(bg='white')
window.resizable(False, False)
'''



'''
image=PhotoImage(file="logo.png")
font = tkinter.font.Font(family="맑은 고딕", size=15)


lbl = Label(window, image=image, bd=0)
lbl.pack(pady=10)

txt = Entry(window, relief="groove", insertbackground="green", highlightthickness=2, highlightcolor="lightgreen", font=font)
txt.pack(fill=X, padx=10)

btn = Button(window, text="검색", font=font, cursor="hand2")
btn.config(command=Search)
btn.pack(pady=10)


window.mainloop()
'''

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("다나와 최저가 검색")
        self.geometry("1280x720+100+100")
        self.configure(bg='white')
        self.resizable(False, False)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        def Search(): #버튼 누를시 실행할 함수
            검색어 = txt.get()
            searchBox = driver.find_element(By.CLASS_NAME,"search__input")
            searchBox.click()
            time.sleep(2)
            searchBox.send_keys(검색어)
            search = driver.find_element(By.CLASS_NAME, "search__submit")
            search.click()
            Search_list()

        tk.Frame.__init__(self, master)
        tk.Label(self, image = PhotoImage(file="logo.png")).pack(pady=10)
        txt = tk.Entry(self, relief="groove", insertbackground="green", highlightthickness=2, highlightcolor="lightgreen")
        txt.pack(fill=X, padx=10)
        tk.Button(self, text="검색", cursor="hand2", command=Search).pack(pady=10)
        tk.Button(self, text="Go to page one",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Go to page two",
                  command=lambda: master.switch_frame(PageTwo)).pack()


def Search_list():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    goods_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')
    for v in goods_list:
        new_text = ""
        if v.find('div', class_='prod_main_info'):
            name = v.select_one('p.prod_name > a').text.strip()
            prod_info = ''  # 제품스펙
            for s in v.select('div.spec_list > a'):
                prod_info += s.text + '/'
            product_link = v.select_one('p.prod_name > a')['href']
            img_link = v.select_one('div.thumb_image > a > img').get('data-original')
        if img_link == None:
            img_link = v.select_one('div.thumb_image > a > img').get('src')
            new_text = new_text + "\n" + "제품명:" + name + "\n" + "제품 정보:" + prod_info + "\n" + "이미지 링크:" + img_link + "\n" + "제품 링크:" + product_link + "\n"
        print(new_text)

class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='blue')
        tk.Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()














