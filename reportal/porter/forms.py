from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import ReportSet, Template, Field, Report
from account.models import Group

def form_horizontal():
    helper = FormHelper()
    helper.form_tag = False
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    return helper

class ReportSetForm(forms.ModelForm):
    class Meta:
        model = ReportSet
        fields = ['name', 'group']

    def __init__(self, user, *args, **kwargs):
        super(ReportSetForm, self).__init__(*args, **kwargs)
        # limit group options based on user
        self.fields['group'].queryset = Group.objects.filter(profiles__user=user)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = form_horizontal()

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        self.helper = form_horizontal()

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'dtype']

    def __init__(self, *args, **kwargs):
        super(FieldForm, self).__init__(*args, **kwargs)
        self.helper = form_horizontal()

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'method', 'templates']

    def __init__(self, rspk, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['templates'].queryset = Template.objects.filter(report_set=rspk)
        self.helper = form_horizontal()