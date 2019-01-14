from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.urls import reverse
from django.views import View
from .models import ReportSet, Template, Submission, Field, Report
from account.models import Group, User, Profile
from .forms import ReportSetForm, TemplateForm, FieldForm, ReportForm
from django.template.response import TemplateResponse

from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ReportSetSerializer, TemplateSerializer, FieldSerializer, ReportSerializer

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
        template.js controls form action and adds parameters to url"""
    scope = 'field'
    instance = get_object_or_404(Field, pk=pk) if pk else None
    form = FieldForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.template_id = tpk
        obj.save()
    html = TemplateResponse(request, 'porter/create.html', {'form': form, 'scope': scope, 'rspk': rspk})
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