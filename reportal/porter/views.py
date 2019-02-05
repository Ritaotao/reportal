from django.shortcuts import redirect, get_object_or_404
from django.http.response import HttpResponse, StreamingHttpResponse
from django.template.response import TemplateResponse
from .models import ReportSet, Template, Submission, Field, RuleSet, Report
from account.models import Group, Profile
from .forms import ReportSetForm, TemplateForm, FieldForm, FieldImportForm, RuleSetForm, ReportForm, SubmissionForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
from .serializers import (ReportSetSerializer, TemplateSerializer, FieldSerializer, RuleSetSerializer, 
    ReportSerializer, SubmissionSerializer)

import os
from io import StringIO
import pandas as pd
import csv
import random
from .quality import check_quality

# Create your views here.
# create portal
@login_required(login_url='/account/signin/')
def reportsetIndex(request, pk=None):
    '''Reportset organizes both Templates and Reports, under a Group/Account'''
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

@login_required(login_url='/account/signin/')
def templateIndex(request, rspk, pk=None):
    '''Template organizes Fields and Rulesets, under a Reportset'''
    scope = 'template'
    instance = get_object_or_404(Template, pk=pk) if pk else None
    form = TemplateForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.report_set_id = rspk
        if not pk:
            obj.create_by = request.user        
        obj.save()
    html = TemplateResponse(request, 'porter/create.html', {'form': form, 'scope': scope})
    return HttpResponse(html.render())

@login_required(login_url='/account/signin/')
def templateDuplicate(request, rspk, pk):
    '''Duplicate template and nested fields and rulesets'''
    # save template
    template = get_object_or_404(Template, pk=pk)
    template.pk = None
    template.name = template.name + '_v2' # to avoid duplicate of reportset - template pair
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

@login_required(login_url='/account/signin/')
def fieldIndex(request, rspk, tpk, pk=None):
    '''Field defines column name and column datatypes, under a Template'''
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

@login_required(login_url='/account/signin/')
def rulesetIndex(request, rspk, tpk, pk=None):
    '''Ruleset combines Field and Rule, define the list of qa process, under a Template'''   
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

@login_required(login_url='/account/signin/')
def reportIndex(request, rspk, pk=None):
    '''Report defines the set of templates to be QA'ed against'''
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

# submit portal
@login_required(login_url='/account/signin/')
def listIndex(request):
    '''List reports available to user for submit/download'''
    scope = 'list'
    html = TemplateResponse(request, 'porter/submit.html', {'scope': scope})
    return HttpResponse(html.render())

@login_required(login_url='/account/signin/')
def submissionIndex(request, rpk):
    '''Make a new Submission for Report/Template selected'''
    scope = 'submission'
    form = SubmissionForm(rpk, request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            cxt = check_quality(request, request.FILES['upload'], form.cleaned_data['template'])
            if cxt:
                obj = form.save(commit=False)
                obj.report_id = rpk
                obj.name = request.FILES['upload'].name
                obj.submitted_by = request.user
                if cxt['clean'] == 'false':
                    obj.is_clean = False
                    obj.upload.delete(save=False)
                else:
                    obj.is_clean = True
                request.session['analysis'] = cxt
                obj.save()
                return redirect('porter:result', rpk=rpk)
        else:
            messages.error(request, 'Please submit a valid xlsx or csv file')
    html = TemplateResponse(request, 'porter/submit.html', {'form': form, 'scope': scope})
    return HttpResponse(html.render())

class SubmissionViewSet(viewsets.ModelViewSet):
    '''
        drf to datatable, filter qs
    '''
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        queryset = Submission.objects.all()
        report = self.request.query_params.get('report', None)
        clean = self.request.query_params.get('is_clean', None)
        if report is not None:
            queryset = queryset.filter(report__id=report)
        if clean is not None:
            queryset = queryset.filter(is_clean=True)
        groups = Profile.objects.get(user=self.request.user).groups.all()
        return queryset.filter(report__report_set__group__in=groups)

@login_required(login_url='/account/signin/')
def resultIndex(request, rpk):
    '''Result page showing analysis of data quality'''
    scope = 'result'
    df_meta, df_report = None, None
    if 'analysis' in request.session:
        cxt = request.session['analysis']
        clean, df_meta, df_report = cxt['clean'], cxt['df_meta'], cxt['df_report']
        if clean == 'true':
            messages.success(request, 'SUCCESS: Uploaded data passes all quality checks. Thank you!')
        elif clean == 'false':
            messages.error(request, 'ERROR: Quality check for submission failed, please correct accordingly and resubmit')
        del request.session['analysis']
    else:
        messages.error(request, 'SYSTEM ERROR: No valid submission found')
        return redirect('porter:submission', rpk=rpk)
    html = TemplateResponse(request, 'porter/result.html', {'scope': scope, 'df_meta': df_meta, 'df_report': df_report})
    return HttpResponse(html.render())

@login_required(login_url='/account/signin/')
def downloadIndex(request, rpk, pk=None):
    '''Download submitted files that pass data quality check'''
    scope = 'download'

    if pk:
        download_file = get_object_or_404(Submission, pk=pk)
        filename = os.path.basename(download_file.upload.name)
        if '.xlsx' in filename:
            cnt_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif '.csv' in filename:
            cnt_type = 'text/csv'
        response = HttpResponse(download_file.upload, content_type=cnt_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    html = TemplateResponse(request, 'porter/submit.html', {'scope': scope})
    return HttpResponse(html.render())