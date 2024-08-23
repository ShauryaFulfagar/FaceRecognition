from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User
import face_recognition
import cv2
import numpy as np

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    image = request.files['image'].read()
    image_np = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Encode image
    encoding = face_recognition.face_encodings(face_recognition.load_image_file(image))[0]
    user = User(name=name, encoding=encoding.tobytes())
    db.session.add(user)
    db.session.commit()
    flash('User signed up successfully!')
    return redirect(url_for('index'))

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signin', methods=['POST'])
def sign_in():
    image = request.files['image'].read()
    image_np = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Recognize face
    encoding = face_recognition.face_encodings(image)[0]

    users = User.query.all()
    for user in users:
        known_encoding = np.frombuffer(user.encoding, np.float64)
        matches = face_recognition.compare_faces([known_encoding], encoding)

        if True in matches:
            flash('Welcome back, {}'.format(user.name))
            return redirect(url_for('index'))

    flash('User not recognized')
    return redirect(url_for('signin'))
