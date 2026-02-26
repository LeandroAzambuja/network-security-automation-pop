import os
import json
import time
import signal

LOCK_FILE = "/tmp/scanctl.lock"
STATE_FILE = "/tmp/scanctl_state.json"

def acquire_lock(meta: dict):
    if os.path.exists(LOCK_FILE):
        return False

    pid = os.getpid()
    with open(LOCK_FILE, "w") as f:
        f.write(str(pid))

    meta["pid"] = pid
    meta["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(STATE_FILE, "w") as f:
        json.dump(meta, f, indent=2)

    return True

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

def status():
    if not os.path.exists(LOCK_FILE):
        return None
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"status": "running"}

def cancel():
    if not os.path.exists(LOCK_FILE):
        return False, "Nenhuma execução em andamento."

    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
            pid = state.get("pid")

        if pid:
            os.kill(pid, signal.SIGTERM)

    except Exception:
        pass

    release_lock()
    return True, "Execução cancelada com sucesso."
