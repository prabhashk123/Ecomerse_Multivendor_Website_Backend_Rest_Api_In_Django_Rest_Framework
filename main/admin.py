from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Vendor)
# admin.site.register(models.Product)
admin.site.register(models.ProductCategory)
admin.site.register(models.Customer)
# admin.site.register(models.Order)
admin.site.register(models.CustomerAddress)
admin.site.register(models.ProductRating)
admin.site.register(models.Owner)

# Product image
admin.site.register(models.ProductImage)
class ProductImageInline(admin.StackedInline):
    model=models.ProductImage
    
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','price','usd_price','publish_status','downloads']
    list_editable=['usd_price']
    prepopulated_fields={'slug':('title',)}
    inlines=[
        ProductImageInline,
    ]
admin.site.register(models.Product,ProductAdmin)

# Modify customer admin 
class CustomerAdmin(admin.ModelAdmin):
    list_display=['get_username','mobile']
    def get_username(self,obj):
        return obj.user.username
    
# Modify Order in admin
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','customer_id','customer','order_time','total_amount','total_usd_amount','order_status','payment_mode','trans_ref']
admin.site.register(models.Order,OrderAdmin)

# Modify OrderItems
class OrderItemsAdmin(admin.ModelAdmin):
    list_display=['id','order','product','quantity','price','usd_price']

admin.site.register(models.OrderItems,OrderItemsAdmin)

# Modify Wishlist
class WishlistAdmin(admin.ModelAdmin):
    list_display=['id','product','customer']

admin.site.register(models.Wishlist,WishlistAdmin)
# Modify Notifications model
class NotificationsAdmin(admin.ModelAdmin):
    list_display=['id','owner','subject','notif_created_time']
admin.site.register(models.Notification,NotificationsAdmin)
# for contact
class ContactUsAdmine(admin.ModelAdmin):
    list_display=['id','name','email','code','phone','address','pincode','countary','state','city','query','querydetail']
admin.site.register(models.Contact,ContactUsAdmine)