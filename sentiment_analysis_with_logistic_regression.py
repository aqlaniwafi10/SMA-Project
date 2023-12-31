# -*- coding: utf-8 -*-
"""Sentiment Analysis with Logistic Regression

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11tVMJapOUyYp7RoBY8vmFD042_JxjxO6
"""

!pip install sastrawi -q

"""*Author: Yasir Abdur Rohman*


---


"""

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

import requests

"""# Dataset

Dataset opini film diambil dari

```
Antinasari, P., Perdana, R., & Fauzi, M. (2017). Analisis Sentimen Tentang Opini Film Pada Dokumen Twitter Berbahasa Indonesia Menggunakan Naive Bayes Dengan Perbaikan Kata Tidak Baku. Jurnal Pengembangan Teknologi Informasi Dan Ilmu Komputer, 1(12), 1733-1741. Diambil dari https://j-ptiik.ub.ac.id/index.php/j-ptiik/article/view/629
```


"""

# get dataset
!wget https://gist.githubusercontent.com/yasirabd/08928c274fbb2620c170acc4f47fc6d3/raw/91c01187e8a40b3c3c76e8ca087ff9e2dc62cf0d/opini_film.csv

# load dataset into pandas
data = pd.read_csv('opini_film.csv')
data.head()

"""# Exploratory Data Analysis (EDA)"""

# check missing value
data.isnull().sum()

# check the number of positive and negative tweets
data['Sentiment'].value_counts()

# wordcloud tweet sentiment positive
data_pos = data[data['Sentiment'] == 'positive']

all_text = ' '.join(word for word in data_pos['Text Tweet'])
wordcloud = WordCloud(colormap='Greens', width=1000, height=800, mode='RGBA', background_color='white').generate(all_text)

plt.figure(figsize=(20,10), dpi=80)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()

# wordcloud tweet sentiment negative
data_neg = data[data['Sentiment'] == 'negative']

all_text = ' '.join(word for word in data_neg['Text Tweet'])
wordcloud = WordCloud(colormap='Reds', width=1000, height=800, mode='RGBA', background_color='white').generate(all_text)

plt.figure(figsize=(20,10), dpi=80)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()

"""- Pada wordcloud dokumen bersentimen positive muncul kata-kata sentimen positive seperti `bagus`, `keren`, `menarik`, dan `bangga`.
- Pada wordcloud dokumen bersentimen negative muncuk kata-kata sentimen negative seperti `kecewa`, `jelek`, `kurang`, dan `parah`.
- Terdapat *stopwords* pada dokumen bersentimen positive dan negative seperti kata-kata `yang`, `ini`, `juga`, dan `aja` yang perlu dihapus pada tahap *preprocessing*.

# Preprocessing

Tahap ini melakukan langkah-langkah berikut:
- Cleaning text
- Lowercase
- Remove stopwords
- Stemming / lemmatization
- Tokenization
"""

import re

# cleaning text
def cleaning_text(text):
    # remove url
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text =  url_pattern.sub(r'', text)

    # remove hashtags
    # only removing the hash # sign from the word
    text = re.sub(r'#', '', text)

    # remove mention handle user (@)
    text = re.sub(r'@[\w]*', ' ', text)

    # remove punctuation
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in text.lower():
        if x in punctuations:
            text = text.replace(x, " ")

    # remove extra whitespace
    text = text.strip()

    # lowercase
    text = text.lower()
    return text

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')

# CONSTRUCT STOPWORDS
rama_stopword = "https://raw.githubusercontent.com/ramaprakoso/analisis-sentimen/master/kamus/stopword.txt"
yutomo_stopword = "https://raw.githubusercontent.com/yasirutomo/python-sentianalysis-id/master/data/feature_list/stopwordsID.txt"
fpmipa_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/fpmipa-stopwords.txt"
sastrawi_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/sastrawi-stopwords.txt"
aliakbar_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/aliakbars-bilp.txt"
pebahasa_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-list/pebbie-pebahasa.txt"
elang_stopword = "https://raw.githubusercontent.com/onlyphantom/elangdev/master/elang/word2vec/utils/stopwords-id.txt"
nltk_stopword = stopwords.words('indonesian')

