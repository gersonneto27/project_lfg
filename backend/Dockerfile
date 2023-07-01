# Use a imagem base do Python
FROM python:3.9

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app/backend

# Instala as dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o restante do projeto para o contêiner
COPY . .

# Defina as variáveis de ambiente para o Celery
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0

# Execute o servidor Django
CMD sh -c "celery -A project_lfg worker --loglevel=info & python manage.py runserver 0.0.0.0:8000"