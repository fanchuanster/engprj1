
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval
import os

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging

DATAST_FOLDRE = 'data/archive'

class MovieRecommender:

    def __init__(self):
        # self.metadata_df = None
        # self.top5000_movies = None
        movie_datafile = DATAST_FOLDRE+"/movies_metadata.csv"
        if os.path.exists(movie_datafile):
            self.metadata_df = pd.read_csv(movie_datafile, low_memory=False)
            self.top5000_movies = self.get_top_movies_by_score()

    def get_top_movies_by_score(self, quantile=0.9):
        C = self.metadata_df['vote_average'].mean()
        m = self.metadata_df['vote_count'].quantile(quantile)

        movies_df = self.metadata_df.copy()[self.metadata_df['vote_count'] >= m]

        def weighted_rating(row, m=m, C=C):
            v = row['vote_count']
            r = row['vote_average']
            return v/(v+m) * r + m/(m+v) * C

        movies_df['score'] = movies_df.apply(weighted_rating, axis=1)
        movies_df = movies_df.sort_values(['score'], ascending=False)

        return movies_df[['id', 'title', 'vote_count', 'vote_average', 'score', 'overview']]

    def recommend_by_overview(self, title, index_1_based = 1):
        if not hasattr(self, "metadata_df"):
            return None

        movies_df = self.metadata_df.copy()[self.metadata_df['id'].isin(self.top5000_movies.id) | (self.metadata_df['title']==title)]
        movie_to_searchs = movies_df[movies_df['title']==title]
        if movie_to_searchs.empty:
            return None

        assert len(movie_to_searchs.index)==1, "Should be only one movie matching movie title '%s'" % movie_to_searchs

        movie_to_search = movie_to_searchs.iloc[index_1_based-1]
        idx = movies_df.index.get_loc(movie_to_search.name)

        tfidf = TfidfVectorizer(stop_words='english')
        movies_df['overview'].fillna('', inplace=True)

        matrix = tfidf.fit_transform(movies_df['overview'])    
        cosine_sim = linear_kernel(matrix, matrix)
        
        scores = list(enumerate(cosine_sim[idx]))
        movies_df['score_'] = movies_df.apply(lambda row:scores[movies_df.index.get_loc(row.name)][1], axis=1)
        movies_df.sort_values(['score_'], ascending=False, inplace=True)
        recommendations = movies_df[['title', 'score_']].iloc[1 : 6].values.tolist()
        
        # print(recommendations)
        return recommendations
        


    def recommend_by_features(self, metadata_df, movie_title):
        keywords = pd.read_csv(DATAST_FOLDRE+'/keywords.csv', dtype={'id':'Int64'})
        credits = pd.read_csv(DATAST_FOLDRE+'/credits.csv', dtype={'id':'Int64'})
        metadata_df = metadata_df.drop([19730, 29503, 35587])
        metadata_df['id'] = metadata_df['id'].astype('int')

        # print(metadata_df.shape)
        metadata_df = metadata_df.merge(keywords, how='inner', on='id').merge(credits, how='inner', on='id')
        # print(metadata_df.shape)

        features = ['cast', 'crew', 'keywords', 'genres']
        for feature in features:
            # metadata_df[feature] = metadata_df[feature].apply(lambda f:literal_eval(f[feature].lower() if f[feature] else ""), axis=1)
            metadata_df[feature] = metadata_df[feature].apply(literal_eval)
            print(metadata_df[feature].head(5))
        
        def get_director(x):
            for i in x:
                if 'director' in i['job'].lower():
                    return i['name'].lower().replace(" ", "")
            return np.nan

        metadata_df['director'] = metadata_df['crew'].apply(get_director)

        def get_list(x):
            if isinstance(x, list):
                names = [i['name'].lower().replace(" ", "") for i in x]
                #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
                return names[:3]
            return []

        features = ['cast', 'keywords', 'genres']
        for feature in features:
            metadata_df[feature] = metadata_df[feature].apply(get_list)

        # print(metadata_df[['title', 'cast', 'director', 'keywords', 'genres']].head(3))

        def create_soup(x):
            return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
        # Create a new soup feature
        metadata_df['soup'] = metadata_df.apply(create_soup, axis=1)
        metadata_df[['soup']].head(2)

        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(metadata_df['soup'])
        cosine_sim = cosine_similarity(count_matrix, count_matrix)
        metadata_df = metadata_df.reset_index()


def main():
    
    # pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", 1000)

    mr = MovieRecommender()

    quit = False
    while (not quit):
        print("Input the movie title for recommendations like 'Grumpier Old Men', or 'quit' to quit:")
        title = input()
        title = title.strip("' ")
        print(title)
        if title == 'quit':
            quit = True
            continue

        recommendations = mr.recommend_by_overview(title)
        # recommendations = recommend_by_features(top5000_movies, metadata_df, 'Grumpier Old Men')
        
        print(recommendations)


if __name__ == '__main__':
    main()


#         id                          title  vote_count  vote_average
# 2    15602               Grumpier Old Men        92.0           6.5
# 3    31357              Waiting to Exhale        34.0           6.1
# 6    11860                        Sabrina       141.0           6.2
# 7    45325                   Tom and Huck        45.0           5.4
# 13   10858                          Nixon        72.0           7.1
# 14    1408               Cutthroat Island       137.0           5.7
# 23   12665                         Powder       143.0           6.3
# 25   16420                        Othello        33.0           7.0
# 26    9263                   Now and Then        91.0           6.6
# 27   17015                     Persuasion        36.0           7.4
# 29   37557                 Shanghai Triad        17.0           6.5
# 32   78802               Wings of Courage         4.0           6.8
# 34   47018                     Carrington        16.0           6.4
# 36  139405         Across the Sea of Time         2.0           3.5
# 37   33689                   It Takes Two       149.0           6.1
# 39   34615       Cry, the Beloved Country        13.0           6.7
# 40   31174                    Richard III        50.0           6.9
# 41   11443                Dead Presidents        80.0           6.6
# 42   35196                    Restoration        30.0           6.3
# 45   11861  How To Make An American Quilt        38.0           6.5
# 48    8391          When Night Is Falling        10.0           5.9
# 50  117164                 Guardian Angel         3.0           6.3
# 51   11448               Mighty Aphrodite       145.0           6.7
# 52   49133                       Lamerica        11.0           7.7
# 53   26441                  The Big Green        41.0           5.2
# 54   97406                        Georgia        15.0           6.1
# 55  124057        Kids of the Round Table         1.0           3.0
# 56    9089          Home for the Holidays        39.0           6.3
# 58   99040               The Confessional         2.0           6.5
# 59   11359     The Indian in the Cupboard       136.0           5.9