import os
import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import google.generativeai as genai
from google.oauth2 import service_account
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = 'a86133a2e6ca476cb12a1c3021ed5f60'  # API 키
key_path = r"E:\아들\News_API\news-summarize-466413-caa1714fa7c5.json"

credentials = service_account.Credentials.from_service_account_file(key_path)
model = genai.GenerativeModel(model_name="gemini-1.5-pro")
genai.configure(credentials=credentials)

#News API에서 기사 가져오기
def fetch_articles(query, language, sources, sort, page_size=10): # 키워드, 언어, 언론사, 정렬기준, 기사 개수를 매개변수로 입력
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'language': language,
        'sources': sources,
        'sortBy': sort,
        'pageSize': page_size,
        'apiKey': API_KEY
    }
    response = requests.get(url, params=params) #News API 요청 보내기
    if response.status_code != 200: #200은 요청성공 코드 -> 요청 실패 시 오류코드 출력 
        raise Exception(f"News API 요청 실패: {response.status_code} {response.text}")
    data = response.json() #받은 응답을 json 형식으로 파싱 -> json응답을 파이썬 딕셔너리로 변환
    return data.get('articles', []) #articles는 뉴스 기사 목록


#본문 크롤링 & 텍스트 반환
def crawl_article_text(url):
    headers = {'User-Agent': 'Mozilla/5.0'} # 접근 차단 방지
    try:
        # news API를 통해 가져온 링크로 요청
        page = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')

        # CNN 기사 본문 추출 - cnn기사 형태(cnn에서 아래 3개의 형태로 기사를 작성하기에 3가지 형태에 대응하도록 설계)
        paragraphs = soup.find_all('div', class_='container__paragraph')
        if not paragraphs:
            paragraphs = soup.find_all('div', attrs={'data-component': 'text-block'})
        if not paragraphs:
            paragraphs = soup.find_all('p')

        #본문 내용 전처리 - html의 <p>의 내용을 가져와 문장 합치기
        text = ' '.join([p.get_text(strip=True) for p in paragraphs])
        return text if text else '[본문 없음]'
    #예외 처리 - 크롤링 실패 시 오류 코드 발생
    except Exception as e:
        print(f"[Error] 본문 크롤링 실패 - URL: {url} / 오류: {e}")
        return "[본문 없음]"


#LLM을 통한 요약
def summarize_text(text):
    if not text or text == '[본문 없음]':
        return '[요약 실패]'
    try:
        response = model.generate_content(
            f"다음 기사를 한국어로 3줄로 요약해줘:\n{text}",
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=300
            )
        )
        return response.text
    except Exception as e:
        print(f"[Error] 요약 API 호출 실패: {e}")
        return '[요약 실패]'


#크롤링과 요약 합치기
def process_article(article):
    url = article.get('url', '')
    text = crawl_article_text(url)
    summary = summarize_text(text)
    return {
        'title': article.get('title', ''),
        'source': article.get('source', {}).get('name', ''),
        'url': url,
        'publishedAt': article.get('publishedAt', ''),
        'summary': summary
    }


#파일 저장 - csv형식
def save_articles_to_csv(processed_articles, query, sources, folder_path):
    # 만약 폴더가 존재 하지 않으면 자동 생성
    os.makedirs(folder_path, exist_ok=True)
    today = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
    # 날짜와 키워드 포함된 파일명 생성
    keyword_safe = query.replace(" ", "_")
    sources_safe = sources.replace(',', '_').replace('.', '_')
    filename = os.path.join(folder_path, f"news_{keyword_safe}_{today}_{sources_safe}.csv")

    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['번호', '제목', '출처', 'URL', '게시일', '요약'])

        for i, article in enumerate(processed_articles, 1):
            writer.writerow([
                i,
                article['title'],
                article['source'],
                article['url'],
                article['publishedAt'],
                article['summary']
            ])
    print(f"\n총 {len(processed_articles)}개 기사 저장 완료: {filename}")


# 실행
def main():
    query = 'trump'
    language = 'en'
    sources = 'cnn'
    sort = 'publishedAt'
    page_size = 10
    folder_path = r'E:\아들\News_API\articles'

    try:
        articles = fetch_articles(query, language, sources, sort, page_size)

        processed_articles = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_article, article) for article in articles]
            for future in as_completed(futures):
                try:
                    result = future.result()
                    processed_articles.append(result)
                except Exception as e:
                    print(f"[Error] 기사 처리 중 예외 발생: {e}")

        save_articles_to_csv(processed_articles, query, sources, folder_path)

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == '__main__':
    main()