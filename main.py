from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tkinter import *
from bs4 import BeautifulSoup
import tkinter.font
import time



options = Options()
options.add_argument('headless');  # headless는 화면이나 페이지 이동을 표시하지 않고 동작하는 모드
# webdirver 설정(Chrome, Firefox 등)
driver = webdriver.Chrome(options=options)  # 브라우저 창 안보이기
#driver = webdriver.Chrome() # 브라우저 창 보이기

driver.get("https://danawa.com")
time.sleep(2)

searchBox = driver.find_element(By.CLASS_NAME,"search__input")
searchBox.click()
searchBox.send_keys("레노버")
time.sleep(2)
search = driver.find_element(By.CLASS_NAME, "search__submit")
search.click()
soup = BeautifulSoup(driver.page_source, 'html.parser')


goods_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')

# 상품 리스트 확인
# print(goods_list)

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



# 브라우저 종료
driver.close()

'''
window = Tk()
window.title("다나와 최저가 검색")
window.geometry("1280x720+100+100")
window.configure(bg='white')
window.resizable(False, False)

image=PhotoImage(file="C:\강의\캡스톤 디자인 프로젝트\다나와.png")
font = tkinter.font.Font(family="맑은 고딕", size=15)

lbl = Label(window, image=image, bd=0)
lbl.pack(pady=10)

txt = Entry(window, relief="groove", insertbackground="green", highlightthickness=2, highlightcolor="lightgreen", font=font)
txt.pack(fill=X, padx=10)

btn = Button(window, text="검색", font=font, cursor="hand2")
btn.pack(pady=10)

window.mainloop()
'''












