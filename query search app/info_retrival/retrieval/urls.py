from django.urls import path
from . import views

urlpatterns = [
    path('', views.retrieve_documents, name='retrieve_documents'),
]
