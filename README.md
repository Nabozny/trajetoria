# CEP Search Automation

![Python](https://img.shields.io/badge/Python-3.10+%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-brightgreen)
![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-green)
![Status](https://img.shields.io/badge/Status-Desenvolvimento-yellow)

Este projeto automatiza a busca de informações de endereços usando CEPs através do SEFANET-PR e ViaCEP como backup.

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- Pandas para manipulação de dados
- Selenium para automação web
- Requests para requisições HTTP
- python-dotenv para variáveis de ambiente
- SMTP para envio de emails
- ReportLab para geração de PDFs
- PyPDF2 para manipulação de PDFs

## 🔄 Processo de Busca

1. **Leitura do arquivo CSV**
   - O programa lê um arquivo CSV contendo uma lista de CEPs
   - Remove hífens dos CEPs para padronização

2. **Busca Principal (SEFANET-PR)**
   - Acessa o site SEFANET-PR
   - Para cada CEP:
     - Insere o CEP no formulário
     - Extrai informações: logradouro, complemento, número, bairro e cidade
     - Armazena os dados em um DataFrame

3. **Busca Secundária (ViaCEP)**
   - Para CEPs que falharam na busca principal:
     - Realiza uma requisição à API ViaCEP
     - Extrai as informações disponíveis
     - Adiciona ao DataFrame de resultados

4. **Resultados**
   - Retorna dois elementos:
     - DataFrame com os endereços encontrados
     - Lista de CEPs que falharam em ambas as buscas

## 📋 Pré-requisitos

1. Python 3.8 ou superior
2. pip para instalação de dependências
3. Conta de email Gmail (para envio de notificações)
4. Chrome WebDriver instalado

## 🛠️ Instalação

1. Clone o repositório
```
git clone https://github.com/Nabozny/trajetoria.git
```

2. Instale as dependências
```
pip install -r requirements.txt
```

3. Configure o ambiente
   - Copie `.env.example` para `.env`
   - Preencha as variáveis necessárias

## 💻 Como Usar

1. Prepare um arquivo CSV com uma coluna 'CEP'
2. Execute o script principal:
```python
from scripts.search_ceps import process_ceps

results, failed_ceps = process_ceps('seu_arquivo.csv')
```

## 📊 Estrutura dos Dados

O DataFrame de resultado contém as seguintes colunas:
- CEP
- logradouro
- complemento
- numero
- bairro
- cidade

## ⚙️ Configuração do Ambiente

1. Copie o arquivo `.env.example` para um novo arquivo chamado `.env`
2. Preencha as variáveis no arquivo `.env`:
   - SMTP_SERVER: Servidor SMTP para envio de emails
   - SMTP_PORT: Porta do servidor SMTP
   - EMAIL_SENDER: Email do remetente
   - EMAIL_PASSWORD: Senha do email 

## Geração de Relatório PDF

O sistema gera automaticamente um relatório em PDF após o processamento dos CEPs e envio dos e-mails. O relatório contém:

### Estrutura do PDF
- Logotipo da empresa como marca d'água
- Data e hora de geração
- Lista de destinatários dos e-mails com horário de envio
- Resultados das consultas de CEPs encontrados
- Lista de CEPs não encontrados ou que necessitam verificação manual

### Características do Relatório
- Formato: PDF
- Nome do arquivo: `relatorio_ceps_YYYYMMDD.pdf`
- Localização: Pasta `/reports` no diretório do projeto
- Paginação automática
- Rodapé com data/hora e número da página

### Exemplo de Uso
```python
pdf_filename = generate_pdf_report(results, failed_ceps, email_recipients)
```

## 📝 Notas

- O sistema utiliza autenticação OAuth2 para Gmail
- Recomenda-se o uso de senha de aplicativo para o E-mail
- Os resultados são enviados em formato CSV por email
