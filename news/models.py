from django.db import models
from datetime import datetime
from django.urls import reverse

class User(models.Model):
    name = models.CharField(max_length=64)

class Author(models.Model):
    full_name = models.CharField(max_length=64)
    name = models.CharField(null=True, max_length=64)
    rank = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete = models.CASCADE,primary_key = True )


    def update_rating(self):
        post_rating = sum(dct['rank_post'] for dct in Post.objects.filter(author=self).values('rank_post')) // 3
        author_comm = sum(dct['rank_comment'] for dct in Comment.objects.filter(user=self.user).values('rank_comment'))
        comm_under_posts = sum(dct['rank_comment'] for dct in Comment.objects.filter(post__author=self).values('rank_comment'))
        return post_rating + author_comm + comm_under_posts


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

    def __str__(self):
        return self.head

    def like(self):
        self.rank_post += 1
        self.save()

    def dislike(self):
        self.rank_post -= 1
        self.save()

    def preview(self):
        if len(self.text_post)<=124:
            return self.text_post
        else:
            return self.text_post[:123] + '...'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


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
        self.rank_comment += 1
        self.save()

    def dislike(self):
        self.rank_comment -= 1
        self.save()