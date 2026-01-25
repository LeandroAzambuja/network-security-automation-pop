import subprocess
import json
import os

class ScansDirecionados:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

        # === B1: PORTAS PERMITIDAS ===
        self.portas_permitidas = [22, 80, 443]

        # === B2: MAPEAMENTO POR SERVIÇO ===
        # serviço -> categoria
        self.servico_para_categoria = {
            "ssh": "ssh",
            "http": "web",
            "https": "web"
        }

        # scans por categoria
        self.scans_por_categoria = {
            "web": "nmap -sV --script=http-enum,http-headers -p {porta} {alvo}",
            "ssh": "nmap -sV --script=ssh2-enum-algos -p {porta} {alvo}",
        }

    def executar_scans(self, resultados_coleta, analise, output_dir=None):
        self.logger.info("Executando scans direcionados (B1 + B2)...")
        scans_executados = []

        for alvo in resultados_coleta:
            for porta_info in alvo.get("portas", []):
                porta = porta_info.get("porta")
                servico = (porta_info.get("servico") or "").lower()

                # === B1: filtro por porta ===
                if porta not in self.portas_permitidas:
                    self.logger.info(
                        f"Ignorando porta {porta} em {alvo['alvo']} (fora do escopo)"
                    )
                    continue

                # === B2: decisão por serviço ===
                categoria = self._decidir_por_servico(servico, porta)
                if not categoria:
                    self.logger.info(
                        f"Ignorando porta {porta} em {alvo['alvo']} (serviço não mapeado)"
                    )
                    continue

                scan = self._executar_scan(alvo["alvo"], porta, categoria)
                scans_executados.append(scan)

        resultados = {"scans_executados": scans_executados}
        if output_dir:
            self._salvar_resultados(resultados, output_dir)

        return resultados

    def _decidir_por_servico(self, servico, porta):
        # serviço explícito
        if servico in self.servico_para_categoria:
            return self.servico_para_categoria[servico]

        # fallback por porta (quando serviço vem genérico)
        if porta == 22:
            return "ssh"
        if porta in [80, 443]:
            return "web"

        return None

    def _executar_scan(self, alvo, porta, categoria):
        comando = self.scans_por_categoria[categoria].format(
            alvo=alvo, porta=porta
        )
        self.logger.info(f"Executando scan {categoria} em {alvo}:{porta}")

        try:
            resultado = subprocess.run(
                comando.split(),
                capture_output=True,
                text=True,
                timeout=180
            )
            return {
                "alvo": alvo,
                "porta": porta,
                "categoria": categoria,
                "sucesso": resultado.returncode == 0,
                "comando": comando
            }
        except Exception as e:
            return {
                "alvo": alvo,
                "porta": porta,
                "categoria": categoria,
                "erro": str(e),
                "sucesso": False
            }

    def _salvar_resultados(self, resultados, output_dir):
        reagir_dir = os.path.join(output_dir, "reagir")
        os.makedirs(reagir_dir, exist_ok=True)
        arquivo = os.path.join(reagir_dir, "scans_direcionados.json")
        with open(arquivo, "w") as f:
            json.dump(resultados, f, indent=2)
