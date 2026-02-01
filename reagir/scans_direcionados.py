import subprocess
import os

class ScansDirecionados:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

        nmap_reacao = self.config.get("nmap_reacao", {})
        self.nmap_parametros = nmap_reacao.get("parametros", "-sV -sC -T4")
        scripts = nmap_reacao.get("scripts_direcionados", [])
        self.nmap_scripts = ",".join(scripts) if scripts else "default,vuln"

    def executar_scans(self, resultados_coleta, analise, output_dir):
        """
        Executa UM Nmap consolidado, baseado em governança.
        Gera XML real já aqui.
        """
        os.makedirs(output_dir, exist_ok=True)
        caminho_xml = os.path.join(output_dir, "nmap_scan.xml")

        portas_governanca = self._definir_portas_por_governanca(
            resultados_coleta, analise
        )

        if not portas_governanca:
            self.logger.warning("Nenhuma porta relevante para reação.")
            return {"xml": None, "portas_reagidas": []}

        portas_str = ",".join(str(p) for p in sorted(portas_governanca))
        alvo = resultados_coleta[0].get("alvo")

        comando = (
            f"nmap {self.nmap_parametros} "
            f"--script {self.nmap_scripts} "
            f"-p {portas_str} {alvo} "
            f"-oX {caminho_xml}"
        )

        self.logger.info(f"Executando Nmap consolidado em {alvo}")
        self.logger.info(f"Portas reagidas: {portas_str}")

        subprocess.run(
            comando.split(),
            capture_output=True,
            text=True,
            timeout=900
        )

        self.logger.info(f"📤 XML real gerado em: {caminho_xml}")

        return {
            "xml": caminho_xml,
            "portas_reagidas": sorted(portas_governanca),
            "comando": comando
        }

    def _definir_portas_por_governanca(self, resultados, analise):
        """
        Decide portas com base em análise (governança).
        """
        portas = set()

        # 1) Riscos explícitos
        for risco in analise.get("riscos_potenciais", []):
            portas.add(risco.get("porta"))

        # 2) Serviços relevantes (sem serem risco explícito)
        servicos = analise.get("servicos_identificados", {})
        for categoria in ["web", "remote_access", "banco_dados"]:
            for item in servicos.get(categoria, []):
                portas.add(item.get("porta"))

        # 3) Logar exclusões
        for resultado in resultados:
            for porta_info in resultado.get("portas", []):
                porta = porta_info.get("porta")
                if porta not in portas:
                    self.logger.info(
                        f"Ignorando porta {porta} – fora do escopo (governança)"
                    )

        return portas
