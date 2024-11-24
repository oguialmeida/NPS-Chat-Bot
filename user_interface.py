from flask import Flask, request, jsonify, render_template_string
import requests
from transformers import pipeline

app = Flask(__name__)

# Função para buscar o texto por ID da API
def buscar_texto(base_url, texto_id):
    url = f"{base_url}/buscar_analise/{texto_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": str(e)}

# Função para analisar o texto com Hugging Face Transformers
def analisar_texto_transformers(texto):
    try:
        sentiment_analysis = pipeline("sentiment-analysis")
        resultado = sentiment_analysis(texto)
        return resultado[0]  # Retorna o primeiro resultado
    except Exception as e:
        return {"erro": str(e)}

# Função para classificar o avaliador (Promotor, Neutro ou Detrator)
def classificar_analise(analise):
    score = analise['score']
    
    # Se o sentimento for negativo, sempre será "Detrator"
    if analise['label'] == 'NEGATIVE':
        return 'Detrator'
    
    # Se o sentimento for positivo, classificar com base no score
    if analise['label'] == 'POSITIVE':
        if score > 0.7:
            return 'Promotor'
        elif score >= 0.4:
            return 'Neutro'
        else:
            return 'Detrator'
    
    # Sentimento neutro será sempre "Neutro"
    return 'Neutro'

# Rota para exibir a análise em HTML
@app.route('/analisar_texto/<int:texto_id>')
def analisar_texto(texto_id):
    base_url = "http://127.0.0.1:5000"
    resultado = buscar_texto(base_url, texto_id)

    if "erro" in resultado:
        return f"<h1>Erro ao buscar texto: {resultado['erro']}</h1>"
    
    conteudo = resultado.get('conteudo', 'Texto não encontrado')
    analise = analisar_texto_transformers(conteudo)
    classificacao = classificar_analise(analise)

    # Template HTML com CSS
    template_html = '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Análise de Texto</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f5;
                margin: 0;
                padding: 20px;
            }
            .container {
                background-color: #fff;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .texto {
                margin-bottom: 20px;
            }
            .analise {
                padding: 10px;
                background-color: #e7f3fe;
                border-left: 5px solid #2196F3;
                margin-top: 10px;
            }
            .classificacao {
                margin-top: 20px;
                padding: 10px;
                font-weight: bold;
                background-color: #ffeb3b;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Análise de Texto</h1>
            <div class="texto">
                <strong>Texto:</strong>
                <p>{{ conteudo }}</p>
            </div>
            <div class="analise">
                <strong>Resultado da Análise:</strong>
                <p>Sentimento: {{ analise['label'] }}</p>
                <p>Confiança: {{ analise['score']|round(2) }}</p>
            </div>
            <div class="classificacao">
                <strong>Classificação do Avaliador:</strong>
                <p>{{ classificacao }}</p>
            </div>
        </div>
    </body>
    </html>
    '''
    # Renderiza o HTML substituindo as variáveis
    return render_template_string(template_html, conteudo=conteudo, analise=analise, classificacao=classificacao)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
