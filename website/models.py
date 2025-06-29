from django.db import models

# Create your models here.
class Title(models.Model):
    show_id = models.CharField(max_length = 20, unique = True)
    type = models.CharField(max_length = 20)  # Movie or TV Show
    title = models.CharField(max_length = 255) #Name of Movie/ Series, (Naruto, Blood & Water)
    director = models.TextField(null = True, blank = True)  # Multiple Directors, co directors included as well
    cast = models.TextField(null = True, blank = True)  # A lot of actors, a lot of names
    country = models.TextField(null = True, blank = True)  # Multiple countries possible
    date_added = models.DateField(null = True, blank = True)
    release_year = models.IntegerField()
    rating = models.CharField(max_length = 20, null = True, blank = True) # PG-13 , R and many more
    duration = models.CharField(max_length = 20, null = True, blank = True)
    listed_in = models.TextField()  # Genres
    description = models.TextField() # Synopsis of movie
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Netflix Title'
        verbose_name_plural = 'Netflix Titles'