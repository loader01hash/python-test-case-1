from django.shortcuts import render
from django.http import HttpResponse
from Booking.models import *
from pickle import FALSE
from re import A
from stringprep import c22_specials
from tkinter import Y
from turtle import ycor
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect
from datetime import date, timedelta, datetime
from django.core.files.storage import FileSystemStorage


# Create your views here.

def index(request):
    #print("You are index Admindetails index")
    m = MovieDetails.objects.all()
    c = Show.objects.all()
    s = SeatDetails.objects.all()
    template = loader.get_template('adminOperation.html')
    return render(request, 'adminOperation.html' ,{'m':m,'c':c,'s':s})

def add_movie(request):
    template = loader.get_template('add.html')
    return render(request,'add.html')

#--------  This is the previous version

# def addrecord_movie(request):
#     x = request.POST['moviename']
#     y = request.POST['Price']
#     z = request.POST['screen_no']
#     a = request.POST['certification']
#     b = request.POST['description']
#     g = request.POST['total_seats']
#     d = request.POST['daterange']
#     s1 = request.POST.get('Morning',False)
#     s2 = request.POST.get('Afternoon',False)
#     s3 = request.POST.get('Evening',False)
#     if request.method == 'POST' and request.FILES['upload']:
#         upload = request.FILES['upload']
#         fss = FileSystemStorage()
#     arr = [i.split("/") for i in d.split("-")]
#     m = MovieDetails(moviename=x,screen_no=z,certification=a,description=b,total_seats=g,image=upload,seat_price=y)
#     m.save()
#     sd = date(int(arr[0][2]),int(arr[0][0]),int(arr[0][1]))
#     ed = date(int(arr[1][2]),int(arr[1][0]),int(arr[1][1]))
#     day_count = (ed - sd).days + 1
#     for single_date in [d for d in (sd + timedelta(n) for n in range(day_count)) if d <= ed]:
#         date_n = single_date.strftime("%Y-%m-%d")
#         if s1:
#             v = Show(show_date=date_n,show_type=s1,movie_id=m)
#             v.save()
#         if s2:
#             v = Show(show_date=date_n,show_type=s2,movie_id=m)
#             v.save()
#         if s3:
#             v = Show(show_date=date_n,show_type=s2,movie_id=m)
#             v.save()
#     c = Show.objects.all().filter(movie_id=m)
#     for i in c:
#         for k in range(int(g)):
#             a = SeatDetails(show_id=i,seat_status=False,seat_no=k)
#             a.save()
#     return redirect('Admindetails:index')

def addrecord_movie(request):
    x = request.POST['moviename']
    y = request.POST['Price']
    z = request.POST['screen_no']
    a = request.POST['certification']
    b = request.POST['description']
    g = request.POST['total_seats']
    d = request.POST['daterange']
    s1 = request.POST.get('Morning',False)
    s2 = request.POST.get('Afternoon',False)
    s3 = request.POST.get('Evening',False)
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()

    shows = Show.objects.all()

    arr = [i.split("/") for i in d.split("-")]
    sd = date(int(arr[0][2]),int(arr[0][0]),int(arr[0][1]))
    ed = date(int(arr[1][2]),int(arr[1][0]),int(arr[1][1]))
    day_count = (ed - sd).days + 1
    days_list = [d for d in (sd + timedelta(n) for n in range(day_count)) if d <= ed]
    
    if MovieDetails.objects.all().filter(moviename=x).exists():
        return HttpResponse('<h1>Movie Already Exists !!</h1>')
    else:
        i = 0
        while(i<len(days_list)):
            if not shows.filter(show_date=days_list[i]).exists():
                i+=1
            else:
                movies = list(shows.filter(show_date=days_list[i]))
                for movie in movies:
                    if movie.movie_id.screen_no==int(z):
                        slots = Show.objects.all().filter(show_date=days_list[i],movie_id=movie.movie_id.id)
                        if slots.exists():
                            occupied_slot_lst = [False,False,False]
                            for slot in slots:
                                if slot.show_type == '10:00am-12:00pm':
                                    occupied_slot_lst[0] = True
                                if slot.show_type == '2:00pm-4:00pm':
                                    occupied_slot_lst[1] = True
                                if slot.show_type == '4:00pm-6:00pm':
                                    occupied_slot_lst[2] = True
                            selected_slot_map = list()
                            for s in [s1,s2,s3]:
                                if s == False:
                                    selected_slot_map.append(s)
                                else:
                                    selected_slot_map.append(True)
                            for i in range(len(occupied_slot_lst)):
                                if selected_slot_map[i]:
                                    if occupied_slot_lst[i]:
                                        return HttpResponse('<h1>Slot already booked</h1>')
                                    else:
                                        continue
                                else:
                                    continue
                        else:
                            continue
                    else:
                        continue
            i+=1

        else:
            m = MovieDetails(moviename=x,screen_no=z,certification=a,description=b,total_seats=g,image=upload,seat_price=y)
            m.save()
            for day in days_list:
                day_date = day.strftime("%Y-%m-%d")
                if s1:
                    v = Show(show_date=day_date,show_type=s1,movie_id=m)
                    v.save()
                if s2:
                    v = Show(show_date=day_date,show_type=s2,movie_id=m)
                    v.save()
                if s3:
                    v = Show(show_date=day_date,show_type=s3,movie_id=m)
                    v.save()
            c = Show.objects.all().filter(movie_id=m)
            for i in c:
                for k in range(int(g)):
                    a = SeatDetails(show_id=i,seat_status=False,seat_no=k)
                    a.save()
            return redirect('Admindetails:index')

