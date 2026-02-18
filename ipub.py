#!/usr/bin/env python3
import json
import subprocess
import sys
import urllib.parse
import urllib.request

IP_ENDPOINT = "https://skill-issue.space/ip/index.php"
GEO_ENDPOINT = "http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,lat,lon,timezone,isp,org,as,query"


def usage() -> int:
    print("Usage: ipub -v4 | -v6")
    return 2

def run_curl(args: list[str]) -> str:
    r = subprocess.run(["curl", "-sS"] + args, text=True, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "curl failed")
    return r.stdout.strip()

def fetch_ip(version: str) -> str:
    if version == "v4":
        raw = run_curl(["-4", IP_ENDPOINT])
    else:
        raw = run_curl([IP_ENDPOINT])

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON from IP endpoint: {e}")

    if version == "v4":
        ip = data.get("ipv4") or data.get("ip")
    else:
        ip = data.get("ipv6") or data.get("ip")

    if not ip or not isinstance(ip, str):
        raise RuntimeError("IP not found in endpoint response")
    return ip.strip()


def geo_lookup(ip: str) -> dict:
    url = GEO_ENDPOINT.format(ip=urllib.parse.quote(ip))
    req = urllib.request.Request(url, headers={"User-Agent": "ipub/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body)


def main() -> int:
    if len(sys.argv) != 2:
        return usage()

    arg = sys.argv[1].strip().lower()
    if arg not in ("-v4", "-v6"):
        return usage()

    version = "v4" if arg == "-v4" else "v6"

    try:
        ip = fetch_ip(version)
        geo = geo_lookup(ip)

        out = {
            "status": "ok" if geo.get("status") == "success" else "error",
            "ipv4": ip if version == "v4" else None,
            "ipv6": ip if version == "v6" else None,
            "location": {
                "country": geo.get("country"),
                "region": geo.get("regionName"),
                "city": geo.get("city"),
                "lat": geo.get("lat"),
                "lon": geo.get("lon"),
                "timezone": geo.get("timezone"),
            },
            "isp": {
                "isp": geo.get("isp"),
                "org": geo.get("org"),
                "as": geo.get("as"),
            },
        }

        if geo.get("status") != "success":
            out["error"] = geo.get("message") or "geo lookup failed"

        print(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
        return 0 if out["status"] == "ok" else 1

    except Exception as e:
        err = {"status": "error", "error": str(e)}
        print(json.dumps(err, ensure_ascii=False, indent=2) + "\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
