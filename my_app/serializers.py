from rest_framework import serializers
from .models import ProductCategory, Item, ItemVariant, Product, Cart, Purchase



class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=False, read_only=True)

    class Meta:
        model = Item
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['category'] = instance.category.name if instance.category else None
    #     return representation


class ItemVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVariant
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(many=False, read_only=True)
    item = ItemSerializer(many=False, read_only=True)
    variant = ItemVariantSerializer(many=False, read_only=True)
    

    class Meta:
        model = Product
        fields = ['item', 'category', 'variant', 'color', 'quantity']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['item'] = instance.item.name if instance.item else None
        representation['category'] = instance.category.name if instance.category else None
        representation['variant'] = instance.variant.name if instance.variant else None
        return representation


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity', 'added_at']
        read_only_fields = ['user', 'added_at']



class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'payment_method', 'payment_status', 'purchased_at']
        read_only_fields = ['user', 'total_price', 'payment_status', 'purchased_at']