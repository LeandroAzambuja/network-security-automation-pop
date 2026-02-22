import requests


class DefectDojoAPI:
    def __init__(self, base_url, api_token):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Token {api_token}",
        }

    # --------- ENGAGEMENT ---------

    def create_engagement(self, product_id, name, start_date, end_date):
        url = f"{self.base_url}/api/v2/engagements/"
        payload = {
            "product": product_id,
            "name": name,
            "target_start": start_date,
            "target_end": end_date,
            "status": "In Progress",
        }

        r = requests.post(
            url,
            headers={**self.headers, "Content-Type": "application/json"},
            json=payload,
            timeout=10,
        )

        if r.status_code not in (200, 201):
            if "already exists" not in r.text:
                print("ENGAGEMENT CREATE STATUS:", r.status_code)
                print("ENGAGEMENT CREATE RESPONSE:", r.text)
                r.raise_for_status()

        return True

    # --------- IMPORT CSV ---------

    def import_scan(
        self,
        engagement_id,
        file_path,
        scan_type="Generic Findings Import",
        active=True,
        verified=False,
    ):
        url = f"{self.base_url}/api/v2/import-scan/"

        data = {
            "engagement": engagement_id,
            "scan_type": scan_type,
            "active": str(active).lower(),
            "verified": str(verified).lower(),
            "close_old_findings": "false",
        }

        with open(file_path, "rb") as f:
            files = {
                "file": (file_path.split("/")[-1], f),
            }

            r = requests.post(
                url,
                headers=self.headers,
                files=files,
                data=data,
                timeout=60,
            )

        print("IMPORT STATUS:", r.status_code)
        print("IMPORT RESPONSE:", r.text)

        if r.status_code not in (200, 201):
            r.raise_for_status()

        return r.json()
