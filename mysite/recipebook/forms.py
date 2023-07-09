from django.forms import ModelForm
from recipebook.models import Recipe, CookingMode
from django import forms
from django.core import validators


# Create the form class.
class recipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

class cookingModeForm(ModelForm):
    class Meta:
        model = CookingMode
        fields = '__all__'

class BasicForm(forms.Form):
    name = forms.CharField(
            max_length=50, 
            help_text='Enter a recipe name (e.g. Pizza) \n',
            validators=[validators.MinLengthValidator(4, "Make must be greater than 3 character")])
    mode = forms.CharField(
            max_length=10,
            help_text='Enter the cooking mode (e.g. Owen, wok....) \n',
            validators=[validators.MinLengthValidator(2, "Nickname must be greater than 3 character")]
    )
    comments = forms.CharField(max_length=300)
