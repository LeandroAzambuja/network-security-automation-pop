# 🛡️ Automação de Varredura e Integração com DefectDojo

Automação de segurança defensiva desenvolvida em Python para execução em ambiente Linux (POP), com foco em varredura de serviços, análise de exposição, reação com scans direcionados e integração com DefectDojo para gestão de vulnerabilidades.

Projeto desenvolvido no contexto de honeypot institucional, com arquitetura modular e pipeline auditável.

---

## 🎯 Objetivo do Projeto

- Automatizar varreduras periódicas de rede

- Identificar serviços expostos e potenciais riscos

- Executar scans direcionados de forma inteligente

- Centralizar resultados no DefectDojo

- Facilitar rastreabilidade, histórico e gestão de vulnerabilidades

---

## 🧱 Arquitetura da Automação (Pipeline)

A automação é organizada em fases sequenciais, cada uma com responsabilidade única:

### 1️⃣ COLETAR

- Varredura rápida e completa de portas (1–65535)

- Utiliza RustScan

- Identificação de portas abertas, serviços e protocolos

- Saída estruturada em JSON (coleta.json)

### 2️⃣ OBSERVAR

- Análise dos dados coletados

- Consolidação de informações

- Classificação de severidade:

    - Alta

    - Média

    - Baixa

    - Informacional

- Geração de relatório analítico (analise.json)

### 3️⃣ REAGIR

- Execução de scans direcionados reais com Nmap

- Regras de decisão:

    - Executa apenas em portas relevantes (ex: 22, 80)

    - Ignora portas fora do escopo

    - Seleciona scripts Nmap conforme o serviço

- Resultados armazenados em reagir/

### 4️⃣ SAÍDA – DefectDojo

- Geração automática de CSV compatível com:
Generic Findings Import

- Importação validada com sucesso no DefectDojo

- Organização dos artefatos em:

```
resultados_YYYYMMDD_HHMMSS/saida_defectdojo/
````
---

## 🔧 Pré-requisitos

Para executar a automação corretamente, é necessário:

### Sistema Operacional
- Linux (testado em Kali Linux)

### Ferramentas
- Python 3.9 ou superior
- RustScan
- Nmap
- Docker e Docker Compose (para uso do DefectDojo)

### Bibliotecas Python
Instale as dependências com:

```
pip install -r requirements.txt
````

---

📂 Estrutura de Diretórios

```
automacao_honeypot/

├── coletar/        # RustScan e coleta de portas
├── observar/       # Análise e classificação de riscos
├── reagir/         # Scans direcionados (Nmap)
├── saida/          # Exportação para DefectDojo
├── logs/           # Logs da automação
├── config/         # Arquivos de configuração
├── resultados/     # Histórico de execuções
├── main.py         # Orquestrador principal
````
---
## 🚀 Execução
Execução completa (pipeline inteiro):

```
python3 main.py --target <alvo> --fase completa
```

Exemplo:

```
python3 main.py --target scanme.nmap.org --fase completa
```

---

## 📥 Integração com DefectDojo

- Tipo de importação: Generic Findings Import

- Arquivo gerado automaticamente:

```
defectdojo_findings.csv
```

- Importação realizada via Engagement no DefectDojo

- Suporte a Product e Engagement para rastreabilidade

---

## 🔐 Segurança e Operação

- Execução em ambiente POP

- Separação entre ambiente de varredura e GRC

- Backup da automação realizado via .tar.gz

---

## 📌 Estado Atual do Projeto

✅ Pipeline completo funcionando

✅ Integração com DefectDojo validada

✅ Código modular e organizado

✅ Pronto para avaliação e uso institucional

---

🔜 Próximos Passos Planejados

- Agendamento automático de execuções

- Upload automático via API do DefectDojo

- Padronização final de pastas de produção

- Versionamento e publicação completa no GitHub

---

👤 Autor

Projeto desenvolvido no contexto do Programa Hackers do Bem, com foco em boas práticas, clareza arquitetural e aplicabilidade real em ambientes institucionais.
