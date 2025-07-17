import requests
import json
from datetime import datetime

# 발급받은 News API 키 입력
API_KEY = 'a86133a2e6ca476cb12a1c3021ed5f60'

# 검색할 키워드
query = '삼성전자'

# API 요청 URL 및 파라미터
url = 'https://newsapi.org/v2/everything'
params = {
    'q': query,              # 검색 키워드
    'language': 'ko',        # 한국어 기사만
    'sortBy': 'publishedAt', # 최근 기사부터 정렬
    'pageSize': 10,          # 최대 10개 기사 가져오기
    'apiKey': API_KEY        # 본인의 API 키
}

# 요청 보내기
response = requests.get(url, params=params)

# 결과 확인
if response.status_code == 200:
    data = response.json()
    articles = data['articles']

    # 날짜와 키워드 포함된 파일명 생성
    today = datetime.now().strftime('%Y%m%d')
    keyword_safe = query.replace(" ", "_")  # 공백은 언더스코어로 변경
    filename = f"news_{keyword_safe}_{today}.json"

    # JSON 파일 저장
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"총 {len(articles)}개의 기사 검색됨:\n")
    for i, article in enumerate(articles, 1):
        print(f"[{i}] {article['title']}")
        print(f"    출처: {article['source']['name']}")
        print(f"    링크: {article['url']}\n")
else:
    print("뉴스를 가져오는 데 실패했습니다.")
    print("상태 코드:", response.status_code)
    print("에러 메시지:", response.text)
