# include/py_scripts/reddit_nlp.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ----------------------------
# Sentiment Analysis
# ----------------------------
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text: str) -> str:
    if not text:
        return "Neutral"
    score = analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# ----------------------------
# Intent Detection
# ----------------------------
def detect_intent(text: str) -> str:
    if not text or text.strip() == "":
        return "Unknown"
    
    text = text.strip()
    text_lower = text.lower()
    words = text_lower.split()
    first_word = words[0] if words else ""

    # Keyword categories
    question_words = {"who","what","when","where","why","how","which","whom","whose","is","are","can","do","does","did","could","would","should","will","shall","may","might"}
    help_keywords = ["help","issue","error","fail","problem","stuck","can't","cannot","unable","trouble","support","debug"]
    news_keywords = ["released","launch","announced","update","available","breaking","news"]
    discussion_keywords = ["think","thoughts","opinion","suggestions","should we","would it be","what are your views"]
    tutorial_keywords = ["how to","step by step","guide","tutorial","walkthrough","explained"]
    complaint_keywords = ["hate","terrible","worst","bad","slow","bug","crash","broken","annoying"]
    positive_keywords = ["love","amazing","awesome","great","fantastic","wonderful","cool"]
    meme_keywords = ["😂","🤣","meme","funny","joke","lol"]
    hiring_keywords = ["hiring","job","career","vacancy","apply","opening"]
    event_keywords = ["summit","conference","webinar","meetup","event"]
    compare_keywords = ["vs","versus","better than","compare","comparison"]
    showcase_keywords = ["project","portfolio","showcase","demo","presentation"]
    resource_request_keywords = ["looking for","recommend","suggest","resources"]

    # Intent rules
    if text.endswith("?") or first_word in question_words:
        return "Question"
    if any(word in text_lower for word in help_keywords):
        return "Help Request"
    if any(word in text_lower for word in news_keywords):
        return "Sharing News"
    if any(phrase in text_lower for phrase in discussion_keywords):
        return "Discussion Starter"
    if any(phrase in text_lower for phrase in tutorial_keywords):
        return "Knowledge Sharing"
    if any(word in text_lower for word in complaint_keywords):
        return "Complaint / Negative Feedback"
    if any(word in text_lower for word in positive_keywords):
        return "Appreciation / Opinion"
    if any(word in text_lower for word in meme_keywords):
        return "Meme / Joke"
    if any(word in text_lower for word in hiring_keywords):
        return "Job Opportunity / Hiring"
    if any(word in text_lower for word in event_keywords):
        return "Event / Webinar"
    if any(word in text_lower for word in compare_keywords):
        return "Comparison / Debate"
    if any(word in text_lower for word in showcase_keywords):
        return "Showcase / Portfolio"
    if any(phrase in text_lower for phrase in resource_request_keywords):
        return "Request for Resources"

    if len(words) <= 6 and "?" not in text:
        return "Short Statement / Meme"
    
    return "Other"