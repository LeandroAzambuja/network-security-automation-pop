# 🛡️ Automação de Varredura e Integração com DefectDojo
Versão 2.0 – CLI Operacional, Locking e Exportação CSV

Automação de segurança defensiva desenvolvida em Python, projetada para execução contínua em ambiente Linux (POP), com foco em monitoramento periódico de exposição de serviços, análise inteligente, reação com scans direcionados e integração nativa com DefectDojo para gestão de vulnerabilidades.

O projeto foi construído com arquitetura modular, pipeline auditável e interface operacional de linha de comando (CLI), simulando um cenário real de operação defensiva institucional.


🔄 Esta é a Versão 2.0 da automação, com evolução significativa em operação, controle de execução e integração com DefectDojo.

---

Version 2.0 – Operational CLI, Locking, and CSV Export
A defensive security automation developed in Python, designed for continuous execution in Linux (POP) environments. It focuses on periodic service exposure monitoring, intelligent analysis, reactive targeted scanning, and native DefectDojo integration for vulnerability management.

The project is built with a modular architecture, an auditable pipeline, and an operational command-line interface (CLI), simulating a real-world institutional defensive operations scenario.

🔄 This is Version 2.0 of the automation, featuring significant evolutions in operations, execution control, and DefectDojo integration.

---

## 🆕 O que mudou na Versão 2.0
Principais evoluções implementadas:

- ✅ CLI operacional (scanctl) no padrão de ferramentas Linux
- ✅ Modo interativo mantido, agora como fallback
- ✅ Execução única (test) vs execução operacional (run)
- ✅ Lock de execução para evitar múltiplos scans concorrentes
- ✅ Comando de status para visibilidade operacional
- ✅ Cancelamento manual seguro
- ✅ Exportação CSV compatível com DefectDojo – Generic Findings Import
- ✅ Correção de cabeçalhos e datas (Date)
- ✅ Separação clara entre teste e produção
- ✅ Base preparada para agendamento e expiração automática

Nenhuma funcionalidade da versão anterior foi removida — apenas profissionalizada.

---

## 🎯 Objetivo do Projeto

- Automatizar varreduras periódicas de rede em ambiente POP
- Identificar portas abertas e serviços potencialmente expostos
- Reduzir ruído por meio de análise e escopo controlado
- Executar scans direcionados apenas quando relevante
- Centralizar resultados no DefectDojo para gestão e histórico
- Facilitar rastreabilidade, auditoria e resposta contínua
- Operar de forma segura, previsível e auditável

---

## 🧱 Arquitetura da Automação (Pipeline)

A automação é organizada em fases sequenciais, cada uma com responsabilidade única e desacoplada:

# 1️⃣ COLETAR

- Varredura rápida de portas (1–65535)
- Utiliza RustScan para alta performance
- Identificação de portas abertas, serviços e alvos
- Saída estruturada e reutilizável

---

# 2️⃣ OBSERVAR

- Análise dos dados coletados
- Consolidação e correlação das informações
- Classificação de severidade por exposição:
    - Alta
    - Média
    - Baixa
    - Informacional
- Redução de ruído e priorização realista

---

# 3️⃣ REAGIR

- Execução de scans direcionados reais com Nmap
- Regras de decisão baseadas em escopo:
- Executa apenas em portas relevantes (ex: 21, 22, 80, 443, 445, etc.)
    - Ignora portas fora do escopo definido
    - Scripts e técnicas adequadas por serviço
- Evita varreduras excessivas e falsos positivos

---

# 4️⃣ SAÍDA – DefectDojo (CSV)

- Geração automática de CSV compatível com Generic Findings Import
- Cabeçalhos e campos validados:
    - Title
    - Severity
    - Description
    - Mitigation
    - Date
    - Target
- Importação validada com sucesso no DefectDojo

Estrutura padronizada dos artefatos:

```
resultados/YYYY-MM-DD/HHMMSS/saida_defectdojo/defectdojo_findings.csv
```

---

# 🧭 Modos de Operação (v2)

#🔹 Modo CLI (Recomendado – Produção)

Interface no padrão de ferramentas Linux/Kali:

```
./scanctl run -t 192.168.0.10 -s completo -d 30
```


Parâmetros principais:

- run → execução operacional
- test → execução única (teste)
- status → estado atual da automação
- -t → alvo
- -s → tipo de varredura (rapido | completo)
- -d → duração em dias
- -f → frequência (6, 12 ou 24h)

#🔹 Modo Interativo (Fallback)

Executado automaticamente quando nenhum parâmetro é passado:

```
python3 main.py
```

Solicita interativamente:

- Tipo de varredura
- Alvo
- Frequência
- Duração

Mantido para uso supervisionado ou didático.

---

#🔧 Pré-requisitos
Sistema Operacional

- Linux (testado em Kali Linux)

Ferramentas

- Python 3.9+
- RustScan
- Nmap
- Docker / Docker Compose (DefectDojo)

Bibliotecas Python

```
pip install -r requirements.txt
```

# 📂 Estrutura de Diretórios (v2)

automacao/

```
├── coletar/        # Varredura de portas (RustScan)
├── observar/       # Análise e classificação
├── reagir/         # Scans direcionados (Nmap)
├── saida/          # Exportação CSV (DefectDojo)
├── utils/          # Lock, validações e controle
├── logs/           # Logs operacionais
├── config.yaml     # Configuração
├── main.py         # Orquestrador
├── scanctl         # CLI operacional (entrypoint)
```

# 📥 Integração com DefectDojo

- Tipo de importação: Generic Findings Import
- Arquivo gerado automaticamente:

```
defectdojo_findings.csv
```

- Importação via Product + Engagement
- Findings exibidos corretamente com severidade e alvo
- Histórico preservado

---

🔐 Segurança e Operação

- Lock de execução (/tmp/scanctl.lock)
- Prevenção de múltiplos scans concorrentes
- Status visível em tempo real
- Cancelamento seguro
- Separação clara entre teste e produção
- Código auditável e modular

---

# 📌 Estado Atual do Projeto (v2)

✅ Pipeline completo funcional
✅ CLI profissional implementada
✅ Lock e controle operacional
✅ CSV DefectDojo validado
✅ Modo teste e produção separados
✅ Pronto para uso institucional e avaliação técnica

---

# 🔜 Próximos Passos Planejados

- Expiração automática completa baseada em -d DAYS
- Agendamento automático (cron/systemd)
- Cancelamento via CLI
- Importação automática via API do DefectDojo
- Hardening final e empacotamento
- Documentação visual para banca

---

#👤 Autor

Projeto desenvolvido no contexto da Residência Técnica POP – Hackers do Bem, com foco em automação defensiva, governança e operação realista de segurança.

---




