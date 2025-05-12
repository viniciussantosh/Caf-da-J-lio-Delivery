from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chave_secreta_super_segura'
app.config['DATABASE'] = 'users.db'

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

@app.route('/item/<sub_item>')
def item_page(sub_item):
    return render_template('item.html', item=sub_item)


@app.route('/carrinho')
def carrinho():
    itens = session.get('carrinho', [])
    
    total = 0.0
    for item in itens:
        try:
            preco = float(item['preco']) if not isinstance(item['preco'], (int, float)) else item['preco']
            total += preco
        except (TypeError, ValueError):
            continue  # Ignora itens com preço inválido
    
    return render_template('carrinho.html', itens=itens, total=total)

@app.route('/adicionar_carrinho', methods=['POST'])
def adicionar_carrinho():
    item = request.form.get('item')
    preco = request.form.get('preco')
    
    if not item or not preco:
        flash('Dados do produto incompletos', 'error')
        return redirect(url_for('cardapio'))
    
    try:
        preco_float = float(preco.replace('R$', '').strip().replace(',', '.'))
    except ValueError:
        flash('Formato de preço inválido', 'error')
        return redirect(url_for('cardapio'))
    
    if 'carrinho' not in session:
        session['carrinho'] = []
    
    session['carrinho'].append({
        'item': item,
        'preco': preco_float  
    })
    session.modified = True
    
    flash(f'{item} adicionado ao carrinho!', 'success')
    return redirect(url_for('carrinho'))



@app.route('/remover_item/<int:index>', methods=['POST'])
def remover_item(index):
    if 'carrinho' in session and 0 <= index < len(session['carrinho']):
        item_removido = session['carrinho'].pop(index)
        session.modified = True
        flash(f'{item_removido["item"]} removido do carrinho', 'info')
    return redirect(url_for('carrinho'))




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
                'age' : age,
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
                'email': user['email'],
                'age': user['age']
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
    app.run(host='0.0.0.0', port=5000, debug=True)