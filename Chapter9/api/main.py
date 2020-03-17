import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
from sklearn.linear_model import LogisticRegression
from flask import Flask, request, render_template, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import DataRequired, Email
import io
from flask_restful import Resource, Api
import string
import re
import pickle
from flask_jsonpify import jsonpify

DEBUG = True
app = Flask(__name__)
# app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'abcdefgh'
api = Api(app)

class TextFieldForm(FlaskForm):
    text = StringField('Document Content', validators=[validators.data_required()])

class Flask_Work(Resource):
    def __init__(self):
        pass

    def clean_text(self, text):
        ## Remove puncuation
        text = text.translate(string.punctuation)

        ## Convert words to lower case and split them
        text = text.lower().split()

        ## Remove stop words
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops and len(w) >= 3]

        text = " ".join(text)

        text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
        return text

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)

    def post(self):
        f = open('model.pkl', 'rb')
        P, Q, userid_vectorizer = pickle.load(f), pickle.load(f), pickle.load(f)
        print('in vect')
        sentence = request.form['search']
        print(sentence)
        test_df = pd.DataFrame([sentence], columns=['Text'])
        test_df['Text'] = test_df['Text'].apply(self.clean_text)
        test_vectors = userid_vectorizer.transform(test_df['Text'])
        test_v_df = pd.DataFrame(test_vectors.toarray(), index=test_df.index,
                                 columns=userid_vectorizer.get_feature_names())

        predict_item_rating = pd.DataFrame(np.dot(test_v_df.loc[0], Q.T), index=Q.index, columns=['Rating'])
        top_recommendations = pd.DataFrame.sort_values(predict_item_rating, ['Rating'], ascending=[0])[:10]

        JSONP_data = jsonpify(top_recommendations.to_json())
        return JSONP_data

        return make_response(render_template('index.html'), 200, JSONP_data)


api.add_resource(Flask_Work, '/')


if __name__ == '__main__':
    # Main()
    app.run(host='127.0.0.1', port=4000, debug=True)
