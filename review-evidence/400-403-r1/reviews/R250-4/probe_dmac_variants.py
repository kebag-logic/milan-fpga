"""Exercise the edited _srp_dmac and posture paths on variant configs at two commits.

Usage: python3 -B probe_dmac_variants.py <base-tree> <head-tree> <work-dir>

The five shipped configs all carry a numeric srp.stream_dmac_base, so a
regeneration of them never takes the `maap` branch whose unread
`stream_dmac_alloc` normalisation the delta removed. Each variant here is
endstation_arty_current.yaml with one override. For every variant the real
build() runs in both trees (artifacts to separate directories, in-memory
sweep fragment and shape copies captured); accepted variants must emit
byte-identical artifacts at both commits, and refused variants must be
refused at both commits with the same exception type. The returned cfg dict
is also compared, and must differ at most by the removed srp key (the
top-level `source` path is excluded because it names the per-tree file).
"""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml

base, head, work = (Path(a).resolve() for a in sys.argv[1:4])
VARIANTS = {
    "numeric": {},
    "maap_lower": {"srp": {"stream_dmac_base": "maap"}},
    "maap_mixed_ws": {"srp": {"stream_dmac_base": "  MaAp "}},
    "rx_mac_filter_absent": {"board": {"features": {"rx_mac_filter": False}}},
    "refuse_maap_false_numeric": {"board": {"features": {"maap": False}}},
    "refuse_maap_false_dynamic": {"board": {"features": {"maap": False}},
                                  "srp": {"stream_dmac_base": "maap"}},
    "refuse_rx_hardware": {"platform": {"rx_address_filter": "hardware"}},
    "refuse_rx_hardware_filter_absent": {"platform": {"rx_address_filter": "hardware"},
                                         "board": {"features": {"rx_mac_filter": False}}},
    "refuse_unicast_dmac": {"srp": {"stream_dmac_base": "0x90E0F000FE01"}},
}

CHILD = r"""
import json, sys, hashlib, traceback
from pathlib import Path
sys.path.insert(0, 'sw/builder')
import endstation_builder as eb
cfg_path, out = sys.argv[1], sys.argv[2]
try:
    r = eb.build(cfg_path, out)
except Exception as e:
    print(json.dumps(dict(ok=False, exc=type(e).__name__, msg=str(e)[:400])))
    sys.exit(0)
d = Path(out) / r['cfg']['name']
(d / 'sweep_opts.sh').write_text(r['sweep_opts'])
for key in ('cfg_adp_shape_svh', 'rtl_csr_defaults_svh'):
    if key in r['paths']:
        (d / (key + '.copy')).write_bytes(Path(r['paths'][key]).read_bytes())
def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (int, float, str, bool)) or o is None:
        return o
    return repr(o)
print(json.dumps(dict(ok=True, cfg=clean(r['cfg']))))
"""


def merge(dst, src):
    for k, v in src.items():
        if isinstance(v, dict):
            merge(dst.setdefault(k, {}), v)
        else:
            dst[k] = v


def manifest(root: Path) -> dict:
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def strip_source(root: Path) -> None:
    # Emitted banners record the absolute config path; the two trees differ
    # there by construction, so drop exactly those lines before hashing.
    for p in root.rglob("*"):
        if p.is_file():
            data = p.read_bytes()
            kept = b"".join(l for l in data.splitlines(True)
                            if b"cfg-variant.yaml" not in l)
            p.write_bytes(kept)


raw0 = yaml.safe_load((base / "configs/endstation_arty_current.yaml").read_text())
raw1 = yaml.safe_load((head / "configs/endstation_arty_current.yaml").read_text())
assert raw0 == raw1
report, ok = {}, True
for name, over in VARIANTS.items():
    raw = copy.deepcopy(raw0)
    merge(raw, over)
    rec = {}
    for tag, tree in (("base", base), ("head", head)):
        vdir = work / name / tag
        vdir.mkdir(parents=True)
        cfg = vdir / "cfg-variant.yaml"
        cfg.write_text(yaml.safe_dump(raw, sort_keys=False))
        out = vdir / "out"
        out.mkdir()
        p = subprocess.run([sys.executable, "-B", "-c", CHILD, str(cfg), str(out)],
                           cwd=tree, capture_output=True, text=True)
        res = json.loads(p.stdout.strip().splitlines()[-1]) if p.returncode == 0 else \
            dict(ok=False, exc="child-crash", msg=p.stderr[-400:])
        if res["ok"]:
            strip_source(out)
            res["files"] = manifest(out)
        rec[tag] = res
    b, h = rec["base"], rec["head"]
    v = dict(accepted_base=b["ok"], accepted_head=h["ok"])
    if b["ok"] and h["ok"]:
        v["files"] = len(h["files"])
        v["artifact_differences"] = sorted(k for k in set(b["files"]) | set(h["files"])
                                           if b["files"].get(k) != h["files"].get(k))
        sb, sh = b["cfg"]["srp"], h["cfg"]["srp"]
        v["srp_keys_only_in_base"] = sorted(set(sb) - set(sh))
        v["srp_keys_only_in_head"] = sorted(set(sh) - set(sb))
        v["base_stream_dmac_alloc"] = sb.get("stream_dmac_alloc")
        v["srp_common_values_equal"] = all(sb[k] == sh[k] for k in set(sb) & set(sh))
        # `source` is the absolute variant path, which differs per tree by
        # construction; every other top-level key must be equal.
        rest_b = {k: x for k, x in b["cfg"].items() if k not in ("srp", "source")}
        rest_h = {k: x for k, x in h["cfg"].items() if k not in ("srp", "source")}
        v["cfg_outside_srp_equal"] = rest_b == rest_h
        good = (not v["artifact_differences"] and v["srp_common_values_equal"]
                and v["cfg_outside_srp_equal"] and not v["srp_keys_only_in_head"]
                and v["srp_keys_only_in_base"] in ([], ["stream_dmac_alloc"])
                and not name.startswith("refuse_"))
    else:
        v["base_exc"] = b.get("exc"), b.get("msg")
        v["head_exc"] = h.get("exc"), h.get("msg")
        good = (not b["ok"] and not h["ok"] and b["exc"] == h["exc"] == "ConfigError"
                and name.startswith("refuse_"))
    v["pass"] = good
    ok &= good
    report[name] = v
report["verdict"] = "PASS" if ok else "FAIL"
print(json.dumps(report, indent=1))
sys.exit(0 if ok else 1)
