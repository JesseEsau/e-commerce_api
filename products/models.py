from django.db import models
from users.models import CustomUser

#category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # Max price: 99999999.99
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock_quantity = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.name

    def reduce_stock(self, quantity):
        """Reduce stock when an order is placed."""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
        else:
            raise ValueError("Insufficient stock!")

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_date']

    def __str__(self):
        return f"Image for {self.product.name}"

#rating
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5 scale
    comment = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='wishlisted_by')
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicate wishlist entries for the same product by the same user

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    reserved = models.BooleanField(default=True)  # Mark as reserved or purchased
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Automatically reduce stock when an order is created.
        """
        if not self.pk:  # Only reduce stock for new orders
            self.product.reduce_stock(self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order by {self.user.username} for {self.product.name}"