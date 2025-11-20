import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

# Ensure lexicon is downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(articles):
    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(articles)
    
    if df.empty:
        return []

    # Calculate scores
    df['score'] = df['title'].apply(lambda title: sia.polarity_scores(title)['compound'])
    
    # Assign labels based on score
    def get_label(score):
        if score >= 0.05: return 'positive'
        elif score <= -0.05: return 'negative'
        else: return 'neutral'

    df['sentiment'] = df['score'].apply(get_label)

    # Convert the DataFrame back to a list of dictionaries for the database/API
    # We only keep relevant columns
    result_data = df[['source', 'title', 'sentiment', 'score']].to_dict(orient='records')
    
    return result_data