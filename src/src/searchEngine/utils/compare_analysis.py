from tqdm import tqdm
from joblib import Parallel, delayed
import spacy
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from searchEngine.engine_config import REVIEW_DATA_PATH, BUSINESS_DATA_PATH
import warnings
warnings.filterwarnings('ignore')


def compare_text():
    # read JSON file
    df = pd.read_json(REVIEW_DATA_PATH)
    df.head()
    df_business = pd.read_json(BUSINESS_DATA_PATH)
    df_business.head()

    # # 
    # sentences = []
    # for record in df['text'].values[:1000]:
    #     # sent_tokenize By sentence segmentation,the data has been processed into sentences
    #     sentences.extend(sent_tokenize(record))
    # df['sentences'] = sentences


    comparison_keywords = ["better", "worse", "more than", "less than", "compared to", "as good as"]
  
    comparison_sentences = [sentence for sentence in df['text'] if any(keyword in sentence for keyword in comparison_keywords)]

    # Print the first few sentences that contain comparisons
    print("sentences contain comparisons")
    for sentence in comparison_sentences[:10]:
        print(sentence)


    nlp = spacy.load("en_core_web_sm")


    # Find sentences that contain comparisons
    def contains_comparison(sentence):
        doc = nlp(sentence)
        for token in doc:
            if token.lemma_ in ["compare", "better", "worse"] and token.dep_ in ["advmod", "amod", "prep"]:
                return True
        return False


    # Parallel optimization
    # result = Parallel(backend='multiprocessing', n_jobs=20)(delayed(contains_comparison)(text) for text in tqdm(df['text']))
    # df['contain_comparison'] = result
    df['contain_comparison'] = df['text'].map(lambda x: contains_comparison(x))

    # Filter the text that contains the comparison
    df_business = df_business[df_business['business_id'].isin(df[df['contain_comparison'] == True]['business_id'].unique())].reset_index(drop=True)

    # Cluster processing
    encoder = OneHotEncoder(sparse=False)
    encoded_data = encoder.fit_transform(df_business[['city']])

    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(['city']))

    df_business = pd.concat([df_business, encoded_df], axis=1)
    df_business.head()

    # Standardized data
    scaler = StandardScaler()
    data_normalized = scaler.fit_transform(df_business[['latitude', 'longitude', 'stars', 'review_count']])

    df_business[['latitude', 'longitude', 'stars', 'review_count']] = data_normalized
    df_business.head()

    dbscan = DBSCAN(eps=1, min_samples=5)
    cols = ['latitude', 'longitude', 'stars', 'review_count', 'is_open',
            'city_Carpinteria', 'city_Cerritos', 'city_Goleta', 'city_Isla Vista', 'city_Montecito',
            'city_Santa Barbara', 'city_Santa Clara', 'city_Summerland', 'city_Truckee']
    df_business['lable'] = dbscan.fit_predict(df_business[cols].reset_index(drop=True))
    print(df_business['lable'].value_counts())


if __name__ == '__main__':
    compare_text()
