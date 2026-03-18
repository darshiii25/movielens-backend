from flask import Blueprint, request, jsonify
from ml_models.content_based_model import content_recommend

recommendation = Blueprint("recommendation", __name__)

@recommendation.route("/recommend", methods=["POST"])
def recommend():

    data = request.json
    movie = data.get("movie_name")
    user = data.get("user_id")

    content_movies = content_recommend(movie)

    return jsonify({
        "content_based": content_movies
    })