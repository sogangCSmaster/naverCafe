from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pymysql as psql
import sys
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def crawler(id,password,cafe_address):
    MAX_PAGE = 1000
    #print("sid[%s] :: Start Crawling"%(sid))
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    #options.add_argument('window-size=1920x1080')
    #options.add_argument('disable-gpu')

    #conn = psql.connect(host='localhost', db='', user='', password='',charset='utf8')
    #query = "REPLACE INTO news_total (seq_no,date,naver_link,original_link,sid,company,upload_date,title,text) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    #cur = conn.cursor()


    driver = webdriver.Chrome('chromedriver',chrome_options=options)
    driver.get("https://nid.naver.com/nidlogin.login")
    driver.find_element_by_name('id').send_keys(id)
    driver.find_element_by_name('pw').send_keys(password)
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    driver.get(cafe_address)
    webpage_source = driver.page_source
    soup = BeautifulSoup(webpage_source, 'html.parser')
    club_id = soup.find('div', class_='thm').find('a').get('href').split('clubid=')[1]
    print(club_id)
    #css_selector = "input#topLayerQueryInput"
    #search_inpupt_element = driver.find_element_by_css_selector("input#topLayerQueryInput")
    #search_inpupt_element.send_keys(keyword)
    #search_button_element = driver.find_element_by_css_selector("form[name='frmBoardSearch'] a")
    #search_button_element.click()
    iframe_element = driver.find_element_by_css_selector("iframe#cafe_main")
    driver.switch_to_frame(iframe_element)
    board_url = 'http://cafe.naver.com/ArticleList.nhn?search.clubid={}&search.boardtype=L&search.questionTab=A&search.page='.format(club_id)
    letter = []
    pages = MAX_PAGE
    flag = False
    # Searching
    today = str(datetime.now()).split(' ')[0]
    print(today)
    for i in range(1, pages + 1):
        url = board_url + str(i)
        driver.get(url)
        iframe = driver.find_element_by_name('cafe_main')
        driver.switch_to_frame(iframe)
        driver.find_element_by_id('notice_hidden').click()
        webpage_source = driver.page_source
        soup = BeautifulSoup(webpage_source, 'html.parser')
        posts = soup.find_all('span', class_='aaa')
        for post in posts:
            try:
                title = post.find('a')
                print(title.get_text())
                print('http://cafe.naver.com' + title.get('href'))
                link = 'http://cafe.naver.com' + title.get('href')
                driver.get(link)
                iframe = driver.find_element_by_name('cafe_main')
                driver.switch_to_frame(iframe)
                content = driver.page_source
                content_soup = BeautifulSoup(content, 'html.parser')
                inbox = content_soup.find('div',class_='inbox')
                date = str(inbox.find('td',class_="m-tcol-c date").get_text().split('. ')[0]).replace('.','-')
                if date != today:
                    flag = True
                else:
                    flag = False
                main_paragraph = inbox.find('div',id='tbody').find_all('p')
                main_text = ''
                for p in main_paragraph:
                    main_text += p.get_text()+'\n'
                comments = inbox.find_all('div', class_='comm_cont')
                comment_text = ''
                for comm in comments:
                    comment_text += comm.find('p',class_="comm m-tcol-c").get_text()+'\n'
                print(main_text)
                print(comment_text)
                letter.append((title.get_text,link,date,main_text,comment_text))
            except :
                pass 
        time.sleep(1)
        if flag == True:
            break
    driver.close()
    driver.quit()
    
if __name__ == '__main__':
    id = input('id: ')
    password = input('password: ')
    cafe_address = 'http://cafe.naver.com/'+ input('cafe address: ')
    
    crawler(id,password,cafe_address)
