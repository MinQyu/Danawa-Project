from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from tkinter import *
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen
import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.font
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
#상품 찾는 페이지, 찾은 상품의 가격 페이지 2개
driver = webdriver.Chrome(options=chrome_options) 
Price_driver = webdriver.Chrome(options=chrome_options)  
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

    def switch_frame(self, frame_class): #페이지 전환 함수
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

#상품 정보 리스트 초기화
product_name=[]
product_info=[]
product_link=[]
image_link=[]
idx = -1 # 리스트박스 인덱스

def list_clear():
    global idx
    product_name.clear()
    product_info.clear()
    image_link.clear()
    product_link.clear()
    idx = -1

def scrolling():
    element=driver.find_element(By.TAG_NAME,"html")
    for i in range(30):
        element.send_keys(Keys.SPACE)

#제품 가격 크롤링 함수            
def search_list():
    global product_info
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    goods_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')
    tmp = ""
    for v in goods_list:
        if v.find('div', class_='prod_main_info'):
            name = v.select_one('p.prod_name > a').text.strip()  
            prod_link = v.select_one('p.prod_name > a')['href']
            img_link = v.select_one('div.thumb_image > a > img').get('data-original')
        if img_link == None:
            img_link = v.select_one('div.thumb_image > a > img').get('src')
        if name != tmp:
            product_name.append(name)
            product_link.append(prod_link)
            image_link.append("https:"+img_link)
            tmp = name
    product_info = driver.find_elements(By.CLASS_NAME, "spec_list")



