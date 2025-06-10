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
```
