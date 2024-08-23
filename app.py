import io
import base64
import numpy as np
import cv2
import face_recognition
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash, session
import details

app = Flask(__name__)
app.config['SECRET_KEY'] = details.secretKey

# PostgreSQL connection
conn = psycopg2.connect(
    dbname='face_recg_db',
    user='recg_user',
    password='recg_pass',
    host='localhost'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        image_data = request.form['image'].split(',')[1]
        image = face_recognition.load_image_file(io.BytesIO(base64.b64decode(image_data)))
        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, embedding) VALUES (%s, %s)", (name, face_encoding.tobytes()))
            conn.commit()
            flash('User signed up successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('No face detected. Please try again.', 'danger')
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        image_data = request.form['image'].split(',')[1]
        image = face_recognition.load_image_file(io.BytesIO(base64.b64decode(image_data)))
        face_encodings = face_recognition.face_encodings(image)
        if len(face_encodings) > 0:
            face_encoding = face_encodings[0]
            cursor = conn.cursor()
            cursor.execute("SELECT name, embedding FROM users")
            users = cursor.fetchall()
            for user in users:
                stored_encoding = np.frombuffer(user[1], dtype=np.float64)
                match = face_recognition.compare_faces([stored_encoding], face_encoding)[0]
                if match:
                    flash(f'Welcome back, {user[0]}!', 'success')
                    return redirect(url_for('home'))
            flash('No match found. Please sign up.', 'danger')
        else:
            flash('No face detected. Please try again.', 'danger')
    return render_template('signin.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
