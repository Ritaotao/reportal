from django.urls import path
from . import views

app_name = "porter"
urlpatterns = [
    path('', views.index, name='home'),
    path('reportset/', views.ReportSetView.as_view(), name='reportset'),
    path('reportset/<int:pk>/template/', views.TemplateView.as_view(), name='template'),
]