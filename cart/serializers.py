from django.forms import model_to_dict
from rest_framework import serializers

from book.models import Book
from cart.models import Cart, CartItem


class ActiveCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'price', 'quantity', 'book', 'cart']


class CartSerializers(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)
    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = Cart
        fields = ['id', 'total_quantity', 'total_price', 'status', 'user', "book", "items"]

    def create(self, validated_data):
        print(validated_data)
        book = validated_data.get("book")
        cart = Cart.objects.filter(user_id=validated_data.get("user").id, status=False)
        if not cart.exists():
            cart = Cart.objects.create(user_id=validated_data.get("user").id)
        else:
            cart = cart.first()
        cart_item = CartItem.objects.filter(book_id=book.id, cart_id=cart.id)
        if cart_item.exists():
            cart_item = cart_item.first()
            cart.total_price -= cart_item.price
            cart.total_quantity -= cart_item.quantity
            cart_item.price = validated_data.get("total_quantity") * book.price
            cart_item.quantity = validated_data.get("total_quantity")
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(book_id=book.id, cart_id=cart.id,
                                                quantity=validated_data.get("total_quantity"),
                                                price=validated_data.get("total_quantity") * book.price)

        cart.total_price += cart_item.price
        cart.total_quantity += cart_item.quantity
        cart.save()
        return cart

    def get_items(self, cart):
        items = cart.cartitem_set.filter(cart_id=cart.id)
        items = [model_to_dict(x) for x in items]
        return items
