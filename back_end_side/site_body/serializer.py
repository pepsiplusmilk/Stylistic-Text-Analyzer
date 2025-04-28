from rest_framework import serializers
from .models import *

class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserText
        fields = ["plain_text", "text_file"]