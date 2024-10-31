import random
from collections import Counter

import matplotlib.pyplot as plt
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from whoosh.query import Term, Every, Or

from searchEngine.engine_config import REVIEW_SUMMARY_DISTRIBUTION_FILE_PATH, \
    REVIEW_SUMMARY_RANDOM_REVIEW_COUNT_THRESHOLD, REVIEW_SUMMARY_USER_ID, USE_REVIEW_SUMMARY_RANDOM_USER, QueryType


class ReviewSummaryRunner:
    _instance = None

    def __new__(cls, search_engine):
        if cls._instance is None:
            cls._instance = super(ReviewSummaryRunner, cls).__new__(cls)
            cls._instance._initialize(search_engine)
        return cls._instance

    def _initialize(self, search_engine):
        self._search_engine = search_engine

    def run(self):
        nltk.download('punkt')
        nltk.download('stopwords')

        all_users_query_type = QueryType.REVIEW_SUMMARY_ALL_USERS
        all_users_query_field_name = all_users_query_type.value[0][0]
        all_users_query_raw_query_data = all_users_query_field_name + ": count num of reviews with respect to every user id "
        all_users_query_data = Every(all_users_query_field_name)

        all_users_query_order = self._search_engine.insert_query(all_users_query_raw_query_data, \
                                                                 all_users_query_type, all_users_query_data)
        self._search_engine.search_entry(all_users_query_order)
        # key:user_id, value: review count with respect to user_id
        review_count_by_user_id_dict = self._search_engine.search_results[all_users_query_order]

        # tmp
        print(len(review_count_by_user_id_dict))
        argmax_user_id = max(review_count_by_user_id_dict, key=review_count_by_user_id_dict.get)
        argmin_user_id = min(review_count_by_user_id_dict, key=review_count_by_user_id_dict.get)
        print("The number of reviews being contributed:")
        print(f"argmax_user_id: {argmax_user_id}, max review count: {review_count_by_user_id_dict[argmax_user_id]}")
        print(f"argmin_user_id: {argmin_user_id}, min review count: {review_count_by_user_id_dict[argmin_user_id]}")
        print("\n")

        if USE_REVIEW_SUMMARY_RANDOM_USER:
            filtered_user_ids = [user_id for user_id, review_count in review_count_by_user_id_dict.items() if
                                 review_count >= REVIEW_SUMMARY_RANDOM_REVIEW_COUNT_THRESHOLD]
            user_id = random.choice(filtered_user_ids)
        else:
            user_id = REVIEW_SUMMARY_USER_ID

        user_id_query_type = QueryType.REVIEW_SUMMARY_SPECIFIC_USER
        user_id_field_name = user_id_query_type.value[0][0]
        raw_user_id_query_data = user_id_query_type.value[0][0] + ":" + user_id
        user_id_query_data = Term(user_id_field_name, user_id)
        user_id_query_order = self._search_engine.insert_query(raw_user_id_query_data, user_id_query_type,
                                                               user_id_query_data)
        self._search_engine.search_entry(user_id_query_order)
        # specific user_id relevant documents from review json
        user_id_results_dict_list = self._search_engine.search_results[user_id_query_order]

        # retrieve business_id set from user_id_results_dict_list and search 
        # in business index by these business_ids
        business_id_query_type = QueryType.REVIEW_SUMMARY_BUSINESS_ID
        business_id_field_name = business_id_query_type.value[0][0]
        business_id_set = set([result_dict[business_id_field_name] for result_dict in user_id_results_dict_list])
        raw_business_id_query_data = business_id_field_name + ":"
        business_id_queries = []
        for business_id in business_id_set:
            raw_business_id_query_data += " " + business_id
            business_id_queries.append(Term(business_id_field_name, business_id))
        business_id_query_data = Or(business_id_queries)
        business_id_query_order = self._search_engine.insert_query(raw_business_id_query_data, business_id_query_type,
                                                                   business_id_query_data)
        self._search_engine.search_entry(business_id_query_order)
        # business_id relevant documents from business json
        business_id_results_dict_list = self._search_engine.search_results[business_id_query_order]

        latitude_field_name = business_id_query_type.value[1][1]
        longitude_field_name = business_id_query_type.value[1][2]
        latitude_list = [result_dict[latitude_field_name] for result_dict in business_id_results_dict_list]
        longitude_list = [result_dict[longitude_field_name] for result_dict in business_id_results_dict_list]
        print("Bounding Box(activity area) of the businesses that the user has reviewed:")
        print(f"latitude min: {min(latitude_list)}, latitude max: {max(latitude_list)}")
        print(f"longitude min: {min(longitude_list)}, longitude max: {max(longitude_list)}")
        print("\n")

        # top 10 frequent words
        # Using NLTK for the English stopwords
        stop_words = set(stopwords.words('english'))
        # Tokenize, filter stopwords, and count words using NLTK
        all_words = []
        for i in user_id_results_dict_list:
            review_text = i.get('text', '')
            words = word_tokenize(review_text.lower())
            # Filter out stopwords and non-alphabetic words
            all_words.extend(word for word in words if word.isalpha() and word not in stop_words)

        # Get the top common 'n' words
        most_common_words = FreqDist(all_words).most_common(10)

        print(f"Top {10} most common words:")
        for word, count in most_common_words:
            print(f"{word}: {count}")
        print("\n")

        # top 3 representative
        stop_words_rep = list(stopwords.words('english'))
        sentences = [i.get('text', '') for i in user_id_results_dict_list if i.get('text', '')]

        # Convert sentences to TF-IDF features
        tfidf_convert = TfidfVectorizer(stop_words=stop_words_rep)
        tfidf_matrix = tfidf_convert.fit_transform(sentences)

        # Apply K-Means clustering
        kmeans_model = KMeans(n_clusters=3, random_state=42, init='k-means++', n_init=10)
        kmeans_model.fit(tfidf_matrix)
        clusters_pred = kmeans_model.predict(tfidf_matrix)

        representative_sentences = []
        # The loop will handle each cluster separately, identifying sentences that belong to the current cluster.
        for cluster in range(3):
            indices = np.where(clusters_pred == cluster)[0]
            # get the TF-IDF feature vectors of sentences belonging to the current cluster.
            cluster_tfidf = tfidf_matrix[indices]
            # calculate a score for each sentence within the current cluster based on its TF-IDF feature values.
            cluster_sums = cluster_tfidf.sum(axis=1).flatten()
            # get the sentence with the biggest TF-IDF score that is in the current cluster.
            top_sentence_index = indices[cluster_sums.argmax()]
            # append the representative_sentences list with one sentence per cluster.
            representative_sentences.append(sentences[top_sentence_index])
        print(f"{3} most representative sentences:")
        for i, sentence in enumerate(representative_sentences[:3], 1):
            print(f"{i}. {sentence}")

        # Count the frequency of each unique number of reviews
        review_distribution = Counter(review_count_by_user_id_dict.values())

        # Sort the distribution by the number of reviews
        sorted_review_distribution = dict(sorted(review_distribution.items()))
        # Create a scatter plot
        plt.figure(figsize=(12, 6))
        plt.scatter(sorted_review_distribution.keys(), sorted_review_distribution.values(), alpha=0.7)
        plt.yscale("log")
        plt.xticks(range(0, 500, 25))
        plt.xlabel("No. of Reviews Contributed by a User")
        plt.ylabel("No. of Users Having a Particular No. of Reviews in log scale")
        plt.title("Distribution of Reviews Contributed by Users")
        plt.grid(True, which="both", linestyle="--", linewidth=0.5)
        plt.savefig(REVIEW_SUMMARY_DISTRIBUTION_FILE_PATH)
        plt.show()
        
