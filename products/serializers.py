from rest_framework import serializers
from .models import Product
from .models import Product, Review, Category, Wishlist, Order

#serialize product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        # Ensure required fields have valid values
        if data.get('price') is None or data['price'] <= 0:
            raise serializers.ValidationError(
                {"price": "Price must be greater than zero."})
        if data.get('stock_quantity') is None or data['stock_quantity'] < 0:
            raise serializers.ValidationError(
                {"stock_quantity": "Stock Quantity must be non-negative."})
        if not data.get('name'):
            raise serializers.ValidationError({"name": "Name is required."})
        return data

from rest_framework import serializers
from .models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'uploaded_date']
        read_only_fields = ['id', 'uploaded_date']

#serialize reviews
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of user ID

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_date']
        read_only_fields = ['id', 'user', 'created_date']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_date']  # Include the fields you want to expose
        read_only_fields = ['id', 'created_date']

    def validate_name(self, value):
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value


class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of user ID

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'added_date']
        read_only_fields = ['id', 'user', 'added_date']


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')  # Include product name in response

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'product_name', 'quantity', 'reserved', 'created_date']
        read_only_fields = ['id', 'user', 'product_name', 'created_date']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        product = data['product']
        if product.stock_quantity < data['quantity']:
            raise serializers.ValidationError("Insufficient stock available for this product.")
        return data