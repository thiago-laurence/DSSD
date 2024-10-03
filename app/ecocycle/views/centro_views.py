from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage
from rest_framework.decorators import api_view
from ecocycle.models.recoleccion import Recoleccion

@api_view(['GET'])
def index(request):
    if 'user' not in request.session or request.session['user']['subclase'] != 'centro':
        return redirect('login:index')
    
    id_recoleccion = request.GET.get('id_recoleccion', '')
    context = {
        'id_recoleccion': id_recoleccion,
        'error': False,
    }
    if id_recoleccion:
        if Recoleccion.objects.filter(id=id_recoleccion).exists():
            return redirect('recoleccion:view', id_recoleccion=id_recoleccion)
        
        context['error'] = True
        return render(request, 'centro/index.html', { 'context': context })
        
    return render(request, 'centro/index.html', { 'context': context })

@api_view(['GET'])
def view_perfil(request, id_centro):
    if 'user' not in request.session:
        return redirect('login:index')
    
    return render(request, 'centro/perfil.html')

# @api_view(['GET'])
# def index(request):
#     if 'user' not in request.session:
#         return redirect('login:index')
    
#     query = request.GET.get('query', '')
#     page = int(request.GET.get('page', 1))
#     per_page = 2
    
#     users = Recolector.objects.filter(email__icontains=query).order_by('email')
#     user_list = users.values('id', 'email', 'nombre', 'apellido')
#     paginator = Paginator(user_list, per_page)
#     try:
#         user_list = paginator.page(page)
#     except EmptyPage:
#         user_list = paginator.page(paginator.num_pages)
    
#     context = {
#         'user_list': list(user_list),
#         'query': query,
#         'page': page,
#         'per_page': per_page,
#         'page_range': range(1, paginator.num_pages + 1),
#         'recoleccion': ''
#     }

#     return render(request, 'punto/index.html', { 'context': context })