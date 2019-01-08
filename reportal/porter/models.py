from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from model_utils import Choices

# Create your models here.
class ReportSet(models.Model):
    name = models.CharField(max_length=200, unique=True)
    group = models.ForeignKey('account.Group', default=1, on_delete=models.SET_DEFAULT, related_name='report_sets')
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    create_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='report_sets')
    
    def __str__(self):
        return self.name

def query_rs_by_args(**kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]
    ORDER_COLUMN_CHOICES = Choices(
        ('0', 'id'),
        ('1', 'name'),
        ('2', 'group'),
        ('3', 'create_date'),
        ('4', 'created_by'),
        ('5', 'last_modify_date'),
    )
    order_column = ORDER_COLUMN_CHOICES[order_column]
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column

    queryset = ReportSet.objects.all()
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(id__icontains=search_value) | 
                                        Q(name__icontains=search_value) | 
                                        Q(group__icontains=search_value) | 
                                        Q(create_by__icontains=search_value) | 
                                        Q(create_date__icontains=search_value) | 
                                        Q(last_modify_date__icontains=search_value))

    count = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }










class Report(models.Model):
    name = models.CharField(max_length=200, unique=True)
    directory = models.TextField()
    UPLOAD_METHODS = (
        ('APPEND', 'Append'),
        ('REPLACE', 'Replace'),
    )
    method = models.CharField(max_length=20, choices=UPLOAD_METHODS)
    report_set = models.ForeignKey(ReportSet, on_delete=models.CASCADE, related_name='reports')
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    create_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='reports')
    def __str__(self):
        return self.name

class Template(models.Model):
    name = models.CharField(max_length=200, unique=True)
    uid = models.CharField(max_length=8) # used to retrieve template
    report_set = models.ForeignKey(ReportSet, on_delete=models.CASCADE, related_name='templates')
    last_modify_date = models.DateTimeField(auto_now=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    create_by = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT, related_name='templates')
    def __str__(self):
        return self.name

class Submission(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='submissions')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name='submissions')
    uid = models.CharField(max_length=8) # used to download submissions
    submitted_file = models.FileField(upload_to='not_used',null=True, blank=True)
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