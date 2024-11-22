from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inicialização do Flask #
app = Flask(__name__)


# Configuração do banco de dados #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo das Tabelas para cada Variavel #


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Chamando a Página Inicial HTML#


@app.route('/')
def index():
    tasks = Task.query.all()  # Recupera todas as Tarefas do BD
    return render_template('index.html', tasks=tasks)

# Função para adicionar as Atividades #


@app.route('/add', methods=['POST'])
def add():
    task_content = request.form['task']
    if task_content:
        new_task = Task(content=task_content)  # Cria uma Nova Tarefa #
        db.session.add(new_task)  # Adiciona ao Banco #
        db.session.commit()       # Salva as Alterações #
    return redirect(url_for('index'))

# Função para Marcar / Desmarcar o Check #


@app.route('/complete/<int:task_id>')
def complete(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed  # Alterna o Estado da Tarefa
        db.session.commit()                  # Salva as Alterações
    return redirect(url_for('index'))

# Função para remover a Atividade


@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)  # Remove a Tarefa do Banco #
        db.session.commit()      # Salva as Alterações #
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Cria o Banco de Dados e Tabelas - se ainda não existirem #
    with app.app_context():
        db.create_all()
    app.run(debug=True)
