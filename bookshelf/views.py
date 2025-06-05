from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.db import connection
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.password_validation import validate_password
from .models import Book, Review
from .forms import BookForm



# Create your views here.
def app(request):
    #user = request.user
    #if user.is_authenticated:
        query = request.GET.get('q', '')
        with connection.cursor() as cursor:
            if query:
                sql = f"SELECT id, title, author, publication_year, description_text, genre FROM bookshelf_book WHERE title LIKE '%{query}%'"
                # sql = "SELECT id, title, author, publication_year, description_text, genre FROM bookshelf_book WHERE title LIKE %s"
                # cursor.execute(sql, [f"%{query}%"])
            else:
                sql = "SELECT id, title, author, publication_year, description_text, genre FROM bookshelf_book"
                #cursor.execute(sql)
            cursor.execute(sql)
            books = cursor.fetchall()
        form = BookForm()
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                new_book = form.save(commit=False)
                new_book.save()
                return redirect('/')
        return render(request, 'app.html', {
            'books': books,
            'form': form,
            'query': query
        })
    # else:
    #     return render(request, 'error.html', {
    #         'message': 'You must be logged in to view the main page.'})
  

def book(request, book_id):
    #user = request.user
    #if user.is_authenticated:
        book = Book.objects.get(id=book_id)
        reviews = Review.objects.filter(book=book).select_related('user') 
        return render(request, 'book.html', {
            'book': book,
            'reviews': reviews
        })
    # else:
    #     return render(request, 'error.html', {
    #         'message': 'You must be logged in to view this book.'})


def review(request, book_id):
    # user = request.user
    # if user.is_authenticated:
        if request.method == 'POST':
            book = Book.objects.get(id=book_id)
            rating = request.POST.get('rating')
            review_text = request.POST.get('review_text')
            user = request.user
            if user.is_authenticated:
                Review.objects.create(book=book, user=user, rating=rating, review_text=review_text)
                return redirect(f'/book/{book_id}')
    # else:
    #     return render(request, 'error.html', {
    #         'message': 'You must be logged in to submit a review.'})


def handle_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'error.html', {
                'message': 'Invalid username or password.'})
    return render(request, 'welcome.html')

def welcome(request):
    user = request.user
    if user.is_authenticated:
        return redirect('/book')
    return render(request, 'welcome.html')

def handle_logout(request):
    logout(request)
    return redirect('/')

def create_user(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        # if form.is_valid():
        #      form.save()
        #      return redirect('/')
        # else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'error.html', {
                'message': 'Passwords do not match'})
        try:
            User.objects.create_user(username=username, password=password1)
            return redirect('/')
        except:
            return render(request, 'error.html', {'message': 'User not created.'})

def settings(request):
    #user = request.user
    #if user.is_authenticated:
        if request.method == 'POST':
            password1 = request.POST.get('new_password1')
            password2 = request.POST.get('new_password2')
            if password1 != password2:
                return render(request, 'error.html', {
                    'message': 'Passwords do not match'})
            user = request.user
            if user.is_authenticated:
                if password1:
                    try:
                        #validate_password(password1, user=user)
                        #user.set_password(password1)
                        user.password = password1
                        user.save()
                        update_session_auth_hash(request, user)
                        return redirect('/')
                    except Exception as e:
                        return render(request, 'error.html', {
                            'message': str(e)})
            else:
                return render(request, 'error.html', {
                    'message': 'You must be logged in to change password.'})
        return render(request, 'settings.html')
    # else:
    #     return render(request, 'error.html', {
    #         'message': 'You must be logged in to view settings page.'})
