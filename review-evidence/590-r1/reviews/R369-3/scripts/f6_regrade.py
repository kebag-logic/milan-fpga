#!/usr/bin/env python3
"""R369-3 reviewer regrade of the kept round-3 native evidence (F6).

Usage: f6_regrade.py REPO_ROOT AUTHOR_R3_DIR ARCHIVE_MANIFEST_JSON [ARCHIVE_PREFIX]

0. The archive MANIFEST.json (original_sha256, published_sha256,
   path_redacted) is checked against every published author-r3 file; a
   native artifact whose published bytes differ from native-artifacts.json is
   accepted only when that archive entry is path_redacted with
   original_sha256 equal to the native manifest's hash and published_sha256
   equal to the bytes on disk (publication path redaction, disclosed).

1. Every entry of native-artifacts.json: the stored bytes match size/SHA-256.
   A stored `.gz` that the archive does not carry is looked up uncompressed
   under native-evidence-raw/ and must match raw_size/raw_sha256.
2. Every service receipt (15 runs): the raw simulator log hashes to the
   receipt's log_sha256; the receipt's input_hashes equal the HEAD tree's
   run.inputs(); its build_hashes equal the kept build spec's; and the HEAD
   run.grade() + service_findings() + report_verdict() recompute the receipt's
   rows, liveness, phy, heartbeat and findings from the raw log alone.
   This is `run.py --regrade` minus the rebuild-hash binding, whose binaries
   (Vsim, bios.bin) are not retained.
3. The no-publish control log carries its named PASS and failing raw log.
4. The six capture arms regrade to the committed measurements.json and the
   byte-only control passes grade_byte_only against its bound baseline.
"""
import contextlib
import gzip
import hashlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
A = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "tb/verilator/fw_service_budget"))
import run as svc  # noqa: E402
sys.path.pop(0)
sys.modules.pop("run")
sys.path.insert(0, str(ROOT / "tb/verilator/nvm_capture_cpu"))
import run as cap  # noqa: E402

sha = lambda b: hashlib.sha256(b).hexdigest()  # noqa: E731
fails = []
MAN = json.loads(Path(sys.argv[3]).read_text())
PREFIX = sys.argv[4] if len(sys.argv) > 4 else "review-evidence/590-r1/author-r3/"
arch = {e["file"]: e for e in MAN}
checked = redacted_ok = 0
for f in sorted(A.rglob("*")):
    if f.is_file():
        key = PREFIX + str(f.relative_to(A))
        e = arch.get(key)
        if e is None:
            fails.append(f"published file not in archive manifest: {key}")
            continue
        checked += 1
        if sha(f.read_bytes()) != e["published_sha256"]:
            fails.append(f"archive manifest published hash differs: {key}")
print(f"archive manifest: author-r3 files checked={checked}")
artifacts = json.loads((A / "native-artifacts.json").read_text())
commands = {c["name"]: c for c in json.loads((A / "native-commands.json").read_text())}
body = {}
stored_ok = raw_fallback = 0
for item in artifacts:
    name = item["name"]
    parts = []
    missing = False
    for st in item["stored"]:
        p = A / st["path"]
        if not p.exists():
            missing = True
            break
        b = p.read_bytes()
        if len(b) != st["size"] or sha(b) != st["sha256"]:
            e = arch.get(PREFIX + st["path"], {})
            if e.get("path_redacted") and e.get("original_sha256") == st["sha256"] \
                    and e.get("published_sha256") == sha(b):
                redacted_ok += 1
                missing = "redacted"
                break
            fails.append(f"stored bytes differ: {st['path']}")
        parts.append(b)
    if missing == "redacted":
        # published (path-redacted) bytes; used only for spec fields
        body[name] = b"".join(parts) + (A / item["stored"][len(parts)]["path"]).read_bytes() \
            if len(item["stored"]) == 1 else None
        continue
    if missing:
        plain = name[:-3] if name.endswith(".gz") else name
        p = A / "native-evidence-raw" / plain
        if not p.exists():
            fails.append(f"artifact absent: {name}")
            continue
        raw = p.read_bytes()
        raw_fallback += 1
    else:
        raw = b"".join(parts)
        if name.endswith(".gz"):
            raw = gzip.decompress(raw)
        stored_ok += 1
    if len(raw) != item["raw_size"] or sha(raw) != item["raw_sha256"]:
        fails.append(f"raw bytes differ: {name}")
    body[name[:-3] if name.endswith(".gz") else name] = raw
print(f"artifacts={len(artifacts)} stored-verified={stored_ok} raw-fallback-verified={raw_fallback} "
      f"path-redacted-with-original-hash-bound={redacted_ok}")

