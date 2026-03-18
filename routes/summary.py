from flask import Blueprint, jsonify, request

summary = Blueprint("summary", __name__)

@summary.route("/summary", methods=["POST"])
def generate_summary():
    data = request.json
    movie_name = data.get("movie_name")

    # Dummy summary
    movie_summary = f"{movie_name} is an AI-generated movie summary."

    return jsonify({
        "status": "success",
        "movie": movie_name,
        "summary": movie_summary
    })
