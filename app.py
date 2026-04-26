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

class PersonalRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    exercise_name = db.Column(db.String(100))
    max_weight = db.Column(db.Float)
    max_reps = db.Column(db.Integer)

@app.route('/')
def home():
    return "GymTrack API is running"

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

    record = PersonalRecord.query.filter_by(user_id=user_id, exercise_name=exercise_name).first()
    if not record:
        record = PersonalRecord(user_id=user_id, exercise_name=exercise_name, max_weight=weight, max_reps=reps)
        db.session.add(record)
    elif weight > record.max_weight:
        record.max_weight = weight
        record.max_reps = reps

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

@app.route('/workouts/<int:user_id>', methods=['GET'])
def get_workouts_by_user(user_id):
    workouts = Workout.query.filter_by(user_id=user_id).all()
    output = []
    for workout in workouts:
        output.append({
            "id": workout.id,
            "exercise": workout.exercise_name,
            "sets": workout.sets,
            "reps": workout.reps,
            "weight": workout.weight,
            "date": workout.date
        })
    return output

@app.route('/workout/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return {"message": "Workout not found"}, 404
    db.session.delete(workout)
    db.session.commit()
    return {"message": "Workout deleted successfully"}

@app.route('/workout/<int:workout_id>', methods=['PUT'])
def edit_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return {"message": "Workout not found"}, 404
    data = request.json
    workout.exercise_name = data.get('exercise_name', workout.exercise_name)
    workout.sets = data.get('sets', workout.sets)
    workout.reps = data.get('reps', workout.reps)
    workout.weight = data.get('weight', workout.weight)
    workout.date = data.get('date', workout.date)
    db.session.commit()
    return {"message": "Workout updated successfully"}

@app.route('/records/<int:user_id>', methods=['GET'])
def get_records(user_id):
    records = PersonalRecord.query.filter_by(user_id=user_id).all()
    output = []
    for record in records:
        output.append({
            "exercise": record.exercise_name,
            "max_weight": record.max_weight,
            "max_reps": record.max_reps
        })
    return output

if __name__ == "__main__":
    app.run(debug=True)