from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.simpledialog import askstring
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen
import tkinter as tk
import tkinter.ttk
import tkinter.messagebox as msgbox
import tkinter.font
import time
import re


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        photo = PhotoImage(file='d.png')
        self.wm_iconphoto(False, photo)
        self.title("다나와 최저가 검색")
        self.geometry("1280x720")
        self.configure(bg='white')
        self.resizable(False, False)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=1, fill=BOTH)

eID = ''
ePW = ''
login = 0
def login_eleven():
    global eID, ePW, login
    driver.get('https://www.11st.co.kr')
    button = driver.find_element(By.XPATH,'//*[@id="gnb"]/div/div[3]/div/div[2]/div[1]/a[1]')
    button.click()
    id = driver.find_element(By.ID, 'memID')
    pw = driver.find_element(By.ID, 'memPwd')
    id.click()
    id.send_keys(eID)
    pw.click()
    pw.send_keys(ePW)
    if driver.find_element(By.CLASS_NAME, 'c-error__message'):
        login = 0
        driver.get("https://danawa.com")
    else:
        driver.find_element(By.ID, 'btnSpLoginNotToday').click
        login = 1
        driver.get("https://danawa.com")


#검색페이지
class StartPage(tk.Frame):
    global eID, ePW, login
    def __init__(self, master):
        logo = tk.PhotoImage(file="logo.png")
        icon = tk.PhotoImage(file="icon.png")
        font = tk.font.Font(family="맑은 고딕", size=15)
        def Enter(event):
            Search()
        def Search(): #버튼 누를시 실행할 함수
            if login != 1:
                go = tk.messagebox.askyesno("알림","11번가 로그인이 완료되지 않았습니다."+"\n"+"계속 진행하시겠습니까?")
            if go == False:
                exit()
            search_word = str(txt.get())
            if(search_word != ""):
                progressbar.config(value=10)
                progressbar.update()
                searchBox = driver.find_element(By.CLASS_NAME,"search__input")
                searchBox.click()
                time.sleep(0.5)
                searchBox.send_keys(search_word)
                search = driver.find_element(By.CLASS_NAME, "search__submit")
                search.click()
                progressbar.config(value=20)
                progressbar.update()
                time.sleep(1)
                progressbar.config(value=30)
                progressbar.update()
                scrolling()
                progressbar.config(value=80)
                progressbar.update()
                search_list()
                progressbar.config(value=90)
                progressbar.update()
                master.switch_frame(PageOne) #페이지 전환
            else:
                msgbox.showinfo("알림", "검색어를 입력해주세요")
        def get_id():
            eID = askstring(title="11번가 아이디 입력", prompt="11번가 아이디를 입력해주세요")
            if eID != '':
                ePW = askstring(title="11번가 비밀번호", prompt="11번가 비밀번호를 입력해주세요")
            login_eleven()
            if login != 1:
               msgbox.showinfo("알림", "로그인 정보가 틀립니다. 다시 시도해주세요")
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg="white")
        label = tk.Label(self, image=logo, bd=0, bg="white")
        label.image = logo #가비지 컬렉터 삭제 방지
        label.pack(fill=X, pady=10)
        txt = tk.Entry(self, relief="groove", insertbackground="green", highlightthickness=2, highlightcolor="lightgreen", font=font)
        txt.bind("<Return>",Enter)
        txt.pack(expand=1, side="left", anchor="n", fill=X, padx=5)
        btn = tk.Button(self, image=icon, bd=0, bg="white", relief="solid", repeatinterval=1000, cursor="hand2", command=Search)
        btn.image = icon #가비지 컬렉터 삭제 방지
        btn.pack(side="right", anchor="n", padx=5)
        tk.Button(self, text="11st login", bg="white", command=get_id).place(x=25, y=685)
        progressbar = tkinter.ttk.Progressbar(self, mode="determinate", maximum=100, value=0)
        progressbar.place(x=460, y=685, width=800, height=25)
        msgbox.showinfo("알림", "11번가 쿠폰 정보를 불러오기 위해서는 로그인이 필요합니다. 하단의 버튼을 눌러 로그인 정보를 입력해주세요")


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
    tmp = "";
    for v in goods_list:
        new_text = ""
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
    
coupang_price = '/'
gmarket_price = '/'
auction_price = '/'
eleven_price = '/'
c_coupon = '/'
g_coupon = '/'
a_coupon = '/'
e_coupon = '/'

def price_clear():
    global coupang_price, gmarket_price, auction_price, eleven_price, c_coupon, g_coupon, a_coupon, e_coupon 
    coupang_price = '/'
    gmarket_price = '/'
    auction_price = '/'
    eleven_price = '/'
    c_coupon = '/'
    g_coupon = '/'
    a_coupon = '/'
    e_coupon = '/'

