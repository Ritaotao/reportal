from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.urls import reverse
from django.views import View
from django.db.models import Q
from .models import ReportSet, Template, Submission, Field
from .models import RS_ORDER_COLUMN_CHOICES
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

def query_by_args(queryset, order_column_choices, qs_filter, **kwargs):
    """To prepare elements for datatables server side processing"""
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]
    order_column = order_column_choices[order_column]
    # django orm '-' -> desc
    if order == 'desc':
        order_column = '-' + order_column
    total = queryset.count()
    if search_value:
        queryset = qs_filter(queryset, search_value)
    total_filter = queryset.count()
    queryset = queryset.order_by(order_column)[start:start + length]
    return queryset, draw, total, total_filter

# Create your views here.
# create portal
## Step 1: create a new report set or use an existing one

def reportsetIndex(request):
    form = ReportSetForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.create_by = request.user
        print(obj, 'saved')
        obj.save()
    html = TemplateResponse(request, 'porter/reportset.html', {'form': form})
    return HttpResponse(html.render())

class ReportSetViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSetSerializer
    queryset = ReportSet.objects.all()

    def custom_filter(self, queryset, search_value):
        return queryset.filter(Q(id__icontains=search_value) | 
                                    Q(name__icontains=search_value) | 
                                    Q(group__icontains=search_value) | 
                                    Q(create_by__icontains=search_value) | 
                                    Q(create_date__icontains=search_value) | 
                                    Q(last_modify_date__icontains=search_value))

    #permission_classes = (IsAuthenticated,)
    def list(self, request, **kwargs):
        try:
            result = dict()
            queryset = ReportSet.objects.filter(create_by=self.request.user)
            elements = query_by_args(queryset, RS_ORDER_COLUMN_CHOICES, self.custom_filter, **request.query_params)
            result['draw'] = elements[1]
            result['recordsTotal'] = elements[2]
            result['recordsFiltered'] = elements[3]
            serializer = ReportSetSerializer(elements[0], many=True)  
            result['data'] = serializer.data
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


