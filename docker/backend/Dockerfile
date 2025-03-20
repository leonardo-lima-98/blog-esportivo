# docker/backend/Dockerfile
FROM python:3.1-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências primeiro (melhor cache)
COPY backend/requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código
COPY backend/ .

# Expor a porta da API
EXPOSE 8000

# Comando para iniciar a API em produção
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]