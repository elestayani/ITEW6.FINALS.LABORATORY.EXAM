from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Book, BorrowTransaction
from django.contrib.auth.models import User
from .serializers import BookSerializer, BorrowTransactionSerializer, UserSerializer

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    }, status=201)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username
    })

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# /api/books/ [GET, POST]
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# /api/books/<id>/ [PUT, DELETE]
class BookUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        if BorrowTransaction.objects.filter(book=book, status='borrowed').exists():
            return Response({'error': 'Cannot delete book with active borrow records.'}, status=400)
        return super().delete(request, *args, **kwargs)

# /api/borrow/ [POST]
class BorrowBookView(APIView):
    def post(self, request):
        user_id = request.data.get('user')
        book_id = request.data.get('book')

        book = get_object_or_404(Book, id=book_id)
        if book.copies_available < 1:
            return Response({'error': 'No copies available'}, status=400)

        book.copies_available -= 1
        book.save()

        transaction = BorrowTransaction.objects.create(user_id=user_id, book=book)
        serializer = BorrowTransactionSerializer(transaction)
        return Response(serializer.data, status=201)

# /api/return/<borrow_id>/ [POST]
class ReturnBookView(APIView):
    def post(self, request, borrow_id):
        try:
            transaction = get_object_or_404(BorrowTransaction, id=borrow_id)

            if transaction.status == 'returned':
                return Response({'error': 'Book already returned.'}, status=400)

            transaction.status = 'returned'
            transaction.return_date = timezone.now()
            transaction.save()

            book = transaction.book
            book.copies_available += 1
            book.save()

            return Response({'message': 'Book marked as returned'}, status=status.HTTP_200_OK)

        except BorrowTransaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

# /api/transactions/ [GET]
class TransactionListView(generics.ListAPIView):
    queryset = BorrowTransaction.objects.all()
    serializer_class = BorrowTransactionSerializer
