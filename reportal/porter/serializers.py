from django.conf import settings
from rest_framework import serializers
from .models import ReportSet, Template
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