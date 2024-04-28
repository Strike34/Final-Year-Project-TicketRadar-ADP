from django.test import TestCase
from django.urls import reverse
from .models import Event

class EventTestCase(TestCase):
    def setUp(self):
        # Create test data
        self.event1 = Event.objects.create(event_name='Test Event 1', image='image.png',description='Description 1', ticket_type='Normal', price=10)
        self.event2 = Event.objects.create(event_name='Test Event 2', image='image.png',description='Description 2', ticket_type='VIP', price=20)

        self.assertEqual(self.event1.event_name,'Test Event 1')
        self.assertEqual(self.event1.image,'image.png')
        self.assertEqual(self.event1.description,'Description 1')
        self.assertEqual(self.event1.ticket_type,'Normal')
        self.assertEqual(self.event1.price,10)

    def test_event_list_view(self):
        # Test event list view
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event1.event_name)
        self.assertContains(response, self.event2.event_name)

    def test_event_detail_view(self):
        # Test event detail view
        response = self.client.get(reverse('event_details', args=[self.event1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event1.event_name)
        self.assertContains(response, self.event1.description)

    def test_event_creation(self):
        # Test event creation
        new_event_data = {'event_name': 'Test Event 2', 'description': 'Description 2','image':'image.png' ,'ticket_type': 'VIP', 'price': 20}
        response = self.client.post(reverse('create_event'), data=new_event_data)
        self.assertEqual(response.status_code, 302)  # 302: Redirect after successful POST

        # Check the newly created event
        new_event = Event.objects.latest('id')
        self.assertEqual(new_event.event_name, new_event_data['event_name'])
        self.assertEqual(new_event.description, new_event_data['description'])
        self.assertEqual(new_event.image, new_event_data['image'])
        self.assertEqual(new_event.ticket_type, new_event_data['ticket_type'])
        self.assertEqual(new_event.price, new_event_data['price'])

