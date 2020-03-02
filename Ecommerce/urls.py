from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
# Remind me to include LoginView & LogoutView
from account.views import (register, profile, activate_account)
from Ecommerce.api_routers import router
from django.contrib.auth import views as auth_view
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # core
    path('', include('core.urls', namespace='core')),
    # Account
    path('data/', include('account.urls')),
    # register
    path('register/', register, name='register'),
    # accounts
    path('profile/', profile, name='profile'),
    # login & Logout
    path('login/', auth_view.LoginView.as_view(
        template_name='auth/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(
        template_name='auth/logout.html'), name='logout'),
    # api
    path('api/v1/', include(router.urls)),
    # path('api/v1/auth/login', LoginView.as_view()),
    # path('api/v1/auth/logout', LogoutView.as_view()),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
