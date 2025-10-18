import streamlit as st

import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

tfidf = pickle.load(open("vectorization.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

ps = PorterStemmer()
# stopwords = set(stopwords.words('english'))

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words("english") and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


st.title("Email/Sms Spam Detection")

input_sms = st.text_area("Enter Your Message")

if st.button("Send Your Message"):

    ## 1. preprocess
    transformed_sms = transform_text(input_sms)
    ## 2. vectorize
    vector_input = tfidf.transform([transformed_sms])
    ## 3. predict
    result = model.predict(vector_input)[0]
    ## 4. display
    if result == 1:
        st.success("Your Message was spam")
    else:
        st.error("Your Message was not spam")



