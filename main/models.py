from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count,Sum
import datetime

# Create your models here.
# Admin Model
class Owner(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.PositiveBigIntegerField(unique=True)
    profile_img=models.ImageField(upload_to='owner_imgs/',null=True)

    def __str__(self):
        return self.user.username
# vendor/seller model
class Vendor(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.PositiveBigIntegerField(unique=True,null=True)
    profile_img=models.ImageField(upload_to='seller_imgs/',null=True)
    address=models.TextField(null=True)
    
    def __str__(self):
        return self.user.username
    # For popular products distinct will work on postgresql else not work 
    @property
    def categories(self):
        cats=Product.objects.filter(vendor=self,category__isnull=False).values('category__title','category__id').order_by('category__title','category__id').distinct('category__title')
        return cats
# fetch daily order report
    @property
    def show_chart_daily_orders(self):
        orders=OrderItems.objects.filter(product__vendor=self).values('order__order_time__date').annotate(Count('id'))
        dateList=[]
        countList=[]  
        dataSet={}
        if orders:
            for order in orders:
                dateList.append(order['order__order_time__date'])
                countList.append(order['id__count'])
        dataSet={'dates':dateList,'count':countList}
        return dataSet
# fetch Monthly order report
    @property
    def show_chart_monthly_orders(self):
        orders=OrderItems.objects.filter(product__vendor=self).values('order__order_time__month').annotate(Count('id'))
        dateList=[]
        countList=[]  
        dataSet={}
        if orders:
            for order in orders:
                monthinteger=order['order__order_time__month']
                month=datetime.date(1900,monthinteger,1).strftime('%B')
                dateList.append(month)
                countList.append(order['id__count'])
        dataSet={'dates':dateList,'count':countList}
        return dataSet
# fetch yearly order report
    @property
    def show_chart_yearly_orders(self):
        orders=OrderItems.objects.filter(product__vendor=self).values('order__order_time__year').annotate(Count('id'))
        dateList=[]
        countList=[]  
        dataSet={}
        if orders:
            for order in orders:
                dateList.append(order['order__order_time__year'])
                countList.append(order['id__count'])
        dataSet={'dates':dateList,'count':countList}
        return dataSet

# fetch Total product by vendors
    @property
    def total_products(self):
        products_count=Product.objects.filter(vendor=self).count()
        return products_count
# Category
class ProductCategory(models.Model):
    title=models.CharField(max_length=200)
    detail=models.TextField(null=True)
    cat_img=models.ImageField(upload_to='category_imgs/',null=True)

    def __str__(self):
        return self.title
    # for admin
    class Meta:
        verbose_name_plural='Product Categories'
    # For Popular Categories Downloads
    @property
    def totala_downloads(self):
        totalDownloads=0
        products=Product.objects.filter(category=self)
        for product in products:
            if product.downloads:
                totalDownloads+=int(product.downloads)
        return totalDownloads
# Product
class Product(models.Model):
    category=models.ForeignKey(ProductCategory,on_delete=models.SET_NULL,null=True,related_name='category_product')
    vendor=models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True)
    title=models.CharField(max_length=200)
    detail=models.TextField(null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    usd_price=models.DecimalField(max_digits=10,decimal_places=2,default=80)
    slug = models.SlugField(null=True)
    tags=models.TextField(null=True,blank=True)
    image=models.ImageField(upload_to='product_imgs/',null=True,blank=True)
    demo_url=models.URLField(null=True,blank=True)
    product_file=models.FileField(upload_to='product_files/',null=True)
    downloads=models.CharField(max_length=200,default=0,null=True)
    publish_status=models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.title
    # method
    def tag_list(self):
        if self.tags:
            tagList=self.tags.split(",")
            return tagList
    
# Customer Model
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.PositiveBigIntegerField(unique=True)
    profile_img=models.ImageField(upload_to='customer_imgs/',null=True)
    # address=models.TextField(null=True)

    def __str__(self):
        return self.user.username

# Order Model
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,related_name='customer_orders')
    order_time=models.DateTimeField(auto_now_add=True)
    order_status=models.BooleanField(default=False)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_usd_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    trans_ref=models.TextField(null=True,blank=True)
    payment_mode=models.TextField(max_length=200,null=True,blank=True)
    
    def __str__(self):
        return '%s'% (self.order_time)

# order item model
class OrderItems(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items' )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    usd_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    def __str__(self):
        return self.product.title
    # for admin
    class Meta:
        verbose_name_plural='Order Items'

# Customer Address Model
class CustomerAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='customer_address')
    address=models.TextField()
    default_address=models.BooleanField(default=False)
# By default return address 
    def __str__(self):
        return self.address
# for admin
    class Meta:
        verbose_name_plural='Customer Addresses'
       
# Product rating and reviews
class ProductRating(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='rating_customers')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_ratings')
    rating=models.IntegerField()
    reviews=models.TextField()
    add_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating} - {self.reviews}'
    
# Product image
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,related_name='product_imgs')
    image=models.ImageField(upload_to='product_imgs/',null=True,blank=True)

    def __str__(self):
        return self.image.url

# for wishlist
class Wishlist(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural='Wish List'

    def __str__(self):
        return f"{self.product.title} - {self.customer.user.first_name}"

# For Notifications
class Notification(models.Model):
    owner=models.ForeignKey(Owner,on_delete=models.CASCADE,null=True)
    subject=models.CharField(max_length=200,verbose_name='message',null=True)
    notif_created_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='5. Notifications'
# For Contact
class Contact(models.Model):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    phone=models.CharField(max_length=50,null=True)
    address=models.TextField(max_length=200,null=True)
    query=models.CharField(max_length=200,null=True)
    countary=models.CharField(max_length=100,null=True)
    code=models.CharField(max_length=10,null=True)
    state=models.CharField(max_length=100,null=True)
    city=models.CharField(max_length=100,null=True)
    pincode=models.IntegerField(null=True)
    querydetail=models.TextField(max_length=200,null=True)

    def __str__(self):
        return self.name

    


    



    

