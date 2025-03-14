from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import time

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key_123'  # Replace with a real secret key

# Database configuration
DB_CONFIG = {
    'host': 'db',
    'user': 'testuser',
    'password': 'testpass',
    'db': 'testdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def wait_for_db():
    max_retries = 5
    for _ in range(max_retries):
        try:
            connection = pymysql.connect(**DB_CONFIG)
            connection.close()
            return True
        except pymysql.MySQLError as e:
            print(f"Database connection failed: {e}")
            time.sleep(5)
    return False

def get_db():
    return pymysql.connect(**DB_CONFIG)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            connection = get_db()
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT * FROM users WHERE username = %s AND password = %s',
                    (username, password)
                )
                user = cursor.fetchone()
            if user:
                session['logged_in'] = True
                return 'Login successful!'
            return 'Invalid credentials'
        except Exception as e:
            return f"Database error: {str(e)}"
        finally:
            connection.close()
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            connection = get_db()
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO users (username, password) VALUES (%s, %s)',
                    (username, password))
                connection.commit()
                return redirect(url_for('login'))
        except Exception as e:
            return f"Registration error: {str(e)}"
        finally:
            connection.close()
    return render_template('register.html')

if __name__ == '__main__':
    if wait_for_db():
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Failed to connect to database after multiple attempts")
