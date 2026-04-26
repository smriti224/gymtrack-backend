
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

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    exercise_name = db.Column(db.String(100))
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight = db.Column(db.Float)
    date = db.Column(db.String(50))

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

@app.route('/workout', methods=['POST'])
def add_workout():
    data = request.json

    user_id = data.get('user_id')
    exercise_name = data.get('exercise_name')
    sets = data.get('sets')
    reps = data.get('reps')
    weight = data.get('weight')
    date = data.get('date')

    new_workout = Workout(
        user_id=user_id,
        exercise_name=exercise_name,
        sets=sets,
        reps=reps,
        weight=weight,
        date=date
    )
    db.session.add(new_workout)
    db.session.commit()

    return {
        "message": "Workout saved successfully",
        "exercise": exercise_name,
        "sets": sets,
        "reps": reps,
        "weight": weight,
        "date": date
    }

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()

    output = []
    for workout in workouts:
        output.append({
            "id": workout.id,
            "user_id": workout.user_id,
            "exercise": workout.exercise_name,
            "sets": workout.sets,
            "reps": workout.reps,
            "weight": workout.weight,
            "date": workout.date
        })

    return output

if __name__ == "__main__":
    app.run(debug=True)