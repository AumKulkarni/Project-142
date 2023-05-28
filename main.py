from flask import Flask,jsonify,request
from content_filtering import get_recommendations
import csv
from storage import all_articles,liked_articles,not_liked_articles
from demographic_filtering import output
all_articles=[]
with open("Articles.csv")as f:
    reader=csv.reader(f)
    data=list(reader)
    all_movies=data[1:]
liked_articles=[]
not_liked_articles=[]
app=Flask(__name__)
@app.route("/get-article")
def get_article():
    return jsonify({
        "data":all_articles[0],
        "status":"success"
    })
@app.route("/liked-articles",methods=["POST"])
def liked_article():
    article=all_articles[0]
    
    liked_articles.append(article)
    return jsonify({
        "status":"success"
    }),201

@app.route("/unliked-articles",methods=["POST"])
def unliked_article():
    article=all_articles[0]
    
    not_liked_articles.append(article)
    return jsonify({
        "status":"success"
    }),201
@app.route("/popular_articles")
def popular_articles():
    article_data=[]
    for article in output:
        d={
            "url":article[0],
            "title":article[1],
            "text":article[2],
            "lang":article[3],
            "total_events":article[4],
        }
        article_data.append(d)
    return jsonify({
        "data":article_data,
        "status":"success"
    }),200
@app.route("/recommended-articles")
def recommended_articles():
    all_recommended=[]
    for liked_article in liked_articles:
        output=get_recommendations(liked_article[4])
        for data in output:
            all_recommended.append(data)
    all_recommended.sort()
    article_data=[]
    for recommended in all_recommended:
         d={
            "url":recommended[0],
            "title":recommended[1],
            "text":recommended[2],
            "lang":recommended[3],
            "total_events":recommended[4],
        }
         article_data.append(d)
        
    return jsonify({
        "data":article_data,
        "status":"success"
    }),200

if __name__=="__main__":
    app.run()