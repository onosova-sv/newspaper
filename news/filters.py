
from .models import Post
import django_filters
# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class NewsFilter(django_filters.FilterSet):
   time_in = django_filters.DateFilter(widget = django_filters.widgets.DateInput(attrs={'type': 'date'}))
   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'head': ['icontains'],
           # количество товаров должно быть больше или равно
           'author__name': ['icontains'],
           'time_in': [
                 # цена должна быть меньше или равна указанной
               'gt',  # цена должна быть больше или равна указанной
           ],
       }
