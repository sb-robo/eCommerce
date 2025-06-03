from rest_framework.response import Response
from rest_framework.views import APIView


class CreateView(APIView):
    def get(self, request):
        return Response({"User": "User Created"})
