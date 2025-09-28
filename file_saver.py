# file_saver.py

import os
import csv
from datetime import datetime

def save_articles_to_csv(processed_articles, query, folder_path):
    """처리된 기사 리스트를 CSV 파일로 저장합니다."""
    if not processed_articles:
        print("저장할 기사가 없습니다.")
        return

    os.makedirs(folder_path, exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    filename = os.path.join(folder_path, f"news_{today}.csv")

    # CSV 헤더를 새로운 기능에 맞게 수정
    fieldnames = ['번호', '제목', '출처', 'URL', '게시일', '본문', '진위여부(1:진짜, 0:가짜)', '생성된_가짜뉴스']

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
                '본문': article['text'],
                '진위여부(1:진짜, 0:가짜)': article['is_real'],
                '생성된_가짜뉴스': article['generated_fake_news']
            })
            
    print(f"\n총 {len(processed_articles)}개 기사 저장 완료: {filename}")