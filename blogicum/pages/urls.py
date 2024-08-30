from .views import about, rules
from django.urls import path

app_name = 'pages'

urlpatterns = [
    path('about/', about, name='about'),
    path('rules/', rules, name='rules'),
]
