import io
import base64
import numpy as np
import cv2
import face_recognition
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        image_data = request.POST['image'].split(',')[1]
        image = face_recognition.load_image_file(io.BytesIO(base64.b64decode(image_data)))
        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            User.objects.create(name=name, embedding=face_encoding.tobytes())
            messages.success(request, 'User signed up successfully!')
            return redirect('index')
        else:
            messages.error(request, 'No face detected. Please try again.')
    return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        image_data = request.POST['image'].split(',')[1]
        image = face_recognition.load_image_file(io.BytesIO(base64.b64decode(image_data)))
        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            users = User.objects.all()
            for user in users:
                stored_encoding = np.frombuffer(user.embedding, dtype=np.float64)
                match = face_recognition.compare_faces([stored_encoding], face_encoding)[0]
                if match:
                    messages.success(request, f'Welcome back, {user.name}!')
                    return redirect('home')
            messages.error(request, 'No match found. Please sign up.')
        else:
            messages.error(request, 'No face detected. Please try again.')
    return render(request, 'signin.html')

def home(request):
    return render(request, 'home.html')
