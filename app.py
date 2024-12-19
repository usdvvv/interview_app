from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import sqlite3
from flask_cors import CORS
import warnings

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Hugging Face NLP models
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
question_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
warnings.filterwarnings("ignore", category=FutureWarning)

# Database setup function
def init_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        response TEXT,
        sentiment TEXT,
        confidence REAL,
        relevance TEXT,
        relevance_score REAL,
        category TEXT
    )
    """)
    conn.commit()
    conn.close()

# Initialize database on app start
init_db()

# Route: Home
@app.route('/')
def home():
    return render_template('index.html', credits="Created, designed, and developed by Seif Eddine Mezned")

# Route: Evaluate user response
@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    user_response = data.get('response')
    category = data.get('category')

    # Perform NLP analysis
    sentiment = sentiment_analyzer(user_response)
    relevance = question_classifier(user_response, candidate_labels=[category])

    # Prepare feedback
    feedback = {
        "sentiment": sentiment[0]["label"],
        "confidence": sentiment[0]["score"],
        "relevance": relevance["labels"][0],
        "relevance_score": relevance["scores"][0]
    }

    # Save response to database
    save_response(user_response, feedback, category)

    return jsonify(feedback)

# Save user responses to SQLite database
def save_response(response, feedback, category):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO responses (response, sentiment, confidence, relevance, relevance_score, category) VALUES (?, ?, ?, ?, ?, ?)",
        (response, feedback["sentiment"], feedback["confidence"], feedback["relevance"], feedback["relevance_score"], category)
    )
    conn.commit()
    conn.close()

# Route: Progress Tracker
@app.route('/progress')
def progress():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM responses")
    data = cursor.fetchall()
    conn.close()
    return render_template('progress.html', data=data)

# Route: Contact Page
@app.route('/contact')
def contact():
    contact_info = {
        "linkedin": "https://www.linkedin.com/in/seif-eddine-mezned-b743b530b/",
        "email": "seifmezned.2004@gmail.com"
    }
    return render_template('contact.html', contact_info=contact_info)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
