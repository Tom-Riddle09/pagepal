from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    epub_file = models.FileField(upload_to='books/')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.author}'