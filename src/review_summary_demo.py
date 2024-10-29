import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# Download NLTK resources (only need to do this once)
nltk.download('punkt')
nltk.download('stopwords')
#from preprocessor import DATA_PREPROCESS_DIR, REVIEW_DATA_PATH, BUSINESS_DATA_PATH, USER_DATA_PATH


#visualisation the distribution of Reviews Contributed by Users
import matplotlib.pyplot as plt

def viz_review_distribution(df):
    """viz_review_distribution

    Args:
        df (pd.dataframe): plot x: No. of Reviews Contributed by a User, y: No. of Users Having a Particular No. of Reviews
    """
    # Count the no. of reviews per user
    user_review_counts = df.groupby('user_id')['review_id'].count()

    # Count the frequency of each unique number of reviews
    review_distribution = user_review_counts.value_counts().sort_index()

    # Create a scatter plot
    plt.figure(figsize=(12, 6))
    plt.scatter(review_distribution.index, review_distribution.values, alpha=0.7)
    plt.xlabel("No. of Reviews Contributed by a User")
    plt.ylabel("No. of Users Having a Particular No. of Reviews")
    plt.title("Distribution of Reviews Contributed by Users")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()

import matplotlib.pyplot as plt

#bounding box of user's activity area
def create_bounding_box(df, df_business, user_id):
    """create_bounding_box

    Args:
        df (pd.dataframe): dataframe of user_review
        df_business (pd.dataframe): dataframe of user_businesses 
        user_id (str): to input a specific user_id 

    Returns:
        (dict): returns a dictionary with keys specifying the minimum and maximum latitude/longitude values.
    """
    # Get all business_ids when given user_id
    user_reviews = df[df['user_id'] == user_id]
    business_ids = user_reviews['business_id']

    # look through n get the business DataFrame by the matched business_ids
    user_businesses = df_business[df_business['business_id'].isin(business_ids)]

    if user_businesses.empty:
        return {"There is no such business id"}
     
    # Bounding box using latitude and longitude
    min_lat = user_businesses['latitude'].min()
    max_lat = user_businesses['latitude'].max()
    min_lon = user_businesses['longitude'].min()
    max_lon = user_businesses['longitude'].max()

    return {
        "min_latitude": min_lat,
        "max_latitude": max_lat,
        "min_longitude": min_lon,
        "max_longitude": max_lon
    }

#top 10 frequent words used in his/her review
def create_top_words(df, user_id, n=10):
    """create_top_words

    Args:
        df (pd.dataframe): dataframe of the user_review
        user_id (str): to input a specific user_id 
        n (int): top 10 words

    Returns:
        (list of tuples): return the top frequent words
    """
    user_reviews = df[df['user_id'] == user_id]['text']
    
    #Using NLTK for the english stopwords
    stop_words = set(stopwords.words('english'))
    
    # Tokenize, filter stopwords, and count words using NLTK
    all_words = []
    for review in user_reviews:
        words = word_tokenize(review.lower())
        # Filter out stopwords and non-alphabetic words
        filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
        all_words.extend(filtered_words)
    
    # Using NLTK FreqDist() to get word frequencies
    freq_dist = FreqDist(all_words)
    
    # Get the top common 'n' words that is top 10
    most_common_words = freq_dist.most_common(n)
    
    return most_common_words


def create_clustered_representative_sentences(df, user_id, n=3, n_clusters=3):
    """create_clustered_representative_sentences

    Args:
        df (pd.dataframe): dataframe of the user_review
        user_id (str): to input a specific user_id 
        n (int): _description_. top 3 representative sentences
        n_clusters (int): 3 clusters to form with K-Means for categorizing similar sentences.

    Returns:
        (list): return a list of top 3 representative sentences from the 3 clusters respectively
    """
    stop_words = list(stopwords.words('english'))
    sentences = df[df['user_id'] == user_id]['text']
    
    if sentences.empty:
        return []
    # Convert sentences to TF-IDF features
    tfidf_convert = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = tfidf_convert.fit_transform(sentences)
    
    # Apply K-Means clustering
    kmeans_model = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans_model.fit(tfidf_matrix)
    clusters_pred = kmeans_model.predict(tfidf_matrix)

    representative_sentences = []
    # The loop will handle each cluster separately, identifying sentences that belong to the current cluster.
    for cluster in range(n_clusters):
        indices = np.where(clusters_pred == cluster)[0]
        # extract the TF-IDF feature vectors of sentences belonging to the current cluster.
        cluster_tfidf = tfidf_matrix[indices]
        #calculate a score for each sentence within the current cluster based on its TF-IDF feature values.
        cluster_sums = cluster_tfidf.sum(axis=1).flatten()
        #get the sentence with the biggest TF-IDF score that is in the current cluster.
        top_sentence_index = indices[cluster_sums.argmax()]
        #populates the representative_sentences list with one sentence per cluster.
        representative_sentences.append(sentences.iloc[top_sentence_index])

    return representative_sentences[:n]

# generate the summary of above return values
def generate_user_review_summary(df,df_business, user_id):
    """generate_user_review_summary

    Args:
        df (pd.dataframe): dataframe of the user_review
        df_business (pd.dataframe): dataframe of the user_business
        user_id (str): to input a specific user_id 

    Returns:
        (dict): Returning a dictionary of the summaries
    """
    # Get the no. of reviews by the user
    num_reviews = df[df['user_id'] == user_id].shape[0]

    #  bounding box for the user's reviewed businesses
    bounding_box = create_bounding_box(df, df_business, user_id)

    # Get top words 
    top_words = create_top_words(df, user_id)

    #  Get representative sentences
    representative_sentences = create_clustered_representative_sentences(df, user_id)
    
    summary = {
        "user_id": user_id,
        "num_reviews": num_reviews,
        "bounding_box": bounding_box,
        "top_words": top_words,
        "representative_sentences": representative_sentences,
    }
    return summary

import json

# Load JSON data from file
with open('CA_business.json', 'r') as f:
    business_data = json.load(f)

with open('CA_review.json', 'r') as f:
    review_data = json.load(f)

# Convert JSON data to a pandas DataFrame
if review_data:
    df = pd.DataFrame(review_data)
    df_business = pd.DataFrame(business_data)
    user_id = "uBW16OCkFKvzdezUKZFuUQ" 
    # Generate the user review summary
    user_summary = generate_user_review_summary(df,df_business, user_id)
    print("Generated User Review Summary:")
    print(user_summary)
else:
    print("No review data available to summarize.")


viz_review_distribution(df)