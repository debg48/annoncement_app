from django.urls import path,include
from . import views

urlpatterns = [
    path('apis/', include('apis.urls')), #creation api

]