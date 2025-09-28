# config.py

# API Keys
NEWS_API_KEY = 'a86133a2e6ca476cb12a1c3021ed5f60'  # 본인의 News API 키
GEMINI_CREDENTIALS_PATH = r"E:\아들\News_API\news-summarize-466413-caa1714fa7c5.json" # 본인의 Gemini API 키 경로

# News API Parameters
QUERY = '경제'  # 검색할 키워드를 한국어로 변경
LANGUAGE = 'ko'  # 언어를 한국어로 설정
# country = 'kr' 파라미터를 사용하거나 language='ko'로 검색하는 것이 더 효과적입니다.
# 특정 sources를 지정하는 대신 한국어 전체 기사를 대상으로 검색합니다.
SOURCES = None   # 특정 언론사 지정 해제
SORT_BY = 'publishedAt' # 정렬 기준: 최신순
PAGE_SIZE = 20 # 가져올 기사 수

# File Paths
SAVE_FOLDER_PATH = r'E:\아들\News_API\articles'

# Concurrency
MAX_WORKERS = 5