from rest_framework import viewsets
from rest_framework.response import Response
from app.models import Customer, Product, Order
from app.serializers import CustomerSerializer, ProductSerializer, OrderSerializer

class CustomerViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ProductViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.query_params.get('products', None)
        customer = self.request.query_params.get('customer', None)

        if product:
            queryset = queryset.filter(items__product__name__in=product.split(',')).distinct()
        if customer:
            queryset = queryset.filter(customer__name=customer).distinct()

        return queryset
