from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.urls import reverse
from django.views import View
from .models import ReportSet, Template, Submission, Field
from account.models import Group, User, Profile
from django.db.models import Q, Prefetch
from model_utils import Choices
from .forms import ReportSetForm, TemplateForm, FieldForm
from django.template.response import TemplateResponse

from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import ReportSetSerializer, TemplateSerializer

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

def reportsetIndex(request):
    """template and form: create, update"""
    form = ReportSetForm(request.user, request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.create_by = request.user
        obj.save()
    html = TemplateResponse(request, 'porter/reportset.html', {'form': form})
    return HttpResponse(html.render())

class ReportSetViewSet(viewsets.ModelViewSet):
    """datatable: list, delete"""
    serializer_class = ReportSetSerializer

    def get_queryset(self):
        groups = Group.objects.filter(profiles__user=self.request.user)
        return ReportSet.objects.filter(group__in=groups)

def templateIndex(request, pk):
    """template and form: create, update"""
    form = TemplateForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.uid = genUid()
        obj.report_set_id = pk
        obj.save()
    html = TemplateResponse(request, 'porter/template.html', {'form': form})
    return HttpResponse(html.render())

class TemplateViewSet(viewsets.ModelViewSet):
    """datatable: list, delete"""
    serializer_class = TemplateSerializer

    def get_queryset(self):
        groups = Group.objects.filter(profiles__user=self.request.user)
        queryset = Template.objects.filter(report_set__group__in=groups)
        report_set = self.request.query_params.get('report_set', None)
        if report_set is not None:
            queryset = queryset.filter(report_set__id=report_set)
        return queryset

class FieldView(View):
    form_class = FieldForm
    template_name = "porter/field.html"
    
    def get(self, request, *args, **kwargs):
        pk, tpk = self.kwargs['pk'], self.kwargs['tpk']
        form = self.form_class()
        query_list = Field.objects.filter(template__id=tpk).all()
        return render(request, self.template_name, {'query_list': query_list, 'form': form, 'pk': pk, 'tpk': tpk})

    def post(self, request, *args, **kwargs):
        pk, tpk = self.kwargs['pk'], self.kwargs['tpk']
        form = self.form_class(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.tempalte_id = tpk
            new.save()
            return redirect('porter:field', pk=pk, tpk=tpk)
        query_list = Field.objects.filter(template__id=tpk).all()
        return render(request, self.template_name, {'query_list': query_list, 'form': form, 'pk': pk, 'tpk': tpk})


