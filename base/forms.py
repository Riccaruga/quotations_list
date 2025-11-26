from django import forms
from .models import Quote, LaserCuttingSpec, PressBrakeSpec, TubeLaserSpec

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        # Explicitly define fields for safety, excluding one-to-one related fields
        fields = [
            'title', 
            'manager', 
            'client', 
            'machine_type', 
            'attachment', 
            'completed', 
            'additional_requirements', 
            'user' 
        ]
        widgets = {
            'additional_requirements': forms.Textarea(attrs={'rows': 4}),
            # The attachment widget is manually handled in the template, so no complex widget needed here.
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make file field optional
        self.fields['attachment'].required = False
        # Hide the 'user' field, it will be set in the view
        if 'user' in self.fields:
             self.fields['user'].widget = forms.HiddenInput()


# --- Specification Forms ---

class LaserCuttingForm(forms.ModelForm):
    class Meta:
        model = LaserCuttingSpec
        # CRITICAL: Exclude the FK field so it can be set in the view after Quote is saved
        exclude = ['quote'] 

class PressBrakeForm(forms.ModelForm):
    class Meta:
        model = PressBrakeSpec
        # CRITICAL: Exclude the FK field so it can be set in the view after Quote is saved
        exclude = ['quote']
        widgets = {
            'CNC_type': forms.Select(attrs={'class': 'form-control'}),
            'axis_type': forms.Select(attrs={'class': 'form-control'})
        }

class TubeLaserForm(forms.ModelForm):
    class Meta:
        model = TubeLaserSpec
        # CRITICAL: Exclude the FK field so it can be set in the view after Quote is saved
        exclude = ['quote']
        widgets = {
            'loading_type': forms.Select(attrs={'class': 'form-control'})
        }