from django.shortcuts import render, redirect
#from .forms import MaterialForm

def materials_new(request):
    #if request.method == 'POST':
    #    form = MaterialForm(request.POST)
    #    if form.is_valid():
    #        form.save()
    #        return redirect('/')
    #else:
    #    form = MaterialForm()
    return render(request, 'materials/materials_new.html')#, {'form': form})