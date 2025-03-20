from django.urls import path
from .views import export_document

urlpatterns = [
    path('', export_document, name='export_document'),
]