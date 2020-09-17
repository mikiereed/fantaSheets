from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='fantaSheets'),
    path('<int:fantaSheet_id>', views.fantaSheet, name='fantaSheet'),
    path('create', views.create, name='create'),
]
