from django.shortcuts import redirect, get_object_or_404
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from .models import ReportSet, Template, Submission, Field, RuleSet, Report
from account.models import Group, Profile
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

def reportsetIndex(request, pk=None):
    '''
        render form and form validation,
        reportset.js controls form action and adds parameters to url
    '''
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
    '''
        drf to datatable, filter qs
    '''
    serializer_class = ReportSetSerializer

    def get_queryset(self):
        groups = Profile.objects.get(user=self.request.user).groups.all()
        return ReportSet.objects.filter(group__in=groups)

def templateIndex(request, rspk, pk=None):
    '''
        render form and form validation,
        template.js controls form action and adds parameters to url
    '''
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

def templateDuplicate(request, rspk, pk):
    '''
        Duplicate template and nested fields and rulesets
    '''
    # save template
    template = get_object_or_404(Template, pk=pk)
    template.pk = None
    template.name = template.name + '_v2' # to avoid duplicate of reportset - template pair
    template.uid = genUid()
    template.save()
    # save fields and rulesets
    fields = Field.objects.filter(template__id=pk).all()
    for field in fields:
        rulesets = RuleSet.objects.filter(field__id=field.pk).all()
        field.pk = None
        field.template_id = template.pk
        field.save()
        for ruleset in rulesets:
            ruleset.pk = None
            ruleset.field_id = field.pk
            ruleset.save()
    return redirect("porter:template", rspk=rspk)


class TemplateViewSet(viewsets.ModelViewSet):
    '''
        drf to datatable, filter qs
    '''
    serializer_class = TemplateSerializer

    def get_queryset(self):
        queryset = Template.objects.all()
        report_set = self.request.query_params.get('report_set', None)
        if report_set is not None:
            queryset = queryset.filter(report_set__id=report_set)
        groups = Profile.objects.get(user=self.request.user).groups.all()
        return queryset.filter(report_set__group__in=groups)

def fieldIndex(request, rspk, tpk, pk=None):
    '''
        render form and form validation,
        field.js controls form action and adds parameters to url
    '''
    scope = 'field'
    form = FieldForm()
    importform = FieldImportForm()
    if request.method == 'POST':
        # import post method
        if 'btn_import' in request.POST:
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
        # create and edit post method
        else:
            instance = get_object_or_404(Field, pk=pk) if pk else None
            form = FieldForm(request.POST, instance=instance)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.template_id = tpk
                obj.save()
    context =  {
        'form': form, 'importform': importform, 'scope': scope, 'rspk': rspk, 'tpk': tpk
    }
    html = TemplateResponse(request, 'porter/create.html', context)
    return HttpResponse(html.render())

class FieldViewSet(viewsets.ModelViewSet):
    '''
        drf to datatable, filter qs
    '''
    serializer_class = FieldSerializer

    def get_queryset(self):
        queryset = Field.objects.all()
        template = self.request.query_params.get('template', None)
        if template is not None:
            queryset = queryset.filter(template__id=template)
        groups = Profile.objects.get(user=self.request.user).groups.all()
        return queryset.filter(template__report_set__group__in=groups)

def rulesetIndex(request, rspk, tpk, pk=None):
    '''
        render form and form validation,
        ruleset.js controls form action and adds parameters to url
    '''   
    scope = 'ruleset'
    instance = get_object_or_404(RuleSet, pk=pk) if pk else None
    form = RuleSetForm(tpk, request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    html = TemplateResponse(request, 'porter/create.html', {'form': form, 'scope': scope, 'rspk': rspk, 'tpk': tpk})
    return HttpResponse(html.render())

class RuleSetViewSet(viewsets.ModelViewSet):
    '''
        drf to datatable, filter qs
    '''
    serializer_class = RuleSetSerializer

    def get_queryset(self):
        queryset = RuleSet.objects.all()
        template = self.request.query_params.get('template', None)
        if template is not None:
            queryset = queryset.filter(field__template__id=template)
        groups = Profile.objects.get(user=self.request.user).groups.all()
        return queryset.filter(field__template__report_set__group__in=groups)

def reportIndex(request, rspk, pk=None):
    '''
        render form and form validation,
        report.js controls form action and adds parameters to url
    '''
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
    '''
        drf to datatable, filter qs
    '''
    serializer_class = ReportSerializer

    def get_queryset(self):
        queryset = Report.objects.all()
        report_set = self.request.query_params.get('report_set', None)
        if report_set is not None:
            queryset = queryset.filter(report_set__id=report_set)
        groups = Profile.objects.get(user=self.request.user).groups.all()
        return queryset.filter(report_set__group__in=groups)