import os
import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup


API_KEY = 'a86133a2e6ca476cb12a1c3021ed5f60' # 발급받은 News API 키 입력
query = 'apple' # 검색할 키워드
sources = 'cnn' # 특정 언론사


# API 요청 URL 및 파라미터
url = 'https://newsapi.org/v2/everything'
params = {
    'q': query,
    'language': 'en',
    'sortBy': 'publishedAt',  # 최신 기사 순 정렬
    'pageSize': 10,
    'sources': sources,
    'apiKey': API_KEY
}



folder_path = r'E:\아들\News_API\articles'  # 저장 폴더 위치
os.makedirs(folder_path, exist_ok=True) # 만약 폴더가 존재 하지 않으면 자동 생성

# 날짜와 키워드 포함된 파일명 생성
today = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
keyword_safe = query.replace(" ", "_")
sources_safe = sources.replace(',', '_').replace('.', '_')
filename = os.path.join(folder_path, f"news_{keyword_safe}_{today}_{sources_safe}.csv")


# News API 요청 보내기
response = requests.get(url, params=params)

# 결과 확인
if response.status_code == 200:  # 응답 성공 코드 '200'
    data = response.json() # 받은 응답을 json 형식으로 파싱 -> json응답을 파이썬 딕셔너리로 변환
    articles = data['articles'] #  articles는 뉴스 기사 목록

    # CSV 파일 저장
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['번호', '제목', '출처', 'URL', '게시일', '요약'])  # 헤더

        for i, article in enumerate(articles, 1): # 기사의 수 만큼 반복
            title = article.get('title', '')
            source = article.get('source', {}).get('name', '')
            article_url = article.get('url', '')
            published_at = article.get('publishedAt', '')
            summary = ''

            try:
                # 기사 본문 크롤링
                headers = {'User-Agent': 'Mozilla/5.0'} # 접근 차단 방지
                # news API를 통해 가져온 링크로 요청
                page = requests.get(article_url, headers=headers, timeout=10)
                soup = BeautifulSoup(page.text, 'html.parser')

                # CNN 기사 본문 추출
                paragraphs = soup.find_all('div', class_='container__paragraph')
                if not paragraphs:
                    paragraphs = soup.find_all('div', attrs={'data-component': 'text-block'})  
                if not paragraphs:
                    paragraphs = soup.find_all('p')

                text = ' '.join([p.get_text(strip=True) for p in paragraphs])
                summary = text if text else '[본문 없음]'

            except Exception as e:
                print(f"⚠ 요약 실패 - URL: {article_url}\n   오류 메시지: {e}")  
                summary = "[요약 실패]"  
            
            writer.writerow([i, title, source, article_url, published_at, summary])
    


    print("\n\n")
    print(f"총 {len(articles)}개의 기사 검색됨 ({sources}):\n")
    print(f"CSV 파일 저장 완료: {filename}")
else:
    print("뉴스를 가져오는 데 실패했습니다.")
    print("상태 코드:", response.status_code)
    print("에러 메시지:", response.text)
