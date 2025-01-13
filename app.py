from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.scraper import extract_reviews

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests
@app.route('/')
def home():
    return "Welcome to the Review Scraper API!"

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    # Extract the 'page' query parameter
    page_url = request.args.get('page')
    #if not page_url:
       # return jsonify({"error": "Missing 'page' query parameter"}), 400
    
    # Placeholder response for testing
    return jsonify({
        "reviews_count": 0,
        "reviews": [],
        "page_url": page_url
    })
    
    reviews = extract_reviews(page_url)
    response = {
        "page_url": page_url,
        "reviews_count": len(reviews),
        "reviews": reviews
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)