# create path url for each stopword
path_stopwords = [rama_stopword, yutomo_stopword, fpmipa_stopword, sastrawi_stopword,
                  aliakbar_stopword, pebahasa_stopword, elang_stopword]

# combine stopwords
stopwords_l = nltk_stopword
for path in path_stopwords:
    response = requests.get(path)
    stopwords_l += response.text.split('\n')

custom_st = '''
yg yang dgn ane smpai bgt gua gwa si tu ama utk udh btw
ntar lol ttg emg aj aja tll sy sih kalo nya trsa mnrt nih
ma dr ajaa tp akan bs bikin kta pas pdahl bnyak guys abis tnx
bang banget nang mas amat bangettt tjoy hemm haha sllu hrs lanjut
bgtu sbnrnya trjadi bgtu pdhl sm plg skrg
'''

# create dictionary with unique stopword
st_words = set(stopwords_l)
custom_stopword = set(custom_st.split())

# result stopwords
stop_words = st_words | custom_stopword
print(f'Stopwords: {list(stop_words)[:5]}')

# remove stopwords
from nltk import word_tokenize, sent_tokenize

def remove_stopword(text, stop_words=stop_words):
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return ' '.join(filtered_sentence)

# stemming and lemmatization
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def stemming_and_lemmatization(text):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return stemmer.stem(text)

# tokenization
def tokenize(text):
    return word_tokenize(text)

# example
text = 'Semalam nonton film ini, paginya ane download, malem langsung nonton.. ane smpai begadang.. hasilnya? Ane Kecewa... http://fb.me/13sZi5lbC'
print(f'Original text: \n{text}\n')

# cleaning text and lowercase
text = cleaning_text(text)
print(f'Cleaned text: \n{text}\n')

# remove stopwords
text = remove_stopword(text)
print(f'Removed stopword: \n{text}\n')

# stemming and lemmatization
text = stemming_and_lemmatization(text)
print(f'Stemmed and lemmatized: \n{text}\n')

# tokenization
text = tokenize(text)
print(f'Tokenized: \n{text}')

# pipeline preprocess
def preprocess(text):
    # cleaning text and lowercase
    output = cleaning_text(text)

    # remove stopwords
    output = remove_stopword(output)

    # stemming and lemmatization
    output = stemming_and_lemmatization(output)

    # tokenization
    output = tokenize(output)

    return output

# test pipeline preprocess
text = 'Semalam nonton film ini, paginya ane download, malem langsung nonton.. ane smpai begadang.. hasilnya? Ane Kecewa... http://fb.me/13sZi5lbC'
preprocess(text)

# implement preprocessing
preprocessed_data = data.copy()
preprocessed_data['Text Tweet'] = data['Text Tweet'].map(preprocess)

preprocessed_data.head()

preprocessed_data['Text Tweet'][0]

"""Data sudah dilakukan preprocessing untuk keseluruhan.

Tahap berikutnya melakukan split dataset menjadi data train dan data test.

# Split Dataset
"""

from sklearn.model_selection import train_test_split

X = preprocessed_data['Text Tweet']
y = preprocessed_data['Sentiment']

X.head()

# mapping, negative = 0, positive = 1
y = y.map({'negative':0, 'positive':1})
y.head()

train_x, test_x, train_y, test_y = train_test_split(X, y,
                                                    test_size=0.1,
                                                    stratify=y,
                                                    random_state=2021)

train_x.shape, train_y.shape, test_x.shape, test_y.shape

train_x.head()

"""# Feature Extraction

## Build frequency dictionary
"""