head_inputs = svc.inputs()
runs = sorted(n[:-len("-receipt.json")] for n in body if n.startswith("service-") and n.endswith("-receipt.json"))
print(f"service receipts: {len(runs)}")
for name in runs:
    rec = json.loads(body[name + "-receipt.json"])
    spec = json.loads(body[name + "-spec.json"])
    raw = body[name + "-raw.log"].decode()
    cmd = commands[name]["command"]
    mutation = cmd[cmd.index("--mutation") + 1] if "--mutation" in cmd else "none"
    record = "--record-budget-findings" in cmd
    enforce = "--enforce-service" in cmd
    notes = []
    if spec["mutation"] != mutation:
        notes.append("spec mutation differs from command")
    if rec["log_sha256"] != sha(raw.encode()):
        notes.append("log_sha256 mismatch")
    if rec["raw_log"] != raw:
        notes.append("receipt raw_log differs from kept raw log")
    if rec["input_hashes"] != head_inputs:
        diff = sorted(k for k in set(rec["input_hashes"]) | set(head_inputs)
                      if rec["input_hashes"].get(k) != head_inputs.get(k))
        notes.append(f"input_hashes differ from HEAD: {diff}")
    if rec["build_hashes"] != spec["build_hashes"]:
        notes.append("build_hashes differ from kept spec")
    result = dict(media=rec["media"], shape=rec["shape"], cpu_hz=rec["cpu_hz"], sys_hz=rec["sys_hz"],
                  device_wait_us=rec["device_wait_us"], program_wait_us=rec["program_wait_us"])
    result.update(svc.grade(raw, rec["media"]))
    if enforce:
        result["service_findings"] = svc.service_findings(result, raw)
    for key in result:
        if key in rec and json.loads(json.dumps(result[key])) != rec[key]:
            notes.append(f"recomputed {key} differs")
    findings = result.get("service_findings", result["budget_findings"])
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            svc.report_verdict(mutation, findings, record)
        verdict = out.getvalue().strip().splitlines()[-1]
    except RuntimeError as e:
        verdict = f"REFUSED {e}"
        notes.append(verdict)
    kept = body.get("regrade-" + name + ".log", b"").decode().strip().splitlines()
    kept_last = kept[-1] if kept else "(regrade log not kept)"
    if kept and kept_last != verdict:
        notes.append(f"kept regrade verdict differs: {kept_last}")
    perline = sum(1 for f in findings if f.startswith("console line lacks a dispatch opportunity: "))
    lines = sum(1 for r in result["rows"] if "command_index" in r)
    ticked = sum(1 for r in result["rows"] if "command_index" in r and r.get("tick_calls", 0) > 0)
    unb = re.search(r"unbacked_cycles=(\d+)", raw)
    print(f"{name:<44} mutation={mutation:<15} lines={lines:<5} ticked={ticked:<5} per-line={perline:<5} "
          f"unbacked={unb.group(1) if unb else '-':<11} hb_gap_ms={result.get('heartbeat_max_gap_ms')} "
          f"findings={len(findings)} verdict={verdict!r} {'OK' if not notes else 'FAIL ' + '; '.join(notes)}")
    if mutation == "late-sample":
        print("   late-sample named finding present:",
              "PHY initial gigabit negotiation was not published" in findings)
    if mutation == "remove-dispatch":
        gap = [f for f in findings if "continuous backing lost" in f or "gap" in f][:2]
        print("   remove-dispatch sample findings:", gap, "| first per-line:",
              next((f for f in findings if f.startswith("console line")), None))
    if notes:
        fails.append(name + ": " + "; ".join(notes))

np_log = body.get("service-no-publish-all.log", b"").decode()
np_raw = body.get("service-no-publish-all-raw.log", b"").decode()
ok = "PASS: missing publication caught by target simulation" in np_log and "missing MDIO/publication evidence" in np_raw
print("no-publish control:", "OK" if ok else "FAIL", "|", np_log.strip())
if not ok:
    fails.append("no-publish control")

committed = json.loads((ROOT / "tb/verilator/nvm_capture_cpu/measurements.json").read_text())


def rows_of(raw):
    return [dict((k, int(v)) for k, v in re.findall(r"(\w+)=(\d+)", ln))
            for ln in raw.splitlines() if ln.startswith("CAPTURE index=")]


ncap = 0
for short, mhz in (("1x1", 50), ("8x8", 50), ("8x8", 100)):
    for traffic in ("on", "off"):
        n = f"capture-{short}-{mhz}-{traffic}"
        spec = json.loads(body[n + "-sources.json"])
        rows = rows_of(body[n + "-raw.log"].decode())
        m = cap.grade_rows(rows, spec)
        kept = json.loads(body[n + ".json"])
        match = [e for e in committed["measurements"]
                 if (e["shape"], e["cpu_hz"], e["traffic"]) == (m["shape"], m["cpu_hz"], m["traffic"])]
        same = m == kept and len(match) == 1 and all(match[0].get(k) == v for k, v in m.items())
        print(f"{n:<22} rows={len(rows)} max_ms={m.get('maximum_ms')} firmware={spec.get('firmware_sha256', '')[:12]} "
              f"{'OK' if same else 'FAIL'}")
        ncap += len(rows)
        if not same:
            fails.append(n)
byte = json.loads(body["capture-byte-only-measurement.json"])
base = json.loads(body["capture-8x8-50-on.json"])
spec = json.loads(body["capture-byte-only-sources.json"])
m = cap.grade_rows(rows_of(body["capture-byte-only-capture.log"].decode()), spec)
try:
    cap.grade_byte_only(m, base)
    verdict = "PASS"
except Exception as e:  # noqa: BLE001
    verdict = f"REFUSED {e}"
print(f"byte-only: min_ms={m.get('minimum_ms')} max_ms={m.get('maximum_ms')} "
      f"ratio={m.get('minimum_ms', 0) / base['maximum_ms']:.5f} grade_byte_only={verdict} "
      f"baseline_bound={byte.get('baseline_sha256') == sha(body['capture-8x8-50-on.json'])}")
if verdict != "PASS":
    fails.append("byte-only")
print(f"captures regraded: {ncap}")
for f in fails:
    print("FAIL:", f)
print("RESULT:", "FAIL" if fails else "PASS")
sys.exit(1 if fails else 0)
