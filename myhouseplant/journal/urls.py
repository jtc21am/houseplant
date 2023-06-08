from django.urls import path
from . import views
from .views import PlantListView, PlantDetailView, PlantCreateView, PlantUpdateView, PlantDeleteView, EntryCreateView, ChoosePlantView, WaterAllPlantsView, plant_of_the_week

urlpatterns = [
    # Route for the plant of the week
    path('', plant_of_the_week, name='plant_week'),

    # Route for the home page that lists all user's plants
    path('journal-home', PlantListView.as_view(), name='journal-home'),

    # Route for the about page
    path('about/', views.about, name='journal-about'),

    # Route for plant detail view
    # Uses the plant's primary key (pk) to identify the specific plant
    path('plant/<int:pk>/', PlantDetailView.as_view(), name='plant-detail'),

    # Route for updating a plant
    # Uses the plant's primary key (pk) to identify the specific plant
    path('plant/<int:pk>/update/', PlantUpdateView.as_view(), name='plant-update'),

    # Route for deleting a plant
    # Uses the plant's primary key (pk) to identify the specific plant
    path('plant/<int:pk>/delete/', PlantDeleteView.as_view(), name='plant-delete'),

    # Route for creating a new plant
    path('plant/new/', PlantCreateView.as_view(), name='plant-create'),

    # Route for creating a new journal entry for a plant
    # Uses the plant's primary key (pk) to identify the specific plant
    path('plant/<int:pk>/entry/new/', EntryCreateView.as_view(), name='entry-create'),

    # Route for choosing a plant for a journal entry
    path('choose-plant/', ChoosePlantView.as_view(), name='choose-plant'),

    # Route for watering all plants
    path('plants/water-all/', WaterAllPlantsView.as_view(), name='water-all-plants'),

    # Route for the plant of the week
    path('plantoftheweek/', plant_of_the_week, name='plant_week'),

    # Route for the plant of the week
    path('planttechnology/', views.tech, name='plant_technology'),


]
