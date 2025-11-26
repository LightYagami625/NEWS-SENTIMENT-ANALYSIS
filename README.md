# News-Senti

News-Senti is a web-based sentiment analysis tool that fetches the latest news headlines and evaluates their sentiment using Natural Language Processing (NLP). It categorizes news into Positive, Negative, or Neutral and provides a sentiment score for each article.

## Features

- **Live News Fetching**: Retrieves real-time top headlines using NewsAPI.
- **Sentiment Analysis**: Uses NLTK's VADER lexicon to analyze the sentiment of headlines and article content.
- **Category Filtering**: Filter news by categories such as Business, Entertainment, Health, Science, Sports, and Technology.
- **Search Functionality**: Search for specific topics or keywords.
- **Interactive UI**:
    - Hover over headlines to see article details (Image, Summary, Link).
    - Visual sentiment indicators (Green for Positive, Red for Negative, Gray for Neutral).
    - Loading animations for better user experience.
- **Data Persistence**: Saves analyzed headlines to a local SQLite database for record-keeping.
- **Responsive Design**: Optimized for both desktop and mobile viewing.

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3 (Vanilla)
- **NLP Library**: NLTK (VADER Sentiment Intensity Analyzer)
- **Data Processing**: Pandas
- **Database**: SQLite
- **API**: NewsAPI

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd News-Sentiment-Analysis
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   - This project uses NewsAPI to fetch headlines.
   - Open `src/config.py` and replace the `API_KEY` variable with your own API key from [NewsAPI](https://newsapi.org/).

## Usage

1. **Run the application**
   ```bash
   python main.py
   ```

2. **Access the web interface**
   - Open your web browser and navigate to `http://127.0.0.1:5000`.

3. **Analyze News**
   - Select a category or enter a search term.
   - Click "Scrape & Analyze Headlines".
   - View the overall sentiment stats and the list of top headlines with their individual sentiment scores.

## Project Structure

```
News-Sentiment-Analysis/
├── database/
│   ├── db.py            # Database connection and operations
│   └── headlines.db     # SQLite database file (created on run)
├── src/
│   ├── Analysis.py      # Sentiment analysis logic using NLTK
│   ├── config.py        # Configuration (API Key, URLs)
│   └── newsApi.py       # Functions to fetch data from NewsAPI
├── static/
│   ├── style.css        # Application styling
│   └── ...              # Images and icons
├── templates/
│   └── index.html       # Main HTML template
├── main.py              # Flask application entry point
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## API Endpoints

The application also exposes an endpoint for JSON responses:

- **GET /scrape**
    - Parameters:
        - `category` (optional): e.g., 'technology', 'sports'
        - `query` (optional): Search term
        - `api` (optional): Set to '1' to receive a JSON response instead of HTML.
    - Example: `http://127.0.0.1:5000/scrape?category=technology&api=1`

## License

This project is open source and available for educational purposes.
