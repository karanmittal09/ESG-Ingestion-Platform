from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    organization_id = serializers.IntegerField()
    uploaded_by = serializers.CharField()