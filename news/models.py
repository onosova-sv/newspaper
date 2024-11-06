from django.db import models
from datetime import datetime

class User(models.Model):
    name = models.CharField(max_length=64)

class Author(models.Model):
    full_name = models.CharField(max_length=64)
    name = models.CharField(null=True, max_length=64)
    rank = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete = models.CASCADE,primary_key = True )


    def update_rating(self):
        pass

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

news = 'NW'
article = 'AR'

POSITIONS = [
    (news, 'Новость'),
    (article, 'Статья'),
    ]

class Post(models.Model):
    time_in = models.DateTimeField(auto_now_add=True, null=True)
    rank_post = models.IntegerField(default=0)
    text_post = models.TextField()
    head = models.CharField(max_length=255)
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=news)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        rank_post = self.rank_post + 1
        return rank_post

    def dislike(self):
        self.rank_post = self.rank_post - 1
        return self.rank_post

    def preview(self):
        return self.text_post[:123] + '...'

class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    time_in = models.DateTimeField(auto_now_add=True, null=True)
    rank_comment = models.IntegerField(default=1)
    text_comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        rank_comment = self.rank_comment + 1
        return rank_comment

    def dislike(self):
        rank_comment = self.rank_comment - 1
        return rank_comment