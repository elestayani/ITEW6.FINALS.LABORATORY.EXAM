from django.urls import path
from .views import (
    BookListCreateView,
    BookUpdateDeleteView,
    BorrowBookView,
    ReturnBookView,
    TransactionListView,
    UserListView,
    register_user,
    login_user
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/register/', register_user),
    path('api/login/', login_user),
    path('api/users/', UserListView.as_view()),
    path('api/books/', BookListCreateView.as_view()),
    path('api/books/<int:pk>/', BookUpdateDeleteView.as_view()),
    path('api/borrow/', BorrowBookView.as_view()),
    path('api/return/<int:borrow_id>/', ReturnBookView.as_view()),
    path('api/transactions/', TransactionListView.as_view()),
] + static('/', document_root=settings.MEDIA_ROOT)
