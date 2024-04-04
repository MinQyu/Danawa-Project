from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from tkinter import *
from io import BytesIO
from PIL import Image, ImageTk
from urllib.request import urlopen
import subprocess
import chromedriver_autoinstaller
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


def create_window():
    newWindow = Toplevel(app)
    newWindow.title("도움말")
    tk.Label(newWindow, text = "▶ 다나와를 기반으로 쿠팡, G마켓, 옥션, 11번가의 판매 가격과 판매 페이지를 찾아주는 크롤러 프로그램입니다.", anchor="w", font=('맑은 고딕', 11)).grid(row = 0, column = 0, sticky="w", padx = 10, pady = 10)
    tk.Label(newWindow, text = "▶ 다나와에서 취급하는 모든 제품을 검색 가능하나, 되도록 전자제품 검색을 권장합니다.", anchor="w", font=('맑은 고딕', 11)).grid(row = 1, column = 0, sticky="w", padx = 10, pady = 10)
    tk.Label(newWindow, text = "▶ 식품, 잡화 등의 상품은 오픈마켓 4사의 판매가가 최저가가 아닐 확률이 높습니다.", anchor="w", font=('맑은 고딕', 11)).grid(row = 2, column = 0, sticky="w", padx = 10, pady = 10)
    def quit(newWindow):
        newWindow.destroy()

#검색페이지
class StartPage(tk.Frame):
    def __init__(self, master):
        logo = tk.PhotoImage(file="logo.png")
        icon = tk.PhotoImage(file="icon.png")
        font = tk.font.Font(family="맑은 고딕", size=15)
        def help():
            create_window()
        def Enter(event):
            Search()
        def Search(): #버튼 누를시 실행할 함수
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
                scrolling(30)
                progressbar.config(value=80)
                progressbar.update()
                search_list()
                progressbar.config(value=90)
                progressbar.update()
                master.switch_frame(PageOne) #페이지 전환
            else:
                msgbox.showinfo("알림", "검색어를 입력해주세요")
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self, bg="white")
        label = tk.Label(self, image=logo, bd=0, bg="white")
        label.image = logo #가비지 컬렉터 삭제 방지
        label.pack(fill=X, pady=10)
        txt = tk.Entry(self, relief="groove", insertbackground="green", highlightthickness=2, highlightcolor="lightgreen", font=font)
        txt.bind("<Return>",Enter)
        txt.pack(expand=1, side="left", anchor="n", fill=X, padx=5)
        label_msg = tk.Label(self, relief="groove", anchor="w", bd=1, bg="white", text="상단의 검색창에 검색어를 입력 후 Enter키를 눌러주세요", font=('맑은 고딕', 13))
        label_msg.place(x=25, y=645, width=1235)
        btn = tk.Button(self, image=icon, bd=0, bg="white", relief="solid", repeatinterval=1000, cursor="hand2", command=Search)
        btn.image = icon #가비지 컬렉터 삭제 방지
        btn.pack(side="right", anchor="n", padx=5)
        ebtn = tk.Button(self, text="help", bg="white", command=help)
        ebtn.place(x=25, y=685)
        progressbar = tkinter.ttk.Progressbar(self, mode="determinate", maximum=100, value=0)
        progressbar.place(x=460, y=685, width=800, height=25)

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


def scrolling(n):
    element=driver.find_element(By.TAG_NAME,"html")
    for i in range(n):
        element.send_keys(Keys.SPACE)


#제품 가격 크롤링 함수            
def search_list():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    goods_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')
    tmp = "";
    for v in goods_list:
        if v.find('div', class_='prod_main_info'):
            name = v.select_one('p.prod_name > a').text.strip()  
            prod_link = v.select_one('p.prod_name > a')['href']
            img_link = v.select_one('div.thumb_image > a > img').get('data-original')
            prod_info_list = v.select('div.spec_list')
            prod_info = ''
            for spec in prod_info_list:
                if spec.get_text() != '\n':
                    prod_info += spec.get_text().strip()
        if img_link == None:
            img_link = v.select_one('div.thumb_image > a > img').get('src')
        if name != tmp:
            product_name.append(name)
            product_link.append(prod_link)
            image_link.append("https:"+img_link)
            str = re.sub(r'\s+', ' ', prod_info)
            product_info.append(str)
            tmp = name

