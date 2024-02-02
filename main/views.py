# genrics import for data in list api
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import generics,permissions,pagination,viewsets
from . import models
from . import serializers
from django.http import HttpResponse, JsonResponse
# for login paost
from django.views.decorators.csrf import csrf_exempt
# django make hasers password
from django.contrib.auth import authenticate
# create base user
from django.contrib.auth.models import User
# for mobile no unique
from django.db import IntegrityError
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password 
from django.db.models import Count
# razorpay
import razorpay
# for django mail
from django.conf import settings
from django.core.mail import send_mail
# for search
from django.db.models import Q

# Create your views here.
# vendors & Seller below in order by n (- means desending order)
class VendorList(generics.ListCreateAPIView):
    queryset=models.Vendor.objects.all()
    serializer_class=serializers.VendorSerializer
    # permision for admin level
    # permision_classes=[permissions.IsAuthenticated]
    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.VendorSerializer(queryset,many=True)
        return Response(serializer.data)
    def get_queryset(self):
        qs = super().get_queryset()
        if 'fetch_limit' in self.request.GET:
            limit = int(self.request.GET['fetch_limit'])
            qs=qs.annotate(downloads=Count('product')).order_by('-downloads','-id')
            qs = qs[:limit ]
        return qs   
class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Vendor.objects.all()
    serializer_class=serializers.VendorDetailSerializer
    # permision_classes=[permissions.IsAuthenticated]
