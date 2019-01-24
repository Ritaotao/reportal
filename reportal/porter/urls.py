from django.urls import path, re_path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reportset', views.ReportSetViewSet, base_name='reportset')
router.register(r'template', views.TemplateViewSet, base_name='template')
router.register(r'field', views.FieldViewSet, base_name='field')
router.register(r'report', views.ReportViewSet, base_name='report')
router.register(r'ruleset', views.RuleSetViewSet, base_name='ruleset')
router.register(r'submission', views.SubmissionViewSet, base_name='submission')

app_name = "porter"
urlpatterns = [
    re_path(r'^api/', include(router.urls)),
    #re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # create url: 2 urls each, one for get list view, one for form post action
    path('reportset/', views.reportsetIndex, name='reportset'),
    path('reportset/<int:pk>/', views.reportsetIndex, name='reportset_edit'),
    path('template/<int:rspk>/', views.templateIndex, name='template'),
    path('template/<int:rspk>/<int:pk>/', views.templateIndex, name='template_edit'),
    path('template/<int:rspk>/<int:pk>/duplicate/', views.templateDuplicate, name='template_duplicate'),
    path('field/<int:rspk>/<int:tpk>/', views.fieldIndex, name='field'),
    path('field/<int:rspk>/<int:tpk>/<int:pk>/', views.fieldIndex, name='field_edit'),
    path('ruleset/<int:rspk>/<int:tpk>/', views.rulesetIndex, name='ruleset'),
    path('ruleset/<int:rspk>/<int:tpk>/<int:pk>/', views.rulesetIndex, name='ruleset_edit'),
    path('report/<int:rspk>/', views.reportIndex, name='report'),
    path('report/<int:rspk>/<int:pk>/', views.reportIndex, name='report_edit'),
    # submit url
    path('list/', views.listIndex, name='list'),
    path('submission/<int:rpk>/', views.submissionIndex, name='submission'),
]