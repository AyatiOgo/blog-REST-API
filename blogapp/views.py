from django.shortcuts import render
from .models import Blog
from .serializers import UserRegistrationSerializer, BlogSerializer, UpdateUserProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class BlogPaginator(PageNumberPagination):
    page_size = 3

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user =  request.user
    serializer = UpdateUserProfileSerializer(user, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({"message":"Blog Deleted Succesfully"}, status=status.HTTP_204_NO_CONTENT)
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blog(request, id):
    user = request.user
    blog = Blog.objects.get(id=id)
    
    if user != blog.author:
        return Response({'error':'Not VAlid author '}, status= status.HTTP_401_UNAUTHORIZED)
    else:
        blog.delete()
        return Response({"message":"Blog Deleted Succesfully"}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET'])
# def view_blogs(request):
#     blog = Blog.objects.all()
#     serializer = BlogSerializer(blog, many = True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_blogs(request):
    blog = Blog.objects.all()
    paginator = BlogPaginator()
    paginated_blog = paginator.paginate_queryset(blog, request)
    serializer = BlogSerializer(paginated_blog, many = True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_blog(request, id):
    blog = Blog.objects.get(id = id)
    serializer = BlogSerializer(blog,)
    return Response(serializer.data,  status= status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_username(request):
    user = request.user
    username = user.username
    return Response({"username": username })

