from datetime import timedelta
from celery import shared_task
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from .models import Post, UsersSubscribed, Category
from django.shortcuts import render, reverse, redirect

@shared_task()
def send_weekly_articles():
    # Определяем дату неделю назад
    one_week_ago = timezone.now() - timedelta(days=7)

    # Получаем все статьи, добавленные за последнюю неделю
    new_articles = Post.objects.filter(time_in__gte=one_week_ago)

    # Группируем статьи по разделам
    post_by_category = {}
    for post in new_articles:
        if post.category not in post_by_category:
            post_by_category[post.category] = []
        post_by_category[post.category].append(post)

    # Для каждого раздела отправляем письмо подписанным пользователям
    for category, posts in post_by_category.items():
        subscriptions = UsersSubscribed.objects.filter(category=category)
        for subscription in subscriptions:
            user = subscription.user
            subject = f'Новые статьи в разделе {category.name}'
            message = 'Новые статьи за последнюю неделю:\\n\\n'
            for post in posts:
                message += f'- {post.head}\\n{post.text_post[:30]}...\nПодробнее: http://127.0.0.1:8000/posts/{post.id}\\n'
            send_mail(subject, message, 'onosova.sweta@yandex.ru', [user.email])


def clean(self):
    post_count_today = Post.objects.filter(author=self.author, time_in__date=timezone.now().date()).count()
    if post_count_today >= 3:
        raise ValidationError("Вы не можете опубликовать более 3 новостей в сутки.")

@shared_task()
def create_news(request):
    if request.method == 'POST':
        head = request.POST['head']
        text_post = request.POST['text_post']
        category_id = request.POST['category']
        category = Category.objects.get(id=category_id)
        post_id = request.POST['post']
        post = Category.objects.get(id=post_id)

        news = Post(head=head, text_post=text_post, category=category, author=request.user, post = post)
        try:
            news.full_clean()  # вызывает проверку, включая check для лимита
            news.save()

                # Уведомление подписчиков
            subscribers = UsersSubscribed.objects.filter(category=category)
            for subscriber in subscribers:
                send_mail(
                    'Новая новость в вашей категории!',
                    f'Новая новость:\\n\\n{Post.head}\\n{Post.text_post[:30]}...\nПодробнее: http://127.0.0.1:8000/posts/{Post.post_id}',
                    'onosova.sweta@yandex.ru',  # ваш адрес
                    [subscriber.user.email],
                    fail_silently=False,
                )

            messages.success(request, "Новость успешно создана и подписчики уведомлены!")
            return redirect('post_list')
        except ValidationError as e:
            messages.error(request, str(e))

    return render(request, 'post_created.html')