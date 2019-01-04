from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import ReportSet, Template, Report

class ReportSetForm(forms.ModelForm):
    class Meta:
        model = ReportSet
        fields = ['name', 'group']

    def __init__(self, *args, **kwargs):
        super(ReportSetForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Create'))

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(TemplateForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', 'Create'))