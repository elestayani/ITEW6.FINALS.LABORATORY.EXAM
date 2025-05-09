from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, BorrowTransaction
from datetime import timedelta, timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class BookSerializer(serializers.ModelSerializer):
    borrow = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'copies_available', 'book', 'borrow']

    def get_borrow(self, obj):
        borrow = BorrowTransaction.objects.filter(book=obj).first()
        if borrow:
            return {
                'id': borrow.id,
                'status': borrow.status,  
            }
        return None

class BorrowTransactionSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    formatted_borrow_date = serializers.SerializerMethodField()
    formatted_return_date = serializers.SerializerMethodField()

    class Meta:
        model = BorrowTransaction
        fields = [
            'id', 'user', 'book', 'status',
            'formatted_borrow_date', 'formatted_return_date'
        ]
        
    def get_formatted_borrow_date(self, obj):
        western_time = obj.borrow_date.astimezone(timezone(timedelta(hours=-8))) 
        return western_time.strftime('%A, %B %d, %Y %I:%M %p')

    def get_formatted_return_date(self, obj):
        if obj.return_date:
            western_time = obj.return_date.astimezone(timezone(timedelta(hours=-8)))  
            return western_time.strftime('%A, %B %d, %Y %I:%M %p')
        return None

    def get_book(self, obj):
        book = Book.objects.filter(id=obj.book.id).first()
        if book:
            return {
                'id': book.id,
                'title': book.title,
                'image': 'http://127.0.0.1:8000' + book.book.url if book.book else None,
            }
        return None
