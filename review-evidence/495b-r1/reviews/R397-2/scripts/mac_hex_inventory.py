#!/usr/bin/env python3
"""Re-run the #495 item-6 inventory on a checkout with ITS OWN builder parsers.

A. Every tracked YAML: builder configurations must load; every value under a
   builder MAC/hex key anywhere in any tracked YAML is graded by the parser
   the builder uses for that key.
B. Every tracked Markdown page: every double-quoted token that looks like hex or
   MAC text is graded by both parsers and printed with its location, so a
   documented example can be checked against its documented verdict.
C. Lines the predecessor PRs added (base..pred) that carry such a token.
Usage: mac_hex_inventory.py <repo> <base> <pred>
"""
import re, subprocess, sys, yaml
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); base, pred = sys.argv[2], sys.argv[3]
sys.path.insert(0, str(repo / "sw/builder")); sys.path.insert(0, str(repo))
import endstation_builder as eb

def git(*a):
    return subprocess.run(["/usr/bin/git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout

SELECTORS = {"maap", "hash-derived", "mac-derived", "dynamic"}
WIDTH = {"mac_address": "mac", "stream_dmac_base": 48, "entity_model_id": 64, "model_id_pin": 64,
         "entity_id": 64, "formats": 64, "crf_format": 64, "format": 64, "vendor_oui": 24,
         "entity_capabilities": 32}

def grade(key, v):
    if isinstance(v, str) and v.strip().lower() in SELECTORS:
        return "selector"
    try:
        if WIDTH[key] == "mac":
            eb._mac48(v, key)
        else:
            eb._hex_text(v, WIDTH[key], key, "hex")
        return "ACCEPT"
    except eb.ConfigError as e:
        return f"REFUSE ({e})"

def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in WIDTH:
                for i, item in enumerate(v if isinstance(v, list) else [v]):
                    if isinstance(item, (str, int)) and not isinstance(item, bool):
                        out.append((f"{path}.{k}" + (f"[{i}]" if isinstance(v, list) else ""), k, item))
            walk(v, f"{path}.{k}", out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", out)

class AnyTag(yaml.SafeLoader):
    """SafeLoader that reads an unknown application tag as its plain node."""
def _plain(loader, suffix, node):
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node, deep=True)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node, deep=True)
    return loader.construct_scalar(node)
AnyTag.add_multi_constructor("", _plain)

bad = 0
print("== A. tracked YAML")
for rel in git("ls-files", "*.yaml", "*.yml").split():
    doc = list(yaml.load_all((repo / rel).read_text(), Loader=AnyTag))
    vals = []
    for d in doc:
        walk(d, "", vals)
    loaded = ""
    if rel.startswith("configs/endstation_"):
        try:
            eb.load_config(str(repo / rel)); loaded = " load_config=OK"
        except Exception as e:  # noqa: BLE001
            loaded = f" load_config=FAIL {e}"; bad += 1
    print(f"{rel}: {len(vals)} builder hex/MAC values{loaded}")
    for p, k, v in vals:
        g = grade(k, v)
        if g.startswith("REFUSE"):
            bad += 1
        print(f"   {p} = {v!r}: {g}")
for name in ("SRP_DEFAULTS", "CRF_FORMAT_DEFAULT"):
    obj = getattr(eb, name, None)
    print(f"default {name} = {obj!r}")

TOKEN = re.compile(r'"([^"\n]{1,40})"')
LOOKS = re.compile(r"^[+\-\s]*(?:0[xX])?[0-9A-Fa-f][0-9A-Fa-f_:\-\s]*$")
def md_tokens(text):
    for n, line in enumerate(text.splitlines(), 1):
        for m in TOKEN.finditer(line):
            t = m.group(1)
            if LOOKS.match(t) and re.search(r"[0-9]", t):
                yield n, t

print("\n== B. tracked Markdown double-quoted hex/MAC-like tokens")
for rel in git("ls-files", "*.md").split():
    text = (repo / rel).read_text(errors="replace")
    for n, t in md_tokens(text):
        print(f"{rel}:{n}: {t!r}: mac={grade('mac_address', t).split(' (')[0]} hex64={grade('entity_id', t).split(' (')[0]}")

print(f"\n== C. lines added by {base}..{pred} carrying such tokens (any file)")
diff = subprocess.run(["/usr/bin/git", "-C", str(repo), "diff", "-U0", base, pred], capture_output=True, text=True).stdout
f = None; hits = 0
for line in diff.splitlines():
    if line.startswith("+++ "):
        f = line[6:]
    elif line.startswith("+") and not line.startswith("+++"):
        for _, t in md_tokens(line[1:]):
            hits += 1
            print(f"{f}: {t!r}: mac={grade('mac_address', t).split(' (')[0]} hex64={grade('entity_id', t).split(' (')[0]}")
        if re.search(r"mac_address|stream_dmac_base|entity_model_id|model_id_pin|entity_id|vendor_oui|entity_capabilities|crf_format", line):
            print(f"{f}: builder-key mention: {line[1:120]!r}")
print(f"predecessor-added quoted tokens: {hits}")
print(f"\nTRACKED-YAML REFUSALS OR LOAD FAILURES: {bad}")
sys.exit(1 if bad else 0)
