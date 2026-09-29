#!/usr/bin/env python3
"""Item 6 inventory and adversarial probe (reviewer-owned oracle).

Collects (1) every hex/MAC builder field value in every tracked YAML file,
(2) every quoted spelling documented in the three rule pages and every
YAML example in tracked Markdown for those fields, (3) the reviewer's own
adversarial spellings; judges each with the base and head parsers
(item6_judge.py, run once per tree) and with an independent oracle written
from disposition 5882165062. Prints one row per case and a summary.

usage: item6_inventory.py <head-root> <base-root> <workdir>
"""
import json, re, subprocess, sys
from pathlib import Path
import yaml

HEAD, BASE, WORK = (Path(a).resolve() for a in sys.argv[1:4])
JUDGE = Path(__file__).with_name("item6_judge.py")
HEXD = set("0123456789abcdefABCDEF")
FIELD_KIND = {"mac_address": "mac", "stream_dmac_base": "dmac", "vendor_oui": "oui",
              "entity_capabilities": "caps", "entity_model_id": "eui64", "model_id_pin": "eui64",
              "entity_id": "eui64", "crf_format": "eui64", "formats": "eui64", "format": "eui64"}
WIDTH = {"dmac": 12, "eui64": 16, "oui": 6, "caps": 8}
SELECTORS = {"hash-derived", "mac-derived", "maap"}

def hex_text_digits(s):
    """Independent reading of the disposition's hex text: optional 0x/0X, then
    ASCII hex digits, single underscores only between two digits."""
    body = s[2:] if s[:2] in ("0x", "0X") else s
    if not body or body[0] == "_" or body[-1] == "_" or "__" in body:
        return None
    if any(c not in HEXD and c != "_" for c in body):
        return None
    return body.replace("_", "")

def oracle(kind, s):
    if kind == "mac":
        for sep in (":", "-"):
            parts = s.split(sep)
            if len(parts) == 6 and all(len(p) == 2 and set(p) <= HEXD for p in parts):
                other = "-" if sep == ":" else ":"
                if other not in s:
                    return "SHAPE-OK"
        d = hex_text_digits(s)
        return "SHAPE-OK" if d is not None and len(d) == 12 else "REFUSE"
    if kind == "dmac" and s.strip().lower() == "maap":
        return "SHAPE-OK"
    d = hex_text_digits(s)
    return "SHAPE-OK" if d is not None and len(d) <= WIDTH[kind] else "REFUSE"

cases = []  # (source, kind, spelling)
def walk(node, path, src):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, path + [str(k)], src)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + [str(i)], src)
    elif isinstance(node, str):
        keys = [p for p in path if not p.isdigit()]
        kind = FIELD_KIND.get(keys[-1]) if keys else None
        if kind and not (kind == "eui64" and keys[-1] == "format" and "crf_output" not in keys and "clocking" not in keys):
            cases.append((f"{src}:{'.'.join(path)}", kind, node))
        elif re.fullmatch(r"(0[xX])?[0-9A-Fa-f_:-]{6,}", node):
            cases.append((f"{src}:{'.'.join(path)} (hex-looking, unowned field)", "eui64", node))

tracked = subprocess.run(["git", "-C", str(HEAD), "ls-files", "*.yaml", "*.yml"], capture_output=True,
                         text=True, check=True).stdout.split()
class AnyTag(yaml.SafeLoader):
    """SafeLoader that reads unknown tags as plain nodes (e.g. barectf)."""
def _any(loader, suffix, node):
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node, deep=True)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node, deep=True)
    return loader.construct_scalar(node)
AnyTag.add_multi_constructor("", _any)
for rel in tracked:
    for doc in yaml.load_all((HEAD / rel).read_text(), Loader=AnyTag):
        walk(doc, [], rel)

# Documented examples: every quoted token in the three rule pages, judged
# as the kind its sentence names, and YAML example lines in all tracked docs.
docs = {"sw/builder/README-parameters.md": None, "docs/ENDSTATION_BUILDER.md": None,
        "docs/reference/PP_DESCRIPTOR_OWNERSHIP.md": None}
for rel in docs:
    for no, line in enumerate((HEAD / rel).read_text().splitlines(), 1):
        for tok in re.findall(r'`"([^"`]*)"`|`([0-9A-Fa-fxX:_-]{2,})`', line):
            s = tok[0] or tok[1]
            if not s or not any(c in HEXD for c in s):
                continue
            low = line.lower()
            if "mac" in low and "dmac" not in low:
                kind = "mac"
            elif "stream_dmac" in low or "dmac" in low:
                kind = "dmac"
            elif "oui" in low:
                kind = "oui"
            elif "capabilit" in low:
                kind = "caps"
            else:
                kind = "eui64"
            cases.append((f"{rel}:{no} (doc{'' if tok[0] else ', unquoted'})", kind, s))
mds = subprocess.run(["git", "-C", str(HEAD), "ls-files", "*.md"], capture_output=True, text=True,
                     check=True).stdout.split()
for rel in mds:
    if rel.startswith(("protocol-processor/", "gptp-processor/", "external/", "third_party/")):
        continue
    for no, line in enumerate((HEAD / rel).read_text(errors="replace").splitlines(), 1):
        m = re.match(r"\s*-?\s*(mac_address|stream_dmac_base|vendor_oui|entity_capabilities|entity_model_id|"
                     r"model_id_pin|entity_id|crf_format)\s*:\s*(\"[^\"]*\"|'[^']*'|[^\s#]+)", line)
        if m:
            raw = m[2]
            val = yaml.safe_load(raw)
            if isinstance(val, str) and val not in SELECTORS:
                cases.append((f"{rel}:{no} (doc YAML)", FIELD_KIND[m[1]], val))

