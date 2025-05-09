from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chave_secreta_super_segura'
app.config['DATABASE'] = 'users.db'


from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

app.wsgi_app = DispatcherMiddleware(Response("Carregando...", status=202), {
    '/': app.wsgi_app
})

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
        conn.commit()

init_db()



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/cardapio')
def cardapio():
    return render_template('menu.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([name, age, email, password]):
            flash('Preencha todos os campos!', 'danger')
            return render_template('create_account.html')
        
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (name, age, email, password) VALUES (?, ?, ?, ?)',
                    (name, age, email, generate_password_hash(password))
                )
                conn.commit()
            
            session['user'] = {
                'id': cursor.lastrowid,
                'name': name,
                'email': email
            }
            return redirect(url_for('dashboard'))
            
        except sqlite3.IntegrityError:
            flash('Este email já está cadastrado!', 'danger')
            return render_template('create_account.html')
    
    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user'] = {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos!', 'danger')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Por favor, faça login primeiro!', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Você foi desconectado com sucesso.', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, threaded=True)  # Porta 10000 é a padrão do Render