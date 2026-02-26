"""
Módulo de análise dos resultados da coleta.
Hackers do Bem
"""

import json
import os

class AnalisadorResultados:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        self.SERVICOS_COMUNS = {
            20: "ftp-data", 21: "ftp", 22: "ssh", 23: "telnet",
            25: "smtp", 53: "dns", 80: "http", 110: "pop3",
            111: "rpcbind", 135: "msrpc", 139: "netbios-ssn",
            143: "imap", 443: "https", 445: "microsoft-ds",
            993: "imaps", 995: "pop3s", 1723: "pptp",
            3306: "mysql", 3389: "ms-wbt-server", 5900: "vnc",
            8080: "http-proxy", 8443: "https-alt"
        }
        
        self.SERVICOS_DE_RISCO = {
            21: "ftp", 23: "telnet", 135: "msrpc", 
            139: "netbios-ssn", 445: "microsoft-ds", 3389: "ms-wbt-server"
        }
    
    def analisar(self, resultados_coleta, output_dir=None):
        self.logger.info("Analisando resultados da coleta...")
        
        analise = {
            "estatisticas_gerais": self._calcular_estatisticas(resultados_coleta),
            "servicos_identificados": self._identificar_servicos(resultados_coleta),
            "riscos_potenciais": self._identificar_riscos(resultados_coleta),
            "recomendacoes": [],
            "resumo": {}
        }
        
        analise["recomendacoes"] = self._gerar_recomendacoes(analise)
        analise["resumo"] = self._gerar_resumo(analise)
        
        if output_dir:
            self._salvar_analise(analise, output_dir)
        
        self.logger.info(f"Análise concluída: {analise['estatisticas_gerais']['total_portas']} portas analisadas")
        return analise
    
    def _calcular_estatisticas(self, resultados):
        estatisticas = {
            "total_alvos": len(resultados),
            "total_portas": 0,
            "alvos_com_portas": 0,
            "servicos_mais_comuns": {}
        }
        
        for resultado in resultados:
            portas = resultado.get("portas", [])
            num_portas = len(portas)
            estatisticas["total_portas"] += num_portas
            
            if num_portas > 0:
                estatisticas["alvos_com_portas"] += 1
            
            for porta_info in portas:
                porta = porta_info.get("porta")
                if porta in self.SERVICOS_COMUNS:
                    servico = self.SERVICOS_COMUNS[porta]
                    estatisticas["servicos_mais_comuns"][servico] = \
                        estatisticas["servicos_mais_comuns"].get(servico, 0) + 1
        
        return estatisticas
    
    def _identificar_servicos(self, resultados):
        servicos = {
            "web": [], "banco_dados": [], "remote_access": [],
            "file_transfer": [], "outros": []
        }
        
        for resultado in resultados:
            alvo = resultado.get("alvo", "")
            for porta_info in resultado.get("portas", []):
                porta = porta_info.get("porta")
                servico_info = {
                    "alvo": alvo,
                    "porta": porta,
                    "servico": self.SERVICOS_COMUNS.get(porta, f"desconhecido ({porta})"),
                    "protocolo": porta_info.get("protocolo", "tcp")
                }
                
                if porta in [80, 443, 8080, 8443]:
                    servicos["web"].append(servico_info)
                elif porta in [3306]:
                    servicos["banco_dados"].append(servico_info)
                elif porta in [22, 23, 3389, 5900]:
                    servicos["remote_access"].append(servico_info)
                elif porta in [21, 139, 445]:
                    servicos["file_transfer"].append(servico_info)
                else:
                    servicos["outros"].append(servico_info)
        
        return servicos
    
    def _identificar_riscos(self, resultados):
        riscos = []
        
        for resultado in resultados:
            alvo = resultado.get("alvo", "")
            for porta_info in resultado.get("portas", []):
                porta = porta_info.get("porta")
                if porta in self.SERVICOS_DE_RISCO:
                    risco = {
                        "alvo": alvo,
                        "porta": porta,
                        "servico": self.SERVICOS_DE_RISCO[porta],
                        "severidade": self._determinar_severidade(porta),
                        "descricao": self._descricao_risco(porta),
                        "recomendacao": self._recomendacao_risco(porta)
                    }
                    riscos.append(risco)
        
        return riscos
    
    def _determinar_severidade(self, porta):
        if porta in [21, 23]:
            return "alta"
        elif porta in [135, 139, 445, 3389]:
            return "media"
        return "baixa"
    
    def _descricao_risco(self, porta):
        descricoes = {
            21: "FTP exposto - tráfego não criptografado",
            23: "Telnet exposto - credenciais em texto claro",
            135: "Microsoft RPC exposto",
            139: "NetBIOS exposto",
            445: "SMB/CIFS exposto - potencial para exploração",
            3389: "RDP (Remote Desktop) exposto"
        }
        return descricoes.get(porta, f"Serviço potencialmente inseguro na porta {porta}")
    
    def _recomendacao_risco(self, porta):
        recomendacoes = {
            21: "Considerar substituir por SFTP ou FTP over TLS",
            23: "Substituir por SSH",
            135: "Restringir acesso à rede interna",
            139: "Desabilitar NetBIOS se não necessário",
            445: "Aplicar hardening do SMB e restringir acesso",
            3389: "Usar VPN ou bastion host para acesso RDP"
        }
        return recomendacoes.get(porta, "Revisar necessidade de exposição deste serviço")
    
    def _gerar_recomendacoes(self, analise):
        recomendacoes = []
        riscos = analise.get("riscos_potenciais", [])
        estatisticas = analise.get("estatisticas_gerais", {})
        
        if any(r["severidade"] == "alta" for r in riscos):
            recomendacoes.append("Serviços com severidade ALTA detectados. Priorizar correção.")
        
        if riscos:
            recomendacoes.append(f"Total de riscos identificados: {len(riscos)}")
        
        if estatisticas.get("total_portas", 0) > 50:
            recomendacoes.append("Número elevado de portas abertas. Considerar redução da superfície de ataque.")
        
        return recomendacoes
    
    def _gerar_resumo(self, analise):
        estatisticas = analise.get("estatisticas_gerais", {})
        riscos = analise.get("riscos_potenciais", [])
        
        return {
            "alvos_analisados": estatisticas.get("total_alvos", 0),
            "portas_encontradas": estatisticas.get("total_portas", 0),
            "riscos_identificados": len(riscos),
            "riscos_altos": sum(1 for r in riscos if r.get("severidade") == "alta"),
            "riscos_medios": sum(1 for r in riscos if r.get("severidade") == "media"),
            "status": "CRITICO" if any(r.get("severidade") == "alta" for r in riscos) else "ATENCAO" if riscos else "NORMAL"
        }
    
    def _salvar_analise(self, analise, output_dir):
        analise_dir = os.path.join(output_dir, "analise")
        os.makedirs(analise_dir, exist_ok=True)
        
        arquivo_analise = os.path.join(analise_dir, "analise_detalhada.json")
        with open(arquivo_analise, 'w', encoding='utf-8') as f:
            json.dump(analise, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Análise salva em: {arquivo_analise}")