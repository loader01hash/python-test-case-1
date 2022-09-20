from django.urls import path
from . import views
app_name = "Authentication"
urlpatterns = [
    path('', views.index, name='index'),
    #path('usersignup/', views.usersignup, name='usersignup'),
    path('addnewuser/', views.addnewuser, name = 'addnewuser'),
    path('viewprofile/<str:username>', views.viewprofile, name = 'viewprofile'),
    path('viewprofile/updateUserDetails/<int:id>', views.updateUserDetails, name = 'updateUserDetails'),
    #path('updateUserDetails/<str:user_name>', views.updateUserDetails, name='updateUserDetails/'),
    path('validate/',views.validate,name='validation'),
    path('home/<str:username>', views.home, name='home'),
    
]