from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    #slug is the url of the category it should be unique
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
##the function take the name of the category slug and bring to us the url fo particualr category
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
