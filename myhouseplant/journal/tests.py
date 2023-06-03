from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db import transaction
from .forms import EntryCreateForm, EntryWaterForm, PlantCreateForm
from .models import Plant, Entry
import random


class PlantViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a test plant
        self.plant = Plant.objects.create(name='Test Plant', location='Kitchen', owner=self.user)

    def test_plant_list_view_authenticated(self):
        # Create a client and log in the user
        client = Client()
        client.login(username='testuser', password='testpassword')

        # Send a GET request to the plant list view
        response = client.get(reverse('journal-home'))

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the expected plant
        self.assertContains(response, self.plant.name)

    def test_plant_list_view_unauthenticated(self):
        # Create a client
        client = Client()

        # Send a GET request to the plant list view
        response = client.get(reverse('journal-home'))

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response does not contain the plant (since it requires authentication)
        self.assertNotContains(response, self.plant.name)

    def test_plant_detail_view(self):
        # Create a client and log in the user
        client = Client()
        client.login(username='testuser', password='testpassword')

        # Send a GET request to the plant detail view
        url = reverse('plant-detail', kwargs={'pk': self.plant.pk})
        response = client.get(url)

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the expected plant details
        self.assertContains(response, self.plant.name)
        self.assertContains(response, self.plant.location)

    def test_plant_create_view(self):
        # Create a client and log in the user
        client = Client()
        client.login(username='testuser', password='testpassword')

        # Send a GET request to the plant create view
        response = client.get(reverse('plant-create'))

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Send a POST request to the plant create view with form data
        data = {
            'name': 'New Plant',
            'location': 'Living Room',
            # Add other required form fields here
        }
        response = client.post(reverse('plant-create'), data=data)

        # Check that the plant was created successfully (status code 302 - Redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the plant exists in the database
        self.assertTrue(Plant.objects.filter(name='New Plant').exists())

    def test_plant_update_view(self):
        # Create a client and log in the user
        client = Client()
        client.login(username='testuser', password='testpassword')

        # Send a GET request to the plant update view
        url = reverse('plant-update', kwargs={'pk': self.plant.pk})
        response = client.get(url)

        # Check that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Send a POST request to the plant update view with form data
        data = {
            'name': 'Updated Plant',
            'location': 'Bedroom',
            # Add other required form fields here
        }
        response = client.post(url, data=data)

        # Check that the plant was updated successfully (status code 302 - Redirect)
        self.assertEqual(response.status_code, 302)

        # Refresh the plant instance from the database
        self.plant.refresh_from_db()

        # Check that the plant has the updated values
        self.assertEqual(self.plant.name, 'Updated Plant')
        self.assertEqual(self.plant.location, 'Bedroom')

    def test_plant_delete_view(self):
        # Create a client and log in the user
        client = Client()
        client.login(username='testuser', password='testpassword')

        # Send a POST request to the plant delete view
        url = reverse('plant-delete', kwargs={'pk': self.plant.pk})
        response = client.post(url)

        # Check that the plant was deleted successfully (status code 302 - Redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the plant no longer exists in the database
        self.assertFalse(Plant.objects.filter(pk=self.plant.pk).exists())
