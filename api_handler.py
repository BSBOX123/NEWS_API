# api_handler.py

import requests
import google.generativeai as genai
from config import GEMINI_API_KEY # config에서 API 키를 가져오도록 수정

# Gemini 모델 초기화
try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(model_name="gemini-1.5-pro-001") 
except Exception as e:
    print(f"[Fatal Error] Gemini 모델 초기화 실패: {e}")
    gemini_model = None

def fetch_articles(api_key, query, language, sources, sort_by, page_size):
    """News API에서 기사 목록을 가져옵니다."""
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'language': language,
        'sources': sources,
        'sortBy': sort_by,
        'pageSize': page_size,
        'apiKey': api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('articles', [])

def summarize_text_with_gemini(text):
    """Gemini AI를 이용해 텍스트를 요약합니다."""
    if not gemini_model or not text or text == '[본문 없음]':
        return '[요약 실패]'
    try:
        response = gemini_model.generate_content(
            f"다음 기사를 한국어로 3줄로 요약해줘:\n{text}",
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=300
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Error] 요약 API 호출 실패: {e}")
        return '[요약 실패]'