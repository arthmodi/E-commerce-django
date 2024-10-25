from rest_framework.serializers import ModelSerializer, ValidationError, CharField
from app.models import *
from rest_framework.validators import UniqueValidator
from django.utils import timezone


class CustomerSerializer(ModelSerializer):
    name = CharField(
        validators=[UniqueValidator(queryset=Customer.objects.all())]
    )
    
    class Meta:
        model = Customer
        fields = ('name', 'contact_number', 'email')
        read_only_fields = ['id']
        
    # def validate_name(self, data):
    #     if Customer.objects.filter(name=data).exists():
    #         raise ValidationError("Customer name must be unique.")
    #     return data
    
    
class ProductSerializer(ModelSerializer):
    name = CharField(
        validators=[UniqueValidator(queryset=Product.objects.all())]
    )
    
    class Meta:
        model = Product
        fields = ('name', 'weight')
        read_only_fields = ['id']

    # def validate_name(self, data):
    #     if Product.objects.filter(name=data).exists():
    #         raise ValidationError("Product name must be unique.")
    #     return data

    def validate_weight(self, data):
        if data <= 0 or data > 25:
            raise ValidationError("Weight must be positive and not more than 25kg.")
        return data
    
    
class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        
        
class OrderSerializer(ModelSerializer):
    order_item = OrderItemSerializer(many=True, source='items')

    class Meta:
        model = Order
        fields = ['customer', 'order_date', 'address', 'order_item', 'order_number']
        read_only_fields = ['order_number']

    def validate_order_date(self, value):
        if value < timezone.now().date():
            raise ValidationError("Order date cannot be in the past.")
        return value

    def validate(self, data):
        items = data.get('items')
        total_weight = sum(item['quantity'] * item['product'].weight for item in items)

        if total_weight > 150:
            raise ValidationError("Order cumulative weight must be under 150kg.")
        
        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
    
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('items', None)

        instance.customer = validated_data.get('customer', instance.customer)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        if order_items_data is not None:
            for item_data in order_items_data:
                product_id = item_data.get('product') 
                order_item, created = OrderItem.objects.update_or_create(
                    order=instance,
                    product_id=product_id,
                    defaults={'quantity': item_data.get('quantity')}
                )
        return instance