from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import face_recognition
import cv2
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://recg_user:recg_pass@localhost/face_recg_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    encoding = db.Column(db.LargeBinary, nullable=False)

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    image = request.files['image'].read()
    image_np = np.frombuffer(image, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

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

    encoding = face_recognition.face_encodings(image)[0]

    users = User.query.all()
    for user in users:
        known_encoding = np.frombuffer(user.encoding, np.float64)
        matches = face_recognition.compare_faces([known_encoding], encoding)

        if True in matches:
            return render_template('home.html')

    flash('User not recognized')
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
