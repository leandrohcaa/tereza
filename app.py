from flask import Flask, jsonify, render_template_string, abort, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure database
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'schema': 'tereza'}
    
    id = db.Column(db.String(36), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    resultados = db.relationship('Resultado', back_populates='usuario')

class Resultado(db.Model):
    __tablename__ = 'resultados'
    __table_args__ = {'schema': 'tereza'}
    
    id = db.Column(db.String(36), primary_key=True)
    usuario_id = db.Column(db.String(36), db.ForeignKey('tereza.usuarios.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    torneio = db.Column(db.String(150), nullable=False)
    compras = db.Column(db.Numeric(12, 2), default=0.00)
    premiacao = db.Column(db.Numeric(12, 2), default=0.00)

    usuario = db.relationship('Usuario', back_populates='resultados')

class SaldoUsuario(db.Model):
    __tablename__ = 'saldo_usuarios'
    __table_args__ = {'schema': 'tereza'}
    
    usuario_id = db.Column(db.String(36), primary_key=True)
    usuario_nome = db.Column(db.String(100))
    data = db.Column(db.Date, primary_key=True)
    compras = db.Column(db.Numeric(12, 2))
    premiacao = db.Column(db.Numeric(12, 2))
    saldo_dia = db.Column(db.Numeric(12, 2))
    saldo_acumulado = db.Column(db.Numeric(12, 2))

# HTML template for the table
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Resultados</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .uuid {
            font-family: monospace;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <h1>Resultados dos Jogos</h1>
    <table>
        <thead>
            <tr>
                <th>Data</th>
                <th>Usuário</th>
                <th>UUID</th>
                <th>Torneio</th>
                <th>Compras</th>
                <th>Premiação</th>
            </tr>
        </thead>
        <tbody>
            {% for resultado in resultados %}
            <tr>
                <td>{{ resultado.data }}</td>
                <td>{{ resultado.usuario.nome }}</td>
                <td class="uuid">{{ resultado.usuario.id }}</td>
                <td>{{ resultado.torneio }}</td>
                <td>{{ "R$ {:.2f}".format(resultado.compras) }}</td>
                <td>{{ "R$ {:.2f}".format(resultado.premiacao) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

# HTML template for saldos
SALDOS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Saldos dos Usuários</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .uuid {
            font-family: monospace;
            font-size: 0.9em;
        }
        .positive {
            color: green;
        }
        .negative {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Saldos dos Usuários</h1>
    <table>
        <thead>
            <tr>
                <th>Data</th>
                <th>Usuário</th>
                <th>Compras</th>
                <th>Premiação</th>
                <th>Saldo do Dia</th>
                <th>Saldo Acumulado</th>
            </tr>
        </thead>
        <tbody>
            {% for saldo in saldos %}
            <tr>
                <td>{{ saldo.data }}</td>
                <td>{{ saldo.usuario_nome }}</td>
                <td class="negative">{{ "R$ {:.2f}".format(saldo.compras) }}</td>
                <td class="positive">{{ "R$ {:.2f}".format(saldo.premiacao) }}</td>
                <td class="{{ 'positive' if saldo.saldo_dia >= 0 else 'negative' }}">
                    {{ "R$ {:.2f}".format(saldo.saldo_dia) }}
                </td>
                <td class="{{ 'positive' if saldo.saldo_acumulado >= 0 else 'negative' }}">
                    {{ "R$ {:.2f}".format(saldo.saldo_acumulado) }}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route('/admin/resultados')
def index():
    # Get all results with user information
    resultados = Resultado.query.join(Usuario).order_by(Resultado.data.desc()).all()
    return render_template_string(HTML_TEMPLATE, resultados=resultados)

@app.route('/usuario/<string:usuario_id>')
def usuario_resultados(usuario_id):
    # Get results for specific user
    usuario = Usuario.query.get_or_404(usuario_id)
    resultados = Resultado.query.filter_by(usuario_id=usuario_id).order_by(Resultado.data.desc()).all()
    
    return render_template_string(HTML_TEMPLATE, resultados=resultados)

@app.route('/usuario/<string:usuario_id>/saldos')
def usuario_saldos(usuario_id):
    # Get saldos for specific user
    saldos = SaldoUsuario.query.filter_by(usuario_id=usuario_id).order_by(SaldoUsuario.data.desc()).all()
    
    return render_template_string(SALDOS_TEMPLATE, saldos=saldos)

if __name__ == '__main__':
    app.run(debug=True) 