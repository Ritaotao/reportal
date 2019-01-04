from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logout_view, name='logout'),
]