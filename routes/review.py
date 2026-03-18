# from flask import Blueprint, jsonify, request

# review = Blueprint("review", __name__)

# @review.route("/review", methods=["POST"])
# def submit_review():
#     data = request.json
#     review_text = data.get("review")

#     # Dummy sentiment
#     sentiment = "Positive"

#     return jsonify({
#         "status": "success",
#         "review": review_text,
#         "sentiment": sentiment
#     })
from flask import Blueprint, request, jsonify
from utils.db import get_db_connection

review = Blueprint('review', __name__)

@review.route('/review', methods=['POST'])
def add_review():

    data = request.json
    movie_name = data.get("movie_name")
    review_text = data.get("review")

    # Temporary sentiment logic (later ML model will replace this)
    if "good" in review_text.lower():
        sentiment = "Positive"
    else:
        sentiment = "Negative"

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO reviews (movie_name, review, sentiment) VALUES (%s, %s, %s)"
    cursor.execute(query, (movie_name, review_text, sentiment))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Review added successfully",
        "sentiment": sentiment
    })