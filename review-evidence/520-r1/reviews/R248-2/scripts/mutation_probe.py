#!/usr/bin/env python3
"""Disposable fault probes against a COPY of the reviewed clone.

usage: mutation_probe.py <clone> <scratch-dir> <probe-id> [--unit-only]

Copies the clone (cp -a, own .git and submodule gitdirs, so nothing is shared),
applies exactly one named source edit (each edit must match exactly once, or the
probe refuses), and runs the shipping controls in the copy:
  unit:  python3 syn/yosys/result_cache.py --selftest
  live:  python3 syn/yosys/cache_selftest.py   (unit + original arms + ROM arms)
A probe is DETECTED when the relevant control exits non-zero. The clone itself
is never written. Prints one JSON receipt line.
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

# id: (file, old, new, what the edit models)
PROBES = {
    "M1_rom_not_bound": (
        "syn/yosys/run.sh",
        '    ROM_SHA256="$(python3 "$R/syn/yosys/result_cache.py" rom-digest --rom-dir "$TMP")" || {',
        '    ROM_SHA256="$(printf "%064d" 0)"; true || {',
        "pre-#520 defect: cache identity ignores generated ROM bytes (constant digest)"),
    "M2_lookup_store_split": (
        "syn/yosys/run.sh",
        '    --top "$1" --mode "$MODE" --sv2v-file "$TMP/$1.v" --program "$2" \\\n'
        '    --rom-sha256 "$ROM_SHA256" \\\n'
        '    --yosys-version "$YOSYS_ID" --yosys-bin-sha256 "$YOSYS_BIN_SHA" --sv2v-version "$SV2V_ID" \\\n'
        '    --cells',
        '    --top "$1" --mode "$MODE" --sv2v-file "$TMP/$1.v" --program "$2" \\\n'
        '    --rom-sha256 "$(printf "%064d" 0)" \\\n'
        '    --yosys-version "$YOSYS_ID" --yosys-bin-sha256 "$YOSYS_BIN_SHA" --sv2v-version "$SV2V_ID" \\\n'
        '    --cells',
        "store keys on a different ROM identity than lookup"),
    "M3_bundle_omits_ucode": (
        "syn/yosys/result_cache.py",
        'ROM_IMAGES = ("gptp_ucode.hex", "ltn_rom.hex", "ucode.hex")',
        'ROM_IMAGES = ("gptp_ucode.hex", "ltn_rom.hex")',
        "bundle drops the PP AECP image"),
    "M4_digest_before_nonempty": (
        "syn/yosys/run.sh",
        '  for image in "$TMP/ltn_rom.hex" "$TMP/ucode.hex" "$TMP/gptp_ucode.hex"; do\n'
        '    [ -s "$image" ] || { echo "Yosys: generated ROM is empty: $image" >&2; exit 2; }\n'
        '  done\n',
        '  if [ -n "$CACHE" ] || [ -n "$CACHE_SEED" ]; then\n'
        '    python3 "$R/syn/yosys/result_cache.py" rom-digest --rom-dir "$TMP" >/dev/null || {\n'
        '      echo "Yosys: generated ROM bundle could not be digested" >&2; exit 2; }\n'
        '  fi\n'
        '  for image in "$TMP/ltn_rom.hex" "$TMP/ucode.hex" "$TMP/gptp_ucode.hex"; do\n'
        '    [ -s "$image" ] || { echo "Yosys: generated ROM is empty: $image" >&2; exit 2; }\n'
        '  done\n',
        "digest taken before the existing nonempty checks (specific refusal replaced)"),
    "M5_rom_field_unverified": (
        "syn/yosys/result_cache.py",
        "    for name in INPUT_FIELDS:\n        want = getattr(inputs, name)",
        "    for name in INPUT_FIELDS[:-1]:\n        want = getattr(inputs, name)",
        "hit rule stops comparing the recorded rom_sha256 field"),
    "M6_schema_not_bumped": (
        "syn/yosys/result_cache.py",
        'SCHEMA = "milan-yosys-result-cache/2"',
        'SCHEMA = "milan-yosys-result-cache/1"',
        "schema string left at 1 (key already differs; expected behaviour-neutral)"),
    "M7_no_length_framing": (
        "syn/yosys/result_cache.py",
        '        digest.update(len(content).to_bytes(8, "big"))\n',
        "",
        "digest drops the eight-byte length framing"),
    "M8_seed_only_unkeyed": (
        "syn/yosys/run.sh",
        '  ROM_SHA256=""\n  if [ -n "$CACHE" ] || [ -n "$CACHE_SEED" ]; then\n',
        '  ROM_SHA256=""\n  if [ -n "$CACHE" ]; then\n',
        "ROM digest captured for per-head state only, not for seed-only lookup"),
}


def main() -> int:
    clone, scratch, pid = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    unit_only = "--unit-only" in sys.argv[4:]
    path, old, new, what = PROBES[pid]
    copy = scratch / f"probe-{pid}"
    if copy.exists():
        shutil.rmtree(copy)
    subprocess.run(["cp", "-a", str(clone), str(copy)], check=True)
    target = copy / path
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        print(json.dumps({"probe": pid, "error": f"edit matched {count} times"}))
        return 2
    target.write_text(text.replace(old, new), encoding="utf-8")
    receipt = {"probe": pid, "models": what, "file": path}
    for name, cmd in (("unit", ["python3", "syn/yosys/result_cache.py", "--selftest"]),
                      ("live", ["python3", "syn/yosys/cache_selftest.py"])):
        if name == "live" and unit_only:
            continue
        start = time.monotonic()
        proc = subprocess.run(cmd, cwd=copy, capture_output=True, text=True)
        out = proc.stdout + proc.stderr
        (scratch / f"probe-{pid}.{name}.log").write_text(out, encoding="utf-8")
        fails = [l for l in out.splitlines() if "FAIL" in l or "AssertionError" in l][:6]
        receipt[name] = {"exit": proc.returncode, "seconds": round(time.monotonic() - start, 1),
                         "detected": proc.returncode != 0, "first_fail_lines": fails,
                         "last_line": out.strip().splitlines()[-1] if out.strip() else ""}
    print(json.dumps(receipt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
