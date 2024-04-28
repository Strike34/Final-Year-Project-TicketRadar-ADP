from django.urls import path
from . import views
urlpatterns = [
    path('event/',views.event_list,name='event_list'),
    path('event/<int:id>/',views.event_details,name='event_details'),
    path('create-event/',views.create_event,name='create_event'),
    path('dashboard/',views.event_organizer_dash,name='dash'),
    path('update-event/<int:id>/',views.update_event,name='update_event'),
    path('delete/<int:event_id>/',views.delete_event),
    path('buy-ticket/<int:event_id>/',views.buy_ticket),
    path('resale-ticket/<int:ticket_id>/',views.resale_ticket),
    path('allow-resale/<int:ticket_id>/',views.allow_resale_tickets),
    path('cancel-resale/<int:ticket_id>/', views.remove_from_resale_tickets),
]