from django.db import models

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    
    class Meta:
        unique_together = ('email', 'contact_number')
        

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=10, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    address = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('order_number').last()
            if last_order and last_order.order_number.startswith("ORD"):
                try:
                    last_order_number = int(last_order.order_number[3:])
                except ValueError:
                    last_order_number = 0
            else:
                last_order_number = 0

            new_order_number = f"ORD{str(last_order_number + 1).zfill(5)}"
            self.order_number = new_order_number
        super(Order, self).save(*args, **kwargs)
    
    
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
