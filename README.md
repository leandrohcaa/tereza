# Git e Versionamento de Código

Este código será compartilhado via github. Então para baixá-lo basta fazer o git clone to github project. Favor pedir auxilio ao chatGPT.

# Heroku

Heroku é o cloud service. Parece ser o mais barato dentre eles (comparando com AWS, Azure, GCP).

Foi criado um banco de dados Postgresql. Utilizado o sql `initial_load.sql` para carga inicial das tabelas e dos usuários.

E foi deployado um serviço em python (Flask) para mostrar os dados (o código está na pasta /api). Este serviço busca do banco de dados via SQL e mostra via HTML.

# Como acessar via CLI

Primeiro deve-se instalar o heroku CLI.

Para mac: `brew tap heroku/brew && brew install heroku`

Para Windows precisa pesquisar como instalar, mas deve ser simples.

Para logar: `heroku login`

Para buscar as credenciais do banco de dados (host, port, user, password): `heroku pg:credentials:url DATABASE_URL -a tereza`

# Para rodar o import localmente

Deve-se instalar a última versão do python e do pip. Pedir ajuda ao chatGPT.

Criar um virtual environment nesta pasta e rodar o pip install para o requirements.txt. Basta copiar e colar este prompt no chatGPT e ele vai dizer quais comandos rodar.

Após isso, basta rodar o import.py: `python3 import.py`. Atualmente ele vai ler o arquivo input.xlsx que estiver no root da pasta. Se quiser mudar isso, basta mudar o código para passar como parametro.

# Para rodar o web app localmente

É necessário fazer o pip install do requirements.txt, via venv. Pedir auxilio ao chatGPT para saber quais comandos.
Após isso, basta rodar o app.py: `python3 app.py`.

Para fazer o deploy de mudanças no Heroku, o Heroku já está apontando para um github project. Então basta fazer o push das mudanças no github. Favor verificar no chatgpt como fazer push de commits usando o github.

# Melhor ambiente de dev

Baixar o Cursor e usá-lo.
