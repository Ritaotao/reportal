from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, FormView, CreateView, UpdateView
from .models import ReportSet, Template, Submission, Field
from .forms import ReportSetForm, TemplateForm, FieldForm

import random

# utility functions
def genUid():
    rand = str(random.randint(100,999)) + '-' + str(random.randint(1000,9999))
    if Submission.objects.filter(uid = rand).exists() or Template.objects.filter(uid = rand).exists():
        genUid()
    else:
        return rand

# Create your views here.
def index(request):
    return render(request, "porter/home.html")

# create portal
## Step 1: create a new report set or use an existing one

class ReportSetView(View):
    template_name = "porter/reportset.html"
    form_class = ReportSetForm

    def get(self, request, *args, **kwargs):
        object_list = ReportSet.objects.all()
        pk = self.kwargs.get('pk', None)
        initial = ReportSet.objects.filter(pk=pk).first()
        print(initial)
        form = self.form_class(instance=initial)
        return render(request, self.template_name, {'object_list': object_list, 'form': form})

    def post(self, request, *args, **kwargs):
        object_list = ReportSet.objects.all()
        pk = self.kwargs.get('pk', None)
        initial = ReportSet.objects.filter(pk=pk).first()
        form = self.form_class(request.POST, instance=initial)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return redirect('porter:reportset')
        return render(request, self.template_name, {'object_list': object_list, 'form': form})

class TemplateView(View):
    form_class = TemplateForm
    template_name = "porter/template.html"
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = self.form_class()
        query_list = Template.objects.filter(report_set__id=pk).all()
        return render(request, self.template_name, {'query_list': query_list, 'form': form, 'pk': pk})

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = self.form_class(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.uid = genUid()
            new.report_set_id = pk
            new.save()
            return redirect('porter:template', pk=pk)
        query_list = Template.objects.filter(report_set__id=pk).all()
        return render(request, self.template_name, {'query_list': query_list, 'form': form, 'pk': pk})


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


