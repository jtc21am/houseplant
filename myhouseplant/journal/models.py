import os

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime
from image_cropping.fields import ImageRatioField
from PIL import Image, ExifTags

def user_directory_path(instance, filename):
    # This function determines the path where the uploaded file will be stored
    # It will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.owner.id, filename)

class Plant(models.Model):
    # Choices for the 'grown_from' field
    GROWN_FROM_CHOICES = [
        ('SEED', 'Seed'),
        ('SEEDLING', 'Seedling'),
        ('CUTTING', 'Cutting'),
        ('FULLSIZE', 'Full Size'),
        ('BULB', 'Bulb'),
    ]

    # Choices for the 'location' field
    LOCATION_CHOICES = [
        ('KITCHEN', 'Kitchen'),
        ('LIVING RM', 'Living Room'),
        ('MUDROOM', 'Mud Room'),
        ('FR STEPS', 'Front Steps'),
        ('BK DECK', 'Back Deck'),
        ('BK GARDEN', 'Back Garden'),
        ('FR GARDEN', 'Front Garden'),
    ]

    name = models.CharField(max_length=100)
    scientific = models.CharField(max_length=150, default='')
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default='Mud Room')
    grown_from = models.CharField(max_length=100, choices=GROWN_FROM_CHOICES, default='Full Size')
    bought = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', blank=True, upload_to=user_directory_path)
    cropping = ImageRatioField('image', '300x300') # size is "width x height"
    schedule = models.PositiveIntegerField(default=1, blank=1)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    last_watered = models.DateTimeField(default=timezone.now)
    last_fertilized = models.DateTimeField(null=True, blank=True)
    last_repotted = models.DateTimeField(null=True, blank=True)
    last_treated = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # This function is called before saving the Plant object
        # It updates the cropping field to a fixed value of '0,0,300,300'

        self.cropping = '0,0,300,300'

        super().save(*args, **kwargs) # Call the parent class's save method to save the image first

        img = Image.open(self.image.path) # Open this Plant instance's image

        try:
            # Check the image's EXIF data to determine its orientation
            image = Image.open(self.image.path)

            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break

            exif = dict(image._getexif().items())

            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)

            image.save(self.image.path)
            image.close()
        except (AttributeError, KeyError, IndexError):
            # Handle cases where the image doesn't have EXIF data
            pass

        if img.height > 300 or img.width > 300:
            if img.height > img.width:
                output_size = (300, int(img.height / (img.width / 300)))
                img.thumbnail(output_size)
                img.save(self.image.path) # Overwrite the large image
            else:
                output_size = (int(img.width / (img.height / 300)), 300)
                img.thumbnail(output_size)
                img.save(self.image.path) # Overwrite the large image

    @property
    def is_due(self):
        # Returns True if the last_watered date is due based on the schedule
        return (timezone.now() - self.last_watered).days == self.schedule

    @property
    def is_past_due(self):
        # Returns True if the last_watered date is past due based on the schedule
        return (timezone.now() - self.last_watered).days > self.schedule

    @property
    def watered_today(self):
        # Returns True if the plant has been watered within the last 16 hours and 1 day has not passed
        return (timezone.now() - self.last_watered).seconds / 60 / 60 < 16 and (timezone.now() - self.last_watered).days < 1

    def __str__(self):
        return f"{self.name} {self.id}"

    def get_absolute_url(self):
        # Returns the URL to the Plant's detail view
        return reverse('plant-detail', kwargs={'pk': self.pk})

class Entry(models.Model):
    # Choices for the 'watered', 'fertilized', 'repotted', and 'treated' fields
    YES_NO_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    note = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    watered = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    fertilized = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    repotted = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')
    treated = models.CharField(max_length=1, choices=YES_NO_CHOICES, default='N')

    def __str__(self):
        return f"{self.plant.name} {self.plant.id}: {self.note}"

    def get_absolute_url(self):
        # Returns the URL to the associated Plant's detail view
        return reverse('plant-detail', kwargs={'pk': self.plant.pk})
