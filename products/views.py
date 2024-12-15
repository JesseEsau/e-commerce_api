from rest_framework import serializers, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, generics
from .models import Product, Review, Category, ProductImage, Wishlist
from .serializers import ProductSerializer, ReviewSerializer, CategorySerializer, ProductImageSerializer, WishlistSerializer
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

class ProductImageListCreateView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()  # Automatically links user and product

class ProductImageDetailView(generics.RetrieveDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Authenticated users can create

# Retrieve, Update, and Delete a Category
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Authenticated users can edit/delete



class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return wishlist items for the logged-in user
        return Wishlist.objects.filter(user=self.request.user)

class WishlistAddView(generics.CreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Associate the wishlist item with the logged-in user
        serializer.save(user=self.request.user)

class WishlistRemoveView(generics.DestroyAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow users to remove items from their own wishlist
        return Wishlist.objects.filter(user=self.request.user)