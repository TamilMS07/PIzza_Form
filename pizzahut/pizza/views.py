from django.shortcuts import render
from.forms import PizzaForm,MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza

# Create your views here.
def homepage(request):
    return render(request,'pizza/home.html')

def order(request):
    multiple_pizza_form = MultiplePizzaForm()
    created_pizza_Pk = None
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            note = 'Thanks Your order for %s,%s and %s pizza sized pizza was placed!!'%(filled_form.cleaned_data['topping1'],
                                                                            filled_form.cleaned_data['topping2'],
                                                                            filled_form.cleaned_data['size'])
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
        else:
            note = 'please try again...'
        return render(request, 'pizza/order.html', {'note':note,'multiple_pizza_form':multiple_pizza_form,'created_pizza_pk':created_pizza_pk})
    else:
        form = PizzaForm()
        return render(request,'pizza/order.html', {'PizzaForm':form,'multiple_pizza_form':multiple_pizza_form})

def pizzas(request):
    no_of_pizzas = 2
    if request.method == 'GET':
        filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
        if filled_multiple_pizza_form.is_valid():
            no_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
        print(no_of_pizzas)
    PizzaFormSet = formset_factory(PizzaForm,extra=no_of_pizzas)
    formset = PizzaFormSet()
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                form.save()
            note = 'Order placed successfully'
        else:
            note = 'sorry order not placed please try again '
        return render(request, 'pizza/pizzas.html',{'note':note})


    return render(request,'pizza/pizzas.html',{'formset':formset})

def edit(request,pk):
    note = ''
    pizza = Pizza.objects.get(pk = pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'post':
        edited_form = PizzaForm(request.POST,instance=pizza)
        if edited_form.is_valid():
            edited_form.save()
            note = 'Order Edited Successfully!!!'
        else:
            note = 'Sorry Please Try again.......'
    return render(request,'pizza/edit.html',{'pizzaform':form ,'pk':pk,'note':note})