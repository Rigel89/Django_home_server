from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
from django.contrib.auth.models import User
from django.conf import settings

class Recipe(models.Model):
    name = models.CharField(
            max_length=50, 
            help_text='Enter a recipe (e.g. Pizza)',
            validators=[MinLengthValidator(2, "Recipe name must be greater than 2 character")],
            unique=True
    )
    description = models.CharField(max_length=300, null= True, blank=True)
    mode = models.ManyToManyField(
            'CookingMode',
            help_text='Select one or more cooking modes.',
            )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    step = models.ManyToManyField(
                'step',
                through='CookingStep',
                )
    # Shows up in the admin list
    def __str__(self):
        return self.name

class CookingMode(models.Model):
    name = models.CharField(
            max_length=10,
            unique=True,
            help_text='Enter a cooking mode (e.g. Oven)',
            validators=[MinLengthValidator(2, "Make must be greater than 1 character")],
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Step(models.Model):
    step = models.CharField(
            max_length=200, 
            help_text='Enter a short step description.',
            validators=[MinLengthValidator(2, "Make must be greater than 1 character")],
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.step

class CookingStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False)
    step = models.ForeignKey(Step, on_delete=models.CASCADE, null=False)
    step_number = models.PositiveSmallIntegerField()
    class Meta():
        constraints = [
                models.UniqueConstraint('recipe', 'step_number', name='recipe_stepnumber', violation_error_message="recipe and step number cant be repeated")
                ]
    def __str__(self):
        """String for representing the Model object."""
        return str(self.recipe) + str(self.step) + str(self.step_number)
    

