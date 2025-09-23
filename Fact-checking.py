# -------------------------
# 외부 검증(Fact-checking) 테스트 코드
# 단순화: 미리 정의된 사실 기반 지식 그래프 사용

# 1️⃣ 예시 지식 그래프
knowledge_graph = {
    "서울": "대한민국",
    "애플": "미국",
    "파리": "프랑스",
    "도쿄": "일본"
}

# 2️⃣ 기사 문장 예시
test_articles = [
    "서울은 대한민국의 수도이다.",
    "서울은 일본의 수도이다.",
    "애플은 미국에 본사를 둔 기업이다.",
    "파리는 미국의 수도이다."
]

# 3️⃣ 사실 검증 함수
def fact_check_score(text):
    """
    텍스트 내 주어-국가 관계를 확인하여 신뢰도 점수 반환
    S_fact = (#일치 문장 / 전체 문장 수)
    """
    score = 1.0  # 기본 1.0 (신뢰)
    
    for subject, correct_country in knowledge_graph.items():
        if subject in text:
            if correct_country not in text:
                # 불일치 발견 시 0.0으로 간단화
                score = 0.0
                break
    return score

# 4️⃣ 테스트
for article in test_articles:
    score = fact_check_score(article)
    print(f"기사: {article}\n외부 검증 신뢰도: {score}\n")
