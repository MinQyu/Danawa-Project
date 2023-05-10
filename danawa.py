from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tkinter import *
import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.font
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://danawa.com")
time.sleep(2)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        photo = PhotoImage(file='d.png')
        self.wm_iconphoto(False, photo)
        self.title("다나와 최저가 검색")
        self.geometry("1280x720+100+100")
        self.configure(bg='white')
        self.resizable(True, True)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=BOTH)

class StartPage(tk.Frame):
    def __init__(self, master):
        logo = tk.PhotoImage(file="logo.png")
        icon = tk.PhotoImage(file="icon.png")
        font = tk.font.Font(family="맑은 고딕", size=15)
        def Enter(event):
            Search()
        def Search(): #버튼 누를시 실행할 함수
            검색어 = str(txt.get())
            if(검색어 != ""):
                searchBox = driver.find_element(By.CLASS_NAME,"search__input")
                searchBox.click()
                time.sleep(2)
                searchBox.send_keys(검색어)
                search = driver.find_element(By.CLASS_NAME, "search__submit")
                search.click()
                Search_list()
                master.switch_frame(PageOne) #페이지 전환
            else:
                msgbox.showinfo("알림", "검색어를 입력해주세요")
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg="white", width=1280)
        label = tk.Label(self, image=logo, bd=0, bg="white")
        label.image = logo #가비지 컬렉터 삭제 방지
        label.pack(fill=X, pady=10)
        txt = tk.Entry(self, relief="groove", insertbackground="green", highlightthickness=2, highlightcolor="lightgreen", font=font)
        txt.bind("<Return>",Enter)
        txt.pack(expand=1, side="left", fill=X, padx=5)
        btn = tk.Button(self, image=icon, bd=0, bg="white", relief="solid", repeatinterval=1000, cursor="hand2", command=Search)
        btn.image = icon #가비지 컬렉터 삭제 방지
        btn.pack(side="right",padx=5)

 #리스트 초기화
product_list1=[]
product_list2=[]
product_list3=[]
product_list4=[]

def Search_list():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    goods_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')
    for v in goods_list:
        new_text = ""
        if v.find('div', class_='prod_main_info'):
            name = v.select_one('p.prod_name > a').text.strip()
            prod_info = ''  # 제품스펙
            for s in v.select('div.spec_list > a'):
                prod_info += s.text + ':'
            product_link = v.select_one('p.prod_name > a')['href']
            img_link = v.select_one('div.thumb_image > a > img').get('data-original')
        if img_link == None:
            img_link = v.select_one('div.thumb_image > a > img').get('src')
        new_text1 = new_text + "\n" + "제품명:" + name
        new_text2 = new_text + "\n" + "제품정보:" + prod_info
        new_text3 = new_text + "\n" + "제품링크:" + product_link
        new_text4 = new_text + "\n" + "이미지링크:" + img_link
        product_list1.append(new_text1)
        product_list2.append(new_text2)
        product_list3.append(new_text3)
        product_list4.append(new_text4) 
 
class PageOne(tk.Frame):
    def __init__(self, master):
        def Back():
            driver.get("https://danawa.com")
            master.switch_frame(StartPage)
            product_list1.clear()
            product_list2.clear()
            product_list3.clear()
            product_list4.clear()
        
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white', padx=50,pady=50)
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")  
        Listbox = tk.Listbox(self, bg = 'white', width = 0, height = 0, highlightthickness=3 ,highlightcolor="lightgreen",justify=LEFT, font=('맑은 고딕',12,"bold"), selectmode="extended", xscrollcommand=scrollbar.set, yscrollcommand=scrollbar.set)
        for i in range(0,a):
            Listbox.insert(i,"\n")
            Listbox.insert(i,product_list4[i])
            Listbox.insert(i,product_list3[i])
            Listbox.insert(i,product_list2[i])
            Listbox.insert(i,product_list1[i])
            Listbox.insert(i," ")

        Listbox.pack(side="left")
        scrollbar.config(command=Listbox.yview)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()
        tk.Button(self, text="이전 페이지", command=Back).pack(side="top")

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=40)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
