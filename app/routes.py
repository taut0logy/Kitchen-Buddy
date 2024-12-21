from flask import Blueprint, request, jsonify
from app.database import get_session
from app.models import Ingredient
#from app.services import create_chatbot
api = Blueprint('api', __name__)

#chatbot = create_chatbot()

@api.route('/ingredients', methods=['POST'])
def add_ingredient():
    data = request.json
    session = get_session()
    ingredient = Ingredient(name=data['name'], quantity=data['quantity'], unit=data['unit'])
    session.add(ingredient)
    session.commit()
    return jsonify({"message": "Ingredient added!"})


@api.route('/ingredients', methods=['PUT'])
def update_ingredient():
    data = request.json
    session = get_session()
    ingredient = session.query(Ingredient).filter_by(name=data['name']).first()
    if ingredient:
        ingredient.quantity = data['quantity']
        ingredient.unit = data['unit']
        session.commit()
        return jsonify({"message": "Ingredient updated!"})
    return jsonify({"error": "Ingredient not found!"}), 404


# @api.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     response = chatbot.run(data['message'])
#     return jsonify({"response": response})