from django.db import models
from django.conf import settings
import uuid
from django.core.exceptions import ValidationError

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.category} ({self.name})"

class ItemVariant(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.item} ({self.name})"

COLOR_CHOICES=[
    ('red', 'Red'),
    ('white', 'White'),
    ('black', 'Black'),
    ('blue', 'Blue'),
]

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    variant = models.ForeignKey(ItemVariant, on_delete=models.CASCADE, null=True, blank=True)
    color = models.CharField(max_length=70, choices=COLOR_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)


    def clean(self):
        if self.item.category != self.category:
            raise ValidationError(
                f"The item '{self.item.name}' does not belong to the category '{self.category.name}'."
            )

        if self.variant and self.variant.item != self.item:
            raise ValidationError(
                f"The variant '{self.variant.name}' does not belong to the item '{self.item.name}'."
            )


    def save(self, *args, **kwargs):
        self.clean()

        if not self.product_code:
            self.product_code = str(uuid.uuid4())[:15].replace("-", "").upper()

        super().save(*args, *kwargs)

    def __str__(self):
        return f"{self.category.name} -- {self.item.name} -- {self.variant.name if self.variant else 'No Variant'}"




class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Purchase(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.BooleanField(default=False)  # False = Pending, True = Paid
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.payment_method}"