coupang_price = '/'
gmarket_price = '/'
auction_price = '/'
eleven_price = '/'
c_coupon = '/'
g_coupon = '/'
a_coupon = '/'
e_coupon = '/'
c_link = ''
g_link = ''
a_link = ''
e_link = ''

def price_clear():
    global coupang_price, gmarket_price, auction_price, eleven_price, c_coupon, g_coupon, a_coupon, e_coupon
    global c_link, g_link, a_link, e_link
    coupang_price = '/'
    gmarket_price = '/'
    auction_price = '/'
    eleven_price = '/'
    c_coupon = '/'
    g_coupon = '/'
    a_coupon = '/'
    e_coupon = '/'
    c_link = ''
    g_link = ''
    a_link = ''
    e_link = ''

def coupang_search():
    global coupang_price, c_coupon, c_link
    try:
        coupang_link = driver.find_element(By.XPATH, '//img[@alt="쿠팡"]')
        coupang_link.click()
        driver.switch_to.window(driver.window_handles[1])
    except: 
        coupang_price = "판매처가 존재하지 않습니다."
        return
    if check_dc("coupang"):
        try:
            wow = driver.find_element(By.XPATH,'//*[@id="contents"]/div/div[1]/div[3]/div[5]/div[1]/div/div[5]/div/span[2]/b').text
            tmp = wow[0:wow.find("에 구매")]
            c_coupon = "와우 회원가: "+tmp
        except:
            c_coupon = "쿠폰 적용"
        coupang_price = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[3]/div[5]/div[1]/div/div[3]/span[1]/strong').text
    else:
        price = driver.find_element(By.CLASS_NAME, 'total-price').text
        c_coupon = "쿠폰 미적용"
        coupang_price = price
    tmp = driver.current_url
    c_link = tmp[0:tmp.find("?itemId")]
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    

def gmarket_search():
    global gmarket_price, g_coupon, g_link
    class Coupon:
        def __init__(self, dc, dup):
            self.dc = dc
            self.dup = dup
    discount=0
    try:
        gmarket_link = driver.find_element(By.XPATH, '//img[@alt="G마켓"]')
        gmarket_link.click()
        driver.switch_to.window(driver.window_handles[1])
    except:
        gmarket_price = "판매처가 존재하지 않습니다."
        return
    if check_dc("gmarket"):
        g_coupon = "쿠폰 적용"
        tmp = driver.find_element(By.CLASS_NAME, 'text__ellipsis').text
        if tmp.find('%')!=-1:
            price_str = driver.find_element(By.CLASS_NAME, 'price_original').text
            price_int = int(re.sub(r'[^0-9]', '', price_str))
            link = driver.find_element(By.CLASS_NAME, 'box__coupon-inner')
            link.click()
            coupon_list = driver.find_elements(By.CSS_SELECTOR, 'body > div.js__vipci.section__iframe-vipcoupon.section__iframe-vipcoupon--active > div > div.box__coupon-content > div > ul.list__coupon > li')
            coupons = []
            for item in coupon_list:
                title_element = item.find_element(By.CLASS_NAME, 'box__coupon-title')
                detail_element = item.find_element(By.CLASS_NAME, 'button__detail')
                title_text = title_element.text.strip()
                detail_text = detail_element.text.strip()
                dc=0
                percent_off=0
                if (title_text.find('%')>0):
                    percent_off = int(title_text[:title_text.find('%')])
                    if (detail_text.find("최대")>0):
                        dc_max = get_discount(detail_text)
                        if price_int*percent_off/100 > dc_max:
                            dc = dc_max
                        else:
                            dc = round(price_int*percent_off/100)
                    else:
                        dc = round(price_int*percent_off/100)
                else:
                    dc = int(re.sub(r'[^0-9]', '', title_text))
                    if(re.search(r'만원', title_text)):
                        dc *= 10000
                    else:
                        dc *= 1000
                dup = "중복할인" in title_text
                coupon = Coupon(dc, dup)
                coupons.append(coupon)
            if len(coupons) == 1:
                discount = coupons[0].dc
            else:     
                c_max = max((coupon for coupon in coupons if hasattr(coupon, 'dc') and not coupon.dup),
                            default=Coupon(0,False), key=lambda x: getattr(x, 'dc', 0))
                c_dup_max = max((coupon for coupon in coupons if hasattr(coupon, 'dc') and coupon.dup),
                                default=Coupon(0,True), key=lambda x: getattr(x, 'dc', 0))
                discount =  c_max.dc + c_dup_max.dc
        else:
            price_str = driver.find_element(By.CLASS_NAME, 'price_real').text
            price_int = int(re.sub(r'[^0-9]', '', price_str))
            discount = get_discount(tmp)
        price_int -= discount
        gmarket_price = format(price_int,',')+'원'
        
    else:
        gmarket_price = driver.find_element(By.CLASS_NAME, 'price_real').text
        g_coupon = "쿠폰 미적용"
    tmp = driver.current_url
    g_link = tmp[0:tmp.find("&GoodsSale")]
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def get_discount(detail_text):
    detail_text = detail_text[detail_text.find("최대")+3:]
    detail_text = detail_text[:detail_text.find("원")+1]
    won = re.sub(r'[^ㄱ-ㅣ가-힣\s]','',detail_text)
    discount = int(re.sub(r'[^0-9]', '', detail_text))
    if won=="만원":
        discount *= 10000
    elif won=="천원":
        discount *= 1000
    return discount

