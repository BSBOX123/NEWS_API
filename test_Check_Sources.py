import requests


API_KEY = 'a86133a2e6ca476cb12a1c3021ed5f60'
url = f'https://newsapi.org/v2/top-headlines/sources?apiKey={API_KEY}'

response = requests.get(url)
data = response.json()

#news_API에서 제공하는 언론사 목록 출력
if 'sources' in data:
    print("신뢰할 수 있는 언론사 목록:")
    for source in data['sources']:
        if source['category'] in ['general', 'business', 'science']:  # 신뢰도 높은 범주
            print(f"- {source['id']}: {source['name']} ({source['category']})")
else:
    print("Error:", data)


#특정 언론사만 가져오기
sources = ['bbc-news', 'cnn', 'the-wall-street-journal']  # 신뢰할만한 언론사 ID 리스트

for source in sources:
    print(f"\n===== {source.upper()} 뉴스 =====\n")

    url = f'https://newsapi.org/v2/top-headlines?sources={source}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()

    if data.get('articles'):
        for article in data['articles']:
            print("제목:", article.get('title'))
            print("설명:", article.get('description'))
            print("URL:", article.get('url'))
            print("-" * 60)
    else:
        print("기사를 가져올 수 없습니다.")