from django.contrib import admin
from .models import ReportSet, Report, Template, Submission, Field, Rule, RuleSet

# Register your models here.
@admin.register(ReportSet)
class ReportSetAdmin(admin.ModelAdmin):
    list_display=('id','name','group','last_modify_date','create_date','create_by')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display=('id','name','method','report_set','last_modify_date','create_date','create_by')

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display=('id','name','report_set','last_modify_date','create_date','create_by')

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display=('id','template','name','dtype')

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display=('id','name','description','has_argument')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display=('id','report','template','name','upload','submitted_date','submitted_by', 'is_clean')

@admin.register(RuleSet)
class RuleSetAdmin(admin.ModelAdmin):
    list_display=('id','field','rule','action','argument','error_message')