def delete_movie(request, id):
    m = MovieDetails.objects.get(id=id)
    m.delete()
    return redirect('Admindetails:index')

def update_movie(request, id):
    m = MovieDetails.objects.get(id=id) 
    all_shows = Show.objects.all().filter(movie_id=id)
    dates = list(set([str(show.show_date).split()[0] for show in all_shows]))
    dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d")) 
    date_list = [dates[0],dates[-1]]
    print(date_list)
    new_date_list = []
    for i in date_list:
        date = i.split('-')
        new_date_list.append(f'{date[1]}/{date[2]}/{date[0]}')
    show = all_shows.filter(show_date=dates[0])
    shows ={0:False,1:False,2:False}
    for i in show:
        if i.show_type == '10:00am-12:00pm':
            shows[0]=True
        elif i.show_type == '2:00pm-4:00pm':
            shows[1]=True
        else:
            shows[2]=True   
    template = loader.get_template('update.html')
    return render(request, 'update.html' ,{'movie': m, 'dat':new_date_list, 'show':shows})

def updaterecord_movie(request, id):
    x = request.POST['moviename']
    y = request.POST['Price']
    z = request.POST['screen_no']
    a = request.POST['certification']
    b = request.POST['description']
    c = request.POST['total_seats']
    d = request.POST['daterange']
    s1 = request.POST.get('Morning',False)
    s2 = request.POST.get('Afternoon',False)
    s3 = request.POST.get('Evening',False)

    shows = Show.objects.all()

    arr = [i.split("/") for i in d.split("-")]
    sd = date(int(arr[0][2]),int(arr[0][0]),int(arr[0][1]))
    ed = date(int(arr[1][2]),int(arr[1][0]),int(arr[1][1]))
    day_count = (ed - sd).days + 1
    days_list = [d for d in (sd + timedelta(n) for n in range(day_count)) if d <= ed]
    i=0
    while(i<len(days_list)):
        if not shows.filter(show_date=days_list[i]).exists():
            i+=1
        else:
            movies = list(shows.filter(show_date=days_list[i]))
            for movie in movies:
                if movie.movie_id.id == id:
                    continue
                else:
                    if movie.movie_id.screen_no==int(z):
                        slots = Show.objects.all().filter(show_date=days_list[i],movie_id=movie.movie_id.id)
                        if slots.exists():
                            occupied_slot_lst = [False,False,False]
                            for slot in slots:
                                if slot.show_type == '10:00am-12:00pm':
                                    occupied_slot_lst[0] = True
                                if slot.show_type == '2:00pm-4:00pm':
                                    occupied_slot_lst[1] = True
                                if slot.show_type == '4:00pm-6:00pm':
                                    occupied_slot_lst[2] = True
                            selected_slot_map = list()
                            for s in [s1,s2,s3]:
                                if s == False:
                                    selected_slot_map.append(s)
                                else:
                                    selected_slot_map.append(True)
                            for i in range(len(occupied_slot_lst)):
                                if selected_slot_map[i]:
                                    if occupied_slot_lst[i]:
                                        return HttpResponse('<h1>Slot already booked</h1>')
                                    else:
                                        continue
                                else:
                                    continue
                        else:
                            continue
                    else:
                        continue
            i+=1
    else:
        m = MovieDetails.objects.get(id=id)
        m.moviename = x
        m.seat_price= y
        m.screen_no = z
        m.certification= a
        m.description = b
        m.total_seats= c
        m.save()
        s = Show.objects.filter(movie_id=id)
        s.delete()
        for day in days_list:
            day_date = day.strftime("%Y-%m-%d")
            if s1:
                v = Show(show_date=day_date,show_type=s1,movie_id=m)
                v.save()
            if s2:
                v = Show(show_date=day_date,show_type=s2,movie_id=m)
                v.save()
            if s3:
                v = Show(show_date=day_date,show_type=s3,movie_id=m)
                v.save()
        return redirect('Admindetails:index')