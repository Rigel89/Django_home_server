from django.urls import path
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'recipebook'
urlpatterns = [
    #Home path
    path('', TemplateView.as_view(template_name='recipebook/base_menu.html'), name='menu'),
    #Recipies paths
    path('main', TemplateView.as_view(template_name='recipebook/main.html'), name='main'),
    path('example', views.example),
    path('recipe/', views.recipeView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>', views.recipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/create/', views.recipeCreate.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/update/', views.recipeUpdate.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.recipeDelete.as_view(), name='recipe_delete'),
    #Coooking Mode paths
    path('cookingmode/', views.cookingModeView.as_view(), name='cookingMode_list'),
    path('cookingmode/create/', views.cookingModeCreate.as_view(), name='cookingMode_create'),
    path('cookingmode/<int:pk>/update/', views.cookingModeUpdate.as_view(), name='cookingMode_update'),
    path('cookingmode/<int:pk>/delete/', views.cookingModeDelete.as_view(), name='cookingMode_delete'),
    #Step paths
    path('step/', views.stepView.as_view(), name='step_list'),
    path('step/create/', views.stepCreate.as_view(), name='step_create'),
    path('step/<int:pk>/update/', views.stepUpdate.as_view(), name='step_update'),
    path('step/<int:pk>/delete/', views.stepDelete.as_view(), name='step_delete'),
    #Coking Steps paths
    path('cookingstep/<int:rp>', views.cookingStepView.as_view(), name='cookingStep_list'),
    path('cookingstep/<int:rp>/create/<str:sl>', views.cookingStepCreate.as_view(), name='cookingStep_create'),
    path('cookingstep/<int:rp>/<int:pk>/update/', views.cookingStepUpdate.as_view(), name='cookingStep_update'),
    path('cookingstep/<int:rp>/<int:pk>/delete/', views.cookingStepDelete.as_view(), name='cookingStep_delete'),
    #Ingredient paths
    path('ingredient/', views.ingredientView.as_view(), name='ingredient_list'),
    path('ingredient/create/', views.ingredientCreate.as_view(), name='ingredient_create'),
    path('ingredient/<int:pk>/update/', views.ingredientUpdate.as_view(), name='ingredient_update'),
    path('ingredient/<int:pk>/delete/', views.ingredientDelete.as_view(), name='ingredient_delete'),
    #Amount paths
    path('amount/', views.amountView.as_view(), name='amount_list'),
    path('amount/create/', views.amountCreate.as_view(), name='amount_create'),
    path('amount/<int:pk>/update/', views.amountUpdate.as_view(), name='amount_update'),
    path('amount/<int:pk>/delete/', views.amountDelete.as_view(), name='amount_delete'),
    #Coooking CookingIngredient paths
    path('cookingIngredient/<int:rp>', views.cookingIngredientView.as_view(), name='cookingIngredient_list'),
    path('cookingIngredient/<int:rp>/create/<str:sl>', views.cookingIngredientCreate.as_view(), name='cookingIngredient_create'),
    path('cookingIngredient/<int:rp>/<int:pk>/update/', views.cookingIngredientUpdate.as_view(), name='cookingIngredient_update'),
    path('cookingIngredient/<int:rp>/<int:pk>/delete/', views.cookingIngredientDelete.as_view(), name='cookingIngredient_delete'),
]