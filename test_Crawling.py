import os
import requests
import csv
from datetime import datetime

# 발급받은 News API 키 입력
API_KEY = 'a86133a2e6ca476cb12a1c3021ed5f60'

# 검색할 키워드
query = 'Samsung'

# 특정 언론사
sources = 'cnn'

# API 요청 URL 및 파라미터
url = 'https://newsapi.org/v2/everything'
params = {
    'q': query,
    'language': 'en',
    'sortBy': 'publishedAt',
    'pageSize': 10,
    'sources': sources,
    'apiKey': API_KEY
}

# 저장 폴더 위치
folder_path = r'E:\아들\News_API\articles'
os.makedirs(folder_path, exist_ok=True)

# 요청 보내기
response = requests.get(url, params=params)

# 결과 확인
if response.status_code == 200:
    data = response.json()
    articles = data['articles']

    # 날짜와 키워드 포함된 파일명 생성
    today = datetime.now().strftime('%Y%m%d')
    keyword_safe = query.replace(" ", "_")
    sources_safe = sources.replace(',', '_').replace('.', '_')
    filename = os.path.join(folder_path, f"news_{keyword_safe}_{today}_{sources_safe}.csv")

    # CSV 파일 저장
    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['번호', '제목', '출처', 'URL', '게시일'])  # 헤더

        for i, article in enumerate(articles, 1):
            writer.writerow([
                i,
                article.get('title', ''),
                article.get('source', {}).get('name', ''),
                article.get('url', ''),
                article.get('publishedAt', '')
            ])
    
    print(f"총 {len(articles)}개의 기사 검색됨 ({sources}):\n")
    print(f"\nCSV 파일 저장 완료: {filename}")
else:
    print("뉴스를 가져오는 데 실패했습니다.")
    print("상태 코드:", response.status_code)
    print("에러 메시지:", response.text)
