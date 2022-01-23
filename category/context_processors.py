#it takes a request as an argument it will return the dictionary of data as a context 
from .models import Category

def menu_links(request):
    #all the categories from database
    links = Category.objects.all()
    return dict(links=links)