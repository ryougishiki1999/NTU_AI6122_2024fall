import json
import pandas as pd
import nltk
import string
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np
import re
from wordcloud import WordCloud
import random
nltk.download('punkt')
random.seed(0)


with open('business.json', 'r', encoding='utf-8') as business_file:
    businesses = json.load(business_file)


# 读取 review.json 文件
with open('review.json', 'r', encoding='utf-8') as review_file:
    reviews = json.load(review_file)

my_dataset = []
for business in businesses:
    business_reviews = [review for review in reviews if review['business_id'] == business['business_id']]
    my_dataset.append({
        'business_id': business['business_id'],
        'name': business['name'],
        'stars': business['stars'],
        'review_count': business['review_count'],
        'categories': business['categories'],
        'reviews': business_reviews
    })

# 基本统计信息
total_businesses = len(businesses)
total_reviews = sum([len(item['reviews']) for item in my_dataset])

print(f"Selected metropolitan area: California")
print(f"Total businesses: {total_businesses}")
print(f"Total reviews: {total_reviews}")

def deal_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_texts = [word for word in tokens if word not in stop_words and "'" not in word and len(word.strip()) > 1 and not any(char.isdigit() for char in word)]
    punctuation = set(string.punctuation)
    clean_tokens = [word for word in filtered_texts if word not in punctuation]
    lemmatizer = WordNetLemmatizer()
    lemmatized_texts = [lemmatizer.lemmatize(word) for word in clean_tokens]
    processed_texts = [word.lower() for word in lemmatized_texts]
    processed_texts = ' '.join(processed_texts)
    processed_texts = re.sub(r'[^a-zA-Z\s]', '', processed_texts)
    return processed_texts

def process_business(business):
    all_text = " ".join([deal_text(review['text']) for review in business['reviews']])
    words = nltk.word_tokenize(all_text)
    word_freq_before = nltk.FreqDist(words)
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in words]
    word_freq_after = nltk.FreqDist(stemmed_words)
    return word_freq_before, word_freq_after



random_business_1 = random.choice(my_dataset)
word_freq_before_1, word_freq_after_1 = process_business(random_business_1)

print("Top 10 most frequent words before stemming for "+random_business_1['name']+":", word_freq_before_1.most_common(10))
print("Top 10 most frequent words after stemming for "+random_business_1['name']+":", word_freq_after_1.most_common(10))

random_business_2 = random.choice(my_dataset)
while random_business_2 == random_business_1:
    random_business_2 = random.choice(santa_barbara_dataset)
word_freq_before_2, word_freq_after_2 = process_business(random_business_2)

print(f"Top 10 most frequent words before stemming for "+random_business_2['name']+":", word_freq_before_2.most_common(10))
print(f"Top 10 most frequent words after stemming for "+random_business_2['name']+":", word_freq_after_2.most_common(10))


# 可视化词频分布
def plot_word_freq_distribution(word_freq, title):
    top_words = [word for word, freq in word_freq.most_common(20)]
    log_top_freqs = [np.log(freq + 1) for word, freq in word_freq.most_common(20)]
    plt.figure(figsize=(10, 6))
    plt.plot(top_words, log_top_freqs, marker='o')
    plt.title(title)
    plt.xlabel('Words')
    plt.ylabel('Log Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_word_freq_distribution(word_freq_before_1, f'Word Frequency Distribution Before Stemming on a log scale for '+random_business_1['name'])
plot_word_freq_distribution(word_freq_after_1, f'Word Frequency Distribution After Stemming on a log scale for '+random_business_1['name'])
plot_word_freq_distribution(word_freq_before_2, f'Word Frequency Distribution Before Stemming on a log scale for '+random_business_2['name'])
plot_word_freq_distribution(word_freq_after_2, f'Word Frequency Distribution After Stemming on a log scale for '+random_business_2['name'])


def generate_word_cloud(word_freq, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')
    plt.show()

generate_word_cloud(dict(word_freq_after_1.most_common(10)), f'Word Cloud After Stemming for {random_business_1["name"]}')
generate_word_cloud(dict(word_freq_after_2.most_common(10)), f'Word Cloud After Stemming for {random_business_2["name"]}')



df_before_1 = pd.DataFrame(word_freq_before_1.most_common(), columns=['Word', 'Frequency'])
df_after_1 = pd.DataFrame(word_freq_after_1.most_common(), columns=['Word', 'Frequency'])
df_before_2 = pd.DataFrame(word_freq_before_2.most_common(), columns=['Word', 'Frequency'])
df_after_2 = pd.DataFrame(word_freq_after_2.most_common(), columns=['Word', 'Frequency'])

df_before_1.to_excel(random_business_1['name']+'_before_stemming.xlsx', index=False)
df_after_1.to_excel(random_business_1['name']+'_after_stemming.xlsx', index=False)
df_before_2.to_excel(random_business_2['name']+'_before_stemming.xlsx', index=False)
df_after_2.to_excel(random_business_2['name']+'_after_stemming.xlsx', index=False)