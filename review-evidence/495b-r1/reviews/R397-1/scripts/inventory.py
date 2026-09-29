#!/usr/bin/env python3
"""Reviewer inventory for #495 item 6: every tracked YAML value in a quoted
hex/MAC builder field, judged by the base and head parsers, plus a full
load_config comparison of every tracked configuration.

Usage: inventory.py <head-tree> <base-tree> <out.json>
Runs each tree's parser in its own subprocess (same module name).
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

FIELDS = {"mac_address", "stream_dmac_base", "entity_id", "entity_model_id",
          "model_id_pin", "vendor_oui", "entity_capabilities", "formats",
          "crf_format", "format"}
SELECTORS = {"hash-derived", "mac-derived", "maap"}

JUDGE = r'''
import json, sys
from pathlib import Path
tree = Path(sys.argv[1]); sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
items = json.loads(sys.stdin.read())
def judge(key, v):
    try:
        if key == "mac_address":
            return "accept 0x%012x" % eb._mac48(v, key)
        if key == "stream_dmac_base":
            if isinstance(v, str) and v.strip().lower() == "maap":
                return "selector"
            if hasattr(eb, "_hex_text"):
                return "accept 0x%012x" % eb._hex_text(v, 48, key, "a hex MAC-48")
            n = eb._eui64(v, key)
            if n > 0xFFFFFFFFFFFF: return "refuse wider than MAC-48"
            return "accept 0x%012x" % n
        if key == "vendor_oui":
            return "accept 0x%x" % eb._declared_uint(v, 24, key)
        if key == "entity_capabilities":
            return "accept 0x%x" % eb._declared_uint(v, 32, key)
        if v in ("hash-derived", "mac-derived"):
            return "selector"
        return "accept 0x%016x" % eb._eui64(v, key)
    except eb.ConfigError as exc:
        return "refuse " + str(exc)
out = [judge(k, v) for k, v in items]
loads = {}
for cfg in sorted((tree / "configs").glob("endstation_*.yaml")):
    c = eb.load_config(cfg)
    keep = {k: c[k] for k in ("platform", "entity", "srp", "clocking", "streams") if k in c}
    loads[cfg.name] = json.loads(json.dumps(keep, default=str, sort_keys=True))
print(json.dumps({"verdicts": out, "loads": loads}))
'''


def walk(node, path, found):
    if isinstance(node, dict):
        for k, v in node.items():
            p = path + [str(k)]
            if k in FIELDS:
                if isinstance(v, list):
                    for i, e in enumerate(v):
                        found.append((p + [str(i)], k, e))
                elif not isinstance(v, (dict,)):
                    found.append((p, k, v))
            walk(v, p, found)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + [str(i)], found)


def main() -> int:
    import yaml
    head, base, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    files = subprocess.run(["git", "-C", str(head), "ls-files", "*.yaml", "*.yml"],
                           text=True, capture_output=True, check=True).stdout.split()
    found = []
    for rel in files:
        try:
            docs = list(yaml.safe_load_all((head / rel).read_text()))
        except Exception as exc:  # noqa: BLE001 - record, never hide
            print(f"UNPARSED {rel}: {type(exc).__name__}")
            continue
        for doc in docs:
            hits = []
            walk(doc, [], hits)
            for p, k, v in hits:
                # 'format' only counts under crf_output (clocking.crf_output.format)
                if k == "format" and (len(p) < 2 or p[-2] != "crf_output"):
                    continue
                if k == "formats" and not isinstance(v, str):
                    pass
                found.append((rel, ".".join(p), k, v))
    items = [(k if k != "format" else "crf_format", v) for _, _, k, v in found]
    items = [(k if k != "formats" else "format_word", v) for k, v in items]
    res = {}
    for name, tree in (("head", head), ("base", base)):
        r = subprocess.run([sys.executable, "-B", "-c", JUDGE, str(tree)],
                           input=json.dumps(items), text=True, capture_output=True, cwd=tree)
        if r.returncode:
            print(r.stderr)
            return 2
        res[name] = json.loads(r.stdout)
    rows, changed = [], 0
    for (rel, path, k, v), hb, bb in zip(found, res["head"]["verdicts"], res["base"]["verdicts"]):
        same = hb.split()[0] == bb.split()[0] and (hb.split()[0] != "accept" or hb == bb)
        changed += not same
        rows.append(dict(file=rel, path=path, value=v, base=bb, head=hb, same=same))
        print(f"{'SAME' if same else 'CHANGED'} {rel} {path} = {v!r}: base[{bb}] head[{hb}]")
    loads_equal = res["head"]["loads"] == res["base"]["loads"]
    print(f"tracked YAML files={len(files)} field values={len(found)} verdict changes={changed}")
    print(f"load_config of {len(res['head']['loads'])} tracked configurations identical base vs head: {loads_equal}")
    out.write_text(json.dumps(dict(rows=rows, loads_equal=loads_equal), indent=1, default=str))
    return 0 if changed == 0 and loads_equal else 1


if __name__ == "__main__":
    sys.exit(main())
