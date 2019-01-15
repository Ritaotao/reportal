from django.shortcuts import redirect, get_object_or_404
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from .models import ReportSet, Template, Submission, Field, RuleSet, Report
from account.models import Group
from .forms import ReportSetForm, TemplateForm, FieldForm, FieldImportForm, RuleSetForm, ReportForm
from django.contrib import messages

from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
from .serializers import ReportSetSerializer, TemplateSerializer, FieldSerializer, RuleSetSerializer, ReportSerializer

from io import StringIO
import csv
import random

# utility functions
def genUid():
    rand = str(random.randint(100,999)) + '-' + str(random.randint(1000,9999))
    if Submission.objects.filter(uid = rand).exists() or Template.objects.filter(uid = rand).exists():
        genUid()
    else:
        return rand

# Create your views here.
# create portal
## Step 1: create a new report set or use an existing one

def reportsetIndex(request, pk=None):
    """render form and form validation,
        reportset.js controls form action and adds parameters to url"""
    scope = 'reportset'
    instance = get_object_or_404(ReportSet, pk=pk) if pk else None
    form = ReportSetForm(request.user, request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        if not pk:
            obj.create_by = request.user
        obj.save()
    html = TemplateResponse(request, 'porter/create.html', {'form': form, 'scope': scope})
    return HttpResponse(html.render())

class ReportSetViewSet(viewsets.ModelViewSet):
    """drf to datatable, filter qs"""
    serializer_class = ReportSetSerializer

    def get_queryset(self):
        groups = Group.objects.filter(profiles__user=self.request.user)
        return ReportSet.objects.filter(group__in=groups)

def templateIndex(request, rspk, pk=None):
    """render form and form validation,
        template.js controls form action and adds parameters to url"""
    scope = 'template'
    instance = get_object_or_404(Template, pk=pk) if pk else None
    form = TemplateForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.report_set_id = rspk
        if not pk:
            obj.uid = genUid()
            obj.create_by = request.user        
        obj.save()
    html = TemplateResponse(request, 'porter/create.html', {'form': form, 'scope': scope})
    return HttpResponse(html.render())

class TemplateViewSet(viewsets.ModelViewSet):
    """drf to datatable, filter qs"""
    serializer_class = TemplateSerializer

    def get_queryset(self):
        groups = Group.objects.filter(profiles__user=self.request.user)
        queryset = Template.objects.filter(report_set__group__in=groups)
        report_set = self.request.query_params.get('report_set', None)
        if report_set is not None:
            queryset = queryset.filter(report_set__id=report_set)
        return queryset

def fieldIndex(request, rspk, tpk, pk=None):
    """render form and form validation,
        field.js controls form action and adds parameters to url"""
    scope = 'field'
    form = FieldForm()
    importform = FieldImportForm()
    if request.method == 'POST':
        if 'btn_new' in request.POST:
            instance = get_object_or_404(Field, pk=pk) if pk else None
            form = FieldForm(request.POST, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.template_id = tpk
                obj.save()
        elif 'btn_import' in request.POST:
            importform = FieldImportForm(request.POST, request.FILES)
            if importform.is_valid():
                csvf = StringIO(request.FILES['docfile'].read().decode())
                reader = csv.reader(csvf, delimiter=",")
                next(reader) # always skip row 1 as header
                for row in reader:
                    try:
                        new_field, created = Field.objects.get_or_create(name=row[0], dtype=row[1].upper(), template_id=tpk)
                        if created:
                            new_field.save()
                    except Exception as e:
                        messages.error(request, 'Can not parse row: {}. {}'.format(row, e))
            else:
                messages.error(request, 'Please submit a valid csv file')
    context =  {
        'form': form, 'importform': importform, 'scope': scope, 'rspk': rspk, 'tpk': tpk
    }
    html = TemplateResponse(request, 'porter/create.html', context)
    return HttpResponse(html.render())

class FieldViewSet(viewsets.ModelViewSet):
    """drf to datatable, filter qs"""
    serializer_class = FieldSerializer

    def get_queryset(self):
        groups = Group.objects.filter(profiles__user=self.request.user)
        queryset = Field.objects.filter(template__report_set__group__in=groups)
        template = self.request.query_params.get('template', None)
        if template is not None:
            queryset = queryset.filter(template__id=template)
        return queryset

def rulesetIndex(request, rspk, tpk, pk=None):
    """render form and form validation,
        ruleset.js controls form action and adds parameters to url"""
    scope = 'ruleset'
    instance = get_object_or_404(RuleSet, pk=pk) if pk else None
    form = RuleSetForm(tpk, request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    html = TemplateResponse(request, 'porter/create.html', {'form': form, 'scope': scope, 'rspk': rspk, 'tpk': tpk})
    return HttpResponse(html.render())

class RuleSetViewSet(viewsets.ModelViewSet):
    """drf to datatable, filter qs"""
    serializer_class = RuleSetSerializer

    def get_queryset(self):
        groups = Group.objects.filter(profiles__user=self.request.user)
        queryset = RuleSet.objects.filter(field__template__report_set__group__in=groups)
        template = self.request.query_params.get('template', None)
        if template is not None:
            queryset = queryset.filter(field__template__id=template)
        return queryset

def reportIndex(request, rspk, pk=None):
    """render form and form validation,
        report.js controls form action and adds parameters to url"""
    scope = 'report'
    instance = get_object_or_404(Report, pk=pk) if pk else None
    form = ReportForm(rspk, request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.report_set_id = rspk
        if not pk:
            obj.create_by = request.user
        obj.save()
        form.save_m2m()
    html = TemplateResponse(request, 'porter/create.html', {'form': form, 'scope': scope})
    return HttpResponse(html.render())

class ReportViewSet(viewsets.ModelViewSet):
    """drf to datatable, filter qs"""
    serializer_class = ReportSerializer

    def get_queryset(self):
        groups = Group.objects.filter(profiles__user=self.request.user)
        queryset = Report.objects.filter(report_set__group__in=groups)
        report_set = self.request.query_params.get('report_set', None)
        if report_set is not None:
            queryset = queryset.filter(report_set__id=report_set)
        return queryset