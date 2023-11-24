from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import json

app = Flask(__name__)

client = app.test_client()
engine = create_engine('sqlite:///sqlalchemy.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()
from models import *
Base.metadata.create_all(bind=engine)


@app.route('/ad/', methods=['GET'])
def get_advertisement():
    '''Получение объявления с сервера'''
    ad_query = Advertisement.query.all()
    serialization = []
    for element in ad_query:
        serialization.append({
            "id": element.id,
            "title": element.title,
            "description": element.description,
            "created_at": element.created_at,
            "owner": element.owner
        })
    #return jsonify(serialization)
    return json.dumps(serialization, default=str, ensure_ascii=False).encode('utf8')


@app.route('/ad', methods=['POST'])
def post_create_an_ad():
    '''Создание объявления на сервере'''
    income = Advertisement(**request.json)
    session.add(income)
    session.commit()
    serialization = {
        #"id": income.id,
        "title": income.title,
        "description": income.description,
        "owner": income.owner
    }
    return json.dumps(serialization, default=str, ensure_ascii=False).encode('utf8')


@app.route('/ad/<int:ad_id>', methods=['PUT'])
def put_change_an_ad(ad_id):
    '''Изменение объявления на сервере'''
    item = Advertisement.query.filter(Advertisement.id == ad_id).first()
    income = request.json
    if not item:
        return {"message": "There are no ads in database with this id"}, 400
    for key, value in income.items():
        setattr(item, key, value)
    session.commit()
    serialization = {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "owner": item.owner
    }
    return json.dumps(serialization, default=str, ensure_ascii=False).encode('utf8')


@app.route('/ad/<int:ad_id>', methods=['DELETE'])
def delete_an_ad(ad_id):
    '''Удаление объявления на сервере'''
    item = Advertisement.query.filter(Advertisement.id == ad_id).first()
    if not item:
        return {"message": "There are no ads in database with this id"}, 400
    session.delete(item)
    session.commit()
    return "", 204


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run()
