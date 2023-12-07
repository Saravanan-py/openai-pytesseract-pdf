from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.generics import *
from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.generics import *
# Create your views here.
from openai_app.extraction import process_pdfs_and_query_wrapper

import time
import concurrent.futures
import os


def index(request):
    return HttpResponse("hello world")


class OpenApITextExtractionAPI(CreateAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = UploadSerializer


    def post(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('pdf')
            serialized_files = []

            for file in files:
                data = {'pdf': file}
                serializer = UploadSerializer(data=data)
                if serializer.is_valid():
                    saved_instance = serializer.save()
                    serialized_files.append({
                        'pdf': saved_instance.pdf.path,
                        'id': saved_instance.id
                    })

            # Extract file paths and process in a thread pool
            file_paths = [file['pdf'] for file in serialized_files]
            results = process_pdfs_and_query_wrapper(file_paths)
            extracted_text = ''.join(results)

            print(extracted_text)
            data = {
                        'Response Code': status.HTTP_201_CREATED,
                        'Status': 'TRUE',
                        'Message': 'Data Uploaded and Text file is created',
                        "Error": 'None',
                        'Data': extracted_text,
                    }
            return Response(data)

        except Exception as e:
            data = {
                'Response Code': status.HTTP_400_BAD_REQUEST,
                'Status': 'FALSE',
                'Message': 'Upload Failed',
                "Error": str(e),
                'Data': [],
            }
            return Response(data)