def build_freqs(tweets, ys):
    """Build frequencies.
    Input:
        tweets: a list of tweets
        ys: an m x 1 array with the sentiment label of each tweet
            (either 0 or 1)
    Output:
        freqs: a dictionary mapping each (word, sentiment) pair to its
        frequency
    """
    # Convert np array to list since zip needs an iterable.
    # The squeeze is necessary or the list ends up with one element.
    # Also note that this is just a NOP if ys is already a list.
    yslist = np.squeeze(ys).tolist()

    # Start with an empty dictionary and populate it by looping over all tweets
    # and over all processed words in each tweet.
    freqs = {}
    for y, tweet in zip(yslist, tweets):
        for word in tweet:
            pair = (word, y)
            if pair in freqs:
                freqs[pair] += 1
            else:
                freqs[pair] = 1

    return freqs

# create vocabulary / dictionary frequencies
freqs = build_freqs(train_x.tolist(), train_y.tolist())

# check the output
print("type(freqs) = " + str(type(freqs)))
print("len(freqs) = " + str(len(freqs.keys())))

# check frequency
print(f"Freq dari 'kecewa' untuk sentiment 'positive': {freqs[('kecewa', 1)]}")
print(f"Freq dari 'kecewa' untuk sentiment 'negative': {freqs[('kecewa', 0)]}")

"""## Extract Features"""

def extract_features(tweet, freqs):
    '''
    Input:
        tweet: a list of words for one tweet
        freqs: a dictionary corresponding to the frequencies of each tuple (word, label)
    Output:
        x: a feature vector of dimension (1,3)
    '''

    # 3 elements in the form of a 1 x 3 vector
    x = np.zeros((1, 3))

    #bias term is set to 1
    x[0,0] = 1

    # loop through each word in the list of words
    for word in tweet:

        # increment the word count for the positive label 1
        x[0,1] += freqs.get((word, 1.),0)

        # increment the word count for the negative label 0
        x[0,2] += freqs.get((word, 0.),0)

    assert(x.shape == (1, 3))
    return x

# test extract features function
tmp = extract_features(train_x.to_numpy()[0], freqs)

print(f'text: {train_x.to_numpy()[0]}')
print(f'feature extraction result: {tmp}')

# test 2
# check for when the words are not in the freqs dictionary
tmp2 = extract_features('wkwkwk wkwkkwkwkwkwkwk xaxaxaxa', freqs)
print(tmp2)

# extract all of the features

# collect the features 'x' and stack them into a matrix 'X'
X_train = np.zeros((len(train_x), 3))
for i in range(len(train_x)):
    X_train[i, :]= extract_features(train_x.to_numpy()[i], freqs)

X_train[:5]

"""# Logistic Regression"""

# create sigmoid function
def sigmoid(z):
    '''
    Input:
        z: is the input (can be a scalar or an array)
    Output:
        h: the sigmoid of z
    '''
    # calculate the sigmoid of z
    h = 1 / (1 + np.exp(-z))

    return h

# test sigmoid function
sigmoid(-1.4721)

# create gradient descent function

def gradientDescent(x, y, theta, alpha, num_iters):
    '''
    Input:
        x: matrix of features which is (m,n+1)
        y: corresponding labels of the input matrix x, dimensions (m,1)
        theta: weight vector of dimension (n+1,1)
        alpha: learning rate
        num_iters: number of iterations you want to train your model for
    Output:
        J: the final cost
        theta: your final weight vector
    Hint: you might want to print the cost to make sure that it is going down.
    '''
    # get 'm', the number of rows in matrix x
    m = x.shape[0]

    for i in range(0, num_iters):

        # get z, the dot product of x and theta
        z = np.dot(x,theta)

        # get the sigmoid of z
        h = sigmoid(z)

        # calculate the cost function
        J = -1./m * (np.dot(y.transpose(), np.log(h)) + np.dot((1-y).transpose(),np.log(1-h)))

        # update the weights theta
        theta = theta = theta - (alpha/m) * np.dot(x.transpose(),(h-y))

    J = float(J)
    return J, theta

