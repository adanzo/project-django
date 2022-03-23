from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404, redirect
from .forms import ReviewForm
from django.contrib import messages
from carts.models import CartItem
from .models import Product, ReviewRating,ProductGallery
from category.models import Category
from carts.models import  CartItem 
from carts.views import _cart_id# bring the private function _cart_id from app carts
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.db.models import Q
from orders.models import OrderProduct
from django.utils import translation

# Create your views here.
def store(request,category_slug=None):
    # we bringing the slug here from urls file so nowe we have to accept the slug 
    categories = None
    products=None
    if category_slug!=None:
        #bring the categories if found if not found it will return 404 page(error)
      categories = get_object_or_404(Category, slug=category_slug)
      #bring to us all the product of this category
      products = Product.objects.filter(category=categories, is_available=True).order_by('id')
      paginator= Paginator(products,1)#6 is number of the products we want to show in each page  
      page= request.GET.get('page')
      paged_products=paginator.get_page(page)#the 6 product we get stored in paged_products and the (paged_products)pass in the template  
      product_count = products.count()

    else:
      products = Product.objects.all().filter(is_available=True)#we get all the products
      paginator= Paginator(products,5)#6 is number of the products we want to show in each page  
      page= request.GET.get('page')
      paged_products=paginator.get_page(page)#the 6 product we get stored in paged_products and the (paged_products)pass in the template
      product_count = products.count()
      
    context={
        'products': paged_products,#we passed to the template only 6 product in each page 
        'product_count':product_count,
    }
    return render(request,'store/store.html',context)
  
  
  
def product_detail(request, category_slug, product_slug):
      # to pick a product from category first we should get this category and from this category we need to access to the slug to this category 
      # the category is in app.store.models.class product 
      # the slug of this category in  app.category.models.class category
  try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
  except Exception as e:
      raise e

  if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
  else:
        orderproduct = None

    # Get the reviews
  reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
  product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

  context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
  return render(request, 'store/product_detail.html', context)



def search(request):
      #check if the keyword that we get from template navbar does exist if yes we put it in keyword parameter
  if 'keyword' in request.GET:
    keyword=request.GET['keyword']
    if keyword:
      products= Product.objects.order_by('-created_date').filter( Q(description__icontains=keyword) | Q(product_name__icontains=keyword))#icontains means check every thind in the serach if match to keyword Q()is like OR
      product_count = products.count()
  context={
    'products':products,
    'product_count':product_count,
  }
  return render(request,'store/store.html',context)




def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')#store the current url 
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            #we pass the instance because if was a review before we pass it 
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)#the user will add new review 
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')#store the ip address
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)



def store_He(request,He):
    categories = None
    products=None
    products = Product.objects.all().filter(is_available=True)#we get all the products
    paginator= Paginator(products,5)#6 is number of the products we want to show in each page  
    page= request.GET.get('page')
    paged_products=paginator.get_page(page)#the 6 product we get stored in paged_products and the (paged_products)pass in the template
    product_count = products.count()
      
    context={
        'products': paged_products,#we passed to the template only 6 product in each page 
        'product_count':product_count,
    }
    return render(request,'store/store_He.html',context)
  
  
  
  
def store_Ar(request,Ar,category_slug):
    categories = None
    products=None
    if category_slug!=None:
        #bring the categories if found if not found it will return 404 page(error)
      categories = get_object_or_404(Category, slug=category_slug)
      #bring to us all the product of this category
      products = Product.objects.filter(category=categories, is_available=True).order_by('id')
      paginator= Paginator(products,1)#6 is number of the products we want to show in each page  
      page= request.GET.get('page')
      paged_products=paginator.get_page(page)#the 6 product we get stored in paged_products and the (paged_products)pass in the template  
      product_count = products.count()

    else:
      products = Product.objects.all().filter(is_available=True)#we get all the products
      paginator= Paginator(products,5)#6 is number of the products we want to show in each page  
      page= request.GET.get('page')
      paged_products=paginator.get_page(page)#the 6 product we get stored in paged_products and the (paged_products)pass in the template
      product_count = products.count()
      
    context={
        'products': paged_products,#we passed to the template only 6 product in each page 
        'product_count':product_count,
    }
    return render(request,'store/store_Ar.html',context)
  