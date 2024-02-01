from rest_framework import serializers
from .import models
from django.contrib.auth.models import User
from rest_framework.response import Response

# vendors
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Vendor
        fields=['id','user','mobile','address','profile_img','categories']
    def __init__(self,*args,**kwargs):
        super(VendorSerializer,self).__init__(*args, **kwargs)
        # self.Meta.depth=1
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['user']=UserSerializer(instance.user).data
        return response
class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Vendor
        fields=['id','user','mobile','profile_img','address','show_chart_daily_orders','show_chart_monthly_orders','show_chart_yearly_orders','total_products']
    def __init__(self,*args, **kwargs):
        super(VendorDetailSerializer,self).__init__(*args, **kwargs)
        # # self.Meta.depth=1
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response["user"]=UserSerializer(instance.user).data
        return response
# Product Serializer
class ProductListSerializer(serializers.ModelSerializer):
    product_ratings=serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model=models.Product
        fields=['id','category','vendor','title','detail','price','slug','tag_list','product_ratings','image','product_file','downloads','usd_price','tags','publish_status']
    def __init__(self,*args, **kwargs):
        super(ProductListSerializer,self).__init__(*args, **kwargs)
        # self.Meta.depth=1
# product_image
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductImage
        fields='__all__'
class ProductDetailSerializer(serializers.ModelSerializer):
    # product_ratings=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    product_ratings=serializers.StringRelatedField(many=True,read_only=True)
    product_imgs=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        many=True
        model=models.Product
        fields=['id','category','vendor','title','detail','price','slug','tag_list','product_ratings','product_imgs','demo_url','image','product_file','downloads','usd_price','tags','publish_status']
    def __init__(self,*args, **kwargs):
        super(ProductDetailSerializer,self).__init__(*args, **kwargs)
        # self.Meta.depth=1
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['vendor']=VendorSerializer(instance.vendor).data
        return response
# User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name','last_name','username','email']
# Customer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Customer
        fields=['id','user','mobile','profile_img',]
    def __init__(self,*args, **kwargs):
        super(CustomerSerializer,self).__init__(*args, **kwargs)
        # add for fetching vendor customer
        # self.Meta.depth=1
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['user']=UserSerializer(instance.user).data
        return response
class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Customer
        fields=['id','user','mobile','profile_img']
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response["user"]=UserSerializer(instance.user).data
        return response
    
    # def __init__(self,*args, **kwargs):
    #     super(CustomerDetailSerializer,self).__init__(*args, **kwargs)
    #     self.Meta.depth=1
    # response["customer_orders"]=OrderSerializer(instance.customer_orders).data      
# Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Order
        fields=['id','customer','order_status','total_amount','total_usd_amount','trans_ref','payment_mode']
        # for uncomment for customer
    # def __init__(self,*args, **kwargs):
    #     super(OrderSerializer,self).__init__(*args, **kwargs)
    #     self.Meta.depth=1
# OrderItems seralizers
class OrderItemsSerializer(serializers.ModelSerializer):
    # order=OrderSerializer()
    # product=ProductDetailSerializer()
    class Meta:
        model=models.OrderItems
        fields=['id','order','product','quantity','price','usd_price']
        # Nested seralizer
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['order']=OrderSerializer(instance.order).data
        response['customer']=CustomerSerializer(instance.order.customer).data
        response['user']=UserSerializer(instance.order.customer.user).data
        response['product']=ProductDetailSerializer(instance.product).data
        return response
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     order = instance.order
    #     if order and order.customer and order.customer.user:
    #         response['order'] = OrderSerializer(order).data
    #         response['customer'] = CustomerSerializer(order.customer).data
    #         response['user'] = UserSerializer(order.customer.user).data
    #     else:
    #     # Handle cases where order, customer, or user are missing
    #     # Adjust response accordingly
    #         response['product'] = ProductDetailSerializer(instance.product).data
    #     return response
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.OrderItems
        fields=['id','order','product','quantity','price','usd_price','trans_ref','payment_mode']
    def __init__(self,*args, **kwargs):
        super(OrderDetailSerializer,self).__init__(*args, **kwargs)
        # self.Meta.depth=1
# Customer address seralizer
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CustomerAddress
        fields=['id','customer','address','default_address'] 
    def __init__(self,*args, **kwargs):
        super(CustomerAddressSerializer,self).__init__(*args, **kwargs)
        # self.Meta.depth=1
# Rating
class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductRating
        fields=['id','customer','product','rating','reviews','add_time'] 

    def __init__(self,*args, **kwargs):
        super(ProductRatingSerializer,self).__init__(*args, **kwargs)
        # without depth show only id but with depth show customer data here fetch
        # self.Meta.depth=1
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['customer']=CustomerSerializer(instance.customer).data
        return response
# Cateogry
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductCategory
        fields=['id','title','detail','cat_img','totala_downloads',]
    def __init__(self,*args,**kwargs):
        super(CategorySerializer,self).__init__(*args, **kwargs)
        # self.Meta.depth=1
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductCategory
        fields=['id','title','detail','cat_img','totala_downloads']
    def __init__(self,*args, **kwargs):
        super(CategoryDetailSerializer,self).__init__(*args, **kwargs)
        # self.Meta.depth=1
# Wishlist Searlizer
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Wishlist
        fields=['id','product','customer']
    def __init__(self,*args, **kwargs):
        super(WishlistSerializer,self).__init__(*args, **kwargs)
    
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['customer']=CustomerSerializer(instance.customer).data
        response['product']=ProductDetailSerializer(instance.product).data
        return response
# Notifications seralizer
class NotificationsListSerializer(serializers.ModelSerializer):
    class Meta:
         model=models.Notification
         fields=['id','owner','subject','notif_created_time']
    def __init__(self,*args,**kwargs):
        super(NotificationsListSerializer,self).__init__(*args, **kwargs)
class NotificationsDetailSerializer(serializers.ModelSerializer):
    class Meta:
         model=models.Notification
         fields='__all__'
    def __init__(self,*args,**kwargs):
        super(NotificationsDetailSerializer,self).__init__(*args, **kwargs)
#For contact
class contactUsListSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Contact
        fields='__all__'  
class contactUsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Contact
        fields='__all__'  