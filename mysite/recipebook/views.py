from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from recipebook.models import Recipe, CookingMode#, cookingStep
from recipebook.forms import recipeForm, cookingModeForm, BasicForm
from django.http import HttpResponse

# Create your views here.

def example(request) :
    recipe = BasicForm()
    return HttpResponse(recipe.as_table())

class MainView(View):
    def get(self, request):
        return render(request, 'recipebook/main.html', )

class cookingModeView(LoginRequiredMixin, View):
    def get(self, request):
        cml = CookingMode.objects.all()
        ctx = {'cookingMode_list': cml}
        return render(request, 'recipebook/cookingMode_list.html', ctx)

class recipeView(LoginRequiredMixin, View):
    def get(self, request):
        rl = Recipe.objects.all()
        rc = CookingMode.objects.all().count()
        ctx = {'recipe_list': rl, 'cookingMode_count': rc}
        return render(request, 'recipebook/recipe_list.html', ctx)

class recipeDetailView(View):
    reci = Recipe
    def get(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        rm = recipe.mode.all()
        rmc =recipe.mode.count()
        ctx = {'recipe':recipe, 'modes':rm, 'mode_count':rmc}
        return render(request, 'recipebook/recipe_detail.html', ctx)


# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded
class recipeCreate(LoginRequiredMixin, View):
    template = 'recipebook/recipe_form.html'
    success_url = reverse_lazy('recipebook:recipe_list')

    def get(self, request):
        form = recipeForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = recipeForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        recipe = form.save()
        return redirect(self.success_url)


# MakeUpdate has code to implement the get/post/validate/store flow
# AutoUpdate (below) is doing the same thing with no code
# and no form by extending UpdateView
class recipeUpdate(LoginRequiredMixin, View):
    reci = Recipe
    success_url = reverse_lazy('recipebook:recipe_list')
    template = 'recipebook/recipe_form.html'

    def get(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        form = recipeForm(instance=recipe)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        form = recipeForm(request.POST, instance=recipe)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)


class recipeDelete(LoginRequiredMixin, View):
    reci = Recipe
    success_url = reverse_lazy('recipebook:recipe_list')
    template = 'recipebook/recipe_confirm_delete.html'

    def get(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        form = recipeForm(instance=recipe)
        ctx = {'recipe': recipe}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        recipe.delete()
        return redirect(self.success_url)

# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes
class cookingModeCreate(LoginRequiredMixin, View):
    template = 'recipebook/cookingMode_form.html'
    success_url = reverse_lazy('recipebook:cookingMode_list')

    def get(self, request):
        form = cookingModeForm()
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request):
        form = cookingModeForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        mode = form.save()
        return redirect(self.success_url)

class cookingModeUpdate(LoginRequiredMixin, UpdateView):
    model = CookingMode
    fields = '__all__'
    success_url = reverse_lazy('recipebook:cookingMode_list')


class cookingModeDelete(LoginRequiredMixin, DeleteView):
    model = CookingMode
    fields = '__all__'
    success_url = reverse_lazy('recipebook:cookingMode_list')

'''class modeCreate(CreateView):
    mode = cookingStep
    fields = '__all__'
    success_url = reverse_lazy('recipebook:main')


class modeUpdate(UpdateView):
    model = cookingStep
    fields = '__all__'
    success_url = reverse_lazy('recipebook:main')


class modeDelete(DeleteView):
    model = cookingStep
    fields = '__all__'
    success_url = reverse_lazy('recipebook:main')'''