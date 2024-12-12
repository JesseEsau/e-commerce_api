from rest_framework import serializers
from .models import Product
from .models import Product, Review

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