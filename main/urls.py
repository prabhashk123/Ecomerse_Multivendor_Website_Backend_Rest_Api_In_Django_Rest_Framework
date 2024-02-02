from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# for customeraddress router
from rest_framework import routers
router=routers.DefaultRouter()
router.register('address',views.CustomerAddressViewSet)
router.register('productrating',views.ProductRatingViewSet)

urlpatterns = [
    # Admin Panel
    path('owner/login/',views.owner_login,name='owner_login'),
    path('vendor/allnotificatons/',views.NotificationsList.as_view()),
    path('vendor/allnotificaton/<int:id>/',views.NotificationDetail.as_view()),
    path('contactus/',views.contactUsList.as_view(),name='contactus'),
    path('contact/<int:pk>/',views.contactUsDetail.as_view(),name='contactusdetail'),
    # Vendors/Seller
    path('vendors/',views.VendorList.as_view()),
    path('vendor/<int:pk>/dashboard/',views.vendor_dashboard),
    path('vendor-products/<int:vendor_id>/',views.VendorProductList.as_view()),
    path('vendor-change-password/<int:vendor_id>/',views.vendor_change_password),
    path('vendor/<int:pk>/',views.VendorDetail.as_view()),
    path('vendor/register/',views.vendor_register,name='vendor_register'),
    path('vendor/login/',views.vendor_login,name='vendor_login'),
    path('vendor-forgot-password/',views.vendor_forgot_password),
    path('vendor-reset-password/<int:vendor_id>/',views.vendor_reset_password),
    path('vendor/<int:pk>/customers/',views.VendorCustomerList.as_view()),
    path('vendor/<int:vendor_id>/customer/<int:customer_id>/orderitems/',views.VendorCustomerOrderItemList.as_view()),
    # Product and tag
    path('products/',views.ProductList.as_view()),
    path('search-products/<str:searchproductstring>/',views.ProductList.as_view()),
    path('product-imgs/',views.ProductImgsList.as_view()),
    path('product-imgs/<int:product_id>/',views.ProductImgsDetail.as_view()),
    path('product-img/<int:pk>/',views.ProductImgDetail.as_view()),
    path('products/<str:tag>',views.TagProductList.as_view()),
    path('related-products/<int:pk>/',views.RelatedProductList.as_view()),
    path('product/<int:pk>/',views.ProductDetail.as_view()),
    path('product-modify/<int:pk>/',views.ProductModify.as_view()),
    # Product Categories
    path('categories/',views.CategoryList.as_view()),
    path('category/<int:pk>/',views.CategoryDetail.as_view()),
    # Customer & customer dashboard
    path('customer/dashboard/<int:pk>/',views.customer_dashboard,name='customer_dashboard'),
    path('customers/',views.CustomerList.as_view()),
    path('customer/<int:pk>/',views.CustomerDetail.as_view()),
    path('user/<int:pk>/',views.UserDetail.as_view()),
    path('customer/login/',views.customer_login,name='customer_login'),
    path('customer/register/',views.customer_register,name='customer_register'),
    path('customer-change-password/<int:customer_id>/',views.customer_change_password),
    path('customer-forgot-password/',views.customer_forgot_password),
    path('customer-reset-password/<int:customer_id>/',views.customer_reset_password),
    path('customer/<int:pk>/address-list/',views.CustomerAddressList.as_view()),
    path('mark-default-address/<int:pk>/',views.mark_default_address,name='mark-default-address'),
    # Order for both vendor/customer
    path('orders/',views.OrderList.as_view()),
    path('orderitems/',views.OrderItemsList.as_view()),
    path('customer/<int:pk>/orderitems/',views.CustomerOrderItemsList.as_view()),
    path('order/<int:pk>/',views.OrderDetail.as_view()),
    path('create-razorpay-order/',views.create_razorpay_order),
    path('update-order-status/<int:order_id>/',views.update_order_status,name='update_order_status'),
    path('update_product_download_count/<int:product_id>/',views.update_product_download_count,name='update_product_download_count'),
    path('vendor/<int:pk>/orderitems/',views.VendorOrderItemsList.as_view()),
    path('order-modify/<int:pk>/',views.OrderModify.as_view()),
    path('delete-customer-orders/<int:customer_id>/',views.delete_customer_orders),
    # Wishlist
    path('wishlist/',views.WishList.as_view()),
    path('check-in-wishlist/',views.check_in_wishlist,name='check_in_wishlist'),
    path('customer/<int:pk>/wishitems/',views.CustomerWishItemsList.as_view()),
    path('remove-from-wishlist/',views.remove_from_wishlist,name='remove_from_wishlist'),
    
]
urlpatterns+=router.urls
