from django.urls import path
from .views import register, user_login, user_logout, landing, poster_register, poster_login, poster_logout
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', landing, name = 'landing' ),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('poster/register/', poster_register, name='poster_register'),
    path('poster/login/', poster_login, name='poster_login'),
    path('logout_poster/', poster_logout, name='logout_poster'),  # New URL for poster logout
    # # path('topics/', views.topic_list, name='topic_list'),
    # # path('topics/<int:topic_id>/posts/', views.topic_posts, name='topic_posts'),
    # path('subscribe/<int:topic_id>/', views.subscribe_to_post, name='subscribe_to_post'),
    # path('all-posts/', all_posts, name='all_posts'), 
]
