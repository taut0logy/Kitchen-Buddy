
from app.models import Base, engine, session, Recipe, Ingredient, Taste, Review, User
import logging
from werkzeug.security import generate_password_hash
from pathlib import Path
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_file(filename):
    """Read tab-separated file and return list of dictionaries"""
    filepath = Path(f"data/{filename}")
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    data = []
    with open(filepath, 'r') as file:
        headers = file.readline().strip().split('\t')
        for line in file:
            values = line.strip().split('\t')
            if len(values) == len(headers):
                data.append(dict(zip(headers, values)))
    return data

def populate_ingredients():
    try:
        data = read_file('ingredients.txt')
        for item in data:
            ingredient = Ingredient(
                name=item['name'],
                description=item['description']
            )
            session.add(ingredient)
        session.commit()
        logger.info(f"Added {len(data)} ingredients")
    except Exception as e:
        logger.error(f"Error populating ingredients: {str(e)}")
        session.rollback()
        raise


def populate_tastes():
    try:
        with open("data/tastes.txt", 'r') as file:
            tastes = file.read().strip().split()
        for taste_name in tastes:
            taste = Taste(name=taste_name)
            session.add(taste)
        session.commit()
        logger.info(f"Added {len(tastes)} tastes")
    except Exception as e:
        logger.error(f"Error populating tastes: {str(e)}")
        session.rollback()
        raise

def populate_recipes():
    try:
        data = read_file('recipes.txt')
        for item in data:
            recipe = Recipe(
                name=item['nname'],
                description=item['description'],
                preparation_time=30,  # default value
                user_id=1
            )
            
            # Add ingredients
            ingredient_names = [i.strip() for i in item['ingredients_name'].split(',')]
            for ing_name in ingredient_names:
                ingredient = session.query(Ingredient).filter_by(name=ing_name).first()
                if ingredient:
                    recipe.ingredients.append(ingredient)
            
            # Add random taste (example logic)
            tastes = session.query(Taste).all()
            if tastes:
                recipe.tastes.append(tastes[0])  # Add first taste as default
            
            session.add(recipe)
        session.commit()
        logger.info(f"Added {len(data)} recipes")
    except Exception as e:
        logger.error(f"Error populating recipes: {str(e)}")
        session.rollback()
        raise

def populate_reviews():
    try:
        data = read_file('review.txt')
        for item in data:
            review = Review(
                rating=int(item['rating']),
                text=item['text'],
                user_id=1,
                recipe_id=int(item['recipe_id'])
            )
            session.add(review)
        session.commit()
        logger.info(f"Added {len(data)} reviews")
    except Exception as e:
        logger.error(f"Error populating reviews: {str(e)}")
        session.rollback()
        raise

def main():
    try:
        # Clear existing data
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        
        logger.info("Starting database population...")
        
        # Create default user
        default_user = User(
            username="admin",
            email="admin@example.com",
            password=generate_password_hash("admin123")
        )
        session.add(default_user)
        session.commit()
        
        # Populate tables in order
        populate_ingredients()
        populate_tastes()
        populate_recipes()
        populate_reviews()
        
        logger.info("Database population completed successfully!")
    except Exception as e:
        logger.error(f"Database population failed: {str(e)}")
        session.rollback()
        raise

if __name__ == "__main__":
    main()