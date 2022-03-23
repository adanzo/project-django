
from django.urls import path

from web_project import views
from . import views

urlpatterns = [
    path('',views.store, name="store"),
    path('store_Ar/<int:Ar>/',views.store_Ar,name='store_Ar'),
    path('store_He/<int:He>/',views.store_He,name='store_He'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]