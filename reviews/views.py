from django.http import HttpResponse
from django.shortcuts import render
from .utils import *
from .models import Book
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, 'base.html')


def book(request):
    search_text = request.GET.get('search') or 'Bookr'
    return render(request, 'search-results.html', {'search_text': search_text})


def book_search(request, id):
    book = get_object_or_404(Book, pk=id)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
    else:
        book_rating = None
    context = {"book": book,
               "book_rating": book_rating,
               "reviews": reviews
               }

    return render(request, 'book_detail.html', context)
