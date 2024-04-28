# Import necessary modules from Django and Python's standard library
from django.db import models
from account.models import Account
import uuid

# Define the choices for the event types
EVENT_TYPES = [
    ('Normal', 'Normal'),
    ('VIP', 'VIP'),
]

# Define the Event model
class Event(models.Model):
    # Each event is associated with a user (Account)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    # The name of the event
    event_name = models.CharField(max_length=100)
    # The description of the event
    description = models.TextField()
    # The image associated with the event
    image = models.ImageField(upload_to='event_images/', blank=False, null=False)
    # The type of the event (Normal or VIP)
    ticket_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    # The number of available tickets for the event
    available_tickets = models.IntegerField(default=50)
    # The price of the event
    price = models.IntegerField(blank=True, null=True)
    # The date and time when the event was created
    created = models.DateTimeField(auto_now_add=True)
    # The date and time when the event was last updated
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Return the name of the event when the model is converted to a string
        return self.event_name

# Define the Ticket model
class Ticket(models.Model):
    # The unique reference number of the ticket
    reference_number = models.CharField(max_length=100, unique=True)
    # The event associated with the ticket
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_ticket')
    # The type of the ticket (Normal or VIP)
    ticket_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    # The holder of the ticket
    ticket_holder = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name='my_tickets')
    # Whether the ticket is allowed to be resold
    allow_resale = models.BooleanField(default=False)
    # The date and time when the ticket was created
    created = models.DateTimeField(auto_now_add=True)
    # The date and time when the ticket was last updated
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Return a string representation of the ticket
        return f"{self.ticket_holder}'s {self.ticket_type} ticket for {self.event_name}"

    def save(self, *args, **kwargs):
        # If the ticket doesn't have a reference number, generate a unique one
        if not self.reference_number:
            self.reference_number = str(uuid.uuid4())[:8]
        # Call the save method of the superclass
        super().save(*args, **kwargs)

# Define the History model
class History(models.Model):
    # The user associated with the history
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # The body of the history
    body = models.CharField(max_length=250, blank=True)
    # The date and time when the history was created
    created = models.DateTimeField(auto_now_add=True)
    # The date and time when the history was last updated
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Return a string representation of the history
        return f'{self.user} | {self.body}'