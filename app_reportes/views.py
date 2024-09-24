from django.shortcuts import render

# Create your views here.

#definir que funciones va a tener el reporte 
def index(request):
    return render(request, 'index.html')
