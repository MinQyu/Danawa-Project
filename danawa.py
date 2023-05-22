from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from tkinter import *
import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen
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
        self.resizable(False, False)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=BOTH)
#검색페이지
class StartPage(tk.Frame):
    def __init__(self, master):
        logo = tk.PhotoImage(file="logo.png")
        icon = tk.PhotoImage(file="icon.png")
        font = tk.font.Font(family="맑은 고딕", size=15)
        def Enter(event):
            Search()
        def Search(): #버튼 누를시 실행할 함수
            search_word = str(txt.get())
            if(search_word != ""):
                searchBox = driver.find_element(By.CLASS_NAME,"search__input")
                searchBox.click()
                time.sleep(0.5)
                searchBox.send_keys(search_word)
                search = driver.find_element(By.CLASS_NAME, "search__submit")
                search.click()
                time.sleep(1)
                scrolling()
                search_list()
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

product_name=[]
product_info=[]
product_link=[]
image_link=[]

def list_clear():
    product_name.clear()
    product_info.clear()
    image_link.clear()
    product_link.clear()



def scrolling():
    element=driver.find_element(By.TAG_NAME,"html")
    for i in range(30):
        element.send_keys(Keys.SPACE)
   
idx = -1

#제품 가격 크롤링 함수            
def search_list():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    goods_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')
    tmp = "";
    for v in goods_list:
        new_text = ""
        if v.find('div', class_='prod_main_info'):
            name = v.select_one('p.prod_name > a').text.strip()
            prod_info = ''  # 제품스펙
            for s in v.select('div.spec_list > a'):
                prod_info += s.text + '/'
            prod_link = v.select_one('p.prod_name > a')['href']
            img_link = v.select_one('div.thumb_image > a > img').get('data-original')
        if img_link == None:
            img_link = v.select_one('div.thumb_image > a > img').get('src')
        if name != tmp:
            product_name.append(name)
            product_info.append(prod_info)
            product_link.append(prod_link)
            image_link.append("https:"+img_link)
            tmp = name
    for i in range(len(image_link)):
        print(image_link[i])
        print('\n')
#1페이지            
class PageOne(tk.Frame):
    def __init__(self, master):
        def Back():
            driver.get("https://danawa.com")
            master.switch_frame(StartPage)
            list_clear()
        def event_for_listbox(event): 
            global idx
            w = event.widget
            idx = int(w.curselection()[0])
            URL = image_link[idx]
            u = urlopen(URL)
            raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            photo = ImageTk.PhotoImage(im)
            label = tk.Label(image=photo, bg = "white", width = 150, height = 150).place(x = 20, y = 50)
            Info_list = tk.Label(self, text=product_info[idx], height = 8, justify = LEFT ,wraplength = 560,anchor = SW, bg = "white", font=('맑은 고딕', 12, "bold")).place(x=0, y=470)
            label.image = photo
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white')
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")
        Label_img = tk.Label(self, text="이미지", anchor = NW, bg = "white", font=('맑은 고딕', 18, "bold")).place(x=0, y=0)
        Label_info = tk.Label(self, text="제품 정보", height = 5, anchor = SW, bg = "white", font=('맑은 고딕', 18, "bold")).place(x=0, y=250)
        Listbox = tk.Listbox(self, bg='white', width=70, height = 0, justify=LEFT, selectbackground="chartreuse3", highlightcolor="lightgreen", highlightthickness=2, activestyle="none", font=('맑은 고딕',12,"bold"),yscrollcommand=scrollbar.set)
        for i in range(40):
            Listbox.insert(i,product_name[i])
        Listbox.pack(side="right", fill=BOTH, padx=0)
        Listbox.bind('<<ListboxSelect>>', event_for_listbox)
        #다음 페이지로 넘어가는 함수
        def Next():
            if idx == -1:
                msgbox.showinfo("알림", "제품을 선택해주세요")
            else:
                driver.get(product_link[idx])
                master.switch_frame(PageTwo)

        tk.Button(self, text="Back", command=Back).place(x=0, y=670)
        tk.Button(self, text="Select", command=Next).place(x=50, y=670)
        scrollbar["command"]=Listbox.yview

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='red')
        tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
