"""
SAÍDA DefectDojo – Generic Findings Import (CSV)
Automação Honeypot – Hackers do Bem / POP
"""

import csv
import os
from datetime import datetime


class DefectDojoCSVExporter:
    def __init__(self, logger=None):
        self.logger = logger

    def exportar(self, resultados_coleta, analise, output_dir):
        os.makedirs(output_dir, exist_ok=True)

        caminho_csv = os.path.join(output_dir, "defectdojo_findings.csv")
        findings = []

        hoje = datetime.now().strftime("%Y-%m-%d")

        # =====================================================
        # 1) FINDINGS DE RISCO (ALTO / MÉDIO)
        # =====================================================
        for risco in analise.get("riscos_potenciais", []):
            findings.append({
                "Title": f"{risco['servico'].upper()} exposto na porta {risco['porta']}",
                "Severity": self._mapear_severidade(risco["severidade"]),
                "Description": risco["descricao"],
                "Mitigation": risco["recomendacao"],
                "Impact": "Exposição de serviço vulnerável",
                "References": "",
                "Active": "TRUE",
                "Verified": "TRUE",
                "False Positive": "FALSE",
                "Duplicate": "FALSE",
                "CVE": "",
                "CVSSv3": "",
                "Component Name": risco["servico"],
                "Component Version": "",
                "File Path": "",
                "Line Number": "",
                "Test": "Honeypot Automated Scan",
                "Scanner": "RustScan + Nmap Automation",
                "Date": hoje,
                "Target": risco["alvo"],
            })

        # =====================================================
        # 2) FINDINGS INFORMATIVOS (PORTAS ABERTAS)
        # =====================================================
        portas_risco = {r["porta"] for r in analise.get("riscos_potenciais", [])}

        for resultado in resultados_coleta:
            alvo = resultado.get("alvo")
            for porta_info in resultado.get("portas", []):
                porta = porta_info["porta"]

                # evita duplicar portas já reportadas como risco
                if porta in portas_risco:
                    continue

                findings.append({
                    "Title": f"Porta {porta} aberta ({porta_info.get('servico', 'desconhecido')})",
                    "Severity": "Low",
                    "Description": f"Serviço {porta_info.get('servico', 'desconhecido')} acessível na porta {porta}.",
                    "Mitigation": "Validar necessidade de exposição do serviço.",
                    "Impact": "Superfície de ataque ampliada",
                    "References": "",
                    "Active": "TRUE",
                    "Verified": "FALSE",
                    "False Positive": "FALSE",
                    "Duplicate": "FALSE",
                    "CVE": "",
                    "CVSSv3": "",
                    "Component Name": porta_info.get("servico", ""),
                    "Component Version": "",
                    "File Path": "",
                    "Line Number": "",
                    "Test": "Honeypot Automated Scan",
                    "Scanner": "RustScan",
                    "Date": hoje,
                    "Target": alvo,
                })

        # =====================================================
        # 3) FALLBACK – SEM FINDINGS
        # =====================================================
        if not findings:
            findings.append({
                "Title": "Scan executado sem riscos críticos",
                "Severity": "Info",
                "Description": "A automação foi executada e não identificou riscos relevantes.",
                "Mitigation": "Manter monitoramento contínuo.",
                "Impact": "Baixo",
                "References": "",
                "Active": "TRUE",
                "Verified": "TRUE",
                "False Positive": "FALSE",
                "Duplicate": "FALSE",
                "CVE": "",
                "CVSSv3": "",
                "Component Name": "",
                "Component Version": "",
                "File Path": "",
                "Line Number": "",
                "Test": "Honeypot Automated Scan",
                "Scanner": "RustScan + Nmap",
                "Date": hoje,
                "Target": "",
            })

        # =====================================================
        # 4) ESCRITA DO CSV
        # =====================================================
        with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=findings[0].keys())
            writer.writeheader()
            writer.writerows(findings)

        if self.logger:
            self.logger.info(f"📤 CSV DefectDojo gerado em: {caminho_csv}")

        return caminho_csv

    def _mapear_severidade(self, severidade):
        mapa = {
            "alta": "High",
            "media": "Medium",
            "baixa": "Low",
            "informacional": "Info",
        }
        return mapa.get(severidade.lower(), "Medium")
