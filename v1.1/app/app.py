from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import time
import os
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secure_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Database configuration
DB_CONFIG = {
    'host': 'db',
    'user': 'testuser',
    'password': 'testpass',
    'db': 'testdb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_db():
    return pymysql.connect(**DB_CONFIG)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            flash('Invalid credentials')
        except Exception as e:
            flash('Database error')
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
                    (username, password)
                )
                connection.commit()
                flash('Registration successful! Please login.')
                return redirect(url_for('login'))
        except pymysql.IntegrityError:
            flash('Username already exists!')
        except Exception as e:
            flash('Registration error')
        finally:
            connection.close()
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        connection = get_db()
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT blogs.*, users.username 
                FROM blogs 
                JOIN users ON blogs.user_id = users.id 
                ORDER BY blogs.created_at DESC
            ''')
            blogs = cursor.fetchall()
        return render_template('dashboard.html', blogs=blogs)
    finally:
        connection.close()

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        email = request.form.get('email')
        profile_image = request.files.get('profile_image')
        
        try:
            filename = None
            if profile_image and allowed_file(profile_image.filename):
                filename = secure_filename(profile_image.filename)
                profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            connection = get_db()
            with connection.cursor() as cursor:
                if filename:
                    cursor.execute('''
                        UPDATE users 
                        SET email = %s, profile_image = %s 
                        WHERE id = %s
                    ''', (email, filename, session['user_id']))
                else:
                    cursor.execute('''
                        UPDATE users 
                        SET email = %s 
                        WHERE id = %s
                    ''', (email, session['user_id']))
                connection.commit()
                flash('Profile updated successfully!')
        except Exception as e:
            flash('Error updating profile')
        finally:
            connection.close()
        return redirect(url_for('profile'))
    
    try:
        connection = get_db()
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE id = %s', (session['user_id'],))
            user = cursor.fetchone()
        return render_template('profile.html', user=user)
    finally:
        connection.close()

@app.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        try:
            connection = get_db()
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO blogs (user_id, title, content)
                    VALUES (%s, %s, %s)
                ''', (session['user_id'], title, content))
                connection.commit()
                flash('Blog post created!')
                return redirect(url_for('dashboard'))
        except Exception as e:
            flash('Error creating blog post')
        finally:
            connection.close()
    return render_template('create_blog.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=5000, debug=True)
