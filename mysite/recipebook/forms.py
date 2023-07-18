from django.forms import ModelForm
from recipebook.models import *
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
    #recipe = forms.ModelChoiceField(queryset=Recipe.objects.all())
    step = forms.CharField(
        max_length=200, 
        help_text='Enter a short step description.',
        validators=[validators.MinLengthValidator(2, "Make must be greater than 1 character")],
        )
    #step_number = forms.IntegerField(min_value=0)
    class Meta:
        model = CookingStep
        fields = ['recipe', 'step_number']
    field_order = ['recipe', 'step', 'step_number']

class cookingStepForm3(ModelForm):
    recipe = forms.ModelChoiceField(disabled=True, queryset=Recipe.objects)
    step = forms.ModelChoiceField(disabled=True, queryset=Step.objects)
    class Meta:
        model = CookingStep
        fields = ['recipe', 'step', 'step_number']
    field_order = ['recipe', 'step', 'step_number']

class cookingIngredientForm1(ModelForm):
    class Meta:
        model = CookingIngredient
        fields = '__all__'
    field_order = ['recipe', 'ingredient', 'amount']

class cookingIngredientForm2(ModelForm):
    #recipe = forms.ModelChoiceField(queryset=Recipe.objects.all())
    amount = forms.CharField(
            max_length=20, 
            help_text='Enter the quantity.',
            validators=[MinLengthValidator(2, "Make must be greater than 1 character")],
    )
    class Meta:
        model = CookingIngredient
        fields = ['recipe', 'ingredient']
    field_order = ['recipe', 'ingredient', 'amount']

class cookingIngredientForm3(ModelForm):
    recipe = forms.ModelChoiceField(disabled=True, queryset=Recipe.objects)
    ingredient = forms.ModelChoiceField(disabled=False, queryset=Ingredient.objects)
    amount = forms.ModelChoiceField(disabled=False, queryset=Amount.objects)
    class Meta:
        model = CookingIngredient
        fields = ['recipe', 'ingredient', 'amount']
    field_order = ['recipe', 'ingredient', 'amount']

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