# for vendor/seller Productlist
class VendorProductList(generics.ListAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductListSerializer
    # for json error
    def list(self, request,**kwargs):
        queryset = self.get_queryset()
        serializer = serializers.ProductListSerializer(queryset,many=True)
        return Response(serializer.data)
    # For address-list here order_by is use for default address
    def get_queryset(self):
        qs = super().get_queryset()
        vendor_id=self.kwargs['vendor_id']
        qs=qs.filter(vendor__id=vendor_id).order_by('id')
        return qs
# for seller/vendor register
@csrf_exempt
def vendor_register(request):
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    username=request.POST.get('username')
    email=request.POST.get('email')
    mobile=request.POST.get('mobile')
    address=request.POST.get('address')
    password=request.POST.get('password')
    try:
        user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
        print(user)
        if user:
            try:
                # Create vendor unique from vendor model
                vendor=models.Vendor.objects.create(
                    user=user,
                    mobile=mobile,
                    address=address
                )
                msg={
                    'bool':True,
                    'user':user.id,
                    'customer':vendor.id,
                    'msg':'Thank you for your registration! you can login now'
                }
            except IntegrityError:
                 msg={
                'bool':False,
                'msg':'Mobile Number Allready exist',
                }
        else:
            msg={
                'bool':False,
                'msg':'Oops...Something went to Wrong!!',
                }
    except IntegrityError:
        msg={
                'bool':False,
                'msg':'Username Allready exist',
                }

    return JsonResponse(msg)
# vendor login
@csrf_exempt
def vendor_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    # print(username)
    if user:
        vendor=models.Vendor.objects.get(user=user)
        msg={
            'bool':True,
            'user':user.username,
            'id':vendor.id
         }
    else:
        msg={
            'bool':False,
            'msg':'Invalid username/password',
            }
    return JsonResponse(msg)
# Vendor/seller change password
@csrf_exempt
def vendor_change_password(request,vendor_id):
    password=request.POST.get('password')
    vendor=models.Vendor.objects.get(id=vendor_id)
    user=vendor.user
    user.password=make_password(password)
    user.save()
    msg={'bool':True,'msg':'Password has been changed'}
    return JsonResponse(msg)
# Vendor/Seller Forgot password
@csrf_exempt
def vendor_forgot_password(request):
        email=request.POST.get('email')
        # Use the appropriate field path to access it, such as user.email if the email is stored in a related User model.
        verify=models.Vendor.objects.filter(user__email=email).first()
        if verify:
            link=f'http://localhost:3000/seller/resetpassword/{verify.id}'
            subject = 'Your account needs to be verified'
            email_from = settings.EMAIL_HOST_USER
            html_message=f'please click this link. {link}'
            send_mail(subject , html_message , email_from , [email])
            return JsonResponse({'bool':True,'msg':'Email has been sent successfully'})
        else:
            return JsonResponse({'bool':False,'msg':'Invalid Email!!'})
# Vendor/Seller Reset password
@csrf_exempt
def vendor_reset_password(request, vendor_id):
    vendor = models.Vendor.objects.filter(id=vendor_id).first()
    if vendor:
        user=vendor.user      
        if user:
            password = request.POST.get('password')
            if password is not None and password.strip():
                user.set_password(password) #relationship Customer is related to User use set_password()
                user.save() 
                return JsonResponse({'bool': True,  'msg': 'Password has been updated successfully'})
            else:
                return JsonResponse({'bool': False, 'msg': 'Password is Empty'})
        else:
            return JsonResponse({'bool': False, 'msg': 'Vendor has no associated user'})
    else:
        return JsonResponse({'bool': False, 'msg': 'Vendor not found'})
# Product
class ProductList(generics.ListCreateAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductListSerializer
    # pagination_class = pagination.PageNumberPagination
    pagination_class=pagination.LimitOffsetPagination
    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        if self.request.method == 'GET':
            if 'category' in self.request.GET:
                category = self.request.GET['category']
                category = models.ProductCategory.objects.get(id=category)
                qs = qs.filter(category=category)
            if 'fetch_limit' in self.request.GET:
                limit = int(self.request.GET['fetch_limit'])
                qs = qs[:limit ]
            if 'fetch_popular_products_limit' in self.request.GET:
                limit = int(self.request.GET['fetch_popular_products_limit'])
                qs=qs.order_by('-downloads','-id')
                qs = qs[:limit ]
            if 'searchproductstring' in self.kwargs:
                search = self.kwargs['searchproductstring']
                if search:
                    qs = models.Product.objects.filter(Q(title__icontains=search)|Q(detail__icontains=search))
                else:
                    qs = models.Product.objects.all()
            return qs  
# Product Modify For admin
class ProductModify(generics.RetrieveUpdateAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductListSerializer 
# Product Image
class ProductImgsList(generics.ListCreateAPIView):
    queryset=models.ProductImage.objects.all()
    serializer_class=serializers.ProductImageSerializer
    # pagination_class = pagination.PageNumberPagination
    # pagination_class=pagination.LimitOffsetPagination
    def list(self,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.ProductImageSerializer(queryset,many=True)
        return Response(serializer.data)
class ProductImgsDetail(generics.ListCreateAPIView):
    queryset=models.ProductImage.objects.all()
    serializer_class=serializers.ProductImageSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.kwargs['product_id']
        qs = qs.filter(product__id=product_id)
        return  qs
    def list(self,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.ProductImageSerializer(queryset,many=True)
        return Response(serializer.data)
#For image delete
class ProductImgDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.ProductImage.objects.all()
    serializer_class=serializers.ProductImageSerializer
    # for json        
# Taglist
class TagProductList(generics.ListCreateAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductListSerializer
    pagination_class = pagination.PageNumberPagination
    # pagination_class=pagination.LimitOffsetPagination
    # icontains add here
    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.kwargs['tag']
        qs = qs.filter(tags__icontains=tag)
        return qs   
# Related product
class RelatedProductList(generics.ListCreateAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductListSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()
        product_id=self.kwargs['pk']
        product=models.Product.objects.get(id=product_id)
        qs=qs.filter(category=product.category).exclude(id=product_id)
        return qs
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Product.objects.all()
    serializer_class=serializers.ProductDetailSerializer
# for Product downloads
@csrf_exempt
def update_product_download_count(request,product_id):
    msg = {'bool': False}  # Initialize msg here
    if request.method=='POST':
        product=models.Product.objects.get(id=product_id)
        totalDownloads=int(product.downloads)
        totalDownloads+=1
        if totalDownloads==0:
            totalDownloads=1
        updateRes=models.Product.objects.filter(id=product_id).update(downloads=totalDownloads)
        msg={
            'bool':False
        }
        if updateRes:
             msg={
            'bool':True
            }  
    return JsonResponse(msg)
    
# @csrf_exempt
# def update_product_download_count(request, product_id):
#     msg = {'bool': False}  # Initialize msg here
#     if request.method == 'POST':
#         try:
#             product = models.Product.objects.get(id=product_id)
#             totalDownloads = int(product.downloads) 
#             totalDownloads+=1
#             if totalDownloads==0:
#                 totalDownloads=1
#             models.Product.objects.filter(id=product_id).update(downloads=totalDownloads)
#             msg = {'bool': True}  # Update msg on success
#         except Exception as e:
#             # Handle potential errors here
#             msg = {'bool': False, 'error': str(e)}
#     return JsonResponse(msg)

# Customer views
class CustomerList(generics.ListCreateAPIView):
    queryset=models.Customer.objects.all()
    serializer_class=serializers.CustomerSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.CustomerSerializer(queryset,many=True)
        return Response(serializer.data)
class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Customer.objects.all()
    serializer_class=serializers.CustomerDetailSerializer
    def list(self, request,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.CustomerDetailSerializer(queryset,many=True)
        return Response(serializer.data)
#For Auth user 
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.User.objects.all()
    serializer_class=serializers.UserSerializer
    def list(self, request,*args, pk):
        queryset = self.get_queryset()
        serializer = serializers.UserSerializer(queryset,many=True)
        return Response(serializer.data)
# admin login
@csrf_exempt
def owner_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    # print(username)
    if user:
        owner=models.Owner.objects.get(user=user)
        msg={
            'bool':True,
            'user':user.username,
            'id':owner.id
         }
    else:
        msg={
            'bool':False,
            'msg':'Invalid username/password',
            }
    return JsonResponse(msg)    
# customer login
@csrf_exempt
def customer_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password) 
    if user: 
        customer=models.Customer.objects.get(user=user)
        msg={
            'bool':True,
            'user':user.username,
            'id':customer.id
         }
    else:
        msg={
            'bool':False,
            'msg':'Invalid username/password',
            }
    return JsonResponse(msg)
## for customer register use create_user method for create hashd form of password
@csrf_exempt
def customer_register(request):
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    username=request.POST.get('username')
    email=request.POST.get('email')
    mobile=request.POST.get('mobile')
    password=request.POST.get('password')
    try:
        user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
        if user:
            try:
                # Create customer from model
                customer=models.Customer.objects.create(
                    user=user,
                    mobile=mobile
                )
                msg={
                    'bool':True,
                    'user':user.id,
                    'customer':customer.id,
                    'msg':'Thank you for your registration! you can login now'
                }
            except IntegrityError:
                 msg={
                'bool':False,
                'msg':'Mobile Number Allready exist',
                }
        else:
            msg={
                'bool':False,
                'msg':'Oops...Something went to Wrong!!',
                }
    except IntegrityError:
        msg={
                'bool':False,
                'msg':'Username Allready exist',
                }

    return JsonResponse(msg)
# Customer change password
@csrf_exempt
def customer_change_password(request,customer_id):
    password=request.POST.get('password')
    customer=models.Customer.objects.get(id=customer_id)
    user=customer.user
    user.password=make_password(password)
    user.save()
    msg={'bool':True,'msg':'Password has been changed'}
    return JsonResponse(msg)
# Customer Forgot password
@csrf_exempt
def customer_forgot_password(request):
        email=request.POST.get('email')
        # Use the appropriate field path to access it, such as user.email if the email is stored in a related User model.
        verify=models.Customer.objects.filter(user__email=email).first()
        if verify:
            link=f'http://localhost:3000/customer/resetpassword/{verify.id}'
            subject = 'Your account needs to be verified'
            email_from = settings.EMAIL_HOST_USER
            html_message=f'please click this link. {link}'
            send_mail(subject , html_message , email_from , [email])
            return JsonResponse({'bool':True,'msg':'Email sent successfully'})
        else:
            return JsonResponse({'bool':False,'msg':'Invalid Email!!'})
# Customer Reset password
@csrf_exempt
def customer_reset_password(request, customer_id):
    customer = models.Customer.objects.filter(id=customer_id).first()
    if customer:
        user=customer.user      
        if user:
            password = request.POST.get('password')
            if password is not None and password.strip():
                user.set_password(password) #relationship Customer is related to User use set_password()
                user.save() 
                return JsonResponse({'bool': True,  'msg': 'Password has been updated successfully'})
            else:
                return JsonResponse({'bool': False, 'msg': 'Password is Empty'})
        else:
            return JsonResponse({'bool': False, 'msg': 'Customer has no associated user'})
    else:
        return JsonResponse({'bool': False, 'msg': 'customer not found'})
#  Order Views
class OrderList(generics.ListCreateAPIView):
    queryset=models.Order.objects.all()
    serializer_class=serializers.OrderSerializer
    # customer_name = models.Customer.objects.get(user=id)
    # pagination_class=pagination.LimitOffsetPagination
    def list(self,request):
        queryset=self.get_queryset()
        serializer=serializers.OrderSerializer(queryset,many=True)
        return Response(serializer.data)
    # for api
    def post(self, request, *args, **kwargs):
        print(request.POST)
        return super().post(request, *args, **kwargs)
    
# OrderItems
class OrderItemsList(generics.ListCreateAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemsSerializer
    # Json response
    def list(self, request):
            queryset = self.get_queryset()
            serializer = serializers.OrderItemsSerializer(queryset,many=True)
            return Response(serializer.data)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    # all order comes if one id 
    # queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderDetailSerializer
    # for one product for one order by id by built in function get_queryset
    def get_queryset(self):
        order_id=self.kwargs['pk']
        order=models.Order.objects.get(id=order_id)
        orderitem=models.OrderItems.objects.filter(order=order)
        return orderitem
  
# For vendor customer order delete function
@csrf_exempt
def delete_customer_orders(request,customer_id):
    msg = {'bool': False}
    if request.method=='DELETE':
        orders=models.Order.objects.filter(customer__id=customer_id).delete()
        msg={
            'bool':False
            }
        if orders:
             msg={
            'bool':True
            }
        
    return JsonResponse(msg)
   
# update_order_status
@csrf_exempt
def update_order_status(request,order_id):
    msg = {'bool': False}
    if request.method=='POST':
        if 'payment_mode' in request.POST:
            payment_mode=request.POST.get('payment_mode')
            trans_ref=request.POST.get('trans_ref')
            updateRes=models.Order.objects.filter(id=order_id).update(order_status=True,payment_mode=payment_mode,trans_ref=trans_ref)
        else:
            updateRes=models.Order.objects.filter(id=order_id).update(order_status=True)
        msg={
            'bool':False,
            }
        if updateRes:
             msg={
            'bool':True,
            }
    return JsonResponse(msg)

# Customer order item list
class CustomerOrderItemsList(generics.ListAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemsSerializer
# for json error
    def list(self, request,**kwargs):
        queryset = self.get_queryset()
        serializer = serializers.OrderItemsSerializer(queryset,many=True)
        return Response(serializer.data)
    # for 
    def get_queryset(self):
        qs = super().get_queryset()
        customer_id=self.kwargs['pk']
        qs=qs.filter(order__customer__id=customer_id)
        return qs
   
# Customer_address viewsets means not create different function as like above api
class CustomerAddressViewSet(viewsets.ModelViewSet):
    queryset=models.CustomerAddress.objects.all()
    serializer_class=serializers.CustomerAddressSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.CustomerAddressSerializer(queryset,many=True)
        return Response(serializer.data)
    
# for customer address list item
class CustomerAddressList(generics.ListAPIView):
    queryset=models.CustomerAddress.objects.all()
    serializer_class=serializers.CustomerAddressSerializer
    # for json error
    def list(self, request,**kwargs):
        queryset = self.get_queryset()
        serializer = serializers.CustomerAddressSerializer(queryset,many=True)
        return Response(serializer.data)
    # For address-list here order_by is use for default address
    def get_queryset(self):
        qs = super().get_queryset()
        customer_id=self.kwargs['pk']
        qs=qs.filter(customer__id=customer_id).order_by('id')
        return qs
 # Vendor order item list
class VendorOrderItemsList(generics.ListAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemsSerializer
# for json error
    def list(self, request,**kwargs):
        queryset = self.get_queryset()
        serializer = serializers.OrderItemsSerializer(queryset,many=True)
        return Response(serializer.data)
    # for 
    def get_queryset(self):
        qs = super().get_queryset()
        vendor_id=self.kwargs['pk']
        qs=qs.filter(product__vendor__id=vendor_id)
        return qs  
        
# Order Modify For vendor
class OrderModify(generics.RetrieveUpdateAPIView):
    queryset=models.Order.objects.all()
    serializer_class=serializers.OrderSerializer  

# Customerlist for vendor
class VendorCustomerList(generics.ListAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemsSerializer
# for json error
    def list(self, request,**kwargs):
        queryset = self.get_queryset()
        serializer = serializers.OrderItemsSerializer(queryset,many=True)
        return Response(serializer.data)
    # for 
    def get_queryset(self):
        qs = super().get_queryset()
        vendor_id=self.kwargs['pk']
        qs=qs.filter(product__vendor__id=vendor_id)
        return qs   
# CustomerOrderItemlist for vendor
class VendorCustomerOrderItemList(generics.ListAPIView):
    queryset=models.OrderItems.objects.all()
    serializer_class=serializers.OrderItemsSerializer
# for json error
    def list(self, request,**kwargs):
        queryset = self.get_queryset()
        serializer = serializers.OrderItemsSerializer(queryset,many=True)
        return Response(serializer.data)
    # for 
    def get_queryset(self):
        qs = super().get_queryset()
        vendor_id=self.kwargs['vendor_id']
        customer_id=self.kwargs['customer_id']
        qs=qs.filter(order__customer__id=customer_id,product__vendor__id=vendor_id)
        return qs
# mark default address
@csrf_exempt
def mark_default_address(request,pk):
    msg = {'bool': False}
    if request.method=='POST':
        address_id=request.POST.get('address_id')
        models.CustomerAddress.objects.all().update(default_address=False)
        res=models.CustomerAddress.objects.filter(id=address_id).update(default_address=True)
        msg={
            'bool':False
            }
        if res:
             msg={
            'bool':True
            }   
    return JsonResponse(msg)
# Product ratings
class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset=models.ProductRating.objects.all()
    serializer_class=serializers.ProductRatingSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.ProductRatingSerializer(queryset,many=True)
        return Response(serializer.data)
# Category view
class CategoryList(generics.ListCreateAPIView):
    queryset=models.ProductCategory.objects.all()
    serializer_class=serializers.CategorySerializer
    pagination_class=pagination.LimitOffsetPagination
# method for many data in json 
    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.CategorySerializer(queryset,many=True)
        return Response(serializer.data)
    # Popular categories
    def get_queryset(self):
        qs = super().get_queryset()
        if 'fetch_popular_category_limit' in self.request.GET:
            limit = int(self.request.GET['fetch_popular_category_limit'])
            qs=qs.annotate(downloads=Count('category_product')).order_by('-downloads','-id')
            qs = qs[:limit ]
        return qs 
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.ProductCategory.objects.all()
    serializer_class=serializers.CategoryDetailSerializer
    def list(self, request):
        queryset = self.get_queryset()
        serializer = serializers.CategoryDetailSerializer(queryset,many=True)
        return Response(serializer.data)   
# Wishlist View
class WishList(generics.ListCreateAPIView):
    queryset=models.Customer.objects.all()
    serializer_class=serializers.WishlistSerializer
# update_Wishlist_status
@csrf_exempt
def check_in_wishlist(request):
    msg = {'bool': False}
    if request.method=='POST':
        product_id=request.POST.get('product')
        customer_id=request.POST.get('customer')
        checkWishlist=models.Wishlist.objects.filter(product_id=product_id,customer_id=customer_id).count()
        msg={
            'bool':False
            }
        if checkWishlist>0:
             msg={
            'bool':True
            }
        
    return JsonResponse(msg)
# Customer wish item 
class CustomerWishItemsList(generics.ListAPIView):
    queryset=models.Wishlist.objects.all()
    serializer_class=serializers.WishlistSerializer
    # for json error
    def list(self, request,**kwargs):
        queryset = self.get_queryset()
        serializer = serializers.WishlistSerializer(queryset,many=True)
        return Response(serializer.data)
    # For Wishitems
    def get_queryset(self):
        qs = super().get_queryset()
        customer_id=self.kwargs['pk']
        qs=qs.filter(customer__id=customer_id)
        return qs
#Customer Remove Item from wishlist
@csrf_exempt
def remove_from_wishlist(request):
    msg = {'bool': False}
    if request.method=='POST':
        wishlist_id=request.POST.get('wishlist_id')
        res=models.Wishlist.objects.filter(id=wishlist_id).delete()
        msg={
            'bool':False
            }
        if res:
             msg={
            'bool':True
            }
        
    return JsonResponse(msg)
# customer_dashboard
def customer_dashboard(request,pk):
    customer_id=pk
    totalOrders=models.Order.objects.filter(customer__id=customer_id).count()
    totalWishList=models.Wishlist.objects.filter(customer__id=customer_id).count()
    totalAddress=models.CustomerAddress.objects.filter(customer__id=customer_id).count()
    msg={
        'totalOrders':totalOrders,
        'totalWishList':totalWishList,
        'totalAddress':totalAddress,
    }  
    return JsonResponse(msg)    
# vendor_dashboard
def vendor_dashboard(request,pk):
    vendor_id=pk
    totalOrders=models.OrderItems.objects.filter(product__vendor__id=vendor_id).count()
    totalProducts=models.Product.objects.filter(vendor__id=vendor_id).count()
    # fetch unique customer so added by value
    totalCustomers=models.OrderItems.objects.filter(product__vendor__id=vendor_id).values('order__customer').count()
    msg={
        'totalOrders':totalOrders,
        'totalProducts':totalProducts,
        'totalCustomers':totalCustomers,
    }  
    return JsonResponse(msg)
# admin_dashboard
# def owner_dashboard(request,pk):
#     owner_id=pk
#     totalOrders=models.OrderItems.objects.filter(product__owner__id=owner_id).count()
#     totalProducts=models.Product.objects.filter(owner__id=owner_id).count()
#     # fetch unique customer so added by value
#     totalCustomers=models.OrderItems.objects.filter(product__owner__id=owner_id).values('order__customer').count()
#     msg={
#         'totalOrders':totalOrders,
#         'totalProducts':totalProducts,
#         'totalCustomers':totalCustomers,
#     }  
#     return JsonResponse(msg)
# create_razorpay_order in backend
@csrf_exempt
def create_razorpay_order(request):
    client = razorpay.Client(auth=("rzp_test_rkn1lHi2O6nncL", "lnyqIA8kwVpYblrBCh9xBINm"))
    res=client.order.create({
        "amount": int(request.POST.get("amount")),
        "currency": "INR",
        "receipt": request.POST.get('order_id'),
        "partial_payment": False,
    })
    if res:
        msg={
            'bool':True,
            'data':res
        }
    else:
        msg={
            'bool':False
        }
    return JsonResponse(msg)
# Notifications views
class NotificationsList(generics.ListCreateAPIView):
    queryset=models.Notification.objects.all()
    serializer_class=serializers.NotificationsListSerializer
    def list(self, request,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.NotificationsListSerializer(queryset,many=True)
        return Response(serializer.data)
class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Notification.objects.all()
    serializer_class=serializers.NotificationsDetailSerializer
#If not use pk(primary key for id) in url then use lookup_field='id
    lookup_field='id'
    def list(self, request,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.NotificationsDetailSerializer(queryset,many=True)
        return Response(serializer.data)
# Contact views
class contactUsList(generics.ListCreateAPIView):
    queryset=models.Contact.objects.all()
    serializer_class=serializers.contactUsListSerializer
    def list(self, request,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.contactUsListSerializer(queryset,many=True)
        return Response(serializer.data)
class contactUsDetail(generics.RetrieveDestroyAPIView):
    queryset=models.Contact.objects.all()
    serializer_class=serializers.contactUsDetailSerializer
    def list(self, request,*args, **kwargs):
        queryset = self.get_queryset()
        serializer = serializers.contactUsDetailSerializer(queryset,many=True)
        return Response(serializer.data)