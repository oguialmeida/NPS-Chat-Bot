from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Configuração do banco de dados (SQLite como exemplo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo para textos
class Texto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    analises = db.relationship('Analise', backref='texto', lazy=True)

# Modelo para análises
class Analise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto_id = db.Column(db.Integer, db.ForeignKey('texto.id'), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)

# Criação das tabelas
with app.app_context():
    db.create_all()

# Endpoint para receber JSON e inserir um texto no banco
@app.route('/adicionar_texto', methods=['POST'])
def adicionar_texto():
    if not request.json or 'texto' not in request.json:
        return jsonify({"erro": "O JSON deve conter a chave 'texto'"}), 400

    texto_conteudo = request.json['texto']
    novo_texto = Texto(conteudo=texto_conteudo)

    try:
        db.session.add(novo_texto)
        db.session.commit()
        return jsonify({"mensagem": "Texto adicionado com sucesso!", "id": novo_texto.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

# Endpoint para adicionar uma análise associada a um texto existente
@app.route('/adicionar_analise/<int:texto_id>', methods=['POST'])
def adicionar_analise(texto_id):
    texto = Texto.query.get(texto_id)
    if not texto:
        return jsonify({"erro": "Texto não encontrado"}), 404

    if not request.json or 'conteudo' not in request.json:
        return jsonify({"erro": "O JSON deve conter a chave 'conteudo'"}), 400

    analise_conteudo = request.json['conteudo']
    nova_analise = Analise(texto_id=texto_id, conteudo=analise_conteudo)

    try:
        db.session.add(nova_analise)
        db.session.commit()
        return jsonify({"mensagem": "Análise adicionada com sucesso!", "id": nova_analise.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

# Endpoint para buscar um texto com suas análises associadas
@app.route('/buscar_analise/<int:id>', methods=['GET'])
def buscar_analise(id):
    texto = Texto.query.get(id)
    if not texto:
        return jsonify({"erro": "Texto não encontrado"}), 404

    analises = [{"id": analise.id, "conteudo": analise.conteudo} for analise in texto.analises]

    return jsonify({
        "id": texto.id,
        "conteudo": texto.conteudo,
        "analises": analises if analises else "Nenhuma análise disponível"
    }), 200

# Novo endpoint: Listar todos os textos
@app.route('/listar_textos', methods=['GET'])
def listar_textos():
    textos = Texto.query.all()
    resultado = [{"id": texto.id, "conteudo": texto.conteudo} for texto in textos]

    return jsonify({
        "total": len(resultado),
        "textos": resultado
    }), 200

# Novo endpoint: Listar todas as análises
@app.route('/listar_analises', methods=['GET'])
def listar_analises():
    analises = Analise.query.all()
    resultado = [{"id": analise.id, "conteudo": analise.conteudo, "texto_id": analise.texto_id} for analise in analises]

    return jsonify({
        "total": len(resultado),
        "analises": resultado
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
