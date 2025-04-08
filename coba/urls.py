# coba/urls.py
from django.urls import path
from .views import ErrorExampleView, TestView

urlpatterns = [
    path('test', TestView.as_view(), name='test'),
    path('error', ErrorExampleView.as_view(), name='error'),  # endpoint baru
]