#!/usr/bin/env python3
"""Run gen_ucode.py alone on table copies it must refuse, normally and with -O.

Usage: probe_generator.py TREE SCRATCH OUT.json

TREE is never written: hdl/aecp/ucode is copied per probe under SCRATCH.
A refusal must exit non-zero, print no traceback, and name every word given.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path


def named(t, name):
    return next(c for c in t["commands"] if c.get("name") == name)


def setitem(seq, i, v):
    seq[i] = v


PROBES = [
    ("missing-entries", lambda t: named(t, "GET_CLOCK_SOURCE").pop("entries"),
     ["GET_CLOCK_SOURCE", "entries"]),
    ("entries-not-list", lambda t: named(t, "GET_CLOCK_SOURCE").update(entries="GCLKS"),
     ["GET_CLOCK_SOURCE", "entries"]),
    ("entries-empty", lambda t: named(t, "GET_CLOCK_SOURCE").update(entries=[]),
     ["GET_CLOCK_SOURCE", "entries"]),
    ("entries-blank-name", lambda t: named(t, "GET_CLOCK_SOURCE").update(entries=["GCLKS", ""]),
     ["GET_CLOCK_SOURCE", "entries"]),
    ("missing-name", lambda t: named(t, "GET_CLOCK_SOURCE").pop("name"),
     ["0x0017", "name"]),
    ("empty-name", lambda t: named(t, "GET_CLOCK_SOURCE").update(name=""),
     ["0x0017", "name"]),
    ("mvu-opcode-non-hex", lambda t: named(t, "GET_MILAN_INFO").update(opcode="0xZZZZ"),
     ["GET_MILAN_INFO", "opcode"]),
    ("mvu-opcode-five-digits", lambda t: named(t, "GET_MILAN_INFO").update(opcode="0x00000"),
     ["GET_MILAN_INFO", "opcode"]),
    ("mvu-row-missing", lambda t: t["commands"].remove(named(t, "GET_MILAN_INFO")),
     ["GET_MILAN_INFO"]),
    ("missing-commands", lambda t: t.pop("commands"), ["commands"]),
    ("command-not-object", lambda t: setitem(t["commands"], 0, "ACQUIRE_ENTITY"),
     ["commands[0]"]),
    ("entry-never-placed", lambda t: named(t, "GET_CLOCK_SOURCE")["entries"].append("NOPE"),
     ["GET_CLOCK_SOURCE", "NOPE"]),
    ("status-code-not-int", lambda t: t["status_codes"]["BAD_ARGUMENTS"].update(code="7"),
     ["BAD_ARGUMENTS"]),
]


def main() -> int:
    tree, scratch, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    scratch.mkdir(parents=True, exist_ok=True)
    results = []
    for opt in ([], ["-O"]):
        for name, edit, words in [("unmodified", lambda t: None, [])] + PROBES:
            d = scratch / (name + ("-O" if opt else ""))
            if d.exists():
                shutil.rmtree(d)
            shutil.copytree(tree / "hdl/aecp/ucode", d)
            table = d / "aecp_commands.json"
            t = json.loads(table.read_text(encoding="utf-8"))
            edit(t)
            table.write_text(json.dumps(t, indent=2) + "\n", encoding="utf-8")
            p = subprocess.run([sys.executable, "-B"] + opt + [str(d / "gen_ucode.py"), "-o",
                                str(d / "ucode.hex")], capture_output=True, text=True,
                               check=False)
            text = p.stdout + p.stderr
            last = text.strip().splitlines()[-1] if text.strip() else ""
            if name == "unmodified":
                ok = p.returncode == 0
            else:
                ok = (p.returncode != 0 and "Traceback" not in text
                      and all(w in last for w in words))
            results.append({"probe": name, "optimize": bool(opt), "rc": p.returncode,
                            "last_line": last, "traceback": "Traceback" in text,
                            "as_expected": ok})
            print(f"{name}{' -O' if opt else ''}: rc={p.returncode} "
                  f"{'OK' if ok else 'UNEXPECTED'} | {last}")
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return 0 if all(r["as_expected"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
