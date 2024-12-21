# Mofas Kitchen Buddy API

## Overview

This API provides functionality for managing users, recipes, ingredients, and reviews. It includes token-based authentication and rate limiting.

## Authentication

### Login

**Endpoint:** `/api/login`  
**Method:** `POST`  
**Description:** Authenticates a user and returns access and refresh tokens.

**Request Body:**

```json
{
  "username": "user1",
  "password": "password123"
}
```

**Response:**

```json
{
  "access_token": "your_access_token",
  "refresh_token": "your_refresh_token"
}
```

### Refresh Token

**Endpoint:** `/api/refresh`  
**Method:** `POST`  
**Description:** Refreshes the access token using the refresh token.

**Request Body:**

```json
{
  "refresh_token": "your_refresh_token"
}
```

**Response:**

```json
{
  "access_token": "new_access_token"
}
```

### Logout

**Endpoint:** `/api/logout`  
**Method:** `POST`  
**Description:** Revokes the current access token.

**Headers:**

```
Authorization: Bearer your_access_token
```

**Response:**

```json
{
  "message": "Successfully logged out!"
}
```

## User Management

### Create User

**Endpoint:** `/api/users`  
**Method:** `POST`  
**Description:** Creates a new user.

**Request Body:**

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "message": "User created successfully!"
}
```

### Get User

**Endpoint:** `/api/users/<int:user_id>`  
**Method:** `GET`  
**Description:** Retrieves user details.

**Headers:**

```
Authorization: Bearer your_access_token
```

**Response:**

```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com"
}
```

## Ingredient Management

### Add Ingredient

**Endpoint:** `/api/ingredients`  
**Method:** `POST`  
**Description:** Adds a new ingredient.

**Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "name": "Tomato",
  "description": "Fresh red tomatoes"
}
```

**Response:**

```json
{
  "message": "Ingredient added!"
}
```

## Recipe Management

### Add Recipe

**Endpoint:** `/api/recipes`  
**Method:** `POST`  
**Description:** Adds a new recipe.

**Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "name": "Pasta",
  "preparation_time": 30,
  "description": "Delicious pasta with tomato sauce",
  "ingredients": ["Tomato", "Pasta"]
}
```

**Response:**

```json
{
  "message": "Recipe added!"
}
```

### Get Recipe

**Endpoint:** `/api/recipes/<int:recipe_id>`  
**Method:** `GET`  
**Description:** Retrieves recipe details along with reviews.

**Headers:**

```
Authorization: Bearer your_access_token
```

**Response:**

```json
{
  "id": 1,
  "name": "Pasta",
  "preparation_time": 30,
  "description": "Delicious pasta with tomato sauce",
  "reviews": [
    {
      "rating": 5,
      "text": "Amazing recipe!"
    }
  ]
}
```

## Review Management

### Add Review

**Endpoint:** `/api/reviews`  
**Method:** `POST`  
**Description:** Adds a new review for a recipe.

**Headers:**

```
Authorization: Bearer your_access_token
```

**Request Body:**

```json
{
  "rating": 5,
  "text": "Amazing recipe!",
  "recipe_id": 1
}
```

**Response:**

```json
{
  "message": "Review added!"
}
```


## Recipe Suggestion API

### GET /suggest-recipe
Suggests a recipe based on available ingredients using AI.

**Authentication Required**: Yes (JWT Token)
**Rate Limited**: Yes

#### Request
```json
{
    "ingredients": ["tomato", "basil", "mozzarella"]
}

