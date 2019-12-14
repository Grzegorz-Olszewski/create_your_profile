from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import core.views

urlpatterns = [
    path('', core.views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('password/', core.views.password, name='password'),
]
