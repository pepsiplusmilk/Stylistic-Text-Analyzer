from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializer import *

class AnalyzerView(APIView):
    def get(self, request):
        output = [{"user_plain_text" : output.plain_text,
                   "user_file_text" : output.text_file}
                  for output in UserText.objects.all()]

        return Response(output)

    def post(self, request):
        serializer = UserInputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)