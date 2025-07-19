import requests
from bs4 import BeautifulSoup

url = "https://www.cnn.com/2025/07/12/tech/virtual-reality-entertainment-apple-meta-google-disney"
headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# 제목
title = soup.find("h1").get_text(strip=True)

# 본문: 기사 문단은 여러 <div>나 <p> 태그로 나뉘어 있음
paragraphs = soup.find_all("div", class_="paragraph inline-placeholder")
if not paragraphs:  # 구조가 다를 수도 있음
    paragraphs = soup.find_all("p")

content = "\n".join(p.get_text(strip=True) for p in paragraphs)

print("제목:", title)
print("본문:", content)
