from django.shortcuts import render, redirect #, get_object_or_404
from django.urls import reverse
from django.views import View
from .models import ReportSet, Template, Submission
from .forms import ReportSetForm, TemplateForm

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
    form_class = ReportSetForm
    template_name = "porter/reportset.html"
    query_list = ReportSet.objects.all()

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'query_list': self.query_list, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return render(request, self.template_name, {'query_list': self.query_list, 'form': form})


class TemplateView(View):
    form_class = TemplateForm
    template_name = "porter/template.html"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        query_list = Template.objects.filter(report_set__id=self.kwargs['pk']).all()
        return render(request, self.template_name, {'query_list': query_list, 'form': form})

    def post(self, request, *args, **kwargs):
        reportset_id = self.kwargs['pk']
        form = self.form_class(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.uid = genUid()
            new.report_set_id = reportset_id
            new.save()
        query_list = Template.objects.filter(report_set__id=reportset_id).all()
        return render(request, self.template_name, {'query_list': query_list, 'form': form})


class FieldView(View):
    pass


