from rest_framework import serializers
from .models import *

#Maxsulatlar APP

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

        #Savat

class CartItemSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'product_detail']

    def get_product_detail(self, obj):
        return {
            'name': obj.product.name,
            'price': obj.product.price
        }

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['user']

class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'product_detail']

    def get_product_detail(self, obj):
        return {
            'name': obj.product.name,
            'price': obj.product.price
        }

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'items']
        read_only_fields = ['user', 'status']

class CheckoutSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)