def auction_search():
    global auction_price, a_coupon, a_link
    class Coupon:
        def __init__(self, dc, dup):
            self.dc = dc
            self.dup = dup
    discount=0
    try:
        auction_link = driver.find_element(By.XPATH, '//img[@alt="옥션"]')
        auction_link.click()
        driver.switch_to.window(driver.window_handles[1])
    except:
        auction_price = "판매처가 존재하지 않습니다."
        return
    if check_dc("auction"):
        a_coupon = "쿠폰 적용"
        tmp = driver.find_element(By.CLASS_NAME, 'text__coupon').text
        if tmp.find('%')!=-1:
            price_str = driver.find_element(By.CLASS_NAME, 'price_original').text
            price_int = int(re.sub(r'[^0-9]', '', price_str))
            link = driver.find_element(By.CLASS_NAME, 'box__text-coupon')
            link.click()
            coupon_list = driver.find_elements(By.CSS_SELECTOR, 'body > div.js__vipci.section__iframe-vipcoupon.section__iframe-vipcoupon--active > div > div.box__coupon-content > div > ul.list__coupon > li')
            coupons = []
            for item in coupon_list:
                title_element = item.find_element(By.CLASS_NAME, 'box__coupon-title')
                detail_element = item.find_element(By.CLASS_NAME, 'button__detail')
                title_text = title_element.text.strip()
                detail_text = detail_element.text.strip()
                dc=0
                percent_off=0
                if (title_text.find('%')>0):
                    percent_off = int(title_text[:title_text.find('%')])
                    if (detail_text.find("최대")>0):
                        dc_max = get_discount(detail_text)
                        if price_int*percent_off/100 > dc_max:
                            dc = dc_max
                        else:
                            dc = round(price_int*percent_off/100)
                    else:
                        dc = round(price_int*percent_off/100)
                else:
                    dc = int(re.sub(r'[^0-9]', '', title_text))
                    if(re.search(r'만원', title_text)):
                        dc *= 10000
                    else:
                        dc *= 1000
                dup = "중복할인" in title_text
                coupon = Coupon(dc, dup)
                coupons.append(coupon)
            if len(coupons) == 1:
                discount = coupons[0].dc
            else:     
                c_max = max((coupon for coupon in coupons if hasattr(coupon, 'dc') and not coupon.dup),
                            default=Coupon(0,False), key=lambda x: getattr(x, 'dc', 0))
                c_dup_max = max((coupon for coupon in coupons if hasattr(coupon, 'dc') and coupon.dup),
                                default=Coupon(0,True), key=lambda x: getattr(x, 'dc', 0))
                discount =  c_max.dc + c_dup_max.dc
        else:
            price_str = driver.find_element(By.CLASS_NAME, 'price_real').text
            price_int = int(re.sub(r'[^0-9]', '', price_str))
            discount = get_discount(tmp)
        price_int -= discount
        auction_price = round(format(price_int,','))+'원'
    else:
        auction_price = driver.find_element(By.CLASS_NAME, 'price_real').text
        a_coupon = "쿠폰 미적용"
    tmp = driver.current_url
    a_link = "http://itempage3.auction.co.kr/DetailView.aspx?itemno="+tmp[tmp.find("No=")+3:tmp.find("&frm")]
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    

