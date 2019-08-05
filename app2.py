import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import model as model_final

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    result_knn,result_tfidf,result,result_collaborative = model_final.get_input(int_features)
    result_word=[]
    for i in result:
        result_word.append(i[0])
    print(result_collaborative)
    return render_template ( 'index.html',result_knn=result_knn,result_tfidf=result_tfidf,result_word=result_word,result_collaborative=result_collaborative)


if __name__ == "__main__":
    app.run(debug=True)
