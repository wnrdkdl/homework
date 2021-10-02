import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

docs = []
for tr in trs:
    rank = tr.select_one('td.number').text[0:2].strip()
    # rank = tr.select_one('td.number').text.split()[0] split 함수를 이용하여 필요한 문자열만 가져오기
    title = tr.select_one('td.info > a.title.ellipsis').text.strip()
    artist = tr.select_one('td.info > a.artist.ellipsis').text
    print( rank, title, artist ) # 달달한 맛 숙제

    doc = {
        'rank': rank,
        'title': title,
        'star': artist
    }
    # db.musicChart.insert_one(doc) # 쓸씁한 맛 숙제
    # 위와 같은 방법으로 하면, 데이터 베이스와 반복문을 돌면서 매번 왔다 갔다 함. 이렇게 하면 정보가 많을수록 실행 속도가 느려짐.
    # 그러므로 docs라는 배열을 반복문 위에 선언하여 한 번에 insert 할 수 있도록 한다.
    docs.append(doc)
    db.musicChart.insert_many(docs)

    # 반복문으로 출력
    musics = list(db.musicChart.find({'_id' : False}))

    for music in musics:
        print(music)