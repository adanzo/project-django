from django.shortcuts import render,get_object_or_404, redirect
from .models import Product
from category.models import Category

# Create your views here.
def store(request,category_slug=None):
    # we bringing the slug here from urls file so nowe we have to accept the slug 
    categories = None
    products=None
    if category_slug!=None:
        #bring the categories if found if not found it will return 404 page(error)
      categories = get_object_or_404(Category, slug=category_slug)
      #bring to us all the product of this category
      products = Product.objects.filter(category=categories, is_available=True)   
    else:
      products = Product.objects.all().filter(is_available=True)
      product_count = products.count()
    product_count = products.count()
    context={
        'products': products,
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)
  
  
  
def product_detail(request, category_slug, product_slug):
      # to pick a product from category first we should get this category and from this category we need to access to the slug to this category 
      # the category is in app.store.models.class product 
      # the slug of this category in  app.category.models.class category
  try:
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)#category__slug to access to the slug of this category we want to equal to category slug that we take from the user 
  except Exception as e :
   raise e
  context= {
    'single_product':single_product
  }
  return render(request, 'store/product_detail.html',context)
