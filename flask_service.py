from flask import Flask
from flask import jsonify
from movie_recommender import MovieRecommender
# import json

app = Flask(__name__)

@app.route("/recommend/<string:movie_title>")
def recommend(movie_title):
    mr = MovieRecommender()
    recommendations = mr.recommend_by_overview(movie_title)
    # return recommendations
    if not recommendations:
        return "no recommendations for %s" % movie_title
    # return jsonify([ { "title":r[0], "score":r[1] } for r in recommendations ])
    return jsonify([ r[0] for r in recommendations ])

if __name__ == "__main__":
    app.run(debug=True)