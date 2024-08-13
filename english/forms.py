from django import forms
from users.models import Group

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, group):
        return group.name

class LessonForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    groups = CustomMMCF (
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class CardForm(forms.Form):
    text1 = forms.CharField(required=False)
    text2 = forms.CharField(required=False)

