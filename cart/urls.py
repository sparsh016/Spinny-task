# from django.urls import path
# from .views import *

# urlpatterns = [
#     path('products/', ProductList.as_view()),
#     path('cart/<int:user_id>/', CartDetail.as_view()),
#     path('cart/<int:user_id>/add/', AddToCart.as_view()),
#     path('cart/<int:user_id>/remove/<int:product_id>/', RemoveFromCart.as_view()),
# ]



from django.urls import path
from .views import (
    ProductList,
    ProductDetail,
    CartDetail,
    AddToCart,
    RemoveFromCart,
    create_product
)

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),                  # GET, POST
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),    # GET, PUT, PATCH, DELETE
    path('cart/<int:user_id>/', CartDetail.as_view(), name='cart-detail'),         # GET
    path('cart/<int:user_id>/add/', AddToCart.as_view(), name='add-to-cart'),      # POST
    path('cart/<int:user_id>/remove/<int:product_id>/', RemoveFromCart.as_view(), name='remove-from-cart'),  # DELETE
    path('products/create/simple/', create_product, name='create-product'),        # optional POST via function
]

