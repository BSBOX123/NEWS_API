# main.py

import sys
import google.generativeai as genai
print("--- 진단 정보 ---")
print(f"Python 실행 경로: {sys.executable}")
print(f"google-generativeai 라이브러리 버전: {genai.__version__}")
print("-----------------")


import time
import config
from api_handler import fetch_articles, summarize_text_with_gemini
from crawler import crawl_article_text
from file_saver import save_articles_to_csv

def process_article(article):
    """단일 기사를 크롤링하고 요약하는 전체 프로세스."""
    url = article.get('url', '')
    
    text = crawl_article_text(url)
    summary = summarize_text_with_gemini(text)
    
    return {
        'title': article.get('title', ''),
        'source': article.get('source', {}).get('name', ''),
        'url': url,
        'publishedAt': article.get('publishedAt', ''),
        'summary': summary,
        'text': text
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
        print(f"총 {len(articles)}개의 기사를 가져왔습니다. 순차 처리를 시작합니다.")

        processed_articles = []
        # 순차적으로 기사를 처리하며 중간에 딜레이를 줍니다.
        for i, article in enumerate(articles, 1):
            try:
                result = process_article(article)
                processed_articles.append(result)
                # 진행 상황을 표시
                print(f"  ({i}/{len(articles)}) 처리 완료: {result['title'][:30]}...")
                
                # --- 핵심: API 사용량 제한을 피하기 위한 딜레이 ---
                time.sleep(1.1) 
                
            except Exception as e:
                print(f"[Error] '{article.get('title', '')}' 기사 처리 중 예외 발생: {e}")

        processed_articles.sort(key=lambda x: x['publishedAt'], reverse=True)
        save_articles_to_csv(processed_articles, config.QUERY, config.SAVE_FOLDER_PATH)

    except Exception as e:
        print(f"프로세스 실행 중 심각한 오류 발생: {e}")

if __name__ == '__main__':
    main()