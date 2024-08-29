import io
import base64
import numpy as np
import face_recognition
from django.shortcuts import render, redirect
from django.contrib import messages
from .firebase_config import db

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        image_data = request.POST['image'].split(',')[1]
        image = face_recognition.load_image_file(io.BytesIO(base64.b64decode(image_data)))
        face_encodings = face_recognition.face_encodings(image)
        print(face_encodings)
        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            
            # Check if this face encoding already exists in Firebase
            users_ref = db.collection('users')
            docs = users_ref.stream()
            for doc in docs:
                stored_encoding = np.frombuffer(doc.to_dict()['embedding'], dtype=np.float64)
                match = face_recognition.compare_faces([stored_encoding], face_encoding)[0]
                if match:
                    # Redirect to sign in if face is already registered
                    messages.info(request, 'This face is already registered. Please sign in.')
                    return redirect('signin')
            
            # Create new user if face encoding does not match
            db.collection('users').document(name).set({
                'name': name,
                'embedding': face_encoding.tobytes()
            })
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
        print(face_encodings)
        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            # Retrieve users from Firebase
            users_ref = db.collection('users')
            docs = users_ref.stream()
            for doc in docs:
                stored_encoding = np.frombuffer(doc.to_dict()['embedding'], dtype=np.float64)
                match = face_recognition.compare_faces([stored_encoding], face_encoding)[0]
                if match:
                    request.session['user_name'] = doc.id
                    messages.success(request, f'Welcome back, {doc.id}!')
                    return redirect('home')
            messages.error(request, 'No match found. Please sign up.')
        else:
            messages.error(request, 'No face detected. Please try again.')
    return render(request, 'signin.html')

def home(request):
    user_name = request.session.get('user_name', None)
    if not user_name:
        return redirect('index')
    return render(request, 'home.html', {'user_name': user_name})

def logout(request):
    request.session.flush()
    return redirect('index')
