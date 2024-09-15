from django.shortcuts import render

def login(request):
    return render(request, 'login/index.html')

def auth(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        print(username, password)
    return render(request, 'login/index.html')