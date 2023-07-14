from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy

from recipebook.models import Recipe, CookingMode, Step, CookingStep
from recipebook.forms import recipeForm, cookingModeForm, BasicForm, stepForm, cookingStepForm1, cookingStepForm2
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

class cookingStepView(LoginRequiredMixin, View):
    def get(self, request):
        csl = CookingStep.objects.all()
        ctx = {'cookingStep_list': csl}
        return render(request, 'recipebook/cookingStep_list.html', ctx)

class recipeDetailView(LoginRequiredMixin, View):
    reci = Recipe
    def get(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        cookingstep = CookingStep.objects.filter(recipe=recipe.id)
        rm = recipe.mode.all()
        rmc =recipe.mode.count()
        cs = recipe.step.all()
        csc =recipe.step.count()
        ctx = {'recipe':recipe, 'modes':rm, 'mode_count':rmc, 'cookingstep':cookingstep, 'steps':cs, 'step_count':csc}
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

class cookingStepCreate(LoginRequiredMixin, View):
    template = 'recipebook/cookingStep_form.html'
    success_url = reverse_lazy('recipebook:cookingStep_list')
    sl = 'choice'

    def get(self, request, sl):
        if sl == 'choice':
            form = cookingStepForm1()
        else:
            form = cookingStepForm2()
        ctx = {'form': form, 'sl': sl}
        return render(request, self.template, ctx)

    def post(self, request, sl):
        if sl == 'choice':
            form = cookingStepForm1(request.POST)
        else:
            form = cookingStepForm2(request.POST)
        if not form.is_valid():
            ctx = {'form': form, 'sl': sl}
            return render(request, self.template, ctx)
        if sl == 'choice':
            mode = form.save()
        else:
            step = form.cleaned_data['step']
            recipe = form.cleaned_data['recipe']
            step_number = form.cleaned_data['step_number']
            step = Step(step = step)
            step.save()
            cookingstep = CookingStep(recipe=recipe, step=step, step_number=step_number)
            cookingstep.save()
        return redirect(self.success_url)

'''    template = 'recipebook/addStep_form.html'
    success_url = reverse_lazy('recipebook:recipe_detail')

    def get(self, request, pk):
        step = get_object_or_404(self.cookingstep)
        form = cookingStepForm()
        print(form)
        ctx = {'step': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        form = cookingStepForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        cookingStepForm = form.save()
        return redirect(self.success_url)
'''
'''class deleteStep(LoginRequiredMixin, View):
    step = CookingStep
    success_url = reverse_lazy('recipebook:recipe_detail')
    template = 'recipebook/recipe_confirm_delete.html'

    def get(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        form = recipeForm(instance=recipe)
        ctx = {'recipe': recipe}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        recipe = get_object_or_404(self.reci, pk=pk)
        recipe.delete()
        return redirect(self.success_url)'''
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