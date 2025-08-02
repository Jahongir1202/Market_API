# store_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddToCartView, RemoveFromCartView, OrderListCreateView, CheckoutView, AdminOrderListView
from .views import (
    ProductListView, ProductDetailView, ProductCreateView,
    ProductUpdateView, ProductDeleteView, CategoryListCreateView, TagListCreateView,
    ProductViewSet, CartListCreateView, CartDetailView
)

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('store_app/', ProductListView.as_view(), name='product-list'),
    path('store_app/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('admin/store_app/', ProductCreateView.as_view(), name='product-create'),
    path('admin/store_app/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('admin/store_app/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('admin/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('admin/tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('cart/', CartListCreateView.as_view(), name='cart-list-create'),
    path('cart/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-order-list'),

]