def coupang_search():
    global coupang_price, c_coupon
    try:
        coupang_link = driver.find_element(By.XPATH, '//img[@alt="쿠팡"]')
        coupang_link.click()
        driver.implicitly_wait(1)
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(4)
    except: 
        coupang_price = "판매처가 존재하지 않습니다."
        return
    if check_dc("coupang"):
        dc_price = driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[3]/span[1]/strong').text
        c_coupon = "와우 회원만 쿠폰 적용 가능"
        coupang_price = dc_price
    else:
        price = driver.find_element(By.CLASS_NAME, 'total-price').text
        c_coupon = "쿠폰 미적용"
        coupang_price = price
    driver.close()
    driver.implicitly_wait(1.5)
    driver.switch_to.window(driver.window_handles[0])
    driver.implicitly_wait(1.5)


def gmarket_search():
    global gmarket_price, g_coupon
    discount=0
    try:
        gmarket_link = driver.find_element(By.XPATH, '//img[@alt="G마켓"]')
        gmarket_link.click()
        driver.switch_to.window(driver.window_handles[1])
        driver.implicitly_wait(3)
    except:
        gmarket_price = "판매처가 존재하지 않습니다."
        return
    price_str = driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/div/div[4]/span[2]/strong').text
    price_int = int(re.sub(r'[^0-9]', '', price_str))
    if check_dc("gmarket"):
        g_coupon = "쿠폰 적용 가능"
        tmp = driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/button/span[1]/span/em').text
        if tmp.find('%'):
            dc_percentage = int(re.sub(r'[^0-9]', '', tmp))
            link = driver.find_element(By.XPATH, '//*[@id="itemcase_basic"]/button/span[2]')
            link.click()
            driver.implicitly_wait(1)
            tmp_str = driver.find_element(By.XPATH, '/html/body/div[30]/div/div[3]/div/ul[1]/li/div/div[1]/button').text
            tmp_str.strip()
            tmp_str = tmp_str[tmp_str.find("최대")+3:]
            tmp_str = tmp_str[:tmp_str.find("원")+1]
            won = re.sub(r'[^ㄱ-ㅣ가-힣\s]',"",tmp_str)
            dc_max = int(re.sub(r'[^0-9]', '', tmp_str))
            if won=="만원":
                dc_max *= 10000
            elif won=="천원":
                dc_max *= 1000
            if price_int*dc_percentage/100 > dc_max:
                price_int -= dc_max
            else:
                price_int*=(100-dc_percentage)/100
        else:
            won = re.sub(r'[^ㄱ-ㅣ가-힣\s]',"",tmp)
            discount = int(re.sub(r'[^0-9]', '', tmp))
            if won=="만원":
                discount *= 10000
            elif won=="천원":
                discount *= 1000
        price_int-=discount
        gmarket_price = format(price_int,',')+'원'
    else: 
        gmarket_price = price_str
        g_coupon = "쿠폰 미적용"
    driver.close()
    driver.implicitly_wait(1)
    driver.switch_to.window(driver.window_handles[0])
    driver.implicitly_wait(1)

def auction_search():
    global auction_price, a_coupon
    discount=0
    try:
        auction_link = driver.find_element(By.XPATH, '//img[@alt="옥션"]')
        auction_link.click()
        driver.implicitly_wait(3)
        driver.switch_to.window(driver.window_handles[1])
    except:
        auction_price = "판매처가 존재하지 않습니다."
        return
    price_str = driver.find_element(By.CLASS_NAME, 'price_real').text
    price_int = int(re.sub(r'[^0-9]', '', price_str))
    if check_dc("auction"):
        a_coupon = "쿠폰 적용 가능"
        tmp = driver.find_element(By.XPATH,'//*[@id="frmMain"]/div[5]/a/span[1]').text
        if tmp.find('%'):
            dc_percentage = int(re.sub(r'[^0-9]', '', tmp))
            link = driver.find_element(By.XPATH,'//*[@id="frmMain"]/div[5]/a/span[2]/span[1]')
            link.click()
            driver.implicitly_wait(1)
            tmp_str = driver.find_element(By.XPATH, '/html/body/div[43]/div/div[3]/div/ul[1]/li/div/div[1]/button').text
            tmp_str.strip()
            tmp_str = tmp_str[tmp_str.find("최대")+3:]
            tmp_str = tmp_str[:tmp_str.find("원")+1]
            won = re.sub(r'[^ㄱ-ㅣ가-힣\s]',"",tmp_str)
            dc_max = int(re.sub(r'[^0-9]', '', tmp_str))
            if won=="만원":
                dc_max *= 10000
            elif won=="천원":
                dc_max *= 1000
            if price_int*dc_percentage/100 > dc_max:
                price_int -= dc_max
            else:
                price_int*=(100-dc_percentage)/100
        price_int-=discount
        auction_price = format(price_int,',')+'원'
    else: 
        auction_price = price_str
        a_coupon = "쿠폰 미적용"
    driver.close()
    driver.implicitly_wait(1)
    driver.switch_to.window(driver.window_handles[0])
    driver.implicitly_wait(1)


