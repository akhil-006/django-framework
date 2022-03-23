from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.views import View
from .models import FibModel
from .forms import FibForm
from .tasks import fib_task


# Create your views here.
class FibListView(View):
    objects_per_page = 6

    def get(self, request):
        objects = FibModel.objects.all().order_by('-date_created')
        objects = Paginator(objects, self.objects_per_page)
        # print('OBJECTS COUNT: ', objects.count)
        try:
            page_num = request.GET.get('page')
            pages = objects.page(page_num)
        except EmptyPage as ep:
            print(f'Page not found: {ep}')
            pages = objects.page(objects.num_pages)
        except PageNotAnInteger as pgni:
            print(f'Page not an integer error: {pgni}')
            pages = objects.page(1)

        context = {
            'objects': pages
        }
        return render(request, 'fib/calculationresult.html', context)


def Back(request):
    form = FibForm()
    url = reverse('start')
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
            url = f"{reverse('calculate')}?page=1"
            return redirect(url, {'objects': objects})
    form = FibForm()
    return render(request, 'fib/newcalculation.html', {'form': form})

