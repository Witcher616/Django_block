from django.urls import path
from . import views

# http://127.0.0.1:8000/
# path(путь, что сделать, кроткое название)
# path(endpoint, view, name='url name')

urlpatterns = [
    # path('', views.home_view, name='home'),
    path('', views.ArticleListView.as_view(), name='home'),
    path('categories/<str:category_id>/', views.category_articles, name="category_articles"),
    path('articles/<str:article_id>/', views.article_detail, name='article_detail'),

    path('login/', views.login_view, name="login"),
    path('registration/', views.registration_view, name="registration"),
    path('logout/', views.user_logout, name="logout"),

    path('create/article/', views.create_article, name="create"),
    path('delete/article/<int:pk>/', views.ArticleDeleteView.as_view(), name="delete"),
    path('update/article/<int:pk>/', views.ArticleUpdateView.as_view(), name="update"),

    path('search/', views.SearchResult.as_view(), name="search"),

    path('users/<str:username>/', views.profile_view, name="profile"),
    path('add_vote/<int:article_id>/<str:action>/', views.add_like_or_dislike, name='add_vote'),

    path('users/<str:username>/favourites/', views.user_favourites_view, name="user_fav"),
    path('users/<str:username>/favorites/add/<int:article_id>/', views.add_favorite, name='add_fav'),
    path('users/<str:username>/favorites/delete/<int:article_id>/', views.delete_favorite, name='delete_fav'),
]