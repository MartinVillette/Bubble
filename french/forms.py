from django import forms

class QuoteForm(forms.Form):
    AUTHOR = [
        ('Virgile', 'Virgile'),
        ('Simone Weil', 'Simone Weil'),
        ('Michel Vinaver', 'Michel Vinaver'),
    ]
    
    quote = forms.CharField(widget=forms.Textarea())
    author = forms.CharField(widget=forms.Select(choices=AUTHOR))
    page = forms.CharField(required=False)