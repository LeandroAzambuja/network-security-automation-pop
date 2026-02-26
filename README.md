# 🛡️ Automação de Varredura e Integração com DefectDojo

Versão 2.1 – Integração API Automática e Execução Contínua

Automação de segurança defensiva desenvolvida em Python, projetada para execução contínua em ambiente Linux (POP), com foco em monitoramento periódico de exposição de serviços, análise inteligente, reação com scans direcionados e integração nativa com DefectDojo via API REST para gestão centralizada de vulnerabilidades.

A arquitetura é modular, auditável, desacoplada e preparada para operação institucional contínua.

---

🆕 O que mudou na Versão 2.1

Evoluções implementadas:

- ✅ Integração automática via API REST do DefectDojo (v2)
- ✅ Criação automática de Engagement por data
- ✅ Criação automática de Test e Findings
- ✅ Retorno HTTP validado (201 Created)
- ✅ Log explícito de IMPORT STATUS e IMPORT RESPONSE
- ✅ Execução contínua validada via cron
- ✅ Token via variável de ambiente (segurança operacional)
- ✅ Arquitetura desacoplada entre core e integração

A importação não depende mais de ação manual.




---

## 🎯 Objetivo do Projeto

- Automatizar varreduras periódicas de rede em ambiente POP
- Identificar portas abertas e serviços expostos
- Reduzir ruído com governança de escopo
- Executar scans direcionados apenas quando relevante
- Centralizar resultados automaticamente no DefectDojo
- Permitir operação contínua sem intervenção humana
- Detectar alterações indevidas de exposição

---

## 🧱 Arquitetura da Automação (Pipeline)

A automação é organizada em fases sequenciais, cada uma com responsabilidade única e desacoplada:

---

## 1️⃣ COLETAR

- RustScan → varredura rápida 1–65535
- Identificação de portas abertas

---

## 2️⃣ OBSERVAR
- Análise estruturada
- Classificação de severidade

---

## 3️⃣ REAGIR

- Execução de Nmap direcionado
- Apenas portas relevantes (21,22,80,443,445, etc.)
- Ignora escopo fora de governança

---

## 4️⃣ SAÍDA – DefectDojo (API)

Fluxo automático:


```` 
scanctl run
   ↓
Pipeline executado
   ↓
Geração CSV compatível
   ↓
Importação automática via API REST
   ↓
Product → Engagement (por data) → Test → Findings


````
Endpoint utilizado:

````
POST /api/v2/import-scan/
````
Tipo de importação:

````
Generic Findings Import
````
Validação real:

- HTTP 201 Created
- test_id retornado
- engagement_id retornado
- Estatísticas de severidade retornadas

---

## 🔄 Execução Contínua (Operação POP)

A automação é compatível com execução periódica via cron:

````
0 2 * * * /home/user/automacao/run_scan.sh
````
Requisitos:

- Serviço cron ativo
- Token definido via variável de ambiente
- Máquina ligada (cron não executa com sistema desligado)
- Execução validada em ambiente Kali Linux.

---

## 🧭 CLI Operacional

````
/scanctl run -t <IP> -s completo -d 30
```` 
Comandos:

- run → execução operacional
- test → execução pontual
- status → verifica execução ativa
- cancel → cancela execução ativa

---

##🔐 Segurança e Governança

- Lock de execução (/tmp/scanctl.lock)
- Prevenção de concorrência
- Token fora do código (env var)
- Logs estruturados
- Separação clara entre pipeline e API
- Importação idempotente por data

---

## 📂 Estrutura

````
automacao/
├── coletar/
├── observar/
├── reagir/
├── saida/
│   ├── defectdojo_csv.py
│   ├── defectdojo_importer.py
│   └── defectdojo_api.py
├── utils/
├── logs/
├── config.yaml
├── main.py
├── scanctl
````
---
## 📌 Estado Atual (v2.1)

- ✅ Pipeline funcional
- ✅ CLI operacional
- ✅ Lock implementado
- ✅ CSV validado
- ✅ Integração API REST validada
- ✅ Execução via cron validada
- ✅ Testes múltiplos criados automaticamente
- ✅ Operação contínua confirmada

Pronto para uso institucional.

---

## 🔜 Evoluções Futuras (opcional)

- Alertas automáticos por severidade
- Integração com SIEM
- Containerização
- Empacotamento como serviço
- Hardening adicional

---

##👤 Autor

Projeto desenvolvido no contexto da Residência Técnica POP – Hackers do Bem, com foco em automação defensiva, governança e operação contínua de segurança.

Projeto desenvolvido no contexto da Residência Técnica POP – Hackers do Bem, com foco em automação defensiva, governança e operação realista de segurança.
