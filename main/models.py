from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Movie(models.Model):
    title = models.CharField(max_length=200)  
    description = models.TextField()        
    release_date = models.DateField()         
    duration_minutes = models.IntegerField() 
    genre = models.CharField(max_length=100)  
    poster = models.ImageField(upload_to='posters/')  
    imdb_rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

