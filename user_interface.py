import requests
from transformers import pipeline

def buscar_texto(base_url, texto_id):
    """Faz a requisição à API para buscar um texto pelo ID."""
    url = f"{base_url}/buscar_analise/{texto_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": str(e)}

def analisar_texto_transformers(texto):
    """Analisa o texto usando Hugging Face Transformers."""
    try:
        # Carregar o pipeline para análise de sentimentos
        sentiment_analysis = pipeline("sentiment-analysis")
        resultado = sentiment_analysis(texto)
        return resultado[0]  # Retorna o primeiro resultado
    except Exception as e:
        return f"Erro ao analisar texto: {str(e)}"

if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"  # URL base do servidor Flask
    texto_id = int(input("Digite o ID do texto que deseja buscar e analisar: "))

    # Buscar texto
    resultado = buscar_texto(base_url, texto_id)
    if "erro" in resultado:
        print(f"Erro ao buscar texto: {resultado['erro']}")
    else:
        print(f"Texto encontrado: {resultado['conteudo']}\n")

        # Analisar texto com Transformers
        analise = analisar_texto_transformers(resultado['conteudo'])
        print(f"Análise do Texto:\n{analise}")