# Check the function
# Construct a synthetic test case using numpy PRNG functions
np.random.seed(1)
# X input is 10 x 3 with ones for the bias terms
tmp_X = np.append(np.ones((10, 1)), np.random.rand(10, 2) * 2000, axis=1)
# Y Labels are 10 x 1
tmp_Y = (np.random.rand(10, 1) > 0.35).astype(float)

# Apply gradient descent
tmp_J, tmp_theta = gradientDescent(tmp_X, tmp_Y, np.zeros((3, 1)), 1e-8, 700)
print(f"The cost after training is {tmp_J:.8f}.")
print(f"The resulting vector of weights is {[round(t, 8) for t in np.squeeze(tmp_theta)]}")

"""## Training"""

# training labels corresponding to X
Y_train = np.expand_dims(train_y.to_numpy(), axis=1)

# Apply gradient descent
init_theta = np.zeros((3, 1))
init_alpha = 1e-4
iter = 3000

J, theta = gradientDescent(X_train, Y_train, init_theta, init_alpha, iter)

print(f"The cost after training is {J:.8f}.")
print(f"The resulting vector of weights is {[round(t, 8) for t in np.squeeze(theta)]}")

"""## Testing"""

def predict_tweet(tweet, freqs, theta):
    '''
    Input:
        tweet: a string
        freqs: a dictionary corresponding to the frequencies of each tuple (word, label)
        theta: (3,1) vector of weights
    Output:
        y_pred: the probability of a tweet being positive or negative
    '''

    # extract the features of the tweet and store it into x
    x = extract_features(tweet,freqs)
    print(x)

    # make the prediction using x and theta
    y_pred = sigmoid(np.dot(x,theta))

    return y_pred

for tweet in test_x:
    print( '%s -> %f' % (tweet, predict_tweet(tweet, freqs, theta)))

# predict single tweet
tweet1 = 'bagus bagus'
tweet2 = 'jelek jelek'
tweet3 = 'bagus jelek'

print( '%s -> %f' % (tweet1, predict_tweet(preprocess(tweet1), freqs, theta)))
print( '%s -> %f' % (tweet2, predict_tweet(preprocess(tweet2), freqs, theta)))
print( '%s -> %f' % (tweet3, predict_tweet(preprocess(tweet3), freqs, theta)))

predict_tweet(preprocess('pintu berwarna merah yang disana terlihat jelek bukan'), freqs, theta)



#data
url1 = "https://raw.githubusercontent.com/aqlaniwafi10/SMA-Project/main/islamic_law_in_brunei_darussalam_09-09-2023_15-11-33.csv"
url2 = "https://raw.githubusercontent.com/aqlaniwafi10/SMA-Project/main/syariat_islam_di_brunei_darussalam_09-09-2023_15-15-35.csv"
url3 = "https://raw.githubusercontent.com/aqlaniwafi10/SMA-Project/main/islam_in_brunei_darussalam_09-09-2023_18-44-05.csv"
url4 = "https://raw.githubusercontent.com/aqlaniwafi10/SMA-Project/main/islamic_in_brunei_darussalam_09-09-2023_18-41-53.csv"
url5 = "https://raw.githubusercontent.com/aqlaniwafi10/SMA-Project/main/data_tweet.csv"

df1 = pd.read_csv(url1)
df2 = pd.read_csv(url2)
df3 = pd.read_csv(url3)
df4 = pd.read_csv(url4)
df5 = pd.read_csv(url5)

df5 = df5.rename(columns= {"translated_column":"full_text"})
result = pd.concat([df2[["full_text"]], df5], ignore_index=True)
result = result.drop_duplicates()
result



"""## Accuracy test"""

y_hat = []

for tweet in test_x:
    # get the label prediction for the tweet
    y_pred = predict_tweet(tweet, freqs, theta)

    if y_pred > 0.5:
        # append 1.0 to the list
        y_hat.append(1)
    else:
        # append 0 to the list
        y_hat.append(0)

# calculate accuracy
accuracy = (y_hat==np.squeeze(test_y)).sum()/len(test_x)

print(f"Logistic regression model's accuracy = {accuracy:.4f}")

