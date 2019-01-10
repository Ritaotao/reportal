from django.contrib import admin
from .models import ReportSet, Report, Template, Submission, Field, Rule, Quality

# Register your models here.
@admin.register(ReportSet)
class ReportSetAdmin(admin.ModelAdmin):
    list_display=('id','name','group','last_modify_date','create_date','create_by')

admin.site.register(Report)
admin.site.register(Template)
admin.site.register(Field)

