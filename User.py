from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for production

# Mock user data (replace with a database in a real application)
users = [
    {'username': 'user1', 'email': 'user1@example.com', 'password': generate_password_hash('password1'),
     'fullname': 'John Doe', 'billing_address': '123 Main St, Cityville', 'shipping_address': '456 Shipping Ln, Townsville',
     'phone': '123-456-7890', 'newsletter': True, 'language': 'en', 'currency': 'usd'},
    # Add more users as needed
]

@app.route('/')
def home():
    return 'Welcome to the Home Page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = next((user for user in users if user['username'] == username), None)

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect(url_for('profile'))

        return 'Invalid username or password'

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        # Check if the username is already taken
        if any(user['username'] == username for user in users):
            return 'Username is already taken, please choose another.'

        # Create a new user
        new_user = {'username': username, 'email': email, 'password': password}
        users.append(new_user)

        session['username'] = username  # Log in the new user
        return redirect(url_for('profile'))

    return render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' in session:
        username = session['username']
        user = next((user for user in users if user['username'] == username), None)

        if request.method == 'POST':
            # Update user information based on the form data
            user['fullname'] = request.form['fullname']
            user['billing_address'] = request.form['billing_address']
            user['shipping_address'] = request.form['shipping_address']
            user['phone'] = request.form['phone']
            user['newsletter'] = 'newsletter' in request.form
            user['language'] = request.form['language']
            user['currency'] = request.form['currency']

        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
