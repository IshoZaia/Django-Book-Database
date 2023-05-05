from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Welcome Bookr'),
    path('book-search/', views.book,  name='Bookr Search'),
    path('books/<int:id>/', views.book_search, name='View Book')
]