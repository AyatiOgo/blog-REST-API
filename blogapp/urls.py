from django.urls import path
from .views import register_user,create_blog,view_blogs

urlpatterns = [
    path('register_user/', register_user, name= 'register_user' ),
    path('create_blog/', create_blog, name= 'create_blog' ),
    path('blogs/', view_blogs , name= 'blogs' ),
]