def eleven_search():
    global eleven_price, e_coupon, eID, ePW, login
    cp_list = []
    discount=0
    try:
        eleven_link = driver.find_element(By.XPATH, '//img[@alt="11번가"]')
        eleven_link.click()
        driver.implicitly_wait(3)
        driver.switch_to.window(driver.window_handles[1])
    except:
        eleven_price = "판매처가 존재하지 않습니다"
        print("제품이 존재하지 않습니다.")
        return
    price_str = driver.find_element(By.CLASS_NAME, 'value')
    isCoupon = driver.find_element(By.XPATH, '//*[@id="couponDownButton"]')
    if isCoupon.text == "쿠폰받기" and login:
        link = driver.find_element(By.XPATH,'//*[@id="couponDownButton"]')
        if link.text == '쿠폰받기': 
            link.click()
            driver.implicitly_wait(1)
            id = driver.find_element(By.ID, 'memID')
            pw = driver.find_element(By.ID, 'memPwd')
            id.click()
            id.send_keys(eID)
            pw.click()
            pw.send_keys(ePW)
            if driver.find_element(By.CLASS_NAME, 'c-error__message'):
                e_coupon = "로그인에 실패했습니다."
                return
            else:
                button = driver.find_element(By.XPATH,'//*[@id="arModalQuickInfo"]/div/div/div[4]/button')
                button.click()
                button2 = driver.find_element(By.XPATH,'//*[@id="arModalAddAccount"]/div[2]/button')
                button2.click()
                cp = driver.find_element(By.XPATH,'//*[@id="couponDownButton"]')
                cp.click()
                cp_list = driver.find_elements(By.XPATH,'//*[@id="couponCont"]/div/section[2]/ul')
                print(cp_list[0].text, cp_list[1].text)
        else:
            return
        eleven_price = price_str







def check_dc(market):
    if market == "coupang":
        xpath = '//*[@id="contents"]/div[1]/div/div[3]/div[5]/div[1]/div/div[3]/span[1]/strong'
    elif market == "gmarket":
        xpath = '//*[@id="itemcase_basic"]/button/span[1]/span'
    elif market == "auction":
        xpath = '//*[@id="frmMain"]/div[5]/a/span[2]'

    try:
        driver.find_element(By.XPATH, xpath)
        driver.implicitly_wait(2)
        return True
    except:
        return False

#1페이지            
class PageOne(tk.Frame):
    global eID, ePW, login
    def __init__(self, master):
        def Back(): #이전 페이지
            driver.get("https://danawa.com")
            master.switch_frame(StartPage)
            list_clear()
        def Next():#다음 페이지로 넘어가는 함수
            if idx == -1:
                msgbox.showinfo("알림", "제품을 선택해주세요")
            else:
                if login != 1:
                    get_id()
                #제품 선택 시 4사 마켓의 제품가격, 쿠폰 적용 여부, 실제 가격 확인
                progressbar.config(value=10)
                progressbar.update()
                driver.get(product_link[idx])
                coupang_search()
                driver.implicitly_wait(1)
                progressbar.config(value=30)
                progressbar.update()
                gmarket_search()
                driver.implicitly_wait(1)
                progressbar.config(value=50)
                progressbar.update()
                auction_search()
                driver.implicitly_wait(1)
                progressbar.config(value=80)
                progressbar.update()
                eleven_search()
                driver.implicitly_wait(1)
                if login == 0:
                    get_id()
                    eleven_search()
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
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg='white')
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")
        tk.Label(self, text="이미지", anchor = W, bg = "white", font=('맑은 고딕', 15, "bold")).place(x=7, y=10)
        tk.Label(self, text="제품 정보", anchor = SW, bg = "white", font=('맑은 고딕', 15, "bold")).place(x=7, y=315)
        tk.Label(self, text="제품 목록", anchor = W, bg = "white", font=('맑은 고딕', 15, "bold")).place(x=637, y=10)
        label_info= tk.Label(self, text="상품을 선택 후 select 버튼을 눌러주세요", height = 15, width = 68, highlightthickness=2, highlightbackground="lightgreen",
                             relief="groove", justify = LEFT ,wraplength = 600, anchor = NW, bg = "white", font=('맑은 고딕', 12))
        label_info.place(x=7, y=350)
        label_img = tk.Label(self, bg = "white")
        label_img.place(x = 202, y = 60)
        Listbox = tk.Listbox(self, bg='white', width=68, height = 0, justify=LEFT, selectbackground="chartreuse3",
                             relief="groove", highlightbackground="lightgreen", highlightcolor="lightgreen", highlightthickness=2, activestyle="none",
                             font=('맑은 고딕',12),yscrollcommand=scrollbar.set)
        if len(product_name)<40: #검색 결과가 40개 미만인 경우
            for i in range(len(product_name)):
                Listbox.insert(i,product_name[i])
        else:
            for i in range(40):
                Listbox.insert(i,product_name[i])
        Listbox.pack(side="right", fill=BOTH, padx=5, pady=45)
        tk.Button(self, text="Back", bg="white", command=Back).place(x=25, y=685)
        tk.Button(self, text="Select", bg="white", command=Next).place(x=85, y=685)
        Listbox.bind('<<ListboxSelect>>', event_for_listbox)
        progressbar = tkinter.ttk.Progressbar(self, mode="determinate", maximum=100, value=0)
        progressbar.place(x=460, y=685, width=800, height=25)
        scrollbar["command"]=Listbox.yview


