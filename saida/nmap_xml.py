import os
import xml.etree.ElementTree as ET
from datetime import datetime


class NmapXMLExporter:
    """
    Gera Nmap XML compatível com DefectDojo (Nmap Scan).
    """

    def __init__(self, logger=None):
        self.logger = logger

    def exportar(self, resultados_coleta, output_dir):
        """
        output_dir JÁ deve ser o diretório saida_defectdojo.
        """
        os.makedirs(output_dir, exist_ok=True)

        caminho_xml = os.path.join(output_dir, "nmap_scan.xml")

        nmaprun = ET.Element(
            "nmaprun",
            {
                "scanner": "nmap",
                "args": "nmap -sS -sV",
                "start": str(int(datetime.now().timestamp())),
                "version": "7.94",
                "xmloutputversion": "1.05",
            },
        )

        for resultado in resultados_coleta:
            host = ET.SubElement(
                nmaprun,
                "host",
                {
                    "starttime": str(int(datetime.now().timestamp())),
                    "endtime": str(int(datetime.now().timestamp())),
                },
            )

            ET.SubElement(host, "status", {"state": "up", "reason": "syn-ack"})

            alvo = resultado.get("alvo", "0.0.0.0")

            ET.SubElement(
                host,
                "address",
                {"addr": alvo, "addrtype": "ipv4"},
            )

            hostnames = ET.SubElement(host, "hostnames")
            ET.SubElement(
                hostnames,
                "hostname",
                {"name": alvo, "type": "user"},
            )

            ports = ET.SubElement(host, "ports")

            for porta_info in resultado.get("portas", []):
                port = ET.SubElement(
                    ports,
                    "port",
                    {
                        "protocol": porta_info.get("protocolo", "tcp"),
                        "portid": str(porta_info.get("porta")),
                    },
                )

                ET.SubElement(
                    port,
                    "state",
                    {"state": "open", "reason": "syn-ack"},
                )

                ET.SubElement(
                    port,
                    "service",
                    {
                        "name": porta_info.get("servico", "unknown"),
                        "method": "table",
                        "conf": "3",
                    },
                )

        runstats = ET.SubElement(nmaprun, "runstats")
        ET.SubElement(
            runstats,
            "finished",
            {
                "time": str(int(datetime.now().timestamp())),
                "elapsed": "1",
                "summary": "Nmap done",
            },
        )
        ET.SubElement(
            runstats,
            "hosts",
            {"up": "1", "down": "0", "total": "1"},
        )

        tree = ET.ElementTree(nmaprun)
        tree.write(caminho_xml, encoding="utf-8", xml_declaration=True)

        if self.logger:
            self.logger.info(f"📤 Nmap XML gerado em: {caminho_xml}")

        return caminho_xml
