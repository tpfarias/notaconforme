# API Nota Conforme
Este repositório contém o código-fonte da API **Nota Conforme**, além de instruções detalhadas para sua instalação, configuração e execução como serviço no Linux (via `systemd`).

---

## Requisitos do Sistema
Certifique-se de estar utilizando uma distribuição Linux com suporte a `apt` (como Ubuntu ou Debian).

---

## 1. Atualização dos Pacotes do Sistema Operacional
Antes de qualquer instalação, atualize os pacotes do sistema para garantir que tudo esteja na versão mais recente e segura:

```bash
sudo apt update && sudo apt upgrade -y
```

---

## 2. Instalação de Dependências
Instale as ferramentas necessárias para compilar, gerenciar pacotes Python, banco de dados PostgreSQL e outras dependências:

```bash
apt install build-essential git unzip zip tree python3-dev python3-pip python3-venv postgresql postgresql-contrib -y
```

---

## 3. Preparação dos Diretórios para Aplicação e Logs
Crie as pastas onde a aplicação e seus logs serão armazenados, garantindo permissões adequadas:

```bash
sudo mkdir /apps
sudo chmod 777 /apps

sudo mkdir -p /apps/logs/notaconforme_api
sudo touch /apps/logs/notaconforme_api/app_log

cd /apps
```

---

## 4. Clonagem do Código Fonte da API Nota Conforme
Clone o projeto do repositório oficial:

```bash
git clone https://github.com/tpfarias/notaconforme_api.git
```

---

## 5. Configuração do Ambiente Virtual Python e Instalação de Dependências
Entre na pasta do projeto, crie um ambiente virtual para isolar as dependências e instale os pacotes listados:

```bash
cd /apps/notaconforme_api

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## 6. Configuração do Banco de Dados PostgreSQL

### 6.1 Criação do Usuário PostgreSQL para a Aplicação
Execute o comando abaixo e siga as instruções para criar o usuário `user_notaconforme` sem permissões de superusuário:

```bash
sudo -u postgres createuser --interactive
# Informe (de acordo com suas preferências e políticas de sua organização):
# Enter name of role to add: user_notaconforme
# Shall the new role be a superuser? (y/n) y
```
### 6.2 Definição de Senhas para os Usuários PostgreSQL
Acesse o prompt do PostgreSQL para definir as senhas do usuário criado e do `postgres`:

```bash
sudo -i -u postgres
psql
```

No prompt do PostgreSQL, substitua `senha_aqui` por uma senha de sua preferência e execute:

```sql
ALTER USER user_notaconforme WITH PASSWORD 'senha_aqui'; 
ALTER USER postgres WITH PASSWORD 'senha_aqui';
```
Saia do prompt do PostgreSQL com `CTRL` + `D`

### 6.3 Ajuste do Método de Autenticação no PostgreSQL
Edite o arquivo de configuração para permitir autenticação via senha (md5) nas conexões locais:

```bash
sudo vim /etc/postgresql/14/main/pg_hba.conf
```
Localize as duas primeiras linhas que usam o método `peer` para `local` e altere para `md5`.
Salve e saia (`ESC` + `:wq`).

Reinicie o serviço PostgreSQL para aplicar as mudanças:
```bash
sudo systemctl restart postgresql
```
### 6.4 Criação do Banco de Dados e Concessão de Privilégios
Volte ao prompt do PostgreSQL e crie o banco de dados usado pela aplicação, concedendo permissões ao usuário criado:

```bash
sudo -i -u postgres
psql
```
Execute:

```sql
CREATE DATABASE notaconforme;
GRANT ALL PRIVILEGES ON DATABASE notaconforme TO user_notaconforme;
```
Saia do prompt do PostgreSQL com `CTRL` + `D`

## 7. Inicialização do Banco de Dados da Aplicação
Acesse a raiz do projeto, ative o ambiente virtual e execute o script para criar as tabelas e estruturas iniciais no banco:

```bash
cd /apps/notaconforme_api/
source venv/bin/activate
python create_database.py
```

## 8. Configuração do Serviço da API com systemd para Inicialização Automática
### 8.1 Criação do Arquivo de Serviço systemd
Abra um editor para criar o arquivo de configuração do serviço:

```bash
sudo vim /etc/systemd/system/notaconforme_api.service
```
### 8.2 Conteúdo Completo para o arquivo ```notaconforme_api.service```
```ini
[Unit]
Description=API Nota Conforme
After=network.target

[Service]
WorkingDirectory=/apps/notaconforme_api
ExecStart=/apps/notaconforme_api/venv/bin/gunicorn main:app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker -w 4 --graceful-timeout 0 --access-logfile /apps/logs/notaconforme_api/app_log
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```
Salve e saia do editor

### 8.3 Ativação e Inicialização do Serviço
Execute os comandos para habilitar o serviço na inicialização do sistema e iniciá-lo imediatamente:
```bash
sudo systemctl enable notaconforme_api.service
sudo systemctl start notaconforme_api.service
sudo systemctl status notaconforme_api.service
```

8.4 Reiniciando o Serviço Após Alterações
Sempre que modificar o arquivo de serviço, rode os comandos abaixo para aplicar as mudanças:

```bash
sudo systemctl daemon-reload
sudo systemctl restart notaconforme_api.service
```

# Pronto!
A API Nota Conforme estará rodando e disponível na porta 8000 do servidor.

Se precisar de ajuda ou encontrar algum problema, abra uma issue ou entre em contato!
