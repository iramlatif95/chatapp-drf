from django.shortcuts import render
from rest_framework import viewsets,status 
from django.contrib.auth import authenticate,login,logout
from.serializers import RegisterSerializer,Loginserializer 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from.models import User 
from axes.exceptions import AxesBackendPermissionDenied



class RegisterViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]
    http_method_names=['post']

    def create(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({"message":"user registration is successfull"},status=status.HTTP_201_CREATED)


class LoginViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=Loginserializer 
    permission_classes=[AllowAny]
    http_method_names=['post']
    

    
    def create(self,request,*args,**kwargs):
        username=request.data.get('username')
        password=request.data.get('password')
        try:
                user=authenticate(request,username=username,password=password)
        except AxesBackendPermissionDenied:
             return Response({"error":"you are block try after the 1 hour"},status=status.HTTP_403_FORBIDDEN)
        if user:
            login(request,user)
            request.session.set_expiry(60*60)
            return Response({'message':" login successful"},status=status.HTTP_200_OK)
        return Response({"message":"invalid credientials"},status=status.HTTP_401_UNAUTHORIZED)
    

class logoutView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        logout(request)
        return Response({"message":"session is logout"},status=status.HTTP_200_OK)





        

# Create your views here.
