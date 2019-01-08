from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.urls import reverse
from django.views import View
from .models import ReportSet, Template, Submission, Field
from .models import query_rs_by_args
from .forms import ReportSetForm, TemplateForm, FieldForm
from django.template.response import TemplateResponse

from rest_framework import viewsets, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import list_route
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ReportSetSerializer

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
    form = ReportSetForm(request.POST or None)
    if form.is_valid():
        print('saved')
        form.save()
    html = TemplateResponse(request, 'porter/reportset.html', {'form': form})
    return HttpResponse(html.render())

class ReportSetViewSet(viewsets.ModelViewSet):
    queryset = ReportSet.objects.all()
    serializer_class = ReportSetSerializer

    #permission_classes = (IsAuthenticated,)

    def list(self, request, **kwargs):
        try:
            reportset = query_rs_by_args(**request.query_params)
            serializer = ReportSetSerializer(reportset['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = reportset['draw']
            result['recordsTotal'] = reportset['total']
            result['recordsFiltered'] = reportset['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

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


