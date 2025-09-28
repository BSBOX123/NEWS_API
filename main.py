# main.py

import time
import config
from concurrent.futures import ThreadPoolExecutor, as_completed
from api_handler import fetch_articles, analyze_and_generate_fake_news 
from crawler import crawl_article_text
from file_saver import save_articles_to_csv

def process_article(article):
    """단일 기사를 크롤링하고, 진위 여부 판별 및 가짜뉴스를 생성합니다."""
    url = article.get('url', '')
    
    text = crawl_article_text(url)
    is_real, generated_fake_news = analyze_and_generate_fake_news(text) 
    
    return {
        'title': article.get('title', ''),
        'source': article.get('source', {}).get('name', ''),
        'url': url,
        'publishedAt': article.get('publishedAt', ''),
        'text': text,
        'is_real': is_real,
        'generated_fake_news': generated_fake_news
    }

def main():
    """메인 실행 함수"""
    print("뉴스 기사 수집 및 분석을 시작합니다...")
    try:
        articles = fetch_articles(
            config.QUERY,
            config.LANGUAGE,
            config.SOURCES,
            config.SORT_BY,
            config.PAGE_SIZE
        )
        print(f"총 {len(articles)}개의 기사를 가져왔습니다. 병렬 배치 처리를 시작합니다.")

        processed_articles = []
        
        batches = [articles[i:i + config.BATCH_SIZE] for i in range(0, len(articles), config.BATCH_SIZE)]

        for i, batch in enumerate(batches):
            print(f"\n--- 배치 {i+1}/{len(batches)} 처리 시작 ({len(batch)}개) ---")
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_article = {executor.submit(process_article, article): article for article in batch}
                
                for future in as_completed(future_to_article):
                    try:
                        result = future.result()
                        processed_articles.append(result)
                        print(f"  - 처리 완료: {result['title'][:30]}...")
                    except Exception as e:
                        print(f"[Error] 기사 처리 중 예외 발생: {e}")

            if i < len(batches) - 1:
                print(f"--- 배치 {i+1} 처리 완료. API 사용량 제한 초기화를 위해 61초간 대기합니다... ---")
                time.sleep(61)

        processed_articles.sort(key=lambda x: x['publishedAt'], reverse=True)
        save_articles_to_csv(processed_articles, config.QUERY, config.SAVE_FOLDER_PATH)

    except Exception as e:
        print(f"프로세스 실행 중 심각한 오류 발생: {e}")

if __name__ == '__main__':
    main()