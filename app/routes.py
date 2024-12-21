from flask import Blueprint, request, jsonify, g
from app.database import get_session
from scripts.recipe_suggestor import RecipeSuggestor
from app.models import Ingredient, User, Recipe, Review
from app.auth import generate_token, token_required, rate_limited, refresh_access_token, revoke_token
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400
    
    session = get_session()
    user = session.query(User).filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password!'}), 401
    
    tokens = generate_token(user.id)
    return jsonify(tokens)

@api.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.json.get('refresh_token')
    if not refresh_token:
        return jsonify({'message': 'Refresh token is required!'}), 400
    return refresh_access_token(refresh_token)

@api.route('/logout', methods=['POST'])
@token_required
def logout():
    token = request.headers.get('Authorization').split(" ")[1]
    revoke_token(token)
    return jsonify({'message': 'Successfully logged out!'})

@api.route('/protected', methods=['GET'])
@token_required
@rate_limited
def protected():
    return jsonify({'message': 'This is a protected route.'})

@api.route('/ingredients', methods=['POST'])
@token_required
@rate_limited
def add_ingredient():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    
    if not name:
        return jsonify({"message": "Ingredient name is required!"}), 400
    
    session = get_session()
    if session.query(Ingredient).filter_by(name=name).first():
        return jsonify({"message": "Ingredient with this name already exists!"}), 400
    
    ingredient = Ingredient(name=name, description=description)
    session.add(ingredient)
    session.commit()
    return jsonify({"message": "Ingredient added!"})


@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required!'}), 400
    
    session = get_session()
    if session.query(User).filter_by(username=username).first() or session.query(User).filter_by(email=email).first():
        return jsonify({'message': 'User with this username or email already exists!'}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    session.add(new_user)
    session.commit()
    
    return jsonify({'message': 'User created successfully!'})

@api.route('/users/<int:user_id>', methods=['GET'])
@token_required
@rate_limited
def get_user(user_id):
    session = get_session()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'User not found!'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })

@api.route('/recipes', methods=['POST'])
@token_required
@rate_limited
def add_recipe():
    data = request.json
    name = data.get('name')
    preparation_time = data.get('preparation_time')
    description = data.get('description')
    ingredient_names = data.get('ingredients')
    
    if not name or not preparation_time or not description or not ingredient_names:
        return jsonify({"message": "Name, preparation time, description, and ingredients are required!"}), 400
    
    session = get_session()
    ingredients = session.query(Ingredient).filter(Ingredient.name.in_(ingredient_names)).all()
    
    if len(ingredients) != len(ingredient_names):
        return jsonify({"message": "Some ingredients were not found!"}), 400
    
    recipe = Recipe(
        name=name,
        preparation_time=preparation_time,
        description=description,
        user_id=g.user_id
    )
    recipe.ingredients = ingredients
    session.add(recipe)
    session.commit()
    return jsonify({"message": "Recipe added!"})

@api.route('/reviews', methods=['POST'])
@token_required
@rate_limited
def add_review():
    data = request.json
    session = get_session()
    review = Review(
        rating=data['rating'],
        text=data['text'],
        user_id=g.user_id,
        recipe_id=data['recipe_id']
    )
    session.add(review)
    session.commit()
    return jsonify({"message": "Review added!"})

@api.route('/recipes/<int:recipe_id>', methods=['GET'])
@token_required
@rate_limited
def get_recipe(recipe_id):
    session = get_session()
    recipe = session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({'message': 'Recipe not found!'}), 404
    
    reviews = session.query(Review).filter_by(recipe_id=recipe_id).all()
    reviews_data = [{'rating': review.rating, 'text': review.text} for review in reviews]
    
    return jsonify({
        'id': recipe.id,
        'name': recipe.name,
        'preparation_time': recipe.preparation_time,
        'description': recipe.description,
        'reviews': reviews_data
    })


@api.route('/suggest-recipe', methods=['POST'])
@token_required
@rate_limited
def suggest_recipe():
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    
    suggestor = RecipeSuggestor()
    recipe = suggestor.suggest_recipe(ingredients)
    
    return jsonify({'recipe': recipe})