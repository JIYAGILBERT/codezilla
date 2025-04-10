from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('',views.home, name='home'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]