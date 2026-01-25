"""
SAÍDA DefectDojo – CSV Generic Findings Import
Projeto: Automação RustScan (POP)
Responsabilidade única: gerar CSV compatível com DefectDojo
"""

import csv
import os
from datetime import datetime
from typing import Dict, List


class DefectDojoCSVExporter:
    """
    Gera arquivo CSV no formato Generic Findings Import do DefectDojo.
    """

    def __init__(self, logger=None):
        self.logger = logger

    def exportar(
        self,
        resultados_coleta: List[Dict],
        analise: Dict,
        resultados_reagir: Dict,
        output_dir: str,
        nome_arquivo: str = "defectdojo_findings.csv",
    ) -> str:
        """
        Gera o CSV de findings e retorna o caminho do arquivo.
        """

        saida_dir = os.path.join(output_dir, "saida_defectdojo")
        os.makedirs(saida_dir, exist_ok=True)

        caminho_csv = os.path.join(saida_dir, nome_arquivo)

        findings = self._extrair_findings(analise, resultados_reagir)

        if not findings:
            findings = [self._finding_informacional()]

        with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=findings[0].keys())
            writer.writeheader()
            writer.writerows(findings)

        if self.logger:
            self.logger.info(f"📤 CSV DefectDojo gerado em: {caminho_csv}")

        return caminho_csv

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------

    def _extrair_findings(self, analise: Dict, resultados_reagir: Dict) -> List[Dict]:
        """
        Constrói findings a partir da análise e dos scans direcionados.
        """
        findings = []
        idx = 1
        hoje = datetime.now().strftime("%Y-%m-%d")

        # 1) Findings vindos da análise de risco
        for risco in analise.get("riscos_potenciais", []):
            findings.append({
                "id": f"F-{idx:04d}",
                "title": f"Service exposed: {risco.get('servico')} on port {risco.get('porta')}",
                "severity": self._mapear_severidade(risco.get("severidade")),
                "description": risco.get("descricao", ""),
                "mitigation": risco.get(
                    "recomendacao",
                    "Review service exposure and harden configuration."
                ),
                "impact": "Unauthorized access or information exposure",
                "references": "",
                "active": "true",
                "verified": "true",
                "duplicate": "false",
                "cve": "",
                "cvssv3": "",
                "target": risco.get("alvo", ""),
                "port": str(risco.get("porta", "")),
                "service": risco.get("servico", ""),
                "protocol": "tcp",
                "scanner": "RustScan/Nmap Automation",
                "discovered_date": hoje,
                "reported_date": hoje,
                "type": "Network Service Exposure",
            })
            idx += 1

        # 2) Findings informacionais dos scans direcionados
        for scan in resultados_reagir.get("scans_executados", []):
            if scan.get("sucesso"):
                findings.append({
                    "id": f"F-{idx:04d}",
                    "title": f"Service enumeration: {scan.get('categoria')} on port {scan.get('porta')}",
                    "severity": "Low",
                    "description": "Service enumeration executed successfully.",
                    "mitigation": "Ensure the service is necessary and properly secured.",
                    "impact": "Information disclosure",
                    "references": "",
                    "active": "true",
                    "verified": "true",
                    "duplicate": "false",
                    "cve": "",
                    "cvssv3": "",
                    "target": scan.get("alvo", ""),
                    "port": str(scan.get("porta", "")),
                    "service": scan.get("categoria", ""),
                    "protocol": "tcp",
                    "scanner": "RustScan/Nmap Automation",
                    "discovered_date": hoje,
                    "reported_date": hoje,
                    "type": "Service Enumeration",
                })
                idx += 1

        return findings

    def _finding_informacional(self) -> Dict:
        """
        Finding padrão quando não há riscos.
        """
        hoje = datetime.now().strftime("%Y-%m-%d")
        return {
            "id": "F-0001",
            "title": "Security scan completed with no significant findings",
            "severity": "Informational",
            "description": "Automated scan completed and did not identify significant security issues.",
            "mitigation": "Maintain current security controls and continue monitoring.",
            "impact": "Low",
            "references": "",
            "active": "true",
            "verified": "true",
            "duplicate": "false",
            "cve": "",
            "cvssv3": "",
            "target": "",
            "port": "",
            "service": "",
            "protocol": "",
            "scanner": "RustScan/Nmap Automation",
            "discovered_date": hoje,
            "reported_date": hoje,
            "type": "Security Assessment",
        }

    def _mapear_severidade(self, severidade: str) -> str:
        """
        Mapeia severidade interna para DefectDojo.
        """
        mapa = {
            "alta": "High",
            "media": "Medium",
            "baixa": "Low",
            "informacional": "Informational",
        }
        return mapa.get(severidade, "Medium")
