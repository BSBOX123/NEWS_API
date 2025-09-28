# main.py

from concurrent.futures import ThreadPoolExecutor, as_completed
import config
from api_handler import fetch_articles, summarize_text_with_gemini
from crawler import crawl_article_text
from file_saver import save_articles_to_csv

def process_article(article):
    """단일 기사를 크롤링하고 요약하는 전체 프로세스. (본문 반환 추가)"""
    url = article.get('url', '')
    
    # 1. 본문 크롤링
    text = crawl_article_text(url)
    
    # 2. 본문 요약
    summary = summarize_text_with_gemini(text)
    
    return {
        'title': article.get('title', ''),
        'source': article.get('source', {}).get('name', ''),
        'url': url,
        'publishedAt': article.get('publishedAt', ''),
        'summary': summary,
        'text': text  # 저장할 수 있도록 본문(text)을 결과에 포함
    }

def main():
    """메인 실행 함수"""
    print("뉴스 기사 수집 및 요약을 시작합니다...")
    try:
        articles = fetch_articles(
            api_key=config.NEWS_API_KEY,
            query=config.QUERY,
            language=config.LANGUAGE,
            sources=config.SOURCES,
            sort_by=config.SORT_BY,
            page_size=config.PAGE_SIZE
        )
        print(f"총 {len(articles)}개의 기사를 가져왔습니다. 병렬 처리를 시작합니다.")

        processed_articles = []
        with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
            future_to_article = {executor.submit(process_article, article): article for article in articles}
            for future in as_completed(future_to_article):
                try:
                    result = future.result()
                    processed_articles.append(result)
                    print(f"  - 처리 완료: {result['title'][:30]}...")
                except Exception as e:
                    print(f"[Error] 기사 처리 중 예외 발생: {e}")

        # 게시일 기준으로 정렬하여 저장
        processed_articles.sort(key=lambda x: x['publishedAt'], reverse=True)
        
        save_articles_to_csv(processed_articles, config.QUERY, config.SAVE_FOLDER_PATH)

    except Exception as e:
        print(f"프로세스 실행 중 심각한 오류 발생: {e}")

if __name__ == '__main__':
    main()