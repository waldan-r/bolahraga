import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.core.management import call_command
from django.contrib import messages

# Import model lu
from main.models import Product
from main.forms import ProductForm

# =================================================
#  VIEWS UTAMA (HTML/TEMPLATE)
# =================================================

def show_main(request):
    filter_type = request.GET.get('filter', 'all')
    form = ProductForm()

    if filter_type == 'all':
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)
    
    context = {
        'product_list' : product_list,
        'last_login' : request.COOKIES.get('last_login', 'Never'),
        'form' : form,
        'filter_type' : filter_type,
    }
    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
        
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse('main:show_main'))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)

    context = {'form':form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {'product':product}
    return render(request, "product_detail.html", context)

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')
    
    context = {'form':form}
    return render(request, 'edit_product.html', context)

# =================================================
#  AJAX / FLUTTER AUTHENTICATION
# =================================================

@csrf_exempt  
def register_ajax(request):
    if request.method == 'POST':
        # Logic ganda: Coba baca JSON dulu, kalau gagal baru baca POST biasa
        # Ini penting biar support Flutter (JSON) dan HTML Form biasa
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST

        # UserCreationForm butuh data dictionary
        form = UserCreationForm(data)

        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "Account created! Please log in."})
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
            
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@csrf_exempt  
def login_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"status": "success", "message": "Login successful!", "username": username})
            else:
                return JsonResponse({"status": "error", "message": "Invalid username or password."}, status=401)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@csrf_exempt
def logout_ajax(request):
    logout(request)
    return JsonResponse({
        "status": True,
        "message": "Logout berhasil!",
        "username": ""
    })

# =================================================
#  PRODUCT API (JSON/XML)
# =================================================

def get_product_json(request):
    filter_param = request.GET.get('filter')
    if filter_param == 'my':
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "User not authenticated"}, status=401)
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.all()
    
    product_list = []
    for product in products:
        product_list.append({
            'pk': product.pk,
            'name': product.name,
            'category': product.get_category_display(), # Mengambil label human-readable
            'description': product.description,
            'thumbnail': product.thumbnail, # Pastikan ini string URL di model lu
            'user': product.user.username if product.user else 'Anonymous',
            'price': product.price,
        })
    
    return JsonResponse(product_list, safe=False)

def get_product_for_edit(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        if product.user != request.user:
            return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
        
        product_data = {
            "pk": product.pk,
            "name": product.name,
            "category": product.category, 
            "description": product.description,
            "price": product.price,
        }
        return JsonResponse({"status": "success", "data": product_data})
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found"}, status=404)

@login_required
def delete_product(request, pk):
    if request.method == "POST":
        try:
            product = Product.objects.get(pk=pk)
            if product.user == request.user:
                product.delete()
                return JsonResponse({"status": "success", "message": "Product deleted."})
            else:
                return JsonResponse({"status": "error", "message": "Unauthorized."}, status=403)
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found."}, status=404)
    
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

@login_required
def add_product_ajax(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            
            product_data = {
                'pk': new_product.pk,
                'name': new_product.name,
                'category': new_product.get_category_display(),
                'description': new_product.description,
                'thumbnail': new_product.thumbnail, # Sesuaikan jika pake ImageField (.url)
                'user': new_product.user.username,
            }

            return JsonResponse({"status": "success", "product": product_data})
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@login_required
def update_product_ajax(request, pk):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=pk)
            if product.user != request.user:
                return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
                
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return JsonResponse({"status": "success", "message": "Product updated successfully."})
            else:
                return JsonResponse({"status": "error", "errors": form.errors}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        json_data = serializers.serialize("json", product_item)
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    
@login_required(login_url='/login/')
def show_json(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


# =================================================
#  FLUTTER SPECIFIC HANDLERS
# =================================================

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Pastikan user sudah login (punya session cookie)
            if not request.user.is_authenticated:
                return JsonResponse({"status": "error", "message": "Unauthorized. Please login first."}, status=401)

            new_product = Product.objects.create(
                user=request.user,
                name=data["name"],
                price=int(data["price"]),
                description=data["description"],
                category=data["category"],
                thumbnail=data["thumbnail"], # Anggap string URL
                is_featured=str(data["is_featured"]).lower() == 'true'
            )
            new_product.save()
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def edit_product_flutter(request, id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=id)
            if product.user != request.user:
                 return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)

            data = json.loads(request.body)
            
            product.name = data['name']
            product.price = int(data['price'])
            product.description = data['description']
            product.category = data['category']
            product.thumbnail = data['thumbnail']
            product.is_featured = str(data['is_featured']).lower() == 'true'
            
            product.save()
            
            return JsonResponse({"status": "success", "message": "Product updated!"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=401)

@csrf_exempt
def delete_product_flutter(request, id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=id)
            
            if product.user != request.user:
                return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
            
            product.delete()
            return JsonResponse({"status": "success", "message": "Product deleted!"}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found"}, status=404)
            
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=401)

# Utility buat reset DB (Hati-hati dipake di prod)
def db_tools(request):
    try:
        call_command('migrate')
        
        # Cek user admin ada atau belum
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("Superuser created")
        
        user = User.objects.first()
        
        if not Product.objects.exists():
            Product.objects.create(
                user=user,
                name="Jersey Timnas", 
                price=150000, 
                description="Jersey merah kebanggaan", 
                category="player_gear",
                thumbnail="https://example.com/jersey.jpg", 
                is_featured=True
            )
            Product.objects.create(
                user=user,
                name="Bola Al Rihla", 
                price=500000, 
                description="Bola piala dunia", 
                category="match_equipment", 
                thumbnail="https://example.com/bola.jpg", 
                is_featured=False
            )
                
        return JsonResponse({"status": "success", "message": "Database Migrated & Data Seeded!"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})