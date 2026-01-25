# 🛡️ Automação de Varredura e Integração com DefectDojo

Automação de segurança defensiva desenvolvida em Python, projetada para execução contínua em ambiente Linux (POP), com foco em monitoramento periódico de exposição de serviços, análise inteligente, reação com scans direcionados e integração nativa com DefectDojo para gestão de vulnerabilidades.

O projeto foi construído com arquitetura modular, pipeline auditável e saída compatível com ferramentas corporativas, simulando um cenário real de operação defensiva institucional.

---

## 🎯 Objetivo do Projeto

- Automatizar varreduras periódicas de rede em ambiente POP
- Identificar portas abertas e serviços potencialmente expostos
- Reduzir ruído por meio de análise e escopo controlado
- Executar scans direcionados apenas quando relevante
- Centralizar resultados no DefectDojo para gestão e histórico
- Facilitar rastreabilidade, auditoria e resposta contínua

---

## 🧱 Arquitetura da Automação (Pipeline)

A automação é organizada em fases sequenciais, cada uma com responsabilidade única e desacoplada:

### 1️⃣ COLETAR

- Varredura rápida e completa de portas (1–65535)
- Utiliza RustScan para alta performance
- Identificação de portas abertas, protocolos e alvos
- Saída estruturada em JSON (coleta.json)

---

### 2️⃣ OBSERVAR

- Análise dos dados coletados
- Consolidação e correlação das informações
- Classificação de severidade por exposição:
    - Alta
    - Média
    - Baixa
    - Informacional
- Geração de relatório analítico (analise.json)

---

### 3️⃣ REAGIR

- Execução de scans direcionados reais com Nmap
- Regras de decisão baseadas em escopo e relevância:
    - Executa apenas em portas conhecidas e relevantes (ex: 22, 80, 443)
    - Ignora portas fora do escopo definido
    - Seleciona técnicas de enumeração conforme o serviço
- Resultados controlados e sem ruído excessivo

---

### 4️⃣ SAÍDA – DefectDojo

- Geração automática de Nmap XML compatível com DefectDojo
- Tipo de importação: Nmap Scan
- Importação validada com sucesso no DefectDojo
- Organização padronizada dos artefatos:

```
resultados/YYYY-MM-DD/HHMMSS/saida_defectdojo/nmap_scan.xml
````
---

### 🧭 Interface Inicial (Modo Operacional)

A automação possui interface interativa de inicialização, adequada para operação contínua em servidor:

- Seleção do tipo de varredura:
    - Rápida (portas)
    - Completa (portas + reação)

- Definição de alvo:
    - IP único
    - Hostname/DNS
    - Range CIDR

- Configuração de frequência:
    - A cada 24h (recomendado)
    - A cada 12h
    - A cada 6h

- Definição de duração da automação (em dias)

Essa abordagem permite uso manual, supervisionado ou automatizado via cron.


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
Instalação das dependências:

```
pip install -r requirements.txt
````

---

📂 Estrutura de Diretórios

```
automacao_rustscan/

├── coletar/        # Varredura de portas (RustScan)
├── observar/       # Análise e classificação de exposição
├── reagir/         # Scans direcionados (Nmap)
├── saida/          # Exportação para DefectDojo (Nmap XML)
├── logs/           # Logs da automação
├── config/         # Arquivos de configuração
├── main.py         # Orquestrador principal
````
---
## 🚀 Execução
Execução completa do pipeline:

```
python3 main.py
```

A automação solicitará interativamente:

- Tipo de varredura
- Alvo
- Frequência
- Duração

---

## 📥 Integração com DefectDojo

- Tipo de importação: Nmap Scan
- Arquivo gerado automaticamente:

```
nmap_scan.xml
```

- Importação realizada via Engagement no DefectDojo
- Findings exibidos corretamente (portas abertas e serviços)
- Suporte a Product e Engagement para rastreabilidade

---

## 🔐 Segurança e Operação

- Execução em ambiente POP
- Separação entre automação de varredura e gestão de vulnerabilidades
- Saída padronizada para facilitar importação manual ou futura automação via API
- Backup da automação realizado via .tar.gz

---

## 📌 Estado Atual do Projeto

✅ Pipeline completo funcional
✅ Interface interativa implementada
✅ Integração com DefectDojo validada (Nmap XML)
✅ Código modular, auditável e organizado
✅ Pronto para avaliação técnica e uso institucional

---

##🔜 Próximos Passos Planejados

- Agendamento automático via cron
- Importação automática via API do DefectDojo
- Sanitização final e refino do repositório
- Documentação visual para apresentação
- Evolução para monitoramento contínuo

---

## 👤 Autor

Projeto desenvolvido no contexto do Programa Hackers do Bem, com foco em automação defensiva, boas práticas de segurança, clareza arquitetural e aplicabilidade real em ambientes institucionais.
