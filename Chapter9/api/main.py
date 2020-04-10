import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
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
        self.stopwordSet = set(stopwords.words("english"))
        pass

    def cleanText(line):        
        line = line.translate(string.punctuation)
        line = line.lower().split()
        
        line = [word for word in line if not word in self.stopwordSet and len(word) >= 3]
        line = " ".join(line)
        
        return re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", line) 

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)

    def post(self):
        f = open('model.pkl', 'rb')
        P, Q, userid_vectorizer = pickle.load(f), pickle.load(f), pickle.load(f)
        sentence = request.form['search']
        test_data = pd.DataFrame([sentence], columns=['Text'])
        test_data['Text'] = test_data['Text'].apply(self.cleanText)
        test_vectors = userid_vectorizer.transform(test_data['Text'])
        test_v_df = pd.DataFrame(test_vectors.toarray(), index=test_data.index,
                                 columns=userid_vectorizer.get_feature_names())

        predicted_ratings = pd.DataFrame(np.dot(test_v_df.loc[0], Q.T), index=Q.index, columns=['Rating'])
        predictions = pd.DataFrame.sort_values(predicted_ratings, ['Rating'], ascending=[0])[:10]

        JSONP_data = jsonpify(predictions.to_json())
        return JSONP_data

        # return make_response(render_template('index.html'), 200, JSONP_data)


api.add_resource(Flask_Work, '/')


if __name__ == '__main__':
    # Main()
    app.run(host='127.0.0.1', port=4000, debug=True)
