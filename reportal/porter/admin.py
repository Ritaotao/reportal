from django.contrib import admin
from .models import ReportSet, Report, Template, Submission, Field, Rule, Quality

# Register your models here.
admin.site.register(ReportSet)
admin.site.register(Report)
admin.site.register(Template)
admin.site.register(Field)

