from django.shortcuts import render,redirect,get_object_or_404
from .models import Event,Ticket,History
from django.contrib import messages
from account.models import Account
from django.contrib.auth import get_user_model
from .forms import EventForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def event_list(request):
    search_query = request.GET.get('event')
    if search_query:
        event_list = Event.objects.filter(event_name__contains=search_query)
        return render(request, 'event/event_list.html', {'event_list': event_list})
    event_list = Event.objects.all()
    return render(request,'event/event_list.html',{'event_list':event_list})
def event_details(request,id):
    event = Event.objects.get(id=id)
    tickets = event.event_ticket.filter(allow_resale=True)
    return render(request, 'event/event_details.html', {'event': event,'tickets':tickets})

@login_required()
def create_event(request):
    if request.user.is_event_organizer:
        form = EventForm()
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES)  # Need to include request.FILES for image upload
            if form.is_valid():
                event = form.save(commit=False)  # Commit=False to delay saving to set the user field
                event.user = request.user
                event.save()
                return redirect('event_list')  # Assuming you have an event-detail URL
        return render(request, 'event/create_event.html', {'form': form})
    else:
        return redirect('event_list')
@login_required()
def update_event(request,id):
    if request.user.is_event_organizer:
        form = EventForm()
        event = get_object_or_404(Event,id=id,user=request.user)
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES,instance=event)
            if form.is_valid():
                event = form.save(commit=False)  # Commit=False to delay saving to set the user field
                event.user = request.user
                event.save()
        else:
            form = EventForm(instance=event)
        return render(request, 'event/update_event.html', {'form': form})
# is_event_organizer dash
@login_required()
def event_organizer_dash(request):
    if request.user.is_event_organizer:
        event_list = Event.objects.filter(user=request.user)
        tickets = Ticket.objects.filter(event_name__user=request.user)
        history = History.objects.filter(user=request.user)
        return render(request, 'event/my_event.html', {'event_list': event_list,'tickets':tickets,'history':history})
    else:
        tickets = Ticket.objects.filter(ticket_holder=request.user)
        history = History.objects.filter(user=request.user).order_by('-created')
        return render(request,'event/ticket_dashboard.html',{'tickets':tickets,'history':history})
@login_required()
def delete_event(request,event_id):
    if request.user.is_event_organizer:
        event = get_object_or_404(Event,id = event_id,user=request.user)
        event.delete()
        return redirect('dash')

@login_required
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    User = get_user_model()  # Get the User model dynamically
    user = request.user  # Assuming request.user is an instance of your User model

    if user.amount >= event.price:
        if not event.available_tickets == 0:
            user.amount -= event.price  # Deduct the price from user's amount
            user.save()  # Save the user's updated amount
            History.objects.create(user=user, body=f"Bought ticket for {event.event_name}")

            # Add the deducted price to the event organizer
            event_organizer = event.user  # Assuming you have a 'user' field in your Event model representing the organizer
            event_organizer.amount += event.price
            event_organizer.save()
            History.objects.create(user=event.user, body=f"Received payment for ticket: {event.event_name}")

            ticket = Ticket.objects.create(event_name=event, ticket_holder=user, ticket_type=event.ticket_type)
            event.available_tickets -= 1
            event.save()
            messages.success(request, 'You have successfully purchased a ticket for the event.')
            return redirect('event_list')
        else:
            messages.error(request, "We're sorry, but there are no tickets available for this event at the moment.")
            return redirect('event_list')
    else:
        messages.error(request, "You don't have sufficient funds to buy a ticket.")
        return redirect('event_list')
@login_required
def allow_resale_tickets(request,ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.allow_resale = True
    ticket.save()
    History.objects.create(user=ticket.ticket_holder, body=f"Allowed to resale ticket: {ticket.event_name}")
    messages.success(request, 'Ticket resale has been allowed successfully.')
    return redirect('dash')
@login_required
def remove_from_resale_tickets(request,ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.allow_resale = False
    ticket.save()
    History.objects.create(user=ticket.ticket_holder, body=f"Allowed to resale ticket: {ticket.event_name}")
    messages.success(request, 'Ticket resale has been remove from resale.')
    return redirect('dash')
@login_required
def resale_ticket(request, ticket_id):
    User = get_user_model()
    user = request.user
    ticket = get_object_or_404(Ticket, id=ticket_id)
    print(ticket.ticket_holder)
    if user.amount >= ticket.event_name.price:
        user.amount -= ticket.event_name.price
        user.save()
        History.objects.create(user=user, body=f"Bought ticket for {ticket.event_name}")

        ticket_holder = ticket.ticket_holder
        ticket_holder.amount += ticket.event_name.price
        ticket_holder.save()
        History.objects.create(user=ticket_holder, body=f"Received payment for ticket: {ticket.event_name}")

        ticket.ticket_holder = user
        ticket.allow_resale = False
        ticket.save()
        messages.success(request, 'You have successfully purchased a ticket for the event.')
        return redirect('event_details', ticket.event_name.id)
    else:
        messages.error(request, "You don't have sufficient funds to buy a ticket.")
        return redirect('event_details', ticket.event_name.id)
# from django.http import JsonResponse
# @login_required()
# def create_event(request):
#     form = EventForm()
#     return render(request,'event/create_event.html',{'form': form})


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.core.files import File
#
# @api_view(['POST'])
# def react_api(request):
#     if request.method == 'POST':
#         # Extract data from the POST request
#         get_user = request.data.get('user')
#         user = get_object_or_404(Account,username=get_user)
#         event_name = request.data.get('event_name')
#         description = request.data.get('description')
#         image = request.FILES.get('image')
#         ticket_type = request.data.get('ticket_type')
#         price = request.data.get('price')
#         available_tickets = request.data.get('available_tickets')
#
#         event = Event.objects.create(user=user,event_name=event_name,description=description,image=image,ticket_type=ticket_type,price=price,available_tickets=available_tickets)
#
#         # Return a JSON response indicating success
#         return Response({'message': 'Data received successfully'}, status=status.HTTP_201_CREATED)
#     else:
#         # Return a JSON response with an error message if the request method is not POST
#         return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

