from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('D:/selenium/chromedriver_win32/chromedriver')  # 드라이버를 실행합니다.


url = "https://www.melon.com/search/total/index.htm?q=%EB%A6%AC%EC%8C%8D"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url, headers=headers)

driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
sleep(5)  # 페이지가 로딩되는 동안 5초 간 기다립니다. 

driver.execute_script("document.querySelector('#conts > div.section_atist > div > div.atist_dtl_info > div > a').click();")
sleep(5)

req = driver.page_source  # html 정보를 가져옵니다.
driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

# soup = BeautifulSoup(data.text, 'html.parser')
soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.

songs = soup.select("#conts > div.wrap_dtl_atist > div > div.wrap_atist_info > p")
print(songs)


# for song in songs:
#     title = song.select_one("td > div > div.wrap_song_info > div.rank01 > span > a").text
#     artist = song.select_one("td > div > div.wrap_song_info > div.rank02 > span > a").text
#     likes = song.select_one("td > div > button.like > span.cnt").text
#     print(title, artist, likes)