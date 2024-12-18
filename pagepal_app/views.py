from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookUploadForm
from .models import Book
from ebooklib import epub
import ebooklib
from bs4 import BeautifulSoup
import re



# Function to clean excessive newlines, multiple spaces, and extra whitespace
def clean_html(content):
    # Replace multiple newlines with a single space or remove them completely
    content = re.sub(r'\n+', ' ', content)
    
    # Replace multiple spaces with a single space
    content = re.sub(r'\s+', ' ', content)
    
    # Remove leading and trailing spaces
    content = content.strip()
    
    return content

def home(request):
    query = request.GET.get('query', '') # obtain search query
    if query:
        books = Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            author__icontains = query
        ) | Book.objects.filter(
            genre__icontains = query
        )
    else:
        books = Book.objects.all()
    return render(request,'pagepal_app/home.html',{'books':books})

def upload(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookUploadForm()

    return render(request,'pagepal_app/upload_form.html',{'form':form})

def reader(request, book_id): #epub book reader
    book = get_object_or_404(Book, id=book_id)
    
    epub_path = book.epub_file.path

    reader = epub.read_epub(epub_path)

    content = []

    for item in reader.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, 'html.parser')
            currnt_content = str(soup)
            content.append(clean_html(currnt_content))  # Get the content as a string

    context = {
        'book':book,
        'book_content':content,
    }
    return render(request, 'pagepal_app/reader.html', context)