from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from smsapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('smsapp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),    
    path('accounts/signup/', views.signup, name='signup'),
]