from django.conf import settings
from rest_framework import serializers
from .models import ReportSet, Template, Field, Report, Rule, RuleSet, Submission
from account.models import Group, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)   

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'id')

class GenericMetaFieldMixin(serializers.Serializer):
    create_by = UserSerializer()
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_date = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)  

class ReportSetSerializer(GenericMetaFieldMixin, serializers.ModelSerializer):
    group = GroupSerializer()
    class Meta:
        model = ReportSet
        fields = "__all__"

class TemplateSerializer(GenericMetaFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = "__all__"

class ReportSerializer(GenericMetaFieldMixin, serializers.ModelSerializer):
    report_set = ReportSetSerializer()
    templates = TemplateSerializer(read_only=True, many=True)
    class Meta:
        model = Report
        fields = "__all__"

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = "__all__"

class RuleSetSerializer(serializers.ModelSerializer):
    field = FieldSerializer()
    rule = RuleSerializer()

    class Meta:
        model = RuleSet
        fields = "__all__"

class SubmissionSerializer(serializers.ModelSerializer):
    report = ReportSerializer()
    template = TemplateSerializer()
    submitted_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    submitted_by = UserSerializer()

    class Meta:
        model = Submission
        fields = "__all__"  