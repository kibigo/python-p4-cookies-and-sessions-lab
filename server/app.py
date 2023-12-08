#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    articles = []

    for item in Article.query.all():
        
        body = {
            "id": item.id,
            "author":item.author,
            "title":item.title,
            "content":item.content,
            "preview":item.preview,
            "minutes_to_read":item.minutes_to_read,
            "date": item.date
        }

        articles.append(body)

    response = make_response(
        jsonify(articles),
        200
    )
    
    return response

@app.route('/articles/<int:id>')
def show_article(id):

    article_id = Article.query.filter_by(id=id).first()
    session['page_views'] = 0 if not session.get('page_views') else session.get('page_views')
    session['page_views'] += 1

    if session['page_views'] <= 3:
        response = make_response(
            jsonify(article_id.to_dict()),
            200
        )

        return response
    
    else:
        message = {
            "message":"Maximum pageview limit reached"
        }

        response = make_response(
            jsonify(message),
            401
        )

        return response



if __name__ == '__main__':
    app.run(port=5555)
