from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, One_news, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleDelete, ArticleUpdate, create_news


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(), name='news_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', One_news.as_view(), name='news_detail'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('create/', ArticleCreate.as_view(), name='news_create'),
   path('<int:pk>/update/', ArticleUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', ArticleDelete.as_view(), name='news_delete'),
   path('postcreate/', create_news, name='post_created'),

]