"""
URL configuration for backend_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    3.httppi install
   "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMjc0Njc1NiwiaWF0IjoxNzAyNjYwMzU2LCJqdGkiOiI4MGI5NDExNDkxYjI0MjViYTVhYTk4MzA5MWIzOThhMyIsInVzZXJfaWQiOjF9.nWHc0iRm6lopd8zerde-sN_6YCrIq-6fxivBTP1MLrI",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyNjYwNjU2LCJpYXQiOjE3MDI2NjAzNTYsImp0aSI6ImVjNmUyOTE1YzQ4YTRlNjU5NGFmNjFiMmY1ZTBlZGFmIiwidXNlcl9pZCI6MX0.71hDkjZU5jcczKPRTtp4Du2JmmBiVIQ_LPM1hf5ro2c"
}
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('main.urls')),
    # default jwt url simple
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/',include('rest_framework.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
