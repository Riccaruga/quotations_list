from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = '__all__'
        widgets = {
            'additional_requirements': forms.Textarea(attrs={'rows': 4}),
            'attachment': forms.FileInput(attrs={
                'class': 'file-upload-input',
                'onchange': 'updateFileName(this)'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make file field optional
        self.fields['attachment'].required = False
