from django.conf import settings
from rest_framework import serializers
from .models import ReportSet

class ReportSetSerializer(serializers.ModelSerializer):
    last_modify_date = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_date = serializers.DateTimeField(format=settings.DATE_FORMAT, required=False)

    class Meta:
        model = ReportSet
        fields = '__all__'
        depth = 1
