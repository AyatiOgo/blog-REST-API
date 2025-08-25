from rest_framework import serializers
from .models import CustomUSer, Blog
from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
        

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        password = validated_data['password']

        user = get_user_model()
        new_user = user.objects.create_user(email=email, username = username, first_name = first_name, 
                                        last_name = last_name, password=password)

        return new_user
    
class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name","bio","profile_img"
                  ,"facebook", "instagram","twitter","linkedin",  ]

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name']

class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only = True)
    class Meta:
        model = Blog
        fields = [ 'id', 'title','slug', 'content', 'author', 'created_at', 'updated_at', 
                    'published_time', 'is_draft', 'category', 'featured_img',  ]

