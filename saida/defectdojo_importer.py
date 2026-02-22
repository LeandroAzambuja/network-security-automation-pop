import os
from datetime import date
from saida.defectdojo_api import DefectDojoAPI


def importar_para_defectdojo(csv_path, config):
    """
    Wrapper isolado para importação no DefectDojo.
    Integração determinística via engagement ID.
    """

    if not config.get("enabled", False):
        print("[DefectDojo] Integração desabilitada.")
        return

    api_url = config["api_url"]
    api_token = os.environ.get(config["api_token_env"])

    if not api_token:
        raise RuntimeError("DEFECTDOJO_API_TOKEN não definido no ambiente")

    product_id = config["product_id"]

    today = date.today().isoformat()
    engagement_name = f"Scan automatizado - {today}"

    dd = DefectDojoAPI(api_url, api_token)

    # 1) cria engagement
    dd.create_engagement(
        product_id=product_id,
        name=engagement_name,
        start_date=today,
        end_date=today,
    )

    # 2) buscar ID do engagement criado (determinístico)
    engagement_id = None

    url = f"{api_url.rstrip('/')}/api/v2/engagements/"
    headers = {"Authorization": f"Token {api_token}"}

    import requests
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    data = r.json()["results"]

    for e in data:
        if e["name"] == engagement_name and e["product"] == product_id:
            engagement_id = e["id"]
            break

    if not engagement_id:
        raise RuntimeError("Não foi possível localizar o engagement criado.")

    # 3) importar CSV usando ID
    result = dd.import_scan(
        engagement_id=engagement_id,
        file_path=csv_path,
        scan_type="Generic Findings Import",
        active=True,
        verified=False,
    )

    print("[DefectDojo] Importação concluída:", result)
