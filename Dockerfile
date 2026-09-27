# Imagem base: Python 3.12 em versão "slim" (mais leve que a imagem completa)
FROM python:3.12-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia primeiro só o requirements.txt (aproveita cache do Docker: só reinstala
# as dependências se esse arquivo mudar, mesmo que o código da API mude depois)
COPY requirements.txt .

# Instala as dependências Python dentro do container
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da API para dentro do container
COPY . .

# Informa que o container vai expor a porta 5000 (mesma porta do Flask)
EXPOSE 5000

# Comando executado quando o container sobe: inicia a API
CMD ["python", "app.py"]
