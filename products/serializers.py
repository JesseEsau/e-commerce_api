from rest_framework import serializers
from .models import Product


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
