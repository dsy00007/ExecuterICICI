from django.urls import path
from .views import *

urlpatterns = [
    path('display_data/', MyView.as_view(), name='display_data'),
    path('refreshData/',MyView.getDataFromApi, name='getDataFromApi'),
   path('setSessionKey/', MyView.setSessionKey, name ='setSessionKey')
]