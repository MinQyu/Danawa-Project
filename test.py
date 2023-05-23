# 다나와 사이트 검색
chrome_options = Options()
chrome_options.add_argument('headless')
driver1 = webdriver.Chrome(options=chrome_options)
driver2 = webdriver.Chrome(options=chrome_options)
driver3 = webdriver.Chrome(options=chrome_options)
driver4 = webdriver.Chrome(options=chrome_options)
# webdirver 설정(Chrome, Firefox 등)
 # 브라우저 창 보이기
 
# 크롬 브라우저 내부 대기 (암묵적 대기)
driver1.implicitly_wait(10)
driver2.implicitly_wait(10)
driver3.implicitly_wait(10)
driver4.implicitly_wait(10)
# 브라우저 사이즈
driver1.set_window_size(700,700)
driver2.set_window_size(700,700)
driver3.set_window_size(700,700)
driver4.set_window_size(700,700)

#G마켓 상품 정보 크롤링
def Gmarket_number():
    driver1.get('https://prod.danawa.com/info/?pcode=16635776&keyword=lg+%EA%B7%B8%EB%9E%A8+17%EC%9D%B8%EC%B9%98&cate=112758&_gl=1*16yypzb*_ga*MTQzNjg2NjY3LjE2Nzg3OTkzNzE.*_ga_L8D5P2KD8Z*MTY4NDg1Njg5My4zOS4xLjE2ODQ4NTY5NDYuNy4wLjA.')
    try: 
        Gmarket_link = driver1.find_element(By.XPATH, '//img[@alt="G마켓"]')
        Gmarket_link.click()
    except NoSuchElementException: 
        print("제품이 존재하지 않습니다.")
        driver1.close()
    else:
        driver1.switch_to.window(driver1.window_handles[1])
        driver1.implicitly_wait(10)
        Gmarket_url = driver1.current_url
        First_index= Gmarket_url.find("link_pcode")
        Last_index = Gmarket_url.find("&package")
        driver1.close()
        driver1.switch_to.window(driver1.window_handles[0])
        driver1.close()
        Gmarket_prodnumber = Gmarket_url[First_index+len("link_pcode")+1:Last_index]
        return Gmarket_prodnumber

#옥션 상품 정보 크롤링
def Auction_number():
    driver2.implicitly_wait(10)
    driver2.get('https://prod.danawa.com/info/?pcode=16635776&keyword=lg+%EA%B7%B8%EB%9E%A8+17%EC%9D%B8%EC%B9%98&cate=112758&_gl=1*16yypzb*_ga*MTQzNjg2NjY3LjE2Nzg3OTkzNzE.*_ga_L8D5P2KD8Z*MTY4NDg1Njg5My4zOS4xLjE2ODQ4NTY5NDYuNy4wLjA.')
    try: 
        Auction_link = driver2.find_element(By.XPATH, '//img[@alt="옥션"]')
        Auction_link.click()
    except NoSuchElementException: 
        print("제품이 존재하지 않습니다.")
        driver2.close()
    else:
        driver2.switch_to.window(driver2.window_handles[1])
        driver2.implicitly_wait(10)
        Auction_url = driver2.current_url
        First_index= Auction_url.find("link_pcode")
        Last_index = Auction_url.find("&package")
        driver2.close()
        driver2.switch_to.window(driver2.window_handles[0])
        driver2.close()
        Auction_prodnumber = Auction_url[First_index+len("link_pcode")+1:Last_index]
        return Auction_prodnumber

#쿠팡 상품 정보 크롤링
def Coupang_number():
    driver3.implicitly_wait(10)
    driver3.get('https://prod.danawa.com/info/?pcode=16635776&keyword=lg+%EA%B7%B8%EB%9E%A8+17%EC%9D%B8%EC%B9%98&cate=112758&_gl=1*16yypzb*_ga*MTQzNjg2NjY3LjE2Nzg3OTkzNzE.*_ga_L8D5P2KD8Z*MTY4NDg1Njg5My4zOS4xLjE2ODQ4NTY5NDYuNy4wLjA.')
    try: 
        Coupang_link = driver3.find_element(By.XPATH, '//img[@alt="쿠팡"]')
        Coupang_link.click()
    except NoSuchElementException: 
        print("제품이 존재하지 않습니다.")
        driver3.close()
    else:
        driver3.switch_to.window(driver3.window_handles[1])
        driver3.implicitly_wait(10)
        Coupang_url = driver3.current_url
        First_index= Coupang_url.find("link_pcode")
        Last_index = Coupang_url.find("&package")
        driver3.close()
        driver3.switch_to.window(driver3.window_handles[0])
        driver3.close()
        Coupang_prodnumber = Coupang_url[First_index+len("link_pcode")+2:Last_index]
        return Coupang_prodnumber

#11번가 상품 정보 크롤링
def Ele_number():
    driver4.implicitly_wait(10)
    driver4.get('https://prod.danawa.com/info/?pcode=16635776&keyword=lg+%EA%B7%B8%EB%9E%A8+17%EC%9D%B8%EC%B9%98&cate=112758&_gl=1*16yypzb*_ga*MTQzNjg2NjY3LjE2Nzg3OTkzNzE.*_ga_L8D5P2KD8Z*MTY4NDg1Njg5My4zOS4xLjE2ODQ4NTY5NDYuNy4wLjA.')
    try: 
        Ele_link = driver4.find_element(By.XPATH, '//img[@alt="11번가"]')
        Ele_link.click()
    except NoSuchElementException: 
        print("제품이 존재하지 않습니다.")
        driver4.close()
    else:
        driver4.switch_to.window(driver4.window_handles[1])
        driver4.implicitly_wait(10)
        Ele_url = driver4.current_url
        First_index= Ele_url.find("link_pcode")
        Last_index = Ele_url.find("&package") 
        driver4.close()
        driver4.switch_to.window(driver4.window_handles[0])
        driver4.close()
        Ele_pronumber = Ele_url[First_index+len("link_pcode")+1:Last_index]
        return Ele_pronumber
    
print(Ele_number())
print(Coupang_number())
print(Auction_number())
print(Gmarket_number())
