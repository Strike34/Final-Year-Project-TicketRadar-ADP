from django.shortcuts import render,redirect,get_object_or_404
from .models import Event,Ticket,History
from django.contrib import messages
from account.models import Account
from django.contrib.auth import get_user_model
from .forms import EventForm
from django.contrib.auth.decorators import login_required
# Create your views here.
# Import necessary modules
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Event, Ticket, History
from .forms import EventForm

# Function to display a list of events
def event_list(request):
    # Get the search query from the request
    search_query = request.GET.get('event')
    # If there is a search query, filter the events by the query
    if search_query:
        event_list = Event.objects.filter(event_name__contains=search_query)
        # Render the event list template with the filtered events
        return render(request, 'event/event_list.html', {'event_list': event_list})
    # If there is no search query, get all events
    event_list = Event.objects.all()
    # Render the event list template with all events
    return render(request,'event/event_list.html',{'event_list':event_list})

# Function to display the details of an event
def event_details(request,id):
    # Get the event by its id
    event = Event.objects.get(id=id)
    # Get the tickets for the event that are allowed to be resold
    tickets = event.event_ticket.filter(allow_resale=True)
    # Render the event details template with the event and its tickets
    return render(request, 'event/event_details.html', {'event': event,'tickets':tickets})

# Function to create an event
@login_required()
def create_event(request):
    # Check if the user is an event organizer
    if request.user.is_event_organizer:
        # Create a new event form
        form = EventForm()
        # If the request method is POST, process the form data
        if request.method == 'POST':
            # Bind the form data to the form
            form = EventForm(request.POST, request.FILES)  # Need to include request.FILES for image upload
            # If the form is valid, save the form data but don't commit yet
            if form.is_valid():
                event = form.save(commit=False)  # Commit=False to delay saving to set the user field
                # Set the user field to the current user
                event.user = request.user
                # Save the event
                event.save()
                # Redirect to the event list
                return redirect('event_list')  # Assuming you have an event-detail URL
        # If the request method is not POST, render the form
        return render(request, 'event/create_event.html', {'form': form})
    # If the user is not an event organizer, redirect to the event list
    else:
        return redirect('event_list')

# Function to update an event
@login_required()
def update_event(request,id):
    # Check if the user is an event organizer
    if request.user.is_event_organizer:
        # Get the event by its id and the current user
        event = get_object_or_404(Event,id=id,user=request.user)
        # If the request method is POST, process the form data
        if request.method == 'POST':
            # Bind the form data to the form and the event instance
            form = EventForm(request.POST, request.FILES,instance=event)
            # If the form is valid, save the form data but don't commit yet
            if form.is_valid():
                event = form.save(commit=False)  # Commit=False to delay saving to set the user field
                # Set the user field to the current user
                event.user = request.user
                # Save the event
                event.save()
        # If the request method is not POST, create a form with the event instance
        else:
            form = EventForm(instance=event)
        # Render the update event template with the form
        return render(request, 'event/update_event.html', {'form': form})

# Function to display the event organizer dashboard
@login_required()
def event_organizer_dash(request):
    # Check if the user is an event organizer
    if request.user.is_event_organizer:
        # Get the events and tickets by the current user
        event_list = Event.objects.filter(user=request.user)
        tickets = Ticket.objects.filter(event_name__user=request.user)
        # Get the history by the current user
        history = History.objects.filter(user=request.user)
        # Render the event organizer dashboard template with the events, tickets, and history
        return render(request, 'event/my_event.html', {'event_list': event_list,'tickets':tickets,'history':history})
    # If the user is not an event organizer, get the tickets and history by the current user
    else:
        tickets = Ticket.objects.filter(ticket_holder=request.user)
        history = History.objects.filter(user=request.user).order_by('-created')
        # Render the ticket dashboard template with the tickets and history
        return render(request,'event/ticket_dashboard.html',{'tickets':tickets,'history':history})

# Function to delete an event
@login_required()
def delete_event(request,event_id):
    # Check if the user is an event organizer
    if request.user.is_event_organizer:
        # Get the event by its id and the current user
        event = get_object_or_404(Event,id = event_id,user=request.user)
        # Delete the event
        event.delete()
        # Redirect to the dashboard
        return redirect('dash')

