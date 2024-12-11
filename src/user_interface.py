# app.py
from flask import Flask, request, jsonify, render_template_string
import json
import matplotlib.pyplot as plt
import io
import base64
import os  # Para verificar a existência do arquivo

app = Flask(__name__)

# Função para carregar pesquisas simuladas
def carregar_pesquisas(arquivo='pesquisas.json'):
    if not os.path.exists(arquivo):  # Verifica se o arquivo existe
        with open(arquivo, 'w') as f:
            json.dump([], f)  # Cria o arquivo vazio com um array JSON
    with open(arquivo, 'r') as f:
        return json.load(f)

# Função para salvar pesquisas simuladas (para persistência de dados enviados)
def salvar_pesquisas(pesquisas, arquivo='pesquisas.json'):
    with open(arquivo, 'w') as f:
        json.dump(pesquisas, f, indent=4)

# Função para classificar promotores, detratores e neutros
def classificar_pesquisas(pesquisas):
    resultados = {"Promotor": 0, "Detrator": 0, "Neutro": 0}
    for pesquisa in pesquisas:
        analise = pesquisa['analise']
        classificacao = classificar_analise(analise)
        resultados[classificacao] += 1
    return resultados

# Reutiliza a função classificar_analise existente
def classificar_analise(analise):
    score = analise['score']
    if analise['label'] == 'NEGATIVE':
        return 'Detrator'
    if analise['label'] == 'POSITIVE':
        if score > 0.7:
            return 'Promotor'
        elif score >= 0.4:
            return 'Neutro'
        else:
            return 'Detrator'
    return 'Neutro'

# Função para gerar gráfico de barras
def gerar_grafico(resultados):
    labels = list(resultados.keys())
    valores = list(resultados.values())
    porcentagens = [v / sum(valores) * 100 for v in valores]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, porcentagens, color=['green', 'red', 'blue'])
    plt.xlabel('Classificação')
    plt.ylabel('Porcentagem (%)')
    plt.title('Distribuição das Avaliações')
    plt.ylim(0, 100)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagem_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return imagem_base64

# Rota para receber e salvar dados enviados ao servidor
@app.route('/buscar_analise', methods=['POST'])
def buscar_analise():
    try:
        # Obtém o dado enviado no corpo da requisição
        data = request.json
        if not data:
            return jsonify({"erro": "Nenhum dado enviado"}), 400
        
        # Carrega os dados existentes, adiciona o novo e salva novamente
        pesquisas = carregar_pesquisas()
        pesquisas.append(data)
        salvar_pesquisas(pesquisas)
        return jsonify({"status": "Dado salvo com sucesso", "conteudo": data}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para exibir gráfico e resultados
@app.route('/resultado_analise')
def resultado_analise():
    pesquisas = carregar_pesquisas()
    resultados = classificar_pesquisas(pesquisas)
    grafico_base64 = gerar_grafico(resultados)

    # Template HTML para exibir o gráfico
    template_html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Resultado da Análise</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f5;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                text-align: center;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Resultado da Análise de Avaliações</h1>
            <img src="data:image/png;base64,{{ grafico_base64 }}" alt="Gráfico de Barras">
            <h2>Classificação</h2>
            <ul>
                <li>Promotores: {{ resultados['Promotor'] }}</li>
                <li>Detratores: {{ resultados['Detrator'] }}</li>
                <li>Neutros: {{ resultados['Neutro'] }}</li>
            </ul>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template_html, grafico_base64=grafico_base64, resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
