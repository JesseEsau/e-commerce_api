from django.urls import path
from .views import ProductListCreateView, ProductDetailView, ProductSearchView, ReviewListCreateView, ProductReviewListView, CategoryListCreateView, CategoryDetailView, ProductImageListCreateView, ProductImageDetailView, WishlistListView, WishlistAddView, WishlistRemoveView, OrderListCreateView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/search/', ProductSearchView.as_view(), name='product-search'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('products/<int:product_id>/reviews/', ProductReviewListView.as_view(), name='product-reviews'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('product-images/', ProductImageListCreateView.as_view(), name='product-image-list-create'),
    path('product-images/<int:pk>/', ProductImageDetailView.as_view(), name='product-image-detail'),
    path('wishlist/', WishlistListView.as_view(), name='wishlist-list'),
    path('wishlist/add/', WishlistAddView.as_view(), name='wishlist-add'),
    path('wishlist/remove/<int:pk>/', WishlistRemoveView.as_view(), name='wishlist-remove'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
]
