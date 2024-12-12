from django.urls import path
from .views import ProductListCreateView, ProductDetailView, ProductSearchView, ReviewListCreateView, ProductReviewListView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('products/<int:product_id>/reviews/', ProductReviewListView.as_view(), name='product-reviews'),
]
