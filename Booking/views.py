from django.shortcuts import render,HttpResponse
from multiprocessing import context
from re import template
from unittest import loader
from Booking.models import *
import datetime
from datetime import datetime
from json import dumps
from django.shortcuts import render,redirect
from Booking.models import *
from django.core.mail import send_mail
from django.conf import settings

def movie_des(request, id, username):
    m=MovieDetails.objects.filter(id=id)
    context = {
        'Selected_movie' : m,
        'username': username
    }
    #print(username)
    return render(request, 'mov_des.html' ,context)

def showlist(request, id, username):
    #print(username)
    movie=MovieDetails.objects.filter(id=id)
    shows = Show.objects.all().filter(movie_id_id = id)
    #print(shows[0].show_date)
    #print(shows)
    #---- This datelist will contain the upcoming unique 3 dates in ascending order 
    datelist=[]
    thisdict= {}
    for item in shows:
        date = item.show_date
        #print(date)

        
        
        #print(thisdict)
        if date.strftime('%d-%b-%y') not in thisdict.keys():
            thisdict[date.strftime('%d-%b-%y')] = [item.show_type, item.id]
        else:
            thisdict[date.strftime('%d-%b-%y')] = (thisdict[date.strftime('%d-%b-%y')])+[item.show_type, item.id]
        

        if date.strftime('%d-%b-%y') not in datelist:
            datelist.append(date.strftime('%d-%b-%y'))
    datelist.sort(key=lambda date: datetime.strptime(date, "%d-%b-%y"))
    #print(datelist)
    #print(thisdict[datelist[0]])
    #print(thisdict[datelist[0]][0])

    nestedshowlist = []
    nestedshowlist.append(thisdict[datelist[0]])
    nestedshowlist.append(thisdict[datelist[1]])
    nestedshowlist.append(thisdict[datelist[2]])
    
    #print(nestedshowlist)



    

    context = {
        'Selected_movie' : movie, 
        'DateDetails' : datelist,
        'ShowDetails' : nestedshowlist,
        'username': username
    }
    return render(request, 'showtimings.html' ,context)
    #return render(request,'showtimings.html')

def seatbooking(request, id, username):
    print(username)
    print(id)
    s = Show.objects.get(id=id)
    print(s.movie_id_id)
    m = MovieDetails.objects.get(id=s.movie_id_id)
    print(m.total_seats)
    seatdeatils = SeatDetails.objects.all().filter(show_id_id = id)
    # -------------- thisdict is key value pair where key is the seat no and value is tge corresponding seat status
    thisdict = {}
    for i in range(m.total_seats):
        thisdict[seatdeatils[i].seat_no] = seatdeatils[i].seat_status
    
    #print(thisdict)
    dataJSON = dumps(thisdict)    

    #return render(request, 'seating.html', {'data': dataJSON, 'id':id , 'username': username})
    return render(request, 'seat.html', {'data': dataJSON, 'id':id , 'username': username})

def bookseats(request, id, username):
    #s1 = request.POST.get("0",False)
    user_id = UserDetails.objects.get(user_name=username).id
    
    


    
    seat = SeatDetails.objects.filter(show_id_id=id)
    no_of_seats_selected = 0
    for i in range(len(seat)):
        c = request.POST.get(str(i),False)
        #print(c)
        
        if c == 'on':
            no_of_seats_selected+=1
            currentseatobj = seat[i]
            currentseatobj.seat_status = True
            currentseatobj.userid_id = user_id
            currentseatobj.save()

    
    seatsQuery = SeatDetails.objects.filter(userid_id = user_id, show_id_id = id)

    ########
    movie_id_Query = Show.objects.filter(id = id)
    movie_id = movie_id_Query[0].movie_id_id

    perSeatPrice = (MovieDetails.objects.get(id = movie_id)).seat_price
    
    
    
    movieSelectedQuery = MovieDetails.objects.filter(id = movie_id) 
    movieSelectedObj = movieSelectedQuery[0]

    
    seatdetQuery=SeatDetails.objects.filter(userid_id = user_id, show_id_id = id)
    print(seatdetQuery)
    showid = seatdetQuery[0].show_id_id
    showtimingquery = Show.objects.filter(id = showid, movie_id_id = movie_id)
    showtime = showtimingquery[0].show_type
    ########
    Details = {}
    seatDetails = []
    for item in seatsQuery:
        seatDetails.append(item.seat_no)
    
    userQuery = UserDetails.objects.filter(id = user_id)
    userobj = userQuery[0]
    
    Details['userId'] = user_id
    Details['userMail'] = userobj.user_name
    Details['seats'] = seatDetails
    Details['movieName'] = movieSelectedObj.moviename
    Details['certification'] = movieSelectedObj.certification
    Details['screenno'] = movieSelectedObj.screen_no
    Details['showtime'] = showtime
    Details['amount'] = perSeatPrice * no_of_seats_selected

    

    #print(Details)
    subject = 'Booking Detail'
    message = '_____Congratulation your Booking is done :____ ' + '\n' + 'User Id = ' + str(Details['userId']) + '\n'+'Seat Details = ' + str(Details['seats']) + '\n' + 'Movie Name = ' + str(Details['movieName']) + '\n' + 'movie certification = ' + str(Details['certification']) + '\n' + 'screen no =' + str(Details['screenno']) + '\n' + 'Movie showtiming =' + str(Details['showtime']) + '\n'  + 'Total Amount = '+ str(Details['amount']) + '\n' + 'Thanks for using The Golden Cinemas.'+ '\n' + 'You are like family to us.'
    email_from = settings.EMAIL_HOST_USER
    #recipient_list = ['anujyadavsky@gmail.com']
    recipient_list = [username]
    send_mail( subject, message, email_from, recipient_list )
    return render(request, 'final.html')
    
    # ------ The booked seats for the current user has been update din the database
    # ------ call the mail() to send a mail stating the details of booking

    


