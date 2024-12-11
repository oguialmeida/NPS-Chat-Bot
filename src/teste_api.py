import random
import requests

# Configurações do endpoint
BASE_URL = "http://127.0.0.1:5002"  # Atualize conforme necessário
ENDPOINT = "/buscar_analise"

# Função para gerar dados simulados com sentimentos fixos
def gerar_dado_simulado(sentimento):
    score = round(random.uniform(0.3, 0.99), 2) if sentimento != 'NEUTRAL' else 0.5
    texto = f"Exemplo de texto com sentimento {sentimento} e score {score}"
    return {
        "conteudo": texto,
        "analise": {
            "label": sentimento,
            "score": score
        }
    }

# Função para enviar os dados simulados ao endpoint
def enviar_dados_simulados(num_dados=30):
    # Calcular o número de pesquisas para cada sentimento com base nas proporções
    num_positivas = int(num_dados * 0.80)
    num_negativas = int(num_dados * 0.15)
    num_neutras = num_dados - num_positivas - num_negativas  # O restante será neutro
    
    # Criar lista com os sentimentos, ajustados para o número proporcional
    sentimentos = ['POSITIVE'] * num_positivas + ['NEGATIVE'] * num_negativas + ['NEUTRAL'] * num_neutras
    
    # Embaralhar a lista para garantir aleatoriedade
    random.shuffle(sentimentos)

    for i, sentimento in enumerate(sentimentos, 1):
        dado = gerar_dado_simulado(sentimento)
        try:
            response = requests.post(f"{BASE_URL}{ENDPOINT}", json=dado)
            if response.status_code == 200:
                print(f"Dado {i} enviado com sucesso: {response.json()}")
            else:
                print(f"Erro ao enviar dado {i}: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na conexão ao enviar dado {i}: {e}")

if __name__ == "__main__":
    enviar_dados_simulados()
