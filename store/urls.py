from django.urls import path
from store.views import *
from django.urls import path, include

urlpatterns = [
    path('',index,name="index"),
    path('books/',bookListView,name="book-list"),
    path('book/<int:bid>/',bookDetailView,name='book-detail' ),
    path('books/loaned/',viewLoanedBooks,name="view-loaned"),
    path('books/loan/',loanBookView,name="loan-book"),
    path('books/return',returnBookView,name="return-book"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', login_user, name="login"),
    path('books/rating', returnRating, name="return-rating"),
    path('signup/', signup, name="sign-up")
]
