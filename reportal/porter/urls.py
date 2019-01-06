from django.urls import path
from . import views

app_name = "porter"
urlpatterns = [
    path('', views.index, name='home'),
    path('reportset/', views.ReportSetView.as_view(), name='reportset'),
    path('reportset=<int:pk>', views.TemplateView.as_view(), name='template'),
    path('reportset=<int:pk>&template=<int:tpk>', views.FieldView.as_view(), name='field'),
]