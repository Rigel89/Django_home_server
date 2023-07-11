from django.urls import path
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'recipebook'
urlpatterns = [
    path('', TemplateView.as_view(template_name='recipebook/base_menu.html'), name='menu'),
    path('main', TemplateView.as_view(template_name='recipebook/main.html'), name='main'),
    path('example', views.example),
    path('recipe/', views.recipeView.as_view(), name='recipe_list'),
    path('recipe/<int:pk>', views.recipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/create/', views.recipeCreate.as_view(), name='recipe_create'),
    path('recipe/<int:pk>/update/', views.recipeUpdate.as_view(), name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.recipeDelete.as_view(), name='recipe_delete'),
    path('lookup/', views.cookingModeView.as_view(), name='cookingMode_list'),
    path('lookup/create/', views.cookingModeCreate.as_view(), name='cookingMode_create'),
    path('lookup/<int:pk>/update/', views.cookingModeUpdate.as_view(), name='cookingMode_update'),
    path('lookup/<int:pk>/delete/', views.cookingModeDelete.as_view(), name='cookingMode_delete'),
]