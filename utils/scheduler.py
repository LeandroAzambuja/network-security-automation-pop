import subprocess
import json
import os

CRON_TAG = "# scanctl-managed"
STATE_FILE = "/tmp/scanctl_state.json"

def _get_crontab():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else ""

def _write_crontab(content):
    p = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
    p.communicate(content)

def schedule(command, freq_hours, days):
    cron = _get_crontab()
    cron = "\n".join([l for l in cron.splitlines() if CRON_TAG not in l])

    hour = f"*/{freq_hours}"
    entry = f"0 {hour} * * * {command} {CRON_TAG}"

    cron = cron + "\n" + entry + "\n"
    _write_crontab(cron)

    with open(STATE_FILE, "w") as f:
        json.dump({
            "status": "scheduled",
            "command": command,
            "frequency_hours": freq_hours,
            "duration_days": days
        }, f, indent=2)

def cancel():
    cron = _get_crontab()
    cron = "\n".join([l for l in cron.splitlines() if CRON_TAG not in l])
    _write_crontab(cron)

    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

def status():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return None
