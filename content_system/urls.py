from django.urls import path,include
from . import views
from .views import subscribe_to_post, post_detail


urlpatterns = [
    # path('', post_list, name = 'post_list'),
    path("post/", views.post_list, name="post_list"),
    path("create/", views.create_post, name="create_post"),
    path("update/<pk>/", views.update_post, name="update_post"),
    path("delete/<pk>/", views.delete_post, name="delete_post"),
    path('dashboard/', include('users.urls')),
    path('posts/', views.all_posts, name='all_posts'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('subscribe/<int:post_id>/', views.subscribe_to_post, name='subscribe_to_post'),
    path('subscription_success/<int:post_id>/', views.subscription_success, name='subscription_success'),
    path('posts/<int:post_id>/', views.topic_posts, name='topic_posts'),
    path('fetch-posts/', views.fetch_fastapi_posts, name='fetch_fastapi_posts'),
    
]

# path('post/<int:post_id>/<str:action>/', views.like_dislike_post, name='like_dislike_post'),
    # path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    # path('create/', views.content_create, name='content_create'),
    # path('<int:id>/update/', views.content_update, name='content_update'),
    # path('<int:id>/delete/', views.content_delete, name='content_delete'),

    
