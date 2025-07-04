# 🎯 YouTube Comment Sentiment Analyzer

A Streamlit app that analyzes the sentiment of YouTube video comments (positive, negative, or neutral) using NLP. Found this academic project while cleaning up local files and decided to share it here.

## 🔍 Features

- Extract comments using YouTube Data API
- Analyze sentiments with VADER
- Visualize results via bar and pie charts
- Display video and channel statistics
- Download comments as CSV

## 🛠️ Tech Stack

- Python
- Streamlit
- Google API Client
- VADER Sentiment Analysis (NLTK)
- Plotly (for visualization)
- dotenv (for API key management)

## 🚀 How to Run

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set `YOUTUBE_API_KEY` in a `.env` file
4. Run the app: `streamlit run app.py`

