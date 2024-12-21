from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from app.config import DATABASE_URI

Base = declarative_base()

# Association tables for many-to-many relationships
recipe_ingredient_association = Table('recipe_ingredient', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
)

recipe_taste_association = Table('recipe_taste', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('taste_id', Integer, ForeignKey('tastes.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    recipes = relationship('Recipe', back_populates='user')
    reviews = relationship('Review', back_populates='user')

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    preparation_time = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='recipes')
    ingredients = relationship('Ingredient', secondary=recipe_ingredient_association, back_populates='recipes')
    tastes = relationship('Taste', secondary=recipe_taste_association, back_populates='recipes')
    reviews = relationship('Review', back_populates='recipe')

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    recipes = relationship('Recipe', secondary=recipe_ingredient_association, back_populates='ingredients')

class Taste(Base):
    __tablename__ = 'tastes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    recipes = relationship('Recipe', secondary=recipe_taste_association, back_populates='tastes')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    text = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    user = relationship('User', back_populates='reviews')
    recipe = relationship('Recipe', back_populates='reviews')

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Initialize Database
Base.metadata.create_all(engine)
