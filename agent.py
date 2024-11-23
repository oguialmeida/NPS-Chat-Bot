from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados (SQLite como exemplo)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definindo o modelo (tabela)
class Texto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    analise = db.Column(db.Text, nullable=True)  # Novo campo 'analise'

# Criação das tabelas
with app.app_context():
    db.create_all()

# Endpoint para receber JSON e inserir dados no banco
@app.route('/adicionar_texto', methods=['POST'])
def adicionar_texto():
    if not request.json or 'texto' not in request.json:
        return jsonify({"erro": "O JSON deve conter a chave 'texto'"}), 400
    
    texto_conteudo = request.json['texto']
    analise_conteudo = request.json.get('analise', None)  # 'analise' opcional
    
    novo_texto = Texto(conteudo=texto_conteudo, analise=analise_conteudo)
    
    try:
        db.session.add(novo_texto)
        db.session.commit()
        return jsonify({"mensagem": "Texto adicionado com sucesso!", "id": novo_texto.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

# Nova rota: Buscar 'analise' por ID
@app.route('/buscar_analise/<int:id>', methods=['GET'])
def buscar_analise(id):
    texto = Texto.query.get(id)
    if texto is None:
        return jsonify({"erro": "Texto não encontrado"}), 404
    
    return jsonify({
        "id": texto.id,
        "conteudo": texto.conteudo,
        "analise": texto.analise if texto.analise else "Nenhuma análise disponível"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

