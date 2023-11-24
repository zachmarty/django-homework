from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'catalog/index.html')

def contacts(request):
    if request.method == 'POST':
        return render(request, 'catalog/thanks.html')
    return render(request, 'catalog/contacts.html')