def eleven_search():
    global eleven_price, e_coupon, e_link
    try:
        eleven_link = driver.find_element(By.XPATH, '//img[@alt="11번가"]')
        eleven_link.click()
        driver.switch_to.window(driver.window_handles[1])
    except:
        eleven_price = "판매처가 존재하지 않습니다"
        return
    try:
        driver.find_element(By.ID, 'loadingStop').click()
        E_link = driver.current_url
        Eleven_link = "https://www.11st.co.kr/products/"+E_link[E_link.find("link_pcode=")+11:E_link.find("&package")]
    except:
        
        E_link = driver.current_url
        Eleven_link = E_link[0:E_link.find("?service")]
    driver.get("https://www.11st.co.kr")
    
    driver.switch_to.window(driver.window_handles[1])
    driver.get(Eleven_link)
    
    try:
        price_str = driver.find_element(By.XPATH, '//*[@id="finalDscPrcArea"]/dd[2]/strong/span[1]').text
        
    except:
        try:
            price_str = driver.find_element(By.XPATH, '//*[@id="finalDscPrcArea"]/dd/strong/span[1]').text
        except:
            price_str = driver.find_element(By.XPATH, '//*[@id="layBodyWrap"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[3]/div/div/dl/div[2]/dd[2]/strong/span[1]').text
        
    element=driver.find_element(By.TAG_NAME,"html")
    element.send_keys(Keys.SPACE) #스크롤
    try:
        isCoupon = driver.find_element(By.ID, 'maxDiscountResult')
        e_coupon = '쿠폰 적용'
        price = driver.find_element(By.XPATH, '//*[@id="maxDiscountResult"]/dd[2]').text.strip()
        if not(price.find(',')): 
            price = driver.find_element(By.XPATH, '//*[@id="maxDiscountResult"]/dd[1]').text.strip()
            if not(price.find(',')): price = driver.find_element(By.XPATH, '//*[@id="finalDscPrcArea"]/dd/strong/span[1]').text
        eleven_price = re.sub("\n", "", price)
    except:
        eleven_price = price_str
    if eleven_price.find("원") < 0 : eleven_price+="원"
    eleven_price = eleven_price[0:eleven_price.find("원")+1]
    e_link = Eleven_link
    driver.close()
    
    driver.switch_to.window(driver.window_handles[0])
    

