from django.db.models.signals import post_save
from .models import Entry, Plant # entry is the sender
from django.dispatch import receiver # need to create a receiver
from django.utils import timezone

@receiver(post_save, sender=Entry)
def save_profile(sender, instance, **kwargs):
    # Execute this function every time an Entry object is saved

    # Check if the Entry's 'watered' field is set to "Y"
    if instance.watered == "Y":
        # Update the 'last_watered' field of the associated Plant object with the current time
        instance.plant.last_watered = str(timezone.now())
        instance.plant.save(update_fields=['last_watered'])

    # Check if the Entry's 'repotted' field is set to "Y"
    if instance.repotted == "Y":
        # Update the 'last_repotted' field of the associated Plant object with the current time
        instance.plant.last_repotted = str(timezone.now())
        instance.plant.save(update_fields=['last_repotted'])

    # Check if the Entry's 'fertilized' field is set to "Y"
    if instance.fertilized == "Y":
        # Update the 'last_fertilized' field of the associated Plant object with the current time
        instance.plant.last_fertilized = str(timezone.now())
        instance.plant.save(update_fields=['last_fertilized'])

    # Check if the Entry's 'treated' field is set to "Y"
    if instance.treated == "Y":
        # Update the 'last_treated' field of the associated Plant object with the current time
        instance.plant.last_treated = str(timezone.now())
        instance.plant.save(update_fields=['last_treated'])
