# Import the path function from django.urls module
from django.urls import path
# Import the views from the current directory
from . import views

# Define the URL patterns for the application
urlpatterns = [
    # Map the URL 'event/' to the event_list view
    path('event/',views.event_list,name='event_list'),
    # Map the URL 'event/<int:id>/' to the event_details view, passing the id as a parameter
    path('event/<int:id>/',views.event_details,name='event_details'),
    # Map the URL 'create-event/' to the create_event view
    path('create-event/',views.create_event,name='create_event'),
    # Map the URL 'dashboard/' to the event_organizer_dash view
    path('dashboard/',views.event_organizer_dash,name='dash'),
    # Map the URL 'update-event/<int:id>/' to the update_event view, passing the id as a parameter
    path('update-event/<int:id>/',views.update_event,name='update_event'),
    # Map the URL 'delete/<int:event_id>/' to the delete_event view, passing the event_id as a parameter
    path('delete/<int:event_id>/',views.delete_event),
    # Map the URL 'buy-ticket/<int:event_id>/' to the buy_ticket view, passing the event_id as a parameter
    path('buy-ticket/<int:event_id>/',views.buy_ticket),
    # Map the URL 'resale-ticket/<int:ticket_id>/' to the resale_ticket view, passing the ticket_id as a parameter
    path('resale-ticket/<int:ticket_id>/',views.resale_ticket),
    # Map the URL 'allow-resale/<int:ticket_id>/' to the allow_resale_tickets view, passing the ticket_id as a parameter
    path('allow-resale/<int:ticket_id>/',views.allow_resale_tickets),
    # Map the URL 'cancel-resale/<int:ticket_id>/' to the remove_from_resale_tickets view, passing the ticket_id as a parameter
    path('cancel-resale/<int:ticket_id>/', views.remove_from_resale_tickets),
]