def check_dc(market):
    if market == "coupang":
        name = 'applied-coupon__label'
    elif market == "gmarket":
        name = 'text__ellipsis'
    elif market == "auction":
        name = 'text__coupon'
    try:
        driver.find_element(By.CLASS_NAME, name)
        
        return True
    except:
        return False

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
                progressbar.config(value=10)
                progressbar.update()
                driver.get(product_link[idx])
                coupang_search()
                progressbar.config(value=30)
                progressbar.update()
                gmarket_search()
                progressbar.config(value=50)
                progressbar.update()
                auction_search()
                progressbar.config(value=80)
                progressbar.update()
                eleven_search()
                master.switch_frame(PageTwo) 
        def event_for_listbox(event): #리스트박스 항목 클릭시
            global idx
            w = event.widget
            idx = int(w.curselection()[0])
            label_info.config(text=product_info[idx])
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
        tk.Label(self, text="제품 정보", anchor = W, bg = "white", font=('맑은 고딕', 15, "bold")).place(x=7, y=315)
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
            for i in range(len(product_name)-1):
                Listbox.insert(i,product_name[i])
        else:
            for i in range(39):
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
        global idx, c_link, g_link, a_link, e_link
        img_c = PhotoImage(file='coupang.png')
        img_g = PhotoImage(file='gmarket.png')
        img_a = PhotoImage(file='auction.png')
        img_e = PhotoImage(file='eleven.png')
        def go_first(): #처음 페이지
            idx = -1
            price_clear()
            list_clear()
            master.switch_frame(StartPage)
            driver.get("https://danawa.com")
        def link_open(l):
            if l == 'c' and c_link!='':
                driver.get(c_link)
                driver.maximize_window()
            elif l == 'g' and g_link!='':
                driver.get(g_link)
                driver.maximize_window()
            elif l == 'a' and a_link!='':
                driver.get(a_link)
                driver.maximize_window()
            elif l == 'e' and e_link!='':
                driver.get(e_link)
                driver.maximize_window()
            else:
                msgbox.showinfo("알림", "판매처가 존재하지 않습니다")
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
        label_g.place(x=60, y=425)
        label_a.place(x=60, y=520)
        label_e.place(x=60, y=600)
        label_c_coupon = tk.Label(self, bg="white", text=c_coupon, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_c_price = tk.Label(self, bg="white", text=coupang_price, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_g_coupon = tk.Label(self, bg="white", text=g_coupon, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_g_price = tk.Label(self, bg="white", text=gmarket_price, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_a_coupon = tk.Label(self, bg="white", text=a_coupon, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_a_price = tk.Label(self, bg="white", text=auction_price.replace("판매가","").strip(), height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_e_coupon = tk.Label(self, bg="white", text=e_coupon, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_e_price = tk.Label(self, bg="white", text=eleven_price, height=1, width=35, highlightthickness=2, highlightbackground="lightgreen", relief="groove", font=('맑은 고딕', 13))
        label_c_coupon.place(x=350, y=340)
        label_c_price.place(x=750, y=340)
        label_g_coupon.place(x=350, y=430)
        label_g_price.place(x=750, y=430)
        label_a_coupon.place(x=350, y=520)
        label_a_price.place(x=750, y=520)
        label_e_coupon.place(x=350, y=610)
        label_e_price.place(x=750, y=610)        
        label_img.place(x=50, y=50)
        label_info.place(x=350, y=80)
        button_c = tk.Button(self, text="구매링크", bg="white", command=lambda:link_open('c'))
        button_g = tk.Button(self, text="구매링크", bg="white", command=lambda:link_open('g'))
        button_a = tk.Button(self, text="구매링크", bg="white", command=lambda:link_open('a'))
        button_e = tk.Button(self, text="구매링크", bg="white", command=lambda:link_open('e'))
        button_c.place(x=1150, y=340)
        button_g.place(x=1150, y=430)
        button_a.place(x=1150, y=520)
        button_e.place(x=1150, y=610)   
        tk.Label(self, text=product_name[idx], anchor = W, bg = "white", font=('맑은 고딕', 17, "bold")).place(x=30, y=15)
        button = tk.Button(self, text="first page", bg="white", command=go_first)
        button.place(x=25, y=685)

if __name__ == "__main__":
    #봇 탐지 우회를 위한 디버거 크롬 실행
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('headless')
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    driver = webdriver.Chrome(f'./123/chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(5)
    driver.get("https://danawa.com")
    app = App()
    app.mainloop()


'''
#셀레니움 4.10.0 버전 이후
if __name__ == "__main__":  
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    driver.get("https://danawa.com")
    app = App()
    app.mainloop()
'''