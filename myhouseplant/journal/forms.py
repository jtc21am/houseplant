```python
from django import forms
from django.forms.widgets import FileInput
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from image_cropping import ImageCropWidget
from .models import Entry, Plant

class EntryCreateForm(forms.ModelForm):
    """
    Form for creating a new entry.
    It includes fields for plant, note, and various actions performed on the plant (watered, fertilized, repotted, treated).
    The 'plant' field is hidden as it is automatically set based on the context.
    """

    class Meta:
        model = Entry
        fields = ['plant', 'note', 'watered', 'fertilized', 'repotted', 'treated']
        widgets = {
            'plant': forms.HiddenInput,
        }

class EntryWaterForm(forms.ModelForm):
    """
    Form for updating the watered field of an entry.
    It includes fields for the plant and the watered date.
    Both fields are hidden as they are automatically set based on the context.
    """

    class Meta:
        model = Entry
        fields = ['plant', 'watered']
        widgets = {
            'plant': forms.HiddenInput,
            'watered': forms.HiddenInput,
        }

class PlantCreateForm(forms.ModelForm):
    """
    Form for creating a new plant.
    It includes fields for the plant's name, scientific name, origin (grown from), location, purchase date, watering schedule, image, and cropping coordinates.
    The 'schedule' field provides help text to guide the user on how to enter the number of days between waterings.
    The 'location' field provides placeholder text as an example of how to enter the location.
    The 'image' field provides help text indicating the maximum file size and a warning that the image will be cropped to a square.
    The 'clean_image()' method performs custom validation to ensure the uploaded image meets the specified criteria.
    """

    def __init__(self, *args, **kwargs):
        super(PlantCreateForm, self).__init__(*args, **kwargs)
        self.fields['schedule'].help_text = "Enter the number of days between waterings <i>(e.g.  7)</i>"
        self.fields['location'].help_text = "<i>(e.g.  Kitchen)</i>"
        self.fields['image'].help_text = "Max file size: 5 MB<br> WARNING: This image will be cropped to a square"

    def clean_image(self):
        """
        Custom validation for the image field.
        It checks the file type, size, and ensures it does not exceed the maximum allowed size.
        """
        image = self.cleaned_data['image']
        try:
            content_type = image.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if image.size > int(settings.MAX_UPLOAD_SIZE):
                    raise forms.ValidationError(('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(image.size)))
            else:
                raise forms.ValidationError('File type is not supported')
            return image
        except:
            return image

    class Meta:
        model = Plant
        fields = ['name', 'scientific', 'grown_from', 'location', 'bought', 'schedule', 'image', 'cropping']
        widgets = {
            'bought': forms.SelectDateWidget,
            'image': FileInput,
        }

class SoilMoistureReadingForm(forms.Form):
    """
    Form for capturing soil moisture reading.
    It includes fields for selecting an existing plant and the moisture level.
    """

    plant = forms.ModelChoiceField(queryset=Plant.objects.all())
    moisture_level = forms.FloatField()