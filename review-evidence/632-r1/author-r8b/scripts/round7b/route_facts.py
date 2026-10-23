#!/usr/bin/env python3
"""Round 7b: the facts the #234 findings section quotes, read from one bank
directory (scripts/round7/vivado_bank.sh layout): per-corner WNS/WHS, the
worst setup and hold paths, the routed hierarchy rows, the logs' Synth
8-4445/8-6901 diagnostics, and every recorded memory image rehashed.
usage: route_facts.py <bank dir>
"""
import hashlib, json, re, sys
from pathlib import Path

bank = Path(sys.argv[1])
g1 = bank / "w1/ax7101/gateware"
runs = {"route-1x1": g1, "ooc-1x1": bank / "w1/ax7101-ooc",
        "rtl-8x8": bank / "w8/ax8x8-rtl", "ooc-8x8": bank / "w8/ax8x8-ooc"}


def summary(rpt):
    lines = rpt.read_text().splitlines()
    for i, l in enumerate(lines):
        if l.startswith("| Design Timing Summary"):
            v = lines[i + 6].split()
            return float(v[0]), float(v[4])
    raise SystemExit(f"no summary in {rpt}")


print("== route corners (WNS, WHS ns)")
for c in ("Slow_0C", "Slow_85C", "Fast_0C", "Fast_85C"):
    w, h = summary(g1 / f"alinx_ax7101_signoff_{c}_timing.rpt")
    print(f"{c} {w:+.3f} {h:+.3f}")


def worst_paths(rpt):
    """Every path block of report_timing_summary; the least slack per path type."""
    blocks = re.split(r"\n(?=Slack \()", rpt.read_text())[1:]
    best = {}
    for b in blocks:
        def field(key):
            mm = re.search(rf"^\s*{key}:\s+(.*)$", b, re.M)
            return mm.group(1).strip() if mm else None
        slack = float(re.match(r"Slack \(\w+\) :\s+(-?[0-9.]+)ns", b).group(1))
        kind = "setup" if (field("Path Type") or "").startswith("Setup") else "hold" if (field("Path Type") or "").startswith("Hold") else None
        if kind and (kind not in best or slack < best[kind]["slack"]):
            best[kind] = {"slack": slack, "source": field("Source"), "destination": field("Destination"),
                          "group": field("Path Group"), "type": field("Path Type"),
                          "data path delay": field("Data Path Delay"), "logic levels": field("Logic Levels")}
    return best


print("== worst setup and hold (route signoff, all corners)")
print(json.dumps(worst_paths(g1 / "baseline_timing.rpt"), indent=1))

print("== routed hierarchy rows (post-place): LUT FF RAMB36 RAMB18 DSP")
rows = (g1 / "alinx_ax7101_utilization_hierarchical_place.rpt").read_text().splitlines()
for want in ("milan_datapath ", "pp_shadow ", "g_maap.maap_engine ", "g_mmcm_servo.mmcm_servo ",
             "g_pres_crf.pres_round ", "render_queue ", "media_domain_event ", "crf_tx "):
    for r in rows:
        cells = [c.strip() for c in r.split("|")]
        if len(cells) > 10 and cells[1] + " " == want:
            print(f"{cells[1]:28s} LUT {cells[3]} FF {cells[7]} RAMB36 {cells[8]} RAMB18 {cells[9]} DSP {cells[10]}")
            break

print("== log diagnostics, peaks, minutes")
for n, d in runs.items():
    log = d / "baseline.log"
    if not log.exists():
        print(n, "missing"); continue
    t = log.read_text(errors="replace")
    n4445 = len(re.findall(r"^(WARNING|ERROR|CRITICAL WARNING|INFO): \[Synth 8-4445\]", t, re.M))
    l6901 = sorted({re.sub(r"\s+", " ", m.group(0))[:160] for m in re.finditer(r"WARNING: \[Synth 8-6901\][^\n]*", t)})
    peaks = [float(x) for x in re.findall(r"peak = ([0-9.]+)", t)]
    print(f"{n}: Synth 8-4445 x{n4445}; Synth 8-6901 x{len(re.findall(r'^WARNING: \[Synth 8-6901\]', t, re.M))}; peak {max(peaks) if peaks else 0:.0f} MB; "
          f"log sha256 {hashlib.sha256(log.read_bytes()).hexdigest()} {log.stat().st_size} bytes")
    for l in l6901:
        print("   ", re.sub(r"/(data|home|tmp)/[^ ]*/", "<path>/", l))

print("== memory images rehashed")
ok = bad = 0
for n, d in runs.items():
    man = d / "baseline_images.json"
    if not man.exists():
        continue
    for e in json.loads(man.read_text()):
        p = Path(e["path"])
        if not p.exists():
            # the bank unlinks the ROM links into its clone after the run; the files stay in its roms dir
            alt = [q for q in (bank / "w1/roms" / p.name, bank / "w8/roms" / p.name) if q.exists()]
            if "/sw/builder/out/" in str(p):
                rest = str(p).split("/sw/builder/out/", 1)[1]
                alt = [q for q in (bank / "w1/builder" / rest, bank / "w8/builder" / rest) if q.exists()]
            p = alt[0] if alt and hashlib.sha256(alt[0].read_bytes()).hexdigest() == e["sha256"] else (alt[-1] if alt else p)
        h = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "missing"
        if h == e["sha256"]:
            ok += 1
        else:
            bad += 1
            print("MISMATCH", n, p.name, h, e["sha256"])
print(f"{ok} match, {bad} differ")
