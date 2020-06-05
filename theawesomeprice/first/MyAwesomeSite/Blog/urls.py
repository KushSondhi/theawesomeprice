from django.urls import path
from .import views

urlpatterns=[
    path('<str:blog_name>',views.first,name='firstBlog')
]
