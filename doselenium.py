from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import re

driver = webdriver.Chrome('D:/selenium/chromedriver_win32/chromedriver')  # 드라이버를 실행합니다.


url = "https://www.melon.com/search/total/index.htm?q=%EB%A6%AC%EC%8C%8D"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url, headers=headers)

driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
sleep(5)  # 페이지가 로딩되는 동안 5초 간 기다립니다. 

driver.execute_script("document.querySelector('#conts > div.section_atist > div > div.atist_dtl_info > div > a').click();")
sleep(1)
driver.execute_script("document.querySelector('#conts > div.wrap_tab_atist.type9 > ul > li:nth-child(4) > a').click();")
sleep(1)
driver.execute_script("document.querySelector('#frm > div > ul > li:nth-child(2) > div > a.thumb').click();")
sleep(1)
req = driver.page_source  # html 정보를 가져옵니다.
driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

# soup = BeautifulSoup(data.text, 'html.parser')
soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.

songs = soup.select("#conts > div.section_info > div > div.entry")
print("---------------------------------------")


sing = soup.select("#frm > div > table > tbody")

sings = sing[0].find_all("div",{"class": "ellipsis"})
href = sing[0].find_all("a",{"class": "song_info"})

singlist = []
a1 = []
b1 = []
for te in sings[0::2]:
    title = te.text.strip().replace('\n', '.')
    a1.append(title)
    # print(title)


##정규식으로 바꾸기
dotest = re.compile("[0-9]+")
for t1 in href:
    wht = t1["href"]
    test = dotest.search(wht).group()
    b1.append(test)

for i in zip(a1, b1):
    singlist.append(i)

title = songs[0].select_one("div.info > div.song_name").text.strip()[-3:]
artist = songs[0].select_one("div.info > div.artist").text.strip()
date = songs[0].select("div.meta > dl > dd")[0].text
genre = songs[0].select("div.meta > dl > dd")[1].text
Publisher = songs[0].select("div.meta > dl > dd")[2].text
agency = songs[0].select("div.meta > dl > dd")[3].text
##singlist 이게 곡리스트에요 리스트형태 (노래제목, 링크대체번호) ex)[('Title.눈물 (Feat. 유진 Of 더 씨야)', '4020215'), ('눈물 (Inst.)', '4020216')]
##여기까지 만들었습니다.


#test 프린트
print(title,artist,date,genre,Publisher,agency)