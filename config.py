# config.py

# API Keys
NEWS_API_KEY = 'a86133a2e6ca476cb12a1c3021ed5f60'  # 본인의 News API 키를 입력하세요.
GEMINI_API_KEY = 'AIzaSyBmIXfvMoRC-Y6C_94YZLu5f4hQIR2B9Zg' # Google AI Studio에서 발급받은 키를 입력하세요.

# News API Parameters
QUERY = '인공지능'  # 검색할 키워드를 입력하세요.
LANGUAGE = 'ko'
SOURCES = None
SORT_BY = 'publishedAt'
PAGE_SIZE = 10 # 한 번에 가져올 기사 수를 최대로 설정 (News API 무료 플랜 최대치)

# File Paths
SAVE_FOLDER_PATH = r'E:\아들\News_API\articles' # 저장할 폴더 경로