
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

# Home route
@app.route('/')
def home():
    return "GymTrack API is running"


# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    name = data.get('name')
    email = data.get('email')

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return {
        "message": "User saved successfully",
        "name": name,
        "email": email
    }
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    
    output = []
    for user in users:
        output.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })

    return output

if __name__ == "__main__":
    app.run(debug=True)