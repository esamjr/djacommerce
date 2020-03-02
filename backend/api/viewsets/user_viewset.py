from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.models import Token
from api.serializers import userSerializers
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.models import User 
  
class userviewsets(viewsets.ModelViewSet): 
    queryset = User.objects.all() 
    serializer_class = userSerializers

# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         django_login(request, user)
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({"token":token.key}, status=200)

# class LogoutView(APIView):
#     authentication_classes = (TokenAuthentication,)
#     def post(self, request):
#         django_logout(request)
#         return Response(status=204)
