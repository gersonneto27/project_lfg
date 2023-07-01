import os
from celery import Celery
app = Celery('tasks', broker='pyamqp://guest@localhost//')
# Define o módulo Django como o padrão para configuração do Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_lfg.settings')

# Crie uma instância do objeto Celery
app = Celery('project_lfg')

# Configure o Celery usando as configurações do projeto Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubra automaticamente as tarefas do Celery no projeto
app.autodiscover_tasks()
