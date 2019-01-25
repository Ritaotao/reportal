from django.contrib import admin
from .models import ReportSet, Report, Template, Submission, Field, Rule, RuleSet

# Register your models here.
@admin.register(ReportSet)
class ReportSetAdmin(admin.ModelAdmin):
    list_display=('id','name','group','last_modify_date','create_date','create_by')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display=('id','name','method','report_set','last_modify_date','create_date','create_by')

admin.site.register(Template)
admin.site.register(Field)

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display=('id','name','description','has_argument')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display=('id','report','template','uid','upload','submitted_date','submitted_by', 'is_clean')
