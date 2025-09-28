# crawler.py

import requests
from bs4 import BeautifulSoup

def crawl_article_text(url):
    """URL을 받아 기사 본문을 크롤링합니다. (한국 언론사 환경에 맞게 개선)"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        page = requests.get(url, headers=headers, timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')

        # 한국 주요 언론사들의 기사 본문 영역에 대한 CSS 선택자 리스트
        # 우선순위 순서대로 시도합니다.
        selectors = [
            'article',                   # 연합뉴스, 시사저널 등 (HTML5 시맨틱 태그)
            'div#article-body',          # 다수 언론사
            'div#article_body',          # 중앙일보 등
            'div.article_body',          # 다수 언론사
            'div.article-veiw-body',     # 스포츠서울 등
            'div#newsct_article',        # 네이버 뉴스
            'div.text',                  # 한겨레
            'div.story-news'             # 연합뉴스 (다른 구조)
        ]
        
        content_body = None
        for selector in selectors:
            content_body = soup.select_one(selector)
            if content_body:
                break # 본문 영역을 찾으면 반복 중단
        
        # 선택자로 본문을 찾지 못한 경우, <p> 태그 전체를 대상으로 시도
        if not content_body:
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text(strip=True) for p in paragraphs])
        else:
            # 찾은 본문 영역 내의 텍스트만 추출
            text = content_body.get_text(strip=True, separator=' ')

        return text if text else '[본문 없음]'
    
    except requests.RequestException as e:
        print(f"[Error] 본문 크롤링 요청 실패 - URL: {url} / 오류: {e}")
        return "[본문 없음]"
    except Exception as e:
        print(f"[Error] 본문 파싱 실패 - URL: {url} / 오류: {e}")
        return "[본문 없음]"