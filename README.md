# API Nota Conforme

Este repositório contém o código-fonte da API **Nota Conforme**, além de instruções detalhadas para sua instalação, configuração e execução como serviço no Linux (via `systemd`).

---

## Requisitos do Sistema

Certifique-se de estar utilizando uma distribuição Linux com suporte a `apt` (como Ubuntu ou Debian).

---

## Instalação de Dependências

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install build-essential git unzip zip tree \
python3-dev python3-pip python3-venv \
postgresql postgresql-contrib -y

---

## Preparação dos Diretórios

```bash
mkdir /apps
chmod 777 /apps

mkdir /apps/logs
mkdir /apps/logs/notaconforme_api
touch /apps/logs/notaconforme_api/app_log

cd /apps
