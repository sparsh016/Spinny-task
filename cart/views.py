# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.decorators import api_view
# from .models import Product, Cart, CartItem
# from .serializers import ProductSerializer, CartSerializer, AddCartItemSerializer
# from django.contrib.auth.models import User


# # ✅ List all products or create a new one
# class ProductList(APIView):
#     permission_classes = [IsAuthenticated]  # Use AllowAny for open access

#     def get(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ✅ Get the cart for a user
# class CartDetail(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, user_id):
#         cart, _ = Cart.objects.get_or_create(user_id=user_id)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)


# # ✅ Add item to cart
# class AddToCart(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id):
#         cart, _ = Cart.objects.get_or_create(user_id=user_id)
#         serializer = AddCartItemSerializer(data=request.data)
#         if serializer.is_valid():
#             product = serializer.validated_data['product']
#             quantity = serializer.validated_data['quantity']
#             item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#             if not created:
#                 item.quantity += quantity
#             item.save()
#             return Response({"message": "Added to cart"}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ✅ Remove item from cart
# class RemoveFromCart(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, user_id, product_id):
#         try:
#             cart = Cart.objects.get(user_id=user_id)
#             item = CartItem.objects.get(cart=cart, product_id=product_id)
#             item.delete()
#             return Response({"message": "Removed from cart"}, status=status.HTTP_200_OK)
#         except CartItem.DoesNotExist:
#             return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


# # ✅ Simple product create endpoint for testing
# @api_view(['POST'])
# def create_product(request):
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer, AddCartItemSerializer
from django.contrib.auth.models import User

# ✅ List all products or create a new one
class ProductList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Retrieve, update, or delete a specific product
class ProductDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Product not found'}, status=404)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Product not found'}, status=404)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Product not found'}, status=404)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'error': 'Product not found'}, status=404)
        product.delete()
        return Response({'message': 'Product deleted'}, status=204)

# ✅ Get the cart for a user
class CartDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

# ✅ Add item to cart
class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        cart, _ = Cart.objects.get_or_create(user_id=user_id)
        serializer = AddCartItemSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                item.quantity += quantity
            item.save()
            return Response({"message": "Added to cart"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Remove item from cart
class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id, product_id):
        try:
            cart = Cart.objects.get(user_id=user_id)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response({"message": "Removed from cart"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

# ✅ Optional: Simple product creation via function view (for test/demo)
@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

