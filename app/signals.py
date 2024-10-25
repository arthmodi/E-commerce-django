# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from app.models import Order


# @receiver(pre_save, sender=Order)
# def set_order_number(sender, instance):
#     last_id = Order.objects.only('order_number').order_by('id').last()
#     if last_id:
#         last_order = int(last_id.order_number[3:])
#         instance.order_number = f"ORD{str(last_order+1).zfill(5)}"
#     else:
#         instance.order_number = "ORD00001"