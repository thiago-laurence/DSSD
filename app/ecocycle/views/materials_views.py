from django.shortcuts import render, redirect
from ..forms import RecoleccionForm

def materials_new(request):
    #if request.method == 'POST':
    #    form = RecoleccionForm(request.POST)
    #    if form.is_valid():
    #        form.save()
    #        return redirect('/')
    #else:
    #    form = RecoleccionForm()
    return render(request, 'materials/materials_new.html')#, {'form': form})