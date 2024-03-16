from flask import jsonify, request

from . import app, db
from .models import Opinion


from .views import random_opinion


def opinion_to_dict(opinion):
    return dict(
        id = opinion.id,
        title = opinion.title,
        text = opinion.text,
        source = opinion.source,
        timestamp = opinion.timestamp,
        added_by = opinion.added_by
    )


@app.route('/api/opinions/<int:id>/', methods=['GET'])
def get_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    # Конвертируем объект модели в словарь
    data = opinion_to_dict(opinion)
    return jsonify({'opinion': data}), 200

@app.route('/api/opinions/<int:id>/', methods=['PATCH'])
def update_opinion(id):
    data = request.get_json()
    opinion = Opinion.query.get_or_404(id)
    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    opinion.added_by = data.get('added_by', opinion.added_by)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201

@app.route('/api/opinions/<int:id>/', methods=['DELETE'])
def delete_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    db.session.delete(opinion)
    db.session.commit()
    return '', 204


@app.route('/api/opinions/', methods=['GET'])
def get_opinions():
    opinions = Opinion.query.all()
    # Поочерёдно сериализуется каждый объект,
    # а потом все объекты помещаются в список opinions_list
    opinions_list = [opinion_to_dict(opinion) for opinion in opinions]
    return jsonify({'opinions': opinions_list}), 200


@app.route('/api/opinions/', methods=['POST'])
def add_opinion():
    data = request.get_json()
    if 'title' not in data or 'text' not in data:
        return jsonify({'error':
                        'В запросе отсутствуют обязательные поля'}), 400
    if Opinion.query.filter_by(text=data['text']).first() is not None:
        return jsonify({'error':
                        'Такое мнение уже есть в базе данных'}), 400
    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({'opinion': opinion.to_dict()}), 201

@app.route('/api/get-random-opinion/', methods=['GET'])
def get_random_opinion():
    opinion = random_opinion()
    return jsonify({'opinion': opinion.to_dict()}), 200