from django.urls import path, include
from .views import (ProductApiView, ProductCategoryApiView, ItemApiView, ItemDetailApiView,
                    ProductDetailApiView, CartView, PurchaseView)

urlpatterns = [
    path('product/', ProductApiView.as_view(), name='product'),
    path('product/<int:pk>/', ProductDetailApiView.as_view(), name='product-detail'),
    path('category/', ProductCategoryApiView.as_view(), name='category'),
    path('category/item/', ItemApiView.as_view(), name='item'),
    path('category/item/<int:pk>/', ItemDetailApiView.as_view(), name='item-detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart_detail'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
]
