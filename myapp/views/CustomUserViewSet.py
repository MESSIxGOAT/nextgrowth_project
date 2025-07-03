from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from myapp.models.CustomUser import CustomUser
from myapp.serializers.CustomUserSerializer import CustomUserSerializer
from django.contrib.auth.hashers import make_password

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