class PageTwo(tk.Frame):
    def __init__(self, master):
        global idx
        img_c = PhotoImage(file='coupang.png')
        img_g = PhotoImage(file='gmarket.png')
        img_a = PhotoImage(file='auction.png')
        img_e = PhotoImage(file='eleven.png')
        def go_first(): #이전 페이지
            idx = -1
            price_clear()
            list_clear()
            master.switch_frame(StartPage)
            driver.get("https://danawa.com")
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg="white")
        label_img = tk.Label(self, bg="white")
        url = driver.find_element(By.CSS_SELECTOR,'#baseImage').get_attribute("src")
        u = urlopen(url)
        raw_data = u.read()
        u.close()
        img = Image.open(BytesIO(raw_data))
        img_resize = img.resize((250,250))
        photo = ImageTk.PhotoImage(img_resize)
        label_img.config(image=photo)
        label_img.image = photo
        info = driver.find_element(By.CLASS_NAME, 'items').text
        label_info = tk.Label(self, text=info, height=9, width=75, highlightthickness=2, highlightbackground="lightgreen",
                             relief="groove", justify = LEFT ,wraplength = 600, anchor = NW, bg = "white", font=('맑은 고딕', 13))
        label_c = tk.Label(self, bg="white", image=img_c)
        label_g = tk.Label(self, bg="white", image=img_g)
        label_a = tk.Label(self, bg="white", image=img_a)
        label_e = tk.Label(self, bg="white", image=img_e)
        label_c.image = img_c
        label_g.image = img_g
        label_a.image = img_a
        label_e.image = img_e
        label_c.place(x=60, y=340)
        label_g.place(x=60, y=430)
        label_a.place(x=60, y=525)
        label_e.place(x=60, y=610)
        label_c_coupon = tk.Label(self, bg="white", text=c_coupon, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_c_price = tk.Label(self, bg="white", text=coupang_price, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_g_coupon = tk.Label(self, bg="white", text=g_coupon, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_g_price = tk.Label(self, bg="white", text=gmarket_price, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_a_coupon = tk.Label(self, bg="white", text=a_coupon, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_a_price = tk.Label(self, bg="white", text=auction_price, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_e_coupon = tk.Label(self, bg="white", text=e_coupon, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_e_price = tk.Label(self, bg="white", text=eleven_price, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_c_coupon.place(x=350, y=340)
        label_c_price.place(x=750, y=340)
        label_g_coupon.place(x=350, y=430)
        label_g_price.place(x=750, y=430)
        label_a_coupon.place(x=350, y=525)
        label_a_price.place(x=750, y=525)
        label_e_coupon.place(x=350, y=610)
        label_e_price.place(x=750, y=610)        
        label_img.place(x=50, y=50)
        label_info.place(x=350, y=80)
        tk.Label(self, text=product_name[idx], anchor = W, bg = "white", font=('맑은 고딕', 17, "bold")).place(x=30, y=15)
        button = tk.Button(self, text="first page", bg="white", command=go_first)
        button.place(x=25, y=685)

if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    #chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)
    # 11번가 즐겨찾기
    driver.get('https://www.11st.co.kr')
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('d').perform()
    driver.implicitly_wait(1)
    driver.get("https://danawa.com")
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('d').perform()
    app = App()
    app.mainloop()

