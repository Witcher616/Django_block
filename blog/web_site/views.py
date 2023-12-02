from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DeleteView, ListView

from .forms import UserRegistrationForm, UserAuthenticationForm, ArticleForm, CommentForm
from .models import Article, Category, Comment, ArticleCountView, Like, Dislike, Favorite


class ArticleListView(ListView):
    model = Article
    template_name = "web_site/index.html"
    context_object_name = "articles"


class SearchResult(ArticleListView):
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Article.objects.filter(
            Q(title__iregex=query) | Q(short_description__iregex=query)
        )


class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'web_site/article_form.html'

    # def form_valid(self, form):
    #     print(self.get_success_url())
    #     return redirect('home')


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = "/"


def home_view(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'web_site/index.html', context)


def category_articles(request, category_id):
    category = Category.objects.get(pk=category_id)
    articles = Article.objects.filter(category=category)
    context = {
        'articles': articles
    }
    return render(request, 'web_site/index.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)

    if request.method == 'POST':
        # request.POST
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.article = article
            form.author = request.user
            form.save()
            return redirect('article_detail', article.pk)
    else:
        form = CommentForm()

    # TODO: получить все коментарии статьи и вывести их на детальной
    # TODO: странице продукта
    comments = Comment.objects.filter(article=article)
    print(comments)

    if not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key

    viewed = ArticleCountView.objects.filter(article=article, session_id=session_id)
    if viewed.count() == 0 and str(session_id) != 'None':
        obj = ArticleCountView()
        obj.session_id = session_id
        obj.article = article
        obj.save()

        # изменение кол-ва просмотров
        article.views += 1
        article.save()

    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    total_likes = article.likes.user.all().count()
    total_dislikes = article.dislikes.user.all().count()
    context = {
        "article": article,
        "form": form,
        "comments": comments,
        "total_likes": total_likes,
        "total_dislikes": total_dislikes
    }
    return render(request, "web_site/article_detail.html", context)


def login_view(request):
    if request.method == "POST":
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserAuthenticationForm()
    context = {
        "form": form
    }
    return render(request, "web_site/login.html", context)


def registration_view(request):
    if request.method == "POST":
        print(request.POST)

        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserRegistrationForm()
    context = {
        "form": form
    }
    return render(request, "web_site/registration.html", context)


def user_logout(request):
    logout(request)
    return redirect('home')


def create_article(request):
    if request.method == "POST":
        form = ArticleForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('article_detail', form.pk)
    else:
        form = ArticleForm()

    context = {
        "form": form
    }

    return render(request, 'web_site/article_form.html', context)


def profile_view(request, username):
    user = User.objects.get(username=username)
    articles = user.articles.all()
    total_views = [article.views for article in articles]
    context = {
        "user": user,
        "total_views": sum(total_views),
        "total_comments": 0,
        "articles": articles
    }
    return render(request, "web_site/profile.html", context)


def add_like_or_dislike(request, article_id, action):
    # add_like
    # add_dislike
    from django.shortcuts import get_object_or_404

    article = get_object_or_404(Article, pk=article_id)

    try:
        article.likes
    except Exception as e:
        Like.objects.create(article=article)

    try:
        article.dislikes
    except Exception as e:
        Dislike.objects.create(article=article)

    if action == 'add_like':
        if request.user in article.likes.user.all():
            article.likes.user.remove(request.user.pk)
        else:
            article.likes.user.add(request.user.pk)
            article.dislikes.user.remove(request.user.pk)
    elif action == 'add_dislike':
        if request.user in article.dislikes.user.all():
            article.dislikes.user.remove(request.user.pk)
        else:
            article.dislikes.user.add(request.user.pk)
            article.likes.user.remove(request.user.pk)
    return redirect(request.environ['HTTP_REFERER'])


def add_favorite(request, username, article_id):
    user = User.objects.filter(username=username).first()
    article = Article.objects.filter(pk=article_id).first()

    fav_obj = Favorite.objects.create(
        user=user,
        article=article
    )
    fav_obj.save()
    return redirect('home')


def delete_favorite(request, username, article_id):
    user = User.objects.filter(username=username).first()
    article = Article.objects.filter(pk=article_id).first()
    obj = Favorite.objects.filter(user=user, article=article).first()
    obj.delete()
    return redirect(request.environ['HTTP_REFERER'])


def user_favourites_view(request, username):
    user = User.objects.get(username=username)
    favorites = Favorite.objects.filter(user=user)
    articles = [fav.article for fav in favorites]
    context = {
        "articles": articles
    }
    return render(request, "web_site/favourites.html", context)

