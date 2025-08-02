
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticated

from .models import Product, Category, Tag, Order, OrderItem
from .serializers import ProductSerializer, ProductCreateUpdateSerializer, CategorySerializer, TagSerializer, \
    CartSerializer, OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem, Product
from .serializers import CartItemSerializer

# Maxsulatlar APP
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category__name', 'tags__name', 'price']
    ordering_fields = ['price', 'name']
    search_fields = ['name', 'description']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartListCreateView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
# Create your views here.
#Savat

class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        # User savati
        cart, created = Cart.objects.get_or_create(user=request.user)

        # CartItem qo'shamiz yoki mavjud bo'lsa quantity ni oshiramiz
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if not cart_item:
            return Response({'error': 'Product not in cart'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({'message': 'Product removed from cart'}, status=status.HTTP_200_OK)

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_items = CartItem.objects.filter(cart__user=request.user)
        if not cart_items.exists():
            return Response({"message": "Savat bo'sh!"}, status=400)

        # Order yaratish
        order = Order.objects.create(user=request.user)

        # OrderItem yaratish va Cartdagi mahsulotlarni Orderga o'tkazish
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # Cartni tozalash
        cart_items.delete()

        return Response({"message": f"Buyurtma #{order.id} muvaffaqiyatli qabul qilindi!"})

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class AdminOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    queryset = Order.objects.all()