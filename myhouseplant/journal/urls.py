from django.urls import path
from . import views
from .views import PlantListView, PlantDetailView, PlantCreateView, PlantUpdateView, PlantDeleteView, EntryCreateView, ChoosePlantView, WaterAllPlantsView, plant_of_the_week

urlpatterns = [
    path('', plant_of_the_week, name='plant_week'),
    path('journal-home', PlantListView.as_view(), name='journal-home'),
    path('about/', views.about, name='journal-about'),
    # we will do reverse lookups on this route so we don't want to name it 
    # something generic like home bc then it will collide with other apps
    path('plant/<int:pk>/', PlantDetailView.as_view(), name='plant-detail'),
    path('plant/<int:pk>/update/', PlantUpdateView.as_view(), name='plant-update'),
    path('plant/<int:pk>/delete/', PlantDeleteView.as_view(), name='plant-delete'),
    path('plant/new/', PlantCreateView.as_view(), name='plant-create'),
    path('plant/<int:pk>/entry/new/', EntryCreateView.as_view(), name='entry-create'),
    path('choose-plant/', ChoosePlantView.as_view(), name='choose-plant'),
    path('plants/water-all/', WaterAllPlantsView.as_view(), name='water-all-plants'),
    path('plantoftheweek/', plant_of_the_week, name='plant_week'),

]