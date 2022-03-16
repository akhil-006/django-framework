from django.shortcuts import render, redirect
from django.views import View
from .models import FibModel
from .forms import FibForm
from .tasks import fib_task


# Create your views here.
class FibListView(View):
    def get(self, request):
        objects = FibModel.objects.all()
        return render(request, 'fib/calculationresult.html', {'objects': objects})


def Back(request):
    form = FibForm()
    url = request.path.replace('back', 'start')
    return redirect(url, {'form': form})


def StartNewCalculation(request):
    if request.method.lower() == 'post':
        form = FibForm(request.POST)
        if form.is_valid():
            inpt = FibModel.objects.create(input=form.cleaned_data['input']).input
            # print('INP:: ', inp.input)
            fib_task.delay(int(inpt))
            objects = FibModel.objects.values()
            # print('OUTPUT:: ', objects)
            url = request.path.replace('start', 'calculate')
            return redirect(url, {'objects': objects})
    form = FibForm()
    return render(request, 'fib/newcalculation.html', {'form': form})

