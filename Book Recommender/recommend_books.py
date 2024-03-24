import pandas as pd
import numpy as np

books = pd.read_csv('BookRecommendation/Books.csv', low_memory=False)
ratings = pd.read_csv('BookRecommendation/Ratings.csv', low_memory=False)
users = pd.read_csv('BookRecommendation/Users.csv', low_memory=False)

ratings_book_title = pd.merge(ratings, books, on='ISBN')
ratings_book_title = ratings_book_title.drop(['Book-Author', 'Image-URL-M', 'Image-URL-L'], axis=1)


final_df = ratings_book_title.merge(users.drop('Age', axis=1), on='User-ID')
final_df['Location'] = final_df['Location'].str.split(',').str[-1].str.strip()


# Require users to have a certain amount of ratings to be considered
# user_rating_threshold value can be changed to require more ratings per user or less
user_rating_threshold = 50
rating_per_user = final_df.groupby('User-ID')['Book-Rating'].count()

# Remove users with less than 51 ratings
users_above_threshold = rating_per_user[rating_per_user > user_rating_threshold].index
acceptable_user_ratings = final_df[final_df['User-ID'].isin(users_above_threshold)]

# Require books to have a certain amount of ratings to be considered
# book_rating_threshold value can be changed to require more ratings per book or less
book_rating_threshold = 50
book_num_ratings = acceptable_user_ratings.groupby('Book-Title').count()['Book-Rating']

# Remove books with less than 50 ratings
acceptable_books = book_num_ratings[book_num_ratings > book_rating_threshold].index

# collect the intersection of books above the threshold and ratings from users above the threshold on those books
ratings_final = acceptable_user_ratings[acceptable_user_ratings['Book-Title'].isin(acceptable_books)]

# Create a pivot table to see the ratings of each book by each user
pt = ratings_final.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
pt.fillna(0, inplace=True)

def recommend(book_title):
    """Create a recommendation based on the book title given"""