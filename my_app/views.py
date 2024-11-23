from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .models import ProductCategory, Item, ItemVariant, Product, Cart, Purchase
from .serializers import ProductSerializer, ProductCategorySerializer, ItemSerializer, CartSerializer, PurchaseSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ProductApiView(APIView):
    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)

class ProductDetailApiView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)



class ProductCategoryApiView(APIView):
    def get(self, request):
        product = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(product, many=True)
        return Response(serializer.data)

class ItemApiView(APIView):
    def get(self, request):
        item = Item.objects.all()
        serializer = ItemSerializer(item, many=True)
        return Response(serializer.data)

class ItemDetailApiView(APIView):
    def get(self, request, pk):
        category = Item.objects.get(pk=pk)
        serializer = ItemSerializer(category)
        return Response(serializer.data)




class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            cart_item = Cart.objects.get(pk=pk, user=request.user)
            cart_item.delete()
            return Response({"message": "Item removed from cart."}, status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response({"error": "Item not found in your cart."}, status=status.HTTP_404_NOT_FOUND)

class PurchaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        purchases = []
        for item in cart_items:
            total_price = item.product.price * item.quantity
            purchase = Purchase(
                user=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=total_price,
                payment_method=request.data.get('payment_method', 'cod'),
                payment_status=True  
            )
            purchase.save()
            purchases.append(purchase)

        
        cart_items.delete()

        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
