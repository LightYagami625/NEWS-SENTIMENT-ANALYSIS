import flask
from flask import jsonify, send_from_directory, render_template, request
import os
from src.newsApi import fetch_headlines
from database.db import init_db, save_headlines 
from src.Analysis import analyze_sentiment

# Initialize Flask app with static folder
app = flask.Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['GET'])
def scrape_and_analyze():
    
    headlines = fetch_headlines()

    if not headlines:
        # support both rendered page and API call
        if request.args.get('api') == '1' or request.accept_mimetypes.best == 'application/json':
            return jsonify({"error": "No headlines found"}), 404
        return render_template('index.html', error="No headlines found", data=[])

    headlines_with_sentiment = analyze_sentiment(headlines)  # expected: list of dicts with 'score' key
    top5 = sorted(headlines_with_sentiment, key=lambda x: x.get("score", 0), reverse=True)[:5]

    if headlines_with_sentiment:
        # robustly extract numeric scores
        all_scores = []
        for item in headlines_with_sentiment:
            try:
                s = float(item.get('score', 0))
            except Exception:
                s = 0.0
            all_scores.append(s)

        average_score = sum(all_scores) / len(all_scores) if all_scores else 0.0

        # sentiment_text mapping (adjust thresholds as you like)
        if average_score >= 0.5:
            overall_sentiment = 'positive'
            sentiment_text = 'Very Positive'
        elif average_score >= 0.05:
            overall_sentiment = 'positive'
            sentiment_text = 'Positive'
        elif average_score <= -0.5:
            overall_sentiment = 'negative'
            sentiment_text = 'Very Negative'
        elif average_score <= -0.05:
            overall_sentiment = 'negative'
            sentiment_text = 'Negative'
        else:
            overall_sentiment = 'neutral'
            sentiment_text = 'Neutral'
    else:
        average_score = 0.0
        overall_sentiment = 'neutral'
        sentiment_text = 'Neutral'

    # persist results

    save_headlines(headlines_with_sentiment)
    

    # If the caller asked for JSON API, return JSON
    if request.args.get('api') == '1' or request.accept_mimetypes.best == 'application/json':
        return jsonify({
            "message": f"Processed {len(headlines_with_sentiment)} headlines.",
            "overall_sentiment": overall_sentiment,
            "sentiment_text": sentiment_text,
            "average_score": average_score,
            "data": headlines_with_sentiment
        })

    # otherwise render the page with variables for Jinja
    return render_template(
        'index.html',
        message=f"Processed {len(headlines_with_sentiment)} headlines.",
        overall_sentiment=overall_sentiment,
        sentiment_text=sentiment_text,
        average_score=average_score,
        data=headlines_with_sentiment,
        top5=top5
    )


if __name__ == '__main__':
    init_db()
    app.run(debug=True)