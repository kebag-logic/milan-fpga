#!/usr/bin/env python3
"""A stand-in consumer of the export the parent is to read: load
hdl/aecp/ucode/aecp_commands.json with the standard library only, check the
schema tag, and build the per-(message, opcode) table a firmware dispatcher
would need. Usage: python3 -I export_consumer.py PATH_TO_JSON"""
import json, sys
t = json.load(open(sys.argv[1], encoding="utf-8"))
assert t["schema"] == "aecp-command-table/1", t["schema"]
codes = {n: r["code"] for n, r in t["status_codes"].items()}
hz = t["hazard_classes"]
rows = {}
for c in t["commands"]:
    key = (c["message"], int(c["opcode"], 16))
    assert key not in rows, key
    rows[key] = dict(name=c["name"], cmd_cdl=c["command"]["cdl"], rsp_cdl=c["response"]["cdl"],
                     per=c["response"].get("per"), echo=bool(c["response"].get("echo")),
                     status=sorted(codes[s] for s in c["status"] + t["common_status"][c["message"]]),
                     hazard=hz[c["hazard"]], lock=c["lock"],
                     notify=(c["notify"] or {}).get("kind"))
for (m, op), r in sorted(rows.items()):
    print(f"{m} 0x{op:04X} {r['name']:36} cmd {r['cmd_cdl']:3} rsp {r['rsp_cdl']:3}"
          f"{' +' + str(r['per']) + 'N' if r['per'] else ''}{' echo' if r['echo'] else ''}"
          f" status {r['status']} hz {r['hazard']} lock {int(r['lock'])} notify {r['notify']}")
print(f"export: {len(rows)} commands ({sum(m == 'AEM' for m, _ in rows)} AEM, "
      f"{sum(m == 'MVU' for m, _ in rows)} MVU), {len(codes)} status codes, consumable with the standard library")
