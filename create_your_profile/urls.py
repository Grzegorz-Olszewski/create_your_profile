from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import core.views

urlpatterns = [
    path('', core.views.home, name='home'),
    path('details/', core.views.ProfileDetailsView.as_view(), name='details'),
    path('update_profile/', core.views.ProfileUpdateView.as_view(), name='update_profile'),
    path('delete/', core.views.ProfileDeleteView.as_view(), name='delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('password/', core.views.password, name='password'),
]
