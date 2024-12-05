from flask import Flask,render_template,url_for,request
#import pandas as pd 
import pickle
import numpy as np
import trans as translate
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
from topic_modelling import Topic_modeling,Topic_modeling1
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
import string 
from nltk.stem import WordNetLemmatizer
import sqlite3
import translatereverse as eng2hi


cv=pickle.load(open('transform2.pkl','rb'))
app = Flask(__name__)

@app.route('/home1')
def home1():
	return render_template('home1.html')



@app.route('/')
def home():
	return render_template('home.html')

@app.route("/signup")
def signup():
    
    
    name = request.args.get('username','')
    number = request.args.get('number','')
    email = request.args.get('email','')
    password = request.args.get('psw','')

    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `detail` (`name`,`number`,`email`, `password`) VALUES (?, ?, ?, ?)",(name,number,email,password))
    con.commit()
    con.close()

    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('name','')
    password1 = request.args.get('psw','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `name`, `password` from detail where `name` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()
    print(data)

    if data == None:
        return render_template("signup.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")

@app.route('/predict',methods=['POST'])
def predict():
    message = request.form['message']
    englishmessage=translate.process(message)
    data = [englishmessage]
    df = pd.DataFrame({'sentence':data})
    t,word = Topic_modeling(df)
    wod=[]
    for i in word:
	    tr=eng2hi.process(i)
	    wod.append(tr)
	
	    
    t1,word1 = Topic_modeling1(df)
    
    wod1=[]
    for i in word1:
	    tr1=eng2hi.process(i)
	    wod1.append(tr1)
	
	
    return render_template('result.html',message=message,to = t, wo = wod,to1 = t1, wo1 = wod1)



@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/notebook')
def notebook():
	return render_template('notebook.html')
		
if __name__ == '__main__':
	app.run(debug=False)
