from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import face_recognition
import numpy as np
from .models import User

@api_view(['POST'])
def sign_up(request):
    name = request.data.get('name')
    image_data = request.data.get('image')

    if not name or not image_data:
        return Response({"error": "Name and image are required."}, status=status.HTTP_400_BAD_REQUEST)

    image = face_recognition.load_image_file(image_data)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) == 0:
        return Response({"error": "No face detected."}, status=status.HTTP_400_BAD_REQUEST)

    embedding = face_encodings[0]
    user = User(name=name, embedding=embedding.tobytes())
    user.save()

    return Response({"success": "User registered successfully."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def sign_in(request):
    image_data = request.data.get('image')

    if not image_data:
        return Response({"error": "Image is required."}, status=status.HTTP_400_BAD_REQUEST)

    image = face_recognition.load_image_file(image_data)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) == 0:
        return Response({"error": "No face detected."}, status=status.HTTP_400_BAD_REQUEST)

    embedding = face_encodings[0]

    users = User.objects.all()
    for user in users:
        db_embedding = np.frombuffer(user.embedding, dtype=np.float64)
        if face_recognition.compare_faces([db_embedding], embedding)[0]:
            return Response({"success": f"Welcome back, {user.name}!"}, status=status.HTTP_200_OK)

    return Response({"error": "User not recognized."}, status=status.HTTP_400_BAD_REQUEST)
