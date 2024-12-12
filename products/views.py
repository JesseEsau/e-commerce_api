from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions

from .models import Product
from .serializers import ProductSerializer
from .pagination import ProductPagination

# List and Create Products


class ProductListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Retrieve, Update, and Delete Products


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    # Enable filtering
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'category']  # Search by name or category

    # Define filter fields
    filterset_fields = {
        'category': ['exact'],  # Filter by exact category
        'price': ['gte', 'lte'],  # Filter by price range
        # Filter by stock availability (e.g., in-stock)
        'stock_quantity': ['gte'],
    }
