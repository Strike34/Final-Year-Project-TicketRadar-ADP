from django.contrib import admin
from .models import Event,Ticket,History
# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    pass
