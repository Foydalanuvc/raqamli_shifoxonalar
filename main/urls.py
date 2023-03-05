from django.urls import path
from .views import MainIndexView

app_name = 'main'
urlpatterns = [
    path('', MainIndexView.as_view(), name='index')
]