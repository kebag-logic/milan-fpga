#!/usr/bin/env python3
"""Print status/conclusion/name for a GitHub check-runs JSON document."""
import json
import sys
for r in sorted(json.load(open(sys.argv[1]))["check_runs"], key=lambda r: r["name"]):
    print(f"{r['status']:11} {str(r['conclusion']):8} {r['name']}")
