from django.urls import path, re_path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reportset', views.ReportSetViewSet, base_name='reportset')
router.register(r'template', views.TemplateViewSet, base_name='template')

app_name = "porter"
urlpatterns = [
    re_path(r'^api/', include(router.urls)),
    #re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('reportset/', views.reportsetIndex, name='reportset'),
    path('template/<int:pk>/', views.templateIndex, name='template'),
    path('reportset=<int:pk>/template=<int:tpk>', views.FieldView.as_view(), name='field'),
]