ADVERSARIAL = {
 "mac": ["0x0200_0000_0002", "0X020000000002", "02_00_00_00_00_02", "0x0_2_0_0_0_0_0_0_0_0_0_2",
         "0x0x020000000002", "0x_020000000002", "020000000002_", "_020000000002", "0200__00000002",
         "02:00:00:00:00:02:", ":02:00:00:00:00:02", "02::00:00:00:00:02", "02:00:00:00:00:2",
         "02:00:00:00:00:002", "02.00.00.00.00.02", "0200.0000.0002", "02 00 00 00 00 02",
         "02:00:00:00:00:02\x00", "０２:00:00:00:00:02", "02:00:00:00:00:0２",
         "٠٢٠٠٠٠٠٠٠٠٠٢",
         "020000000002\n", " 020000000002", "020000000002​", "−020000000002",
         "020000000002\r", "0x", "", "02:00:00:00:00:02 ", "02-00-00-00-00:02", "02:00-00-00-00-02",
         "0x02-00-00-00-00-02", "02:_00:00:00:00:02", "0200_0000_0002_", "0x0200_0000_00002",
         "0a:1B:2c:3D:4e:5F", "0A1B2C3D4E5F", "0b0000000002", "2", "-2", "0:2", "2:0:0:0:0:2",
         "02:00:00:00:02", "+020000000002", "00000000000002", "0x00020000000002", "0200000000 02",
         "02:00:00:00:00:02\t", "0x0200-0000-0002", "02:00:00:00:00:02_", "02__00"],
 "dmac": ["0x91E0F000FE01", "91E0F000FE01", "0x91E0_F000_FE01", "91:E0:F0:00:FE:01",
          "0x091E0F000FE01", "+0x91E0F000FE01", " 0x91E0F000FE01", "0x91E0F000FE01 ", "0x10000000000",
          "0x91e0f000fe01", "0X91E0F000FE01", "0x91E0F000FE01\n", "0x_91E0F000FE01", " MAAP", "maap"],
 "eui64": ["0x001BC50AC1000005", "001BC50AC1000005", "0x001B_C50A_C100_0005", "0x0001BC50AC1000005",
           "1234567890123456", "0x1", "1", "0x", "+0x1", "-1", " 0x1", "0x1 ", "0x1_", "0x__1",
           "0xFFFF_FFFF_FFFF_FFFF", "0x1FFFFFFFFFFFFFFFF", "0x0205022000806000",
           "0x041060010000BB80", "0x١", "0x1́", "0x00:1B:C5:0A:C1:00:00:05"],
 "oui": ["0x123456", "123456", "0x12_3456", "1BC5", "0x0123456", "0x1234567", "-1", "+1BC5",
         " 1BC5", "1BC5 ", "0x1_", "0x", "001B_C5", "0x001BC5"],
 "caps": ["0x00000000", "0x0000_0000", "FFFFFFFF", "0x1FFFFFFFF", "0x0FFFFFFFF", "+0x1", "-0",
          "0x", "0x_1", "1__2"],
}
for kind, spellings in ADVERSARIAL.items():
    for s in spellings:
        cases.append(("reviewer adversarial", kind, s))

WORK.mkdir(parents=True, exist_ok=True)
(WORK / "spellings.json").write_text(json.dumps([[k, s] for _, k, s in cases]))
for tag, root in (("head", HEAD), ("base", BASE)):
    subprocess.run([sys.executable, str(JUDGE), str(root), str(WORK / "spellings.json"),
                    str(WORK / f"verdicts_{tag}.json")], check=True)
head = json.loads((WORK / "verdicts_head.json").read_text())
base = json.loads((WORK / "verdicts_base.json").read_text())
mismatch = changed_tracked = crash = 0
for (src, kind, s), (_, _, vh), (_, _, vb) in zip(cases, head, base):
    want = oracle(kind, s)
    shape_ok_head = vh.startswith("ACCEPT") or (
        vh.startswith("REFUSE") and any(w in vh for w in ("I/G bit", "all-zero", "MULTICAST", "not a MULTICAST")))
    agree = (want == "SHAPE-OK") == shape_ok_head
    if not agree:
        mismatch += 1
    if vh.startswith("CRASH") or vb.startswith("CRASH"):
        crash += 1
    tracked_row = not src.startswith("reviewer")
    same = (vh.split(" ", 1)[0] == vb.split(" ", 1)[0]) and (not vh.startswith("ACCEPT") or vh == vb)
    if tracked_row and not same:
        changed_tracked += 1
    flag = ("" if agree else " <<ORACLE-DISAGREES>>") + ("" if (not tracked_row or same) else " <<TRACKED-VERDICT-CHANGED>>")
    print(f"{src}\t{kind}\t{s!r}\toracle={want}\thead={vh[:90]}\tbase={vb[:60]}{flag}")
print(f"SUMMARY cases={len(cases)} tracked_or_documented={sum(not c[0].startswith('reviewer') for c in cases)} "
      f"oracle_disagreements={mismatch} tracked_or_documented_verdict_changes={changed_tracked} crashes={crash}")
