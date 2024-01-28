from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product,Notification

@receiver(post_save,sender=Product)
def notify_admin_on_product_add(sender,instance,**kwargs):
    print(f"Debug: Product '{instance.title} added by username {instance.vendor} and Id is {instance.vendor.id}")
#Create notification for new product added by vendor/seller
    Notification.objects.create(
        subject=f"New product '{instance.title}' added by {instance.vendor} and Id is {instance.vendor.id}"
    ) 

