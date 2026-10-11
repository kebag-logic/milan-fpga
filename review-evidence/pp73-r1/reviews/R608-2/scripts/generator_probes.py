#!/usr/bin/env python3
"""Reviewer probes: gen_ucode.py run alone (as a suite build runs it) on
table defects it reads, under python3 and python3 -O (R608-2).

usage: python3 -I generator_probes.py --src DIR --out FILE
"""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

UC = "hdl/aecp/ucode"


def mvu(t):
    return next(c for c in t["commands"] if c["message"] == "MVU")


def cmd(t, n):
    return next(c for c in t["commands"] if c["name"] == n)


PLANTS = {
    "status-code-not-integer": lambda t: t["status_codes"]["SUCCESS"].update(code="0"),
    "mvu-message-AAU": lambda t: mvu(t).update(message="AAU"),
    "entry-never-placed": lambda t: cmd(t, "GET_CLOCK_SOURCE")["entries"].__setitem__(0, "SCFGRUN2"),
    "entries-field-missing": lambda t: cmd(t, "GET_CLOCK_SOURCE").pop("entries"),
    "entries-not-a-list": lambda t: cmd(t, "GET_CLOCK_SOURCE").update(entries="GCLKS"),
    "name-field-missing": lambda t: cmd(t, "GET_CLOCK_SOURCE").pop("name"),
    "mvu-opcode-not-hex": lambda t: mvu(t).update(opcode="0xZZZZ"),
    "commands-missing": lambda t: t.pop("commands"),
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    lines = []
    for name, plant in PLANTS.items():
        for opt in ([], ["-O"]):
            with tempfile.TemporaryDirectory(prefix="r608-2-gen-") as tmp:
                d = Path(tmp) / "ucode"
                shutil.copytree(a.src / UC, d, ignore=shutil.ignore_patterns("__pycache__"))
                p = d / "aecp_commands.json"
                t = json.loads(p.read_text(encoding="utf-8"))
                plant(t)
                p.write_text(json.dumps(t, indent=2), encoding="utf-8")
                r = subprocess.run(["python3", "-B", *opt, "gen_ucode.py", "-o", str(Path(tmp) / "u.hex")],
                                   cwd=d, capture_output=True, text=True)
            err = [x for x in (r.stdout + r.stderr).splitlines() if x.strip()]
            lines.append(f"{name} python3 {' '.join(opt) or '(no -O)'}: rc {r.returncode}: "
                         f"{err[-1] if err else '(no output)'}")
    a.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
