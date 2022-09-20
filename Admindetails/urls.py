from django.urls import path
from . import views

app_name = 'Admindetails'

urlpatterns = [path('',views.index,name='index'),
               path('add/', views.add_movie, name='add'),
               path('update/<int:id>', views.update_movie, name='update'),
               path('add/addrecord_movie/', views.addrecord_movie, name='addrecord_movie'),
               path('update/updaterecord_movie/<int:id>', views.updaterecord_movie, name='updaterecord_movie'),
               path('delete/<int:id>', views.delete_movie, name='delete'),

              ]