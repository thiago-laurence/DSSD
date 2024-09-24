from django.shortcuts import redirect, render
from rest_framework.decorators import api_view

@api_view(['GET'])
def index(request):
    if 'user' not in request.session:
        return redirect('login:index')
    
    return render(request, 'punto/index.html')