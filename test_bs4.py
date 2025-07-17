import requests
from bs4 import BeautifulSoup

url = 'https://www.hani.co.kr/arti/society/society_general/1208422.html'

headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')

# 바뀐 구조에 맞춰서 수정
article_body = soup.find('div', class_='article-text')

if article_body:
    text = article_body.get_text(strip=True, separator='\n')
    print("본문 추출 성공!\n")
    print(text)
else:
    print("본문을 찾을 수 없습니다.")
