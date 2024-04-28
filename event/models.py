from django.db import models
from account.models import Account
import uuid

EVENT_TYPES = [
    ('Normal', 'Normal'),
    ('VIP', 'VIP'),
]
class Event(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/',blank=False, null=False)
    ticket_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    available_tickets = models.IntegerField(default=50)
    price = models.IntegerField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.event_name

class Ticket(models.Model):
    reference_number = models.CharField(max_length=100, unique=True)
    event_name = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='event_ticket')
    ticket_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    ticket_holder= models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True,related_name='my_tickets')
    allow_resale = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.ticket_holder}'s {self.ticket_type} ticket for {self.event_name}"

    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

class History(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    body = models.CharField(max_length=250,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.user} | {self.body}'
