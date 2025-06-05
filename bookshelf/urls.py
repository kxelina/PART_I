from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('book', views.app, name='addbook'),
    path('book/<int:book_id>/', views.book, name='book'),
    path('login', views.handle_login, name='login'),
    path('logout', views.handle_logout, name='logout'),
    path('create_user', views.create_user, name='create_user'),
    path('review/book/<int:book_id>', views.review, name='review'),
    path('settings', views.settings, name='settings')
]
