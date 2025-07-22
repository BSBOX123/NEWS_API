import cohere

API_KEY = "gMsO7hkpxCL3mOD8sB55mpwkMjtwqIazwfcXFWBz"
co = cohere.Client(API_KEY)

def summarize_article(article_text):
    if len(article_text) < 250:
        return "[요약 불가: 입력 텍스트가 너무 짧습니다 (250자 이상 필요)]"
    
    prompt = f"Summarize the following article clearly and concisely:\n\n{article_text}"
    
    response = co.generate(
        model='command',  # 또는 'command-nightly', 'command-light', 등
        prompt=f"Summarize this article:\n\n{article_text}",
        max_tokens=300,
        temperature=0.3
    )
    
    return response.generations[0].text.strip()

# 예시 테스트
if __name__ == '__main__':
    article = """Markets Hot Stocks Fear & Greed Index Latest Market News Hot 
    Stocks Follow: OpenAI on Thursday announced a new feature for ChatGPT that 
    allows the popular chatbot to execute actions on a user’s behalf. It’s part
    of an industry-wide push to change the way people get things done on the
    Internet: Tech giants hope that instead of bouncing between apps and manually 
    searching the web, users might be able to one day rely onagents to do it all. 
    ChatGPT’s new agent mode, which begins rolling out immediately, is another 
    sign that tech giants are doubling down on digital helpers that demonstrate 
    significantly advanced capabilities. It also heightens the race between OpenAI 
    and Google, which is pursuing similar ambitions with its Gemini helper. OpenAIsaidon 
    Thursday thatChatGPT’s new agent mode “thinks” and “acts” using its own virtual 
    computer, enabling it to handle complex action-oriented requests. For example, 
    users will be able to issue command such as “look at my calendar and brief me on 
    upcoming client meetings based on recent news” or “plan and buy ingredients to make 
    Japanese breakfast for four,” the company said in ablog post. In a video demonstration, 
    OpenAI employees wrote a long and detailed prompt asking the agent to help the user 
    prepare for a wedding. It included a set of specific instructions such as “find an outfit 
    that matches the dress code,” adding that it should propose five options, along with 
    hotels that can accommodate a couple of buffer days around the event. The new feature 
    is available for those who subscribe to a Pro, Plus or Team plan. It builds on and combines 
    capabilities from the ChatGPT Operator and Deep Research tools OpenAI already offers; 
    Operator browses the web, while Deep Research analyzes online resources to do things like 
    compile reports. The update is another step in OpenAI’s efforts to turn ChatGPT in a more 
    comprehensive universal assistant. At the same time, thebroader AI industry is also grappling 
    with how to address important shortcomings and privacy concerns aroundthe technology. AI models 
    are still prone to hallucinations and bias and can act in unpredictable ways, as xAI’s Grok 
    chatbot demonstrated last week when itspewed antisemitic contentafter being prompted to do so. 
    In a blog post, OpenAI acknowledged that ChatGPT’s new functionality presents new risks. It 
    said it has limited the data the model has access to, and certain tasks – like sending an 
    email – require the user’s oversight. The model is also trained to refuse“high-risk tasks” 
    like bank transfers, the company says. “I would explain this to my own family as cutting 
    edge and experimental; a chance to try the future, but not something I’d yet use for high-stakes 
    uses or with a lot of personal information until we have a chance to study and improve it in the 
    wild,” OpenAI CEO Sam Altman said in apost on X announcing the agent. He advised users to be 
    cautious when giving ChatGPT access to personal information. For example, granting access 
    to a calendar to coordinate a group dinner mightmake sense, but the agent wouldn’t need calendar 
    access to shop for clothes on a user’s behalf. The announcement comes as tech giants are 
    increasingly pushing to develop AI agents as they seek to win the AI race. Google made a flurryof 
    AI-related announcementsduring its developer conference in May, including an agent that can make 
    restaurant reservations and buy event tickets, among other tasks. Apple is working on a more 
    advanced version of Siri that can use apps ona user’sbehalf, although that update is delayed indefinitely. Most stock quote data provided by BATS. US market indices are shown in real time, except for the S&P 500 which is refreshed every two minutes. All times are ET. Factset: FactSet Research Systems Inc. All rights reserved. Chicago Mercantile: Certain market data is the property of Chicago Mercantile Exchange Inc. and its licensors. All rights reserved. Dow Jones: The Dow Jones branded indices are proprietary to and are calculated, distributed and marketed by DJI Opco, a subsidiary of S&P Dow Jones Indices LLC and have been licensed for use to S&P Opco, LLC and CNN. Standard & Poor’s and S&P are registered trademarks of Standard & Poor’s Financial Services LLC and Dow Jones is a registered trademark of Dow Jones Trademark Holdings LLC. All content of the Dow Jones branded indices Copyright S&P Dow Jones Indices LLC and/or its affiliates. Fair value provided by IndexArb.com. Market holidays and trading hours provided by Copp Clark Limited. © 2025 Cable News Network. A Warner Bros. Discovery Company. All Rights Reserved.CNN Sans ™ & © 2016 Cable News Network."""
    summary = summarize_article(article)
    print("요약 결과:\n", summary)