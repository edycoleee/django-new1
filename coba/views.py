# coba/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from restapi.utils.response_wrapper import success_response

class TestView(APIView):
    def get(self, request):
        data = {"info": "This is a wrapped response"}
        return Response(success_response("Hello World", data))
