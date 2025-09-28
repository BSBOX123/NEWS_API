# file_saver.py

import os
import csv
from datetime import datetime

def save_articles_to_csv(processed_articles, query, folder_path):
    """처리된 기사 리스트를 CSV 파일로 저장합니다. (본문 포함)"""
    if not processed_articles:
        print("저장할 기사가 없습니다.")
        return

    os.makedirs(folder_path, exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    keyword_safe = "".join(c for c in query if c.isalnum())
    
    filename = os.path.join(folder_path, f"news_{keyword_safe}_{today}.csv")

    # CSV 헤더에 '본문' 추가
    fieldnames = ['번호', '제목', '출처', 'URL', '게시일', '요약', '본문']

    with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, article in enumerate(processed_articles, 1):
            writer.writerow({
                '번호': i,
                '제목': article['title'],
                '출처': article['source'],
                'URL': article['url'],
                '게시일': article['publishedAt'],
                '요약': article['summary'],
                '본문': article['text']  # 본문 데이터 추가
            })
            
    print(f"\n총 {len(processed_articles)}개 기사 저장 완료: {filename}")