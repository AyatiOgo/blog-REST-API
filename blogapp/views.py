from django.shortcuts import render
from .models import Blog
from .serializers import UserRegistrationSerializer, BlogSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog(request):
    user = request.user
    serializer = BlogSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save(author=user)
        return Response(serializer.data, status= status.HTTP_201_CREATED )
    else:
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_blog(request, id):
    user = request.user
    blog = Blog.objects.get(id=id)
    if request.method == 'PUT':
        if user != blog.author:
            return Response({'error':'Not VAlid author '}, status= status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = BlogSerializer(blog, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED )
            else:
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        if user != blog.author:
            return Response({'error':'Not VAlid author '}, status= status.HTTP_401_UNAUTHORIZED)
        else:
            blog.delete()




@api_view(['GET'])
def view_blogs(request):
    blog = Blog.objects.all()
    serializer = BlogSerializer(blog, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)