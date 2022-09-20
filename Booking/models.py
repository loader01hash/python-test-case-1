from django.db import models

# Create your models here.
class MovieDetails(models.Model):
    moviename = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    certification = models.CharField(max_length=255)
    screen_no = models.IntegerField()
    total_seats = models.IntegerField()
    seat_price = models.IntegerField(blank=True,null=True)
    #moviepath = models.CharField(max_length=255, null=True) # Needed to add a default value since this field was added later on
    image = models.ImageField(upload_to='img/',default='slide-1.jpg',null=True)
    
class Show(models.Model):
    show_date = models.DateField(blank=True,null=True)
    #start_time = models.DateTimeField()
    #end_time = models.DateTimeField()
    show_type = models.CharField(max_length=100,blank=True,null=True)
    movie_id = models.ForeignKey(MovieDetails, on_delete=models.CASCADE)

class UserDetails(models.Model):
    user_name = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)
    user_age = models.IntegerField()
    user_phone_no = models.BigIntegerField()

class SeatDetails(models.Model):
    seat_no = models.IntegerField()
    seat_status = models.BooleanField()
    #seat_price = models.IntegerField()
    userid = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=True)
    show_id = models.ForeignKey(Show, on_delete=models.CASCADE)

class AdminDetails(models.Model):
    admin_username = models.CharField(max_length=255)
    admin_password = models.CharField(max_length=255)


