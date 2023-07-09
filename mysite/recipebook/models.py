from django.db import models
from django.core.validators import MinLengthValidator

class Recipe(models.Model):
    name = models.CharField(
            max_length=50, 
            help_text='Enter a recipe (e.g. Pizza)',
            validators=[MinLengthValidator(2, "Recipe name must be greater than 2 character")],
#            default='Pizza'
    )
    description = models.CharField(max_length=300)
    mode = models.ManyToManyField('cookingMode', default=None)

    # Shows up in the admin list
    def __str__(self):
        return self.name

class CookingMode(models.Model):
    name = models.CharField(
            max_length=10, 
            help_text='Enter a cooking mode (e.g. Oven)',
            validators=[MinLengthValidator(2, "Make must be greater than 1 character")],
#            default='Oven'
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name


'''class recipe(models.Model):
    name = models.CharField(
            max_length=50, 
            help_text='Enter a recipe name (e.g. Pizza)',
            validators=[MinLengthValidator(2, "Make must be greater than 3 character")]
    )
    mode = models.ForeignKey('cookingMode', on_delete=models.SET_NULL, null=True)
    #step = models.ForeignKey('cookingMode', on_delete=models.SET_NULL, null=True)
    comments = models.CharField(max_length=300)

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class cookingMode(models.Model):
    mode = models.CharField(
            max_length=10,
            help_text='Enter the cooking mode (e.g. Owen, wok....)',
            validators=[MinLengthValidator(2, "Nickname must be greater than 2 character")]
    )

    # Shows up in the admin list
    def __str__(self):
        return self.mode'''

