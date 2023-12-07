from rest_framework import serializers
from .models import *


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenaiFiles
        fields = "__all__"