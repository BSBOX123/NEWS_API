#텍스트 기반 신뢰도 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


#학습 데이터
texts = [
    "서울은 대한민국의 수도이다.",
    "서울은 일본의 수도이다.",
    "애플은 미국에 본사를 둔 IT 기업이다.",
    "애플은 한국에서만 판매되는 기업이다."
]
labels = [1, 0, 1, 0]  # 1=진짜, 0=가짜


#TF-IDF 벡터화 & ML 모델 학습
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)


# 특정 단어 감점-
def exaggeration_score(text):
    exaggeration_words = ["충격", "긴급", "단독", "믿을 수 없는"]
    count = sum(word in text for word in exaggeration_words)
    score = max(0, 1 - 0.1*count)  # 단어 하나당 -0.2 (향후 변경)
    return score


#최종 신뢰도 계산
def text_based_score(text):
    X_test = vectorizer.transform([text])
    ml_score = model.predict_proba(X_test)[0][1]  # 0~1 확률
    ex_score = exaggeration_score(text)
    final_score = (ml_score*0.7) + (ex_score*0.3)  # 가중치 조합
    return final_score


# 테스트
test_texts = [
    "서울은 대한민국의 수도이다.",
    "서울은 일본의 수도이다.",
    "이번 사건은 충격적인 단독 소식이다!"
]

for t in test_texts:
    score = text_based_score(t)
    print(f"텍스트: {t}\n신뢰도: {score:.2f}\n")
