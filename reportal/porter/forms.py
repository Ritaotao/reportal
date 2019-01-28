from django import forms
from django.core.validators import FileExtensionValidator
from crispy_forms.helper import FormHelper
from .models import ReportSet, Template, Field, RuleSet, Report, Submission
from account.models import Group, Profile

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

class FieldImportForm(forms.Form):
    docfile = forms.FileField(
        widget=forms.FileInput(attrs={'accept': ".csv"}),
        label='Upload',
        help_text='max. 42 meabytes',
        validators = [FileExtensionValidator(allowed_extensions=['csv'])]
    )

    def __init__(self, *args, **kwargs):
        super(FieldImportForm, self).__init__(*args, **kwargs)
        self.helper = form_horizontal()

class RuleSetForm(forms.ModelForm):
    class Meta:
        model = RuleSet
        fields = ['field', 'rule', 'argument', 'action', 'error_message']
        help_texts = {
            'argument': 'if multiple arguments, seperated by comma(,); date argument format: 2019-01-01',
            'action': 'Warning: flagged but submission will be accepted; Error: submission will be rejected',
        }

    def __init__(self, tpk, *args, **kwargs):
        super(RuleSetForm, self).__init__(*args, **kwargs)
        self.fields['field'].queryset = Field.objects.filter(template=tpk)
        self.helper = form_horizontal()

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'method', 'templates']

    def __init__(self, rspk, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['templates'].queryset = Template.objects.filter(report_set=rspk)
        self.helper = form_horizontal()

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['template', 'upload']

    def __init__(self, rpk, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['template'].queryset = Template.objects.filter(reports__id=rpk)
        self.fields['upload'].widget = forms.FileInput(attrs={'accept': ".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"})
        self.fields['upload'].help_text = 'csv/xlsx, one sheet only'
        self.fields['upload'].validators = [FileExtensionValidator(allowed_extensions=['csv', 'xlsx'])]
        self.helper = form_horizontal()