
# Documentação da API

Esta API permite a adição de textos em um banco de dados SQLite e a busca de análises associadas a esses textos.

## Endpoints

### 1. Adicionar Texto
**URL:** `/adicionar_texto`  
**Método:** `POST`  
**Descrição:** Adiciona um texto no banco de dados. Opcionalmente, pode incluir uma análise para o texto.

#### Corpo da Requisição (JSON):
```json
{
    "texto": "Texto obrigatório a ser salvo no banco.",
    "analise": "Texto opcional contendo a análise do conteúdo."
}
```

#### Respostas:
- **201 Created**:
    ```json
    {
        "mensagem": "Texto adicionado com sucesso!",
        "id": 1
    }
    ```
- **400 Bad Request**:
    ```json
    {
        "erro": "O JSON deve conter a chave 'texto'"
    }
    ```
- **500 Internal Server Error** (se ocorrer um problema com o banco):
    ```json
    {
        "erro": "Descrição detalhada do erro"
    }
    ```

---

### 2. Buscar Análise por ID
**URL:** `/buscar_analise/<int:id>`  
**Método:** `GET`  
**Descrição:** Retorna o conteúdo e a análise associada ao texto com o ID fornecido.

#### Parâmetros da URL:
- **id** (inteiro): O identificador do texto no banco de dados.

#### Respostas:
- **200 OK**:
    ```json
    {
        "id": 1,
        "conteudo": "Texto salvo no banco.",
        "analise": "Análise do texto, ou 'Nenhuma análise disponível' se não houver."
    }
    ```
- **404 Not Found**:
    ```json
    {
        "erro": "Texto não encontrado"
    }
    ```

---

## Configuração do Banco de Dados

O banco de dados utilizado é o SQLite. O arquivo `data.db` será criado automaticamente na primeira execução da aplicação. Certifique-se de que o diretório onde a aplicação é executada possui permissões de escrita.

## Como Executar
1. Certifique-se de ter as dependências instaladas:
   ```bash
   pip install flask flask-sqlalchemy
   ```
2. Execute o servidor:
   ```bash
   python nome_do_arquivo.py
   ```
3. Acesse os endpoints em `http://127.0.0.1:5000`.

