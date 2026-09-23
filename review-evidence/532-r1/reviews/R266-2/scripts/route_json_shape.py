#!/usr/bin/env python3
"""Redacted shape of this host's `ip -json -4|-6 route show default` output.

Unprivileged and read-only. Prints only key names, value types, the route
`type` field if present, and whether each route or next hop names a `dev`, so
no interface name or address is recorded. It re-derives, independently of the
runner, what its uplink discovery would conclude: how many distinct
interfaces a unicast default route names, and whether any would be refused.
"""
import json
import re
import subprocess

name_ok = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,14}$")
found = []
for family in ("-4", "-6"):
    result = subprocess.run(["ip", "-json", family, "route", "show", "default"],
                            capture_output=True, text=True, check=False)
    print(f"family {family}: rc={result.returncode}")
    routes = json.loads(result.stdout.strip() or "[]")
    print(f"  top-level type={type(routes).__name__} routes={len(routes)}")
    for index, route in enumerate(routes):
        keys = sorted(route)
        print(f"  route {index}: keys={keys} type={route.get('type', '<absent: unicast>')}"
              f" dev={'present' if isinstance(route.get('dev'), str) else 'absent'}"
              f" nexthops={'present' if 'nexthops' in route else 'absent'}")
        if route.get("type", "unicast") != "unicast":
            continue
        for hop in route.get("nexthops", [route]):
            dev = hop.get("dev")
            if isinstance(dev, str) and dev not in found:
                found.append(dev)
print(f"distinct unicast default-route interfaces: {len(found)}; "
      f"quotable={all(name_ok.fullmatch(d) and d != 'lo' for d in found)}")
