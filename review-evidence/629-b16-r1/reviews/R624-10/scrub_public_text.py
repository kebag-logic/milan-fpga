#!/usr/bin/env python3
"""R624-10: run the repository's identity/privacy scrub, and a host-path sweep, over public text it does not scan.

usage: python3 -I scrub_public_text.py <repo> <out.json> <file> ...

scripts/docs_check.py scrubs tracked files only; a PR body is not tracked. This loads that module from <repo>
and applies scrub_text() to each given file, then lists any absolute host path (a slash path under a system
or user root) and any IPv4 address, with its line. Nothing is written but <out.json>.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

repo, out, files = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
spec = importlib.util.spec_from_file_location("docs_check", repo / "scripts/docs_check.py")
dc = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[0]]
spec.loader.exec_module(dc)
HOST = re.compile(r"(?<![\w.])/(?:home|root|tmp|data|mnt|media|srv|opt|var|Users|run)/[^\s`'\")\]]*")
IPV4 = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
res = []
for f in files:
    p = Path(f)
    text = p.read_text(encoding="utf-8")
    scrub = dc.scrub_text(p.name, text)
    host = [(i, m.group(0)) for i, line in enumerate(text.splitlines(), 1) for m in HOST.finditer(line)]
    ip = [(i, m.group(0)) for i, line in enumerate(text.splitlines(), 1) for m in IPV4.finditer(line)]
    res.append(dict(file=p.name, scrub_findings=scrub, host_paths=host, ipv4=ip))
    print(p.name, "scrub", len(scrub), "host paths", len(host), "ipv4", len(ip))
out.write_text(json.dumps(res, indent=1) + "\n")
