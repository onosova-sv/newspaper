from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Post, UsersSubscribed

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