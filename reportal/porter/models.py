from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

private_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT)

# Create your models here.
class ReportSet(models.Model):
    name = models.CharField(max_length=200, unique=True)
    group = models.ForeignKey('account.Group', default=1, on_delete=models.SET_DEFAULT, related_name='report_sets')
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    create_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='report_sets')
    
    def __str__(self):
        return self.name

class Template(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=8, unique=True) # used to retrieve template
    report_set = models.ForeignKey(ReportSet, on_delete=models.CASCADE, related_name='templates')
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    create_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='templates')

    class Meta:
        unique_together = ('report_set', 'name',)

    def __str__(self):
        return self.name

class Report(models.Model):
    name = models.CharField(max_length=200)
    UPLOAD_METHODS = (
        ('REPLACE', 'Replace'),
        ('APPEND', 'Append'),
    )
    method = models.CharField(max_length=20, choices=UPLOAD_METHODS, default='REPLACE')
    templates = models.ManyToManyField(Template, related_name='reports')
    report_set = models.ForeignKey(ReportSet, on_delete=models.CASCADE, related_name='reports')
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    create_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='reports')

    class Meta:
        unique_together = ('report_set', 'name',)

    def __str__(self):
        return self.name

class Submission(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='submissions')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='submissions')
    uid = models.CharField(max_length=8, unique=True) # used to download submissions
    upload = models.FileField(storage=private_storage, null=True)
    submitted_date = models.DateTimeField(auto_now=True, null=True)
    submitted_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='submissions')
    is_clean = models.BooleanField(default=False)

class Field(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='fields')
    name = models.CharField(max_length=200, unique=True)
    DATA_TYPES = (
        ('INTEGER', 'Integer'),
        ('FLOAT', 'Float'),
        ('STRING', 'String'),
        ('DATE', 'Date'),
        ('DATETIME', 'Datetime')
    )
    dtype = models.CharField(max_length=20, choices=DATA_TYPES)

    class Meta:
        unique_together = ('template', 'name',)

    def __str__(self):
        return self.name

class Rule(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True) # default error message
    has_argument = models.BooleanField(default=False)
    def __str__(self):
        return self.name

# Quality is a set of (template, fields, rules) combined
class Quality(models.Model):
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='qualities')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='qualities')
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='qualities')
    ACTIONS = (
        ('SILENCE', 'Silence'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
    )
    action = models.CharField(max_length=20, choices=ACTIONS)
    argument = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)