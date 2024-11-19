from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    overview = models.TextField(default="No overview provided")  # New field for the post overview
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.title

class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_dislikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_dislikes')
    liked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')  # Ensure a user can only like/dislike a post once

    def __str__(self):
        return f"{self.user.username} - {'Liked' if self.liked else 'Disliked'}: {self.post.title}"


class PostSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_subscriptions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='subscribers')

    class Meta:
        unique_together = ('user', 'post')  # Ensure a user can only subscribe to a post once

    def __str__(self):
        return f"{self.user.username} subscribed to {self.post.title}"








































# class Content(models.Model):
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='contents')
#     title = models.CharField(max_length=255)
#     body = models.TextField()

#     def __str__(self):
#         return self.title



# class Content(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     body = models.TextField()
#     content_type = models.CharField(max_length=100, choices=[
#         ('post', 'Post'),
#         ('image', 'Image'),
#         ('video', 'Video'),
#     ])
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title