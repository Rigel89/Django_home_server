from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse,reverse_lazy

from recipebook.models import *
from recipebook.forms import *

# Create your views here.

def example(request) :
    recipe = BasicForm()
    return HttpResponse(recipe.as_table())

# Main Views

class MainView(View):
    def get(self, request):
        return render(request, 'recipebook/main.html', )

class recipeView(LoginRequiredMixin, View):
    def get(self, request):
        rl = Recipe.objects.all()
        rc = CookingMode.objects.all().count()
        ctx = {'recipe_list': rl, 'cookingMode_count': rc}
        return render(request, 'recipebook/recipe_list.html', ctx)

class recipeDetailView(LoginRequiredMixin, View):
    reci = Recipe
    def get(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        cookingstep = CookingStep.objects.filter(recipe=recipe.id)
        cookingingredient = CookingIngredient.objects.filter(recipe=recipe.id)
        rm = recipe.mode.all()
        rmc =recipe.mode.count()
        cs = recipe.step.all()
        csc =recipe.step.count()
        ci = recipe.ingredient.all()
        cic =recipe.ingredient.count()
        ctx = {'recipe':recipe, 'modes':rm, 'mode_count':rmc,
               'cookingstep':cookingstep, 'steps':cs, 'step_count':csc,
               'cookingingredient':cookingingredient, 'ingredient':ci, 'ingredient_count':cic}
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
    template = 'recipebook/recipe_form.html'
    success_url = reverse_lazy('recipebook:recipe_list')

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
        ctx = {'recipe': recipe}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        recipe.delete()
        return redirect(self.success_url)

#%% This modify the CookingMode DB

class cookingModeView(LoginRequiredMixin, View):
    def get(self, request):
        cml = CookingMode.objects.all()
        ctx = {'cookingMode_list': cml}
        return render(request, 'recipebook/cookingMode_list.html', ctx)

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

#%% This modify the CookingStep DB

class cookingStepView(LoginRequiredMixin, View):
    def get(self, request, rp):
        csl = CookingStep.objects.filter(recipe=rp)
        ctx = {'cookingStep_list': csl, 'rp':rp}
        return render(request, 'recipebook/cookingStep_list.html', ctx)

class cookingStepCreate(LoginRequiredMixin, View):
    template = 'recipebook/cookingStep_form.html'
    data = {'recipe':''}

    def get(self, request, rp, sl):
        self.data['recipe']=Recipe.objects.filter(id=rp)[0]
        if sl == 'choice':
            form = cookingStepForm1(initial=self.data)
        else:
            form = cookingStepForm2(initial=self.data)
        ctx = {'form': form, 'rp': rp, 'sl': sl}
        return render(request, self.template, ctx)

    def post(self, request, rp, sl):
        if sl == 'choice':
            form = cookingStepForm1(request.POST)
        else:
            form = cookingStepForm2(request.POST)
        if not form.is_valid():
            ctx = {'form': form, 'rp': rp, 'sl': sl}
            return render(request, self.template, ctx)
        if sl == 'choice':
            mode = form.save()
        else:
            step = form.cleaned_data['step']
            recipe = Recipe.objects.filter(id=rp)[0]
            step_number = form.cleaned_data['step_number']
            step = Step(step = step)
            step.save()
            cookingstep = CookingStep(recipe=recipe, step=step, step_number=step_number)
            cookingstep.save()
        return redirect('recipebook:cookingStep_list',rp=rp)

class cookingStepUpdate(LoginRequiredMixin, UpdateView):
    cstep = CookingStep
    template = 'recipebook/cookingStep_form.html'
    #success_url = reverse_lazy('recipebook:cookingStep_list')

    def get(self, request, rp, pk):
        cookingstep = get_object_or_404(self.cstep, pk=pk)
        form = cookingStepForm3(instance=cookingstep)
        ctx = {'form': form, 'rp': rp, 'pk': pk}
        return render(request, self.template, ctx)

    def post(self, request, rp, pk):
        cookingstep = get_object_or_404(self.cstep, pk=pk)
        form = cookingStepForm3(request.POST, instance=cookingstep)
        print(form)
        if not form.is_valid():
            ctx = {'form': form,'rp': rp, 'pk': pk}
            return render(request, self.template, ctx)
        form.save()
        return redirect('recipebook:cookingStep_list',rp=rp)

class cookingStepDelete(LoginRequiredMixin, View):
    cstep = CookingStep
    #success_url = reverse_lazy('recipebook:cookingStep_list')
    template = 'recipebook/cookingStep_confirm_delete.html'

    def get(self, request, rp, pk):
        cookingstep = get_object_or_404(self.cstep, pk=pk)
        ctx = {'cookingstep': cookingstep, 'rp': rp, 'pk': pk}
        return render(request, self.template, ctx)

    def post(self, request, rp, pk):
        recipe = get_object_or_404(self.cstep, pk=pk)
        recipe.delete()
        return redirect('recipebook:cookingStep_list',rp=rp)

#%% This modify the Step DB

class stepView(LoginRequiredMixin, ListView):
    model = Step

class stepCreate(LoginRequiredMixin, CreateView):
    model = Step
    fields = '__all__'
    success_url = reverse_lazy('recipebook:step_list')

class stepUpdate(LoginRequiredMixin, UpdateView):
    model = Step
    fields = '__all__'
    success_url = reverse_lazy('recipebook:step_list')


class stepDelete(LoginRequiredMixin, DeleteView):
    model = Step
    fields = '__all__'
    success_url = reverse_lazy('recipebook:step_list')

#%% This modify the Ingridient DB

class ingredientView(LoginRequiredMixin, ListView):
    model = Ingredient

class ingredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = '__all__'
    success_url = reverse_lazy('recipebook:ingredient_list')

class ingredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = '__all__'
    success_url = reverse_lazy('recipebook:ingredient_list')


class ingredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient
    fields = '__all__'
    success_url = reverse_lazy('recipebook:ingredient_list')

#%% This modify the Amount DB

class amountView(LoginRequiredMixin, ListView):
    model = Amount

class amountCreate(LoginRequiredMixin, CreateView):
    model = Amount
    fields = '__all__'
    success_url = reverse_lazy('recipebook:amount_list')

class amountUpdate(LoginRequiredMixin, UpdateView):
    model = Amount
    fields = '__all__'
    success_url = reverse_lazy('recipebook:amount_list')


class amountDelete(LoginRequiredMixin, DeleteView):
    model = Amount
    fields = '__all__'
    success_url = reverse_lazy('recipebook:amount_list')

#%% This modify the CookingIngredient DB

class cookingIngredientView(LoginRequiredMixin, View):
    def get(self, request, rp):
        cil = CookingIngredient.objects.filter(recipe=rp)
        ctx = {'cookingIngredient_list': cil, 'rp':rp}
        return render(request, 'recipebook/cookingIngredient_list.html', ctx)

class cookingIngredientCreate(LoginRequiredMixin, View):
    template = 'recipebook/cookingIngredient_form.html'
    data = {'recipe':''}

    def get(self, request, rp, sl):
        self.data['recipe']=Recipe.objects.filter(id=rp)[0]
        if sl == 'choice':
            form = cookingIngredientForm1(initial=self.data)
        else:
            form = cookingIngredientForm2(initial=self.data)
        ctx = {'form': form, 'rp': rp, 'sl': sl}
        return render(request, self.template, ctx)

    def post(self, request, rp, sl):
        if sl == 'choice':
            form = cookingIngredientForm1(request.POST)
        else:
            form = cookingIngredientForm2(request.POST)
        if not form.is_valid():
            ctx = {'form': form, 'rp': rp, 'sl': sl}
            return render(request, self.template, ctx)
        if sl == 'choice':
            mode = form.save()
        else:
            ingredient = form.cleaned_data['ingredient']
            recipe = form.cleaned_data['recipe']
            #recipe = Recipe.objects.filter(id=rp)[0]
            amount = form.cleaned_data['amount']
            amount = Amount(amount = amount)
            amount.save()
            cookingingredient = CookingIngredient(recipe=recipe, ingredient=ingredient, amount=amount)
            cookingingredient.save()
        return redirect('recipebook:cookingIngredient_list',rp=rp)

class cookingIngredientUpdate(LoginRequiredMixin, UpdateView):
    cingredient = CookingIngredient
    template = 'recipebook/cookingIngredient_form.html'
    #success_url = reverse_lazy('recipebook:cookingIngredient_list')

    def get(self, request, rp, pk):
        cookingingredient = get_object_or_404(self.cingredient, pk=pk)
        form = cookingIngredientForm3(instance=cookingingredient)
        ctx = {'form': form, 'rp': rp, 'pk': pk}
        return render(request, self.template, ctx)

    def post(self, request, rp, pk):
        cookingingredient = get_object_or_404(self.cingredient, pk=pk)
        form = cookingIngredientForm3(request.POST, instance=cookingingredient)
        print(form)
        if not form.is_valid():
            ctx = {'form': form,'rp': rp, 'pk': pk}
            return render(request, self.template, ctx)
        form.save()
        return redirect('recipebook:cookingIngredient_list',rp=rp)

class cookingIngredientDelete(LoginRequiredMixin, View):
    cingredient = CookingIngredient
    #success_url = reverse_lazy('recipebook:cookingIngredient_list')
    template = 'recipebook/cookingIngredient_confirm_delete.html'

    def get(self, request, rp, pk):
        cookingingredient = get_object_or_404(self.cingredient, pk=pk)
        ctx = {'cookingingredient': cookingingredient, 'rp': rp, 'pk': pk}
        return render(request, self.template, ctx)

    def post(self, request, rp, pk):
        recipe = get_object_or_404(self.cingredient, pk=pk)
        recipe.delete()
        return redirect('recipebook:cookingIngredient_list',rp=rp)