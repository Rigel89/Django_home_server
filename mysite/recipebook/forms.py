from django.forms import ModelForm
from recipebook.models import Recipe, CookingMode, Step, CookingStep
from django import forms
from django.core import validators


# Create the form class.
class recipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description','mode', 'owner']

class cookingModeForm(ModelForm):
    class Meta:
        model = CookingMode
        fields = '__all__'

class stepForm(ModelForm):
    class Meta:
        model = Step
        fields = '__all__'

class cookingStepForm1(ModelForm):
    class Meta:
        model = CookingStep
        fields = '__all__'
class cookingStepForm2(ModelForm):
    step = forms.CharField(
        max_length=200, 
        help_text='Enter a short step description.',
        validators=[validators.MinLengthValidator(2, "Make must be greater than 1 character")],
        )
    class Meta:
        model = CookingStep
        fields = ['recipe', 'step_number']

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
