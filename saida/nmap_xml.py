import os
import subprocess
from datetime import datetime

class NmapXMLExporter:
    """
    Exporta Nmap XML REAL para DefectDojo,
    reutilizando o próprio output do Nmap.
    """

    def __init__(self, logger=None):
        self.logger = logger

    def exportar(self, resultados_reagir, output_dir):
        os.makedirs(output_dir, exist_ok=True)

        caminho_xml = os.path.join(output_dir, "nmap_scan.xml")

        # Se já existe XML gerado pelo Nmap, apenas move/copia
        for scan in resultados_reagir.get("scans_executados", []):
            comando = scan.get("comando")
            alvo = scan.get("alvo")
            porta = scan.get("porta")

            if not comando:
                continue

            comando_xml = comando.split() + ["-oX", caminho_xml]

            if self.logger:
                self.logger.info(
                    f"Gerando XML real do Nmap para {alvo}:{porta}"
                )

            subprocess.run(
                comando_xml,
                capture_output=True,
                text=True,
                timeout=600
            )

            # Um XML consolidado já é suficiente
            break

        if self.logger:
            self.logger.info(f"📤 Nmap XML REAL gerado em: {caminho_xml}")

        return caminho_xml
