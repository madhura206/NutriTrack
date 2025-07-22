from flask import Flask, render_template, request, redirect, url_for, session
from flask import session, redirect, url_for, flash
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "nutritrack_secret_key"
DATA_FILE = 'data/log.json'

# Ensure data file exists
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username'].strip().lower()
    password = request.form['password']
    data = load_data()

    if username in data:
        return "Username already exists. Please go back and choose another.", 400

    data[username] = {
    'password': generate_password_hash(password),
    'logs': {},
    'goals': {'water': 8, 'calories': 2000}  # Default goals
}
    save_data(data)
    session['username'] = username
    return redirect(url_for('log_entry'))

@app.route('/goals', methods=['GET', 'POST'])
def goals():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    username = session['username']
    data = load_data()
    
    if request.method == 'POST':
        data[username]['goals'] = {
            'water': int(request.form['water_goal']),
            'calories': int(request.form['calorie_goal'])
        }
        save_data(data)
        return redirect(url_for('summary'))
    
    return render_template('goals.html', 
                          goals=data[username]['goals'])

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].strip().lower()
    password = request.form['password']
    data = load_data()

    if username in data and check_password_hash(data[username]['password'], password):
        session['username'] = username
        return redirect(url_for('log_entry'))
    return "Invalid username or password.", 401

# Food and water logging route
@app.route('/log_entry', methods=['GET', 'POST'])
def log_entry():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = session['username']
        food = request.form['food']
        water = int(request.form['water'])

        # Simplified calorie calculation
        calories_dict = {
            'apple': 95, 'banana': 105, 'rice': 200, 'bread': 80, 'milk': 150
        }
        calories = calories_dict.get(food.lower(), 100)

        data = load_data()
        today = datetime.now().strftime('%Y-%m-%d')

        if today not in data[username]['logs']:
            data[username]['logs'][today] = []

        data[username]['logs'][today].append({
            'food': food,
            'water': water,
            'calories': calories
        })

        save_data(data)
        return redirect(url_for('summary'))

    return render_template('log_entry.html')


# Summary page
@app.route('/summary')
def summary():
    if 'username' not in session:
        return redirect(url_for('index'))

    username = session['username']
    today = datetime.now().strftime('%Y-%m-%d')

    data = load_data()
    user_data = data.get(username, {})
    today_entries = user_data.get('logs', {}).get(today, [])
    
    total_water = sum(entry.get('water', 0) for entry in today_entries)
    total_calories = sum(entry.get('calories', 0) for entry in today_entries)

    # Get goals with default values
    goals = user_data.get('goals', {})
    water_goal = goals.get('water', 8)
    calorie_goal = goals.get('calories', 2000)

    return render_template('summary.html',
                           total_water=total_water,
                           total_calories=total_calories,
                           entries=today_entries,
                           water_goal=water_goal,
                           calorie_goal=calorie_goal,
                           username=username)
# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('index'))
    


#overflow values
@app.template_filter('min')
def min_filter(value, limit):
    return min(value, limit)

if __name__ == '__main__':
    app.run(debug=True)
