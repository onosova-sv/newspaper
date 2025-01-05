from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, UsersSubscribed, Category
from .filters import NewsFilter
from .forms import PostForm
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone

class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')

class EditPost(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'head'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

    def article_list(request):
        news = Post.objects.all().order_by('-time_in')  # Сортируем по времени создания (новые статьи первыми)
        return render(request, 'news.html', {'news': news})

class One_news(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'one_news.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'one_news'

class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'news'
        return super().form_valid(form)

class NewsUpdate(UpdateView, LoginRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'news'
        return super().form_valid(form)

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'news'
        return super().form_valid(form)

class ArticleCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'article'
        return super().form_valid(form)

class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'article'
        return super().form_valid(form)

class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.position = 'article'
        return super().form_valid(form)


def get(self,request,*args, **kwargs):
    return render(request, 'make_post.html', {})

def clean(self):
    post_count_today = Post.objects.filter(author=self.author, created_at__date=timezone.now().date()).count()
    if post_count_today >= 3:
        raise ValidationError("Вы не можете опубликовать более 3 новостей в сутки.")
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