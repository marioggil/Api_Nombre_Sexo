import os
import pandas as pd
import numpy as np
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

Lista = pd.read_csv(
    "./ListaFiltrada.csv",      # relative python path to subdirectory
    sep=',',           # Tab-separated value file.
    #quotechar="'",        # single quote allowed as quote character
    #dtype={"Period": datetime64[ns]},             # Parse the salary column as an integer 
    #usecols=['name', 'birth_date', 'salary'].   # Only load the three columns specified.
    #parse_dates=['birth_date'],     # Intepret the birth_date column as a date
    #skiprows=10,         # Skip the first 10 rows of the file
    na_values=''      # Take any '.' or '??' values as NA
)

Name=Lista["Nombres"].values
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(Name)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X)
clf = MultinomialNB().fit(X_train_tfidf, Lista.Sexo)


def eval_Name(Name,X,Model):
    X = vectorizer.transform(Name)
    X_Eval_tfidf = tfidf_transformer.transform(X)
    Sal=clf.predict(X_Eval_tfidf)
    return Sal

app = Flask(__name__)

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = eval_Name(data.values(),X,clf)

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":#
    app.run(debug=True)

