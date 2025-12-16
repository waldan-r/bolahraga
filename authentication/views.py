import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        # Coba tangkap data dari JSON (Flutter)
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except:
            # Kalau gagal, berarti dari Form HTML biasa
            username = request.POST.get('username')
            password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            response_data = {
                "status": True,
                "message": "Login successful",
                "username": user.username,
            }
            # Cek apakah request minta JSON (dari Flutter biasanya header application/json)
            # Atau kita paksa return JSON kalau berhasil login biar Flutter seneng
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Username atau password salah",
            }, status=401)

    # Kalau GET (buka halaman web biasa)
    return render(request, 'login.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # Coba tangkap data dari JSON (Flutter)
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            password_confirm = data.get('password_confirmation', password) # Default ke password kalau gak ada confirm
        except:
            # Fallback ke Form HTML
            username = request.POST.get('username')
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirmation')

        if not username or not password:
             return JsonResponse({"status": False, "message": "Data tidak lengkap"}, status=400)

        if password != password_confirm:
            return JsonResponse({"status": False, "message": "Password tidak sama"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": False, "message": "Username sudah digunakan"}, status=400)

        # Buat user baru
        new_user = User.objects.create_user(username=username, password=password)
        new_user.save()

        return JsonResponse({"status": True, "message": "Akun berhasil dibuat"}, status=200)

    # Kalau GET
    return render(request, 'register.html')

@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"status": True, "message": "Logout berhasil"}, status=200)