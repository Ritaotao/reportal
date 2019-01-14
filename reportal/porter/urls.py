from django.urls import path, re_path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reportset', views.ReportSetViewSet, base_name='reportset')
router.register(r'template', views.TemplateViewSet, base_name='template')
router.register(r'field', views.FieldViewSet, base_name='field')

app_name = "porter"
urlpatterns = [
    re_path(r'^api/', include(router.urls)),
    #re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 2 urls each, one for get list view, one for form post action
    path('reportset/', views.reportsetIndex, name='reportset'),
    path('reportset/<int:pk>/', views.reportsetIndex, name='reportset'),
    path('template/<int:rspk>/', views.templateIndex, name='template'),
    path('template/<int:rspk>/<int:pk>/', views.templateIndex, name='template'),
    path('field/<int:rspk>/<int:tpk>/', views.fieldIndex, name='field'),
    path('field/<int:rspk>/<int:tpk>/<int:pk>/', views.fieldIndex, name='field'),
]