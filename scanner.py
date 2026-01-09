import nmap
import re

def is_valid_target(target: str) -> bool:
    # Allow IPs and domains (basic validation)
    pattern = r"^[a-zA-Z0-9\.\-]+$"
    return re.match(pattern, target) is not None

def scan_target(target: str):
    if not is_valid_target(target):
        return {"error": "Invalid target"}

    nm = nmap.PortScanner()

    try:
        nm.scan(
            hosts=target,
            arguments="-sV -T4"
        )
    except Exception as e:
        return {"error": str(e)}

    results = {}

    for host in nm.all_hosts():
        results[host] = {
            "state": nm[host].state(),
            "protocols": {}
        }

        for proto in nm[host].all_protocols():
            ports = []
            for port, data in nm[host][proto].items():
                ports.append({
                    "port": port,
                    "state": data.get("state"),
                    "service": data.get("name"),
                    "version": data.get("version", "")
                })
            results[host]["protocols"][proto] = ports

    return results