# Function to buy a ticket
@login_required
def buy_ticket(request, event_id):
    # Get the event by its id
    event = get_object_or_404(Event, id=event_id)
    # Get the User model dynamically
    User = get_user_model()  
    # Get the current user
    user = request.user  # Assuming request.user is an instance of your User model

    # Check if the user has enough funds to buy a ticket
    if user.amount >= event.price:
        # Check if there are available tickets for the event
        if not event.available_tickets == 0:
            # Deduct the price from the user's amount
            user.amount -= event.price  
            # Save the user's updated amount
            user.save()  
            # Create a history record for the user
            History.objects.create(user=user, body=f"Bought ticket for {event.event_name}")

            # Add the deducted price to the event organizer
            event_organizer = event.user  # Assuming you have a 'user' field in your Event model representing the organizer
            event_organizer.amount += event.price
            event_organizer.save()
            # Create a history record for the event organizer
            History.objects.create(user=event.user, body=f"Received payment for ticket: {event.event_name}")

            # Create a ticket for the event and the user
            ticket = Ticket.objects.create(event_name=event, ticket_holder=user, ticket_type=event.ticket_type)
            # Decrease the available tickets for the event by 1
            event.available_tickets -= 1
            event.save()
            # Show a success message
            messages.success(request, 'You have successfully purchased a ticket for the event.')
            # Redirect to the event list
            return redirect('event_list')
        # If there are no available tickets for the event, show an error message
        else:
            messages.error(request, "We're sorry, but there are no tickets available for this event at the moment.")
            return redirect('event_list')
    # If the user doesn't have enough funds to buy a ticket, show an error message
    else:
        messages.error(request, "You don't have sufficient funds to buy a ticket.")
        return redirect('event_list')

# Function to allow resale of tickets
@login_required
def allow_resale_tickets(request,ticket_id):
    # Get the ticket by its id
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # Allow resale of the ticket
    ticket.allow_resale = True
    ticket.save()
    # Create a history record for the ticket holder
    History.objects.create(user=ticket.ticket_holder, body=f"Allowed to resale ticket: {ticket.event_name}")
    # Show a success message
    messages.success(request, 'Ticket resale has been allowed successfully.')
    # Redirect to the dashboard
    return redirect('dash')

# Function to remove tickets from resale
@login_required
def remove_from_resale_tickets(request,ticket_id):
    # Get the ticket by its id
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # Disallow resale of the ticket
    ticket.allow_resale = False
    ticket.save()
    # Create a history record for the ticket holder
    History.objects.create(user=ticket.ticket_holder, body=f"Allowed to resale ticket: {ticket.event_name}")
    # Show a success message
    messages.success(request, 'Ticket resale has been remove from resale.')
    # Redirect to the dashboard
    return redirect('dash')

# Function to resale a ticket
@login_required
def resale_ticket(request, ticket_id):
    # Get the User model dynamically
    User = get_user_model()
    # Get the current user
    user = request.user
    # Get the ticket by its id
    ticket = get_object_or_404(Ticket, id=ticket_id)
    # Check if the user has enough funds to buy the ticket
    if user.amount >= ticket.event_name.price:
        # Deduct the price from the user's amount
        user.amount -= ticket.event_name.price
        user.save()
        # Create a history record for the user
        History.objects.create(user=user, body=f"Bought ticket for {ticket.event_name}")

        # Add the deducted price to the ticket holder
        ticket_holder = ticket.ticket_holder
        ticket_holder.amount += ticket.event_name.price
        ticket_holder.save()
        # Create a history record for the ticket holder
        History.objects.create(user=ticket_holder, body=f"Received payment for ticket: {ticket.event_name}")

        # Change the ticket holder to the user
        ticket.ticket_holder = user
        # Disallow resale of the ticket
        ticket.allow_resale = False
        ticket.save()
        # Show a success message
        messages.success(request, 'You have successfully purchased a ticket for the event.')
        # Redirect to the event details
        return redirect('event_details', ticket.event_name.id)
    # If the user doesn't have enough funds to buy the ticket, show an error message
    else:
        messages.error(request, "You don't have sufficient funds to buy a ticket.")
        return redirect('event_details', ticket.event_name.id)