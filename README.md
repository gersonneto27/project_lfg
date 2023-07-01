# Funcionalidades
Funcionalidade 1: App para Solicitação de Propostas e Avaliação das mesmas.
...
# Instalação
Clone este repositório: git clone https://github.com/gersonneto27/project_lfg.git
Acesse o diretório do projeto: cd project_lfg
Rode o docker com o comando : docker-compose up --build -d
Verifique se tem alguma migração pendente: docker-compose exec backend python manage.py makemigrations
Rode as migrações : Verifique se tem alguma migração pendente: docker-compose exec backend python manage.py migrate
Caso seja necessário crie um usuário admin: docker-compose exec backend python manage.py createsuperuser

...

# Informações Importantes:

ip frontend: localhost:8080 
id admin: localhost:8000/admin
Campos:

Proposal: estão as propostas onde as que estão marcada com a análise humana terá que passar pela análise do analista.abnf
Proposal Config: Estão os campos personalizados para serem adicionados na proposta.

Como proposto no desafio, quando a proposta é criada dispara uma task que faz uma verificão no endpoint e retorna com a análise humana True.
...

