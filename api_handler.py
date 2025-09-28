# api_handler.py

import requests
import google.generativeai as genai
from config import GEMINI_API_KEY, NEWS_API_KEY

# 모델 초기화
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # 현재 사용 가능한 모델 이름을 정확히 기입합니다.
    model = genai.GenerativeModel(model_name="gemini-2.5-flash") 
    print("🤖 Gemini 모델이 성공적으로 준비되었습니다.")
except Exception as e:
    print(f"❌ 모델 설정 중 오류 발생: {e}")
    model = None

def fetch_articles(query, language, sources, sort_by, page_size):
    """News API에서 기사 목록을 가져옵니다."""
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'language': language,
        'sources': sources,
        'sortBy': sort_by,
        'pageSize': page_size,
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('articles', [])

def analyze_and_generate_fake_news(text):
    """
    뉴스 본문을 분석하여 진위 여부를 판단하고, 학습에 적합한 '긴 글' 형태의 가짜뉴스를 생성합니다.
    """
    if not model or not text or text == '[본문 없음]':
        return 1, '[가짜뉴스 생성 실패]' # 진위 여부는 우선 1(진짜)로 고정

    is_real_news = 1 # 모든 원본 뉴스는 '진짜'로 라벨링

    try:
        # 가짜뉴스 생성을 위한 프롬프트
        prompt = f"""
        당신은 사실과 허구를 교묘하게 섞어, 서론-본론-결론 구조를 갖춘 그럴듯한 가짜뉴스를 작성하는 AI 저널리스트입니다.
        아래 원본 기사의 핵심 인물, 장소, 기관명, 사건을 사용하되, 사건의 경과나 결과, 숨겨진 동기 등을 왜곡하고 과장하여 
        사람들이 진짜 기사로 착각할 만한 가짜뉴스를 '최소 3문단 이상'으로 구성된 하나의 완성된 기사 형태로 작성해주세요.

        --- 원본 기사 ---
        {text}
        """
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8, # 창의성을 위해 온도를 약간 높임
                max_output_tokens=3072 # 긴 결과물을 위해 토큰 수 확장
            )
        )
        
        if response.parts:
            fake_news_text = response.text.strip()
        else:
            fake_news_text = f"[가짜뉴스 생성 실패] Finish Reason: {response.candidates[0].finish_reason.name}"
            
    except Exception as e:
        print(f"❌ 가짜뉴스 생성 API 호출 실패: {e}")
        fake_news_text = '[가짜뉴스 생성 실패]'

    return is_real_news, fake_news_text