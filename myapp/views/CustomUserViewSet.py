from django.contrib import messages
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from myapp.models.CustomUser import CustomUser
from myapp.serializers.CustomUserSerializer import CustomUserSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @csrf_exempt
    @action(detail=False, methods=['get', 'post'], url_path='register')
    def register_user(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_number')
            role = request.POST.get('role')

            if not username or not password or not email:
                return render(request, 'register.html', {
                    'error': "Username, password, and email are required."
                })

            if password != confirm_password:
                return render(request, 'register.html', {
                    'error': "Password and Confirm Password do not match."
                })

            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'register.html', {
                    'error': f"Username '{username}' is already taken."
                })

            hashed_password = make_password(password)

            CustomUser.objects.create(
                username=username,
                password=hashed_password,
                email=email,
                contact_number=contact_number,
                role=role
            )
            return render(request, 'register.html', {
                'success': f"User '{username}' registered successfully!"
            })

        return render(request, 'register.html')
    
    @csrf_exempt
    @action(detail=False, methods=['get', 'post'], url_path='login')
    def login(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            try:
                user = CustomUser.objects.get(username=username)
                if check_password(password, user.password):
                    messages.success(request, f"Welcome, {user.username}")
                    return render(request, 'login.html')  
                else:
                    messages.error(request, "Invalid password")
                    return render(request, 'login.html')
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found")
                return render(request, 'login.html')

        return render(request, 'login.html')

