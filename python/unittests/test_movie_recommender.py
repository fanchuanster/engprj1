import unittest
import os, sys, inspect
import shutil

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from movie_recommender import MovieRecommender

class TestMovieRecommender(unittest.TestCase):
    def setUp(self):
        self.mr = MovieRecommender()

    def test_successful_recommendation(self):
        movie_title = 'Waiting to Exhale'
        recommendations = self.mr.recommend_by_overview(movie_title)
        self.assertIsNotNone(recommendations, "should recommend some movies with input movie title " + movie_title)
        self.assertGreater(len(recommendations), 4, "should recommend more than 4 movies with input movie title" + movie_title)
        print("recommendations for '{}' are:\n{}".format(movie_title, recommendations))

    def test_recommend_nothing_with_invalid_input(self):
        invalid_movie_title = "xxxxxtttttyyy xxx"
        recommendations = self.mr.recommend_by_overview(invalid_movie_title)
        self.assertIsNone(recommendations, "should recommend none with invalid input movie title " + invalid_movie_title)

    def test_input_movie_should_not_be_recommended(self):
        movie_title = 'Grumpier Old Men'
        recommendations = self.mr.recommend_by_overview(movie_title)
        self.assertNotIn(movie_title, recommendations, movie_title + " should not be recommended for itself")

    def test_recommendations_descending_order(self):
        movie_title = 'Grumpier Old Men'
        recommendations = self.mr.recommend_by_overview(movie_title)
        prev = recommendations[0]
        for r in recommendations:
            self.assertGreaterEqual(prev[1], r[1], "recommendations should be in descending order as best first: {}".format(recommendations))
            prev = r



if __name__ == '__main__':
    unittest.main()