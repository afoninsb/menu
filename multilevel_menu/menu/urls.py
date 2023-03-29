from django.urls import path

from . import views

app_name = 'menu'

urlpatterns = [
    path('<slug:item>/', views.IndexView.as_view(), name='item'),
    path('',  views.IndexView.as_view(), name='index')
]
