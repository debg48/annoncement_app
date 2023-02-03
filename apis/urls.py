from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.Register.as_view()), #api to register user
    path('login/',views.Login.as_view()), #api to login
    path('logout/',views.LogOut.as_view()), # api to logout
    path('create/',views.Create.as_view()), # api to create annoncement
    path('read/',views.ReadAll.as_view()), #api to read the annoncements
    path('update-status/',views.ChangeStatus.as_view()) #apii to update status

]