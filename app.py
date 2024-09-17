from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar_db():
    conectar = sqlite3.connect('estudantes.db')
    conectar.row_factory = sqlite3.Row 
    return conectar


def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estudantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            curso TEXT NOT NULL,
            email TEXT NOT NULL,
            ano INTEGER)
    ''')
    conectar.commit()
    conectar.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/adicionar_estudante', methods=['POST'])
def adicionar_estudante():
    nome = request.form['nome']
    curso = request.form['curso']
    ano = request.form['ano']
    email = request.form['email']

    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute(
        'INSERT INTO estudantes (nome, curso, ano, email) VALUES (?,?,?,?)', (nome, curso, ano, email)
    )
    conectar.commit()
    conectar.close()
    return redirect(url_for('index'))


@app.route('/estudantes')
def listar_estudantes():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('SELECT * FROM estudantes')
    estudantes = cursor.fetchall()
    conectar.close()


    return render_template('estudantes.html', estudantes=estudantes)

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True, port=8080)