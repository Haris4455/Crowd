from django.db import models
from django.contrib.auth.models import User
import pydotplus
# Create your models here.

# Question Model
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=350)
    detail = models.TextField()
    tags = models.TextField(default='')
    add_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="Ask/images", blank= True, null=True)

    def __str__(self):
        return self.title

# Answer Model
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    details = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to="Ask/images", blank= True, default='')
    def __str__(self):
        return self.details


# Comment Model

class Comment(models.Model):
 answer = models.ForeignKey(Answer, on_delete= models.CASCADE)
 user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_User')
 comment = models.TextField(default='')
 add_time = models.DateTimeField(auto_now_add=True)

# Upvote Model
class Upvote(models.Model):
 answer = models.ForeignKey(Answer, on_delete= models.CASCADE)
 user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upvote_User')

# Downvote Model
class Downvote(models.Model):
 answer = models.ForeignKey(Answer, on_delete= models.CASCADE)
 user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downvote_User')

