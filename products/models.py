from django.db import models
from users.models import CustomUser


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # Max price: 99999999.99
    category = models.CharField(max_length=255, blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True)
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
            raise ValueError("Out of stock stock!")

#rating
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5 scale
    comment = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"