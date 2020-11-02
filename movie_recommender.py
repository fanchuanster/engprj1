
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging

def get_top_movies_by_score(metadata_df, quantile=0.9):

    C = metadata_df['vote_average'].mean()
    m = metadata_df['vote_count'].quantile(quantile)

    movies_df = metadata_df.copy()[metadata_df['vote_count'] >= m]

    def weighted_rating(row, m=m, C=C):
        v = row['vote_count']
        r = row['vote_average']
        return v/(v+m) * r + m/(m+v) * C

    movies_df['score'] = movies_df.apply(weighted_rating, axis=1)
    movies_df = movies_df.sort_values(['score'], ascending=False)

    return movies_df[['id', 'title', 'vote_count', 'vote_average', 'score', 'overview']]

def get_similar_movies_by_overview(top5000_movies, metadata_df, title):

    movies_df = metadata_df.copy()[metadata_df['id'].isin(top5000_movies.id) | (metadata_df['title']==title)]
    search_movie = movies_df[movies_df['title']==title].iloc[-1]
    idx = movies_df.index.get_loc(search_movie.name)

    print(idx)
    print(movies_df.iloc[idx]['title'])
    # print(metadata_df.iloc[idx]['title'])

    tfidf = TfidfVectorizer(stop_words='english')
    movies_df['overview'].fillna('', inplace=True)

    logger.info('linear_kernel start..')
    matrix = tfidf.fit_transform(movies_df['overview'])    
    cosine_sim = linear_kernel(matrix, matrix)
    logger.info('linear_kernel ended.')
    print(type(cosine_sim))
    scores = list(enumerate(cosine_sim[idx]))
    movies_df['score_'] = movies_df.apply(lambda row:scores[movies_df.index.get_loc(row.name)][1], axis=1)
    movies_df.sort_values(['score_'], ascending=False, inplace=True)
    print(movies_df.head(3))
    return movies_df[['title', 'score_']].iloc[0 : 11]




def main():
    dataset_folder = 'data/archive'
    metadata_df = pd.read_csv(dataset_folder+"/movies_metadata.csv", low_memory=False)

    # pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", 1000)

    top5000 = get_top_movies_by_score(metadata_df)
    print(top5000.shape)

    # recommendations = get_similar_movies_by_overview(top5000, metadata_df, 'Grumpier Old Men')
    recommendations = get_similar_movies_by_overview(top5000, metadata_df, 'The Dark Knight Rises')
    
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