from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormMixin, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views import View
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.db import transaction
from django.contrib import messages
from .forms import EntryCreateForm, EntryWaterForm, PlantCreateForm
from .models import Plant, Entry
import random

import random

def plant_of_the_week(request):
    # Retrieve all plants from the database
    plants = Plant.objects.all()
    # Choose a random plant from the list
    random_plant = random.choice(plants)
    # Prepare the context data to be passed to the template
    context = {
        'plants': plants,
        'random_plant': random_plant
    }
    # Render the 'plant_week.html' template with the provided context
    return render(request, 'journal/plant_week.html', context)

def about(request):
    """ Show about page explaining app purpose. """
    # Render the 'about.html' template with the provided context
    return render(request, 'journal/about.html', {'title': 'About'})

class PlantListView(ListView):
    """ List all of user's plants on home page if they are logged in. """
    model = Plant
    template_name = 'journal/home.html'
    context_object_name = 'plants'
    ordering = ['location', 'name']

    def get_queryset(self):
        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            # If authenticated, filter plants by owner and order them by location and name
            return self.model.objects.filter(owner=self.request.user).order_by('location', 'name')
        else:
            # If not authenticated, retrieve the user with username 'asha' as a fallback
            asha = User.objects.filter(username='asha').first()
            # Return all plants owned by 'asha' and order them by location and name
            return super().get_queryset().filter(owner=asha)


class PlantDetailView(DetailView):
    """ Show details of plant and handle 'Water Me!' button submission. """
    model = Plant
    template_name = 'journal/plant_detail.html'

    def get_success_url(self):
        # Specify the URL to redirect to after a successful form submission
        return reverse('plant-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = EntryWaterForm(request.POST)

        if 'water_single' in request.POST:
            if form.is_valid():
                # Update the last_watered field of the plant with the current time
                self.object.last_watered = timezone.now()
                self.object.save()
                # Display a success message to the user
                messages.success(request, f'Your {self.object.name} has been watered!')
        return self.get(request, *args, **kwargs)

    
class WaterAllPlantsView(View):
    def post(self, request, *args, **kwargs):
        # Update the last_watered field of all plants to the current time
        Plant.objects.update(last_watered=timezone.now())
        # Display a success message to the user
        messages.success(request, 'All plants have been watered!')
        # Redirect the user to the home page
        return redirect('journal-home')

    

class PlantCreateView(LoginRequiredMixin, CreateView):
    """ Create a plant and set the owner and cropping fields automatically. """
    model = Plant
    form_class = PlantCreateForm

    def form_valid(self, form):
        # Set the owner of the plant to the current user
        form.instance.owner = self.request.user
        plant = form.save()
        # Set the cropping field based on the dimensions of the uploaded image
        if plant.image.height > plant.image.width:
            form.instance.cropping = f'0,0,{plant.image.width},{plant.image.width}'
        else:
            form.instance.cropping = f'0,0,{plant.image.height},{plant.image.height}'
        return super().form_valid(form)



class PlantUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Update plant if user is the plant owner and auto set the cropping field again. """
    model = Plant
    form_class = PlantCreateForm

    def form_valid(self, form):
        # Set the owner of the plant to the current user
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        # Check if the current user is the owner of the plant being updated
        plant = self.get_object()
        if self.request.user == plant.owner:
            return True
        return False

    def post(self, request, **kwargs):
        plant = self.get_object()
        request.POST = request.POST.copy()
        # Set the cropping field based on the dimensions of the uploaded image
        if plant.image.height > plant.image.width:
            request.POST['cropping'] = f'0,0,{plant.image.width},{plant.image.width}'
        else:
            request.POST['cropping'] = f'0,0,{plant.image.height},{plant.image.height}'
        return super(PlantUpdateView, self).post(request, **kwargs)

class PlantDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete a plant if user is plant owner and redirect to home page with message. """
    model = Plant

    def test_func(self):
        # Check if the current user is the owner of the plant being deleted
        plant = self.get_object()
        if self.request.user == plant.owner:
            return True
        return False
    
    success_url = '/'
    success_message = 'Your plant was successfully deleted.'

    def delete(self, request, *args, **kwargs):
        # Display a success message to the user
        messages.success(self.request, self.success_message)
        return super(PlantDeleteView, self).delete(request, *args, **kwargs)
    

class EntryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """ Create a journal entry with auto-populated plant field. """
    form_class = EntryCreateForm
    model = Entry

    def get_success_url(self):
        # Specify the URL to redirect to after a successful form submission
        return reverse('plant-detail', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        # Set the plant field of the journal entry to the selected plant
        form.instance.plant = Plant.objects.get(id=self.kwargs.get('pk'))
        return super(EntryCreateView, self).form_valid(form)

    def get_initial(self):
        # Get the plant object based on the provided pk and set it as the initial data for the form
        plant = Plant.objects.get(pk=self.kwargs['pk'])
        return {'plant': plant}

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView, self).get_context_data(**kwargs)
        # Pass the plant object to the template for additional context
        context['plant'] = Plant.objects.get(pk=self.kwargs['pk'])
        return context

    def test_func(self):
        # Check if the current user is the owner of the plant associated with the journal entry
        if self.request.user == Plant.objects.get(pk=self.kwargs['pk']).owner:
            return True
        return False
    
class ChoosePlantView(View):
    def get(self, request):
        # Retrieve all plants from the database
        plants = Plant.objects.all()
        context = {'plants': plants}
        # Render the 'choose_plant.html' template with the provided context
        return render(request, 'journal/choose_plant.html', context)

def error_403(request, exception):
    """ Show custom 403 error page. """
    data = {}
    # Render the '403.html' template with the provided context
    return render(request,'journal/403.html', data)

def error_404(request, exception):
    """ Show custom 404 error page. """
    data = {}
    # Render the '404.html' template with the provided context
    return render(request,'journal/404.html', data)

def error_500(request, exception):
    """ Show custom 500 error page. """
    data = {}
    # Render the '500.html' template with the provided context
    return render(request,'journal/500.html', data)
