import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "content_management.settings")
django.setup()

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi.security import OAuth2PasswordBearer
from django.contrib.auth.models import User
from content_system.models import Post, LikeDislike, PostSubscription
from users.models import User_Profile
from django.conf import settings
from datetime import datetime


# Create FastAPI app
app = FastAPI()

# OAuth2 for authentication simulation
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models (for request validation)
class PostIn(BaseModel):
    title: str
    overview: str = "No overview provided"
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    overview: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # This allows Pydantic to work with Django models
    
    

class LikeDislikeIn(BaseModel):
    post_id: int
    liked: bool

class PostSubscriptionIn(BaseModel):
    post_id: int

# Utility function to simulate authentication (you can replace this with real logic)
def authenticate_user(token: str):
    # Simulate a token validation (for now, just check for a placeholder token)
    if not token or token != "valid_token":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return "authenticated_user"

# Database session dependency (uses Django's ORM)
def get_db():
    # In Django, you can access the database directly without needing a custom session management
    return models

# Endpoints
@app.post("/posts/", response_model=PostOut)
def create_post(post: PostIn, token: str = Depends(oauth2_scheme)):
    authenticate_user(token)
    
    # Create a new post in Django's database
    new_post = Post.objects.create(
        title=post.title,
        overview=post.overview,
        content=post.content
    )
    return new_post

@app.get("/posts/", response_model=List[PostOut])
def list_posts():
    # Fetch all posts from the database
    posts = Post.objects.all()
    return posts

@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int):
    # Fetch a specific post by ID
    try:
        post = Post.objects.get(id=post_id)
        # Now convert the post to the PostOut model before returning
        return post
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, post: PostIn, token: str = Depends(oauth2_scheme)):
    authenticate_user(token)
    
    # Fetch the post to update
    try:
        db_post = Post.objects.get(id=post_id)
        db_post.title = post.title
        db_post.overview = post.overview
        db_post.content = post.content
        db_post.save()
        return db_post
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, token: str = Depends(oauth2_scheme)):
    authenticate_user(token)
    
    # Delete the post
    try:
        db_post = Post.objects.get(id=post_id)
        db_post.delete()
        return {"message": "Post deleted"}
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

@app.post("/posts/{post_id}/like", response_model=dict)
def like_post(post_id: int, like_dislike: LikeDislikeIn, token: str = Depends(oauth2_scheme)):
    authenticate_user(token)
    
    # Create or update the like/dislike record
    user = User.objects.get(username="authenticated_user")  # Replace with actual authenticated user
    post = Post.objects.get(id=post_id)
    
    like_dislike_obj, created = LikeDislike.objects.update_or_create(
        user=user, post=post,
        defaults={"liked": like_dislike.liked}
    )
    return {"message": f"Post {post_id} liked: {like_dislike.liked}"}

@app.post("/posts/{post_id}/subscribe", response_model=dict)
def subscribe_to_post(post_id: int, subscription: PostSubscriptionIn, token: str = Depends(oauth2_scheme)):
    authenticate_user(token)
    
    # Simulate subscribing to a post
    user = User.objects.get(username="authenticated_user")  # Replace with actual authenticated user
    post = Post.objects.get(id=post_id)
    
    subscription_obj, created = PostSubscription.objects.update_or_create(
        user=user, post=post
    )
    return {"message": f"User subscribed to post {post_id}"}

@app.post("/posts/{post_id}/unsubscribe", response_model=dict)
def unsubscribe_from_post(post_id: int, subscription: PostSubscriptionIn, token: str = Depends(oauth2_scheme)):
    authenticate_user(token)
    
    # Simulate unsubscribing from a post
    user = User.objects.get(username="authenticated_user")  # Replace with actual authenticated user
    post = Post.objects.get(id=post_id)
    
    subscription_obj = PostSubscription.objects.filter(user=user, post=post)
    if subscription_obj.exists():
        subscription_obj.delete()
        return {"message": f"User unsubscribed from post {post_id}"}
    else:
        raise HTTPException(status_code=404, detail="Subscription not found")

# class UserProfileOut(BaseModel):
#     username: str
#     email: EmailStr
#     bio: str | None = None
#     profile_picture: str | None = None

#     class Config:
#         orm_mode = True

# class UserLogin(BaseModel):
#     username: str
#     password: str

# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str
#     bio: str | None = None
#     profile_picture: str | None = None

# # Create a user (Register)
# @app.post("/users/register", response_model=UserProfileOut)
# def register_user(user_data: UserCreate):
#     try:
#         # Create User object
#         user = User.objects.create_user(
#             username=user_data.username,
#             email=user_data.email,
#             password=user_data.password,
#         )
#         # Create the user profile
#         user_profile = User_Profile.objects.create(
#             user=user,
#             bio=user_data.bio,
#             profile_picture=user_data.profile_picture
#         )
#         return user_profile
#     except IntegrityError:
#         raise HTTPException(status_code=400, detail="Username already taken")

# # User login
# @app.post("/users/login")
# def login_user(credentials: UserLogin):
#     user = authenticate(username=credentials.username, password=credentials.password)
#     if user is None:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"message": "Login successful"}

# # Get user profile by user ID
# @app.get("/users/{user_id}", response_model=UserProfileOut)
# def get_user_profile(user_id: int):
#     try:
#         user_profile = User_Profile.objects.get(user__id=user_id)
#         return user_profile
#     except ObjectDoesNotExist:
#         raise HTTPException(status_code=404, detail="User profile not found")