#1페이지            
class PageOne(tk.Frame):
    def __init__(self, master):
        def Back(): #이전 페이지
            driver.get("https://danawa.com")
            master.switch_frame(StartPage)
            list_clear()
            


        def Next():#다음 페이지로 넘어가는 함수
            if idx == -1:
                msgbox.showinfo("알림", "제품을 선택해주세요")
            else:
                #제품 선택 시 4사 마켓의 제품가격, 쿠폰 적용 여부, 실제 가격 확인
                driver.get(product_link[idx])
                CoupangSearch()
                driver.implicitly_wait(10)
                EleSearch()
                driver.implicitly_wait(10)
                GmarketSearch()
                driver.implicitly_wait(10)
                AuctionSearch()
                driver.implicitly_wait(10)
                master.switch_frame(PageTwo)



        def event_for_listbox(event): #리스트박스 항목 클릭시
            global idx
            w = event.widget
            idx = int(w.curselection()[0])
            label_info.config(text=product_info[idx].text)
            u = urlopen(image_link[idx])
            raw_data = u.read()
            u.close()
            img = Image.open(BytesIO(raw_data))
            img_resize = img.resize((200,200))
            photo = ImageTk.PhotoImage(img_resize)
            label_img.config(image=photo)
            label_img.image = photo #가비지 컬렉터 삭제 방지

        #4사 마켓 가격 크롤링 함수 
        def CoupangSearch(): 
            driver.implicitly_wait(10)
            Cou_number = Coupang_number()
            if Cou_number == None: #해당마켓에 상품 존재하지 않을 시 함수 종료
                return  
            driver.implicitly_wait(10)
            Cou_site = "https://www.coupang.com/vp/products/" + Cou_number
            Price_driver.get(Cou_site)
            driver.implicitly_wait(10)
            Cou_price = Price_driver.find_element(By.CLASS_NAME, "total-price").text
            try: 
                Cou_discountprice = Price_driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[3]/span[1]/strong').text
                print("쿠폰 적용 여부: 와우 회원만 쿠폰 적용 가능")
                print("실제 가격: " + Cou_discountprice)
            except NoSuchElementException: 
               print("쿠폰 적용 여부: X")
               print("실제 가격: " + Cou_price)
        def EleSearch(): 
            driver.implicitly_wait(10)
            E_number = Ele_number()
            if E_number == None:
                return
            driver.implicitly_wait(10)
            E_site = "https://www.11st.co.kr/products/" + E_number
            Price_driver.get(E_site)
            driver.implicitly_wait(10)
            try:
                Ele_discount = Price_driver.find_element(By.CLASS_NAME,'price_modiscount').text
                Ele_discountprice = Price_driver.find_element(By.XPATH, '//*[@id="layBodyWrap"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div/div/ul/li/dl[1]/dd/strong/span[1]').text
                print("쿠폰 적용 여부: " + Ele_discount)
                print("실제 가격: " + Ele_discountprice + "원")
            except NoSuchElementException:                                  
                Ele_price = Price_driver.find_element(By.XPATH, '//*[@id="layBodyWrap"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[2]/div/div/ul/li/dl/dd/strong/span[1]').text
                print("쿠폰 적용 여부: x")
                print("실제 가격: " + Ele_price)    

        def GmarketSearch(): 
            driver.implicitly_wait(10)
            Gmk_number = Gmarket_number()
            if Gmk_number == None:
                return
            driver.implicitly_wait(10)
            G_site = "https://item.gmarket.co.kr/Item?goodscode=" + Gmk_number
            Price_driver.get(G_site)
            driver.implicitly_wait(10)

        def AuctionSearch(): 
            driver.implicitly_wait(10)
            Auc_number = Auction_number()
            if Auc_number == None:
                return
            driver.implicitly_wait(10)
            Auc_site = "http://itempage3.auction.co.kr/DetailView.aspx?itemno=" + Auc_number
            Price_driver.get(Auc_site)
            driver.implicitly_wait(10)



        #4사 마켓 상품 번호 크롤링 함수
        def Gmarket_number():
            try: 
                Gmarket_link = driver.find_element(By.XPATH, '//img[@alt="G마켓"]')
                Gmarket_link.click()
            except NoSuchElementException: 
                print("제품이 존재하지 않습니다.")
            else:
                driver.switch_to.window(driver.window_handles[1])
                driver.implicitly_wait(10)
                Gmarket_url = driver.current_url
                First_index= Gmarket_url.find("link_pcode")
                Last_index = Gmarket_url.find("&package")
                driver.implicitly_wait(10)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.implicitly_wait(10)
                Gmarket_prodnumber = Gmarket_url[First_index+len("link_pcode")+1:Last_index]
                return Gmarket_prodnumber

        def Auction_number():
            try: 
                Auction_link = driver.find_element(By.XPATH, '//img[@alt="옥션"]')
                Auction_link.click()
            except NoSuchElementException: 
                print("제품이 존재하지 않습니다.")
            else:
                driver.switch_to.window(driver.window_handles[1])
                driver.implicitly_wait(10)
                Auction_url = driver.current_url
                First_index= Auction_url.find("link_pcode")
                Last_index = Auction_url.find("&package")
                driver.implicitly_wait(10)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.implicitly_wait(10)
                Auction_prodnumber = Auction_url[First_index+len("link_pcode")+1:Last_index]
                return Auction_prodnumber

        #쿠팡 상품 정보 크롤링
        def Coupang_number():
            try: 
                Coupang_link = driver.find_element(By.XPATH, '//img[@alt="쿠팡"]')
                Coupang_link.click()
            except NoSuchElementException: 
                print("제품이 존재하지 않습니다.")
            else:
                time.sleep(8)
                driver.switch_to.window(driver.window_handles[1])
                Coupang_url = driver.current_url
                First_index= Coupang_url.find("products/")
                Last_index = Coupang_url.find("?")
                driver.implicitly_wait(10)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.implicitly_wait(10)
                Coupang_prodnumber = Coupang_url[First_index +len("products/"):Last_index]
                return Coupang_prodnumber
            
        def Ele_number():
            try: 
                Ele_link = driver.find_element(By.XPATH, '//img[@alt="11번가"]')
                Ele_link.click()
            except NoSuchElementException: 
                print("제품이 존재하지 않습니다.")
            else:
                time.sleep(3)
                driver.switch_to.window(driver.window_handles[1])
                driver.implicitly_wait(10)
                Ele_url = driver.current_url
                First_index= Ele_url.find("link_pcode")
                Last_index = Ele_url.find("&package") 
                driver.implicitly_wait(10)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.implicitly_wait(10)
                Ele_pronumber = Ele_url[First_index+len("link_pcode")+1:Last_index]
                return Ele_pronumber    
            


        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='white')
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")
        tk.Label(self, text="이미지", anchor = NW, bg = "white", font=('맑은 고딕', 15, "bold")).place(x=5, y=0)
        tk.Label(self, text="제품 정보", anchor = SW, bg = "white", font=('맑은 고딕', 15, "bold")).place(x=5, y=320)
        label_info= tk.Label(self, text="상품을 선택 후 select 버튼을 눌러주세요", height = 15, width = 60, highlightthickness=2, highlightbackground="lightgreen",
                             relief="groove", justify = LEFT ,wraplength = 600, anchor = NW, bg = "white", font=('맑은 고딕', 12, "bold"))
        label_info.place(x=5, y=350)
        label_img = tk.Label(self, bg = "white")
        label_img.place(x = 200, y = 60)
        Listbox = tk.Listbox(self, bg='white', width=70, height = 0, justify=LEFT, selectbackground="chartreuse3",
                             highlightbackground="lightgreen", highlightcolor="lightgreen", highlightthickness=2, activestyle="none", font=('맑은 고딕',12,"bold"),yscrollcommand=scrollbar.set)
        for i in range(40):
            Listbox.insert(i,product_name[i])
        Listbox.pack(side="right", fill=BOTH, padx=0)
        Listbox.bind('<<ListboxSelect>>', event_for_listbox)
        tk.Button(self, text="Back", command=Back).place(x=25, y=685)
        tk.Button(self, text="Select", command=Next).place(x=85, y=685)
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
