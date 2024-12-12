from rest_framework import serializers, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics
from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer
from .pagination import ProductPagination

# List and Create Products


class ProductListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Retrieve, Update, and Delete Products


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductSearchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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

#list and create review
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')  # Get the product ID from the request
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product ID.")
        serializer.save(user=self.request.user, product=product)

# Retrieve Reviews for a Specific Product
class ProductReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)