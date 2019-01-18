from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .choices import UPLOAD_METHODS, DATA_TYPES, ACTIONS

private_storage = FileSystemStorage(location=settings.PRIVATE_STORAGE_ROOT)

# Create your models here.
class ReportSet(models.Model):
    name = models.CharField(max_length=200)
    group = models.ForeignKey('account.Group', default=1, on_delete=models.SET_DEFAULT, related_name='report_sets')
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    create_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='report_sets')

    class Meta:
        unique_together = ('group', 'name',)
    
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
    name = models.CharField(max_length=200)
    dtype = models.CharField(max_length=20, choices=DATA_TYPES)
    def __str__(self):
        return self.name
    class Meta:
        unique_together = ('template', 'name',)

# validate field dtype choices for bulk import
def validate_field_choice(sender, instance, **kwargs):
    valid_fields = [t[0] for t in DATA_TYPES]
    if instance.dtype not in valid_fields:
        raise ValidationError('Field Data Type {} is not one of the permitted values: {}'.format(instance.dtype, ', '.join(valid_fields)))
models.signals.pre_save.connect(validate_field_choice, sender=Field)

class Rule(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    has_argument = models.BooleanField(default=False)
    def __str__(self):
        return self.name

# Quality is a set of rules
class RuleSet(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='rule_sets')
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='rule_sets')
    action = models.CharField(max_length=20, choices=ACTIONS)
    argument = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)