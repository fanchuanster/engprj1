from flask import Flask
from mvie_recommender import MovieRecommender
# import json

app = Flask(__name__)

@app.route("/recommend/<string:movie_title>")
def recommend(movie_title):
    mr = MovieRecommender()
    recommendations = mr.recommend_by_overview(title)
    return recommendations

if __name__ == "__main__":
    app.run(debug=True)