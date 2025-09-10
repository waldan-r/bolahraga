from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'namaToko' : 'Bolahraga',
        'nama' : 'Waldan Rafid',
        'kelas' : 'PBP F'
    }
    return render(request, "main.html", context)