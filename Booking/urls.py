#from django.contrib import admin
from django.urls import path 
from . import views

app_name = "Booking"

urlpatterns = [
    #path("" , views.index, name='app_1'),
    #path("about" , views.about, name='about'),
    path("movie_des/<int:id>/<str:username>" , views.movie_des, name='movie_des'),
    path("showlist/<int:id>/<str:username>" , views.showlist, name='showlist'),
    #path('booking' , views.booking , name = 'booking')
    
    ## Merge this url withshow timings page once its ready
    path("seatbooking/<int:id>/<str:username>", views.seatbooking, name='seatbooking'),
    path("bookseats/<int:id>/<str:username>", views.bookseats, name='bookseats'),
    #path("mail/" , views.mail, name='mail'),
]
