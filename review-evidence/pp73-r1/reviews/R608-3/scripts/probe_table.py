#!/usr/bin/env python3
"""Disposable table/registry probes against the AECP command gate.

Usage: probe_table.py TREE SCRATCH OUT.json [PR_BODY.md]

TREE is a pristine extraction of the head under review; it is never written.
Each probe copies TREE to SCRATCH/<name>, applies one edit to the table or the
registry, optionally regenerates the generated references with --write (so a
semantic drift cannot be caught merely as a stale F06.14 cell), then runs the
gate exactly as `make check` does (no selftest) and records rc and output.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

TABLE = "hdl/aecp/ucode/aecp_commands.json"
FIELDS = "hdl/aecp/ucode/aecp_fields.json"
GATE = "scripts/check_aecp_commands.py"


def cmd(t, name):
    return next(c for c in t["commands"] if c.get("name") == name)


def doc(t, name):
    return next(d for d in t["documented"] if d.get("name") == name)


def reg(r, path):
    return next(e for e in r if e["path"] == path)


def set_status(r, path, status):
    e = reg(r, path)
    e["status"] = status
    if status != "held":
        for k in ("consumer", "check", "probe"):
            e.pop(k, None)


# (name, target file, edit, regenerate-first, expectation, words)
#   expectation: "fail" = must exit 1 with every word in one output line;
#                "refuse" = exit 2 with the words; "pass" = exit 0 (declared limit)
PROBES = [
    # round-3 item 2: per on the echo rows held exactly
    ("per-echo-8-to-4-add", TABLE,
     lambda t: (cmd(t, "ADD_AUDIO_MAPPINGS")["command"].update(per=4),
                cmd(t, "ADD_AUDIO_MAPPINGS")["response"].update(per=4)),
     True, "fail", ["ADD_AUDIO_MAPPINGS", "command per is 4", "gcd"]),
    ("per-echo-8-to-4-remove", TABLE,
     lambda t: (cmd(t, "REMOVE_AUDIO_MAPPINGS")["command"].update(per=4),
                cmd(t, "REMOVE_AUDIO_MAPPINGS")["response"].update(per=4)),
     True, "fail", ["REMOVE_AUDIO_MAPPINGS", "command per is 4", "gcd"]),
    ("per-echo-8-to-16-remove", TABLE,
     lambda t: (cmd(t, "REMOVE_AUDIO_MAPPINGS")["command"].update(per=16),
                cmd(t, "REMOVE_AUDIO_MAPPINGS")["response"].update(per=16)),
     True, "fail", ["REMOVE_AUDIO_MAPPINGS", "command per is 16", "gcd"]),
    ("per-echo-8-to-2-add", TABLE,
     lambda t: (cmd(t, "ADD_AUDIO_MAPPINGS")["command"].update(per=2),
                cmd(t, "ADD_AUDIO_MAPPINGS")["response"].update(per=2)),
     True, "fail", ["ADD_AUDIO_MAPPINGS", "command per is 2", "gcd"]),
    # zero / null / negative / non-integer steps refused
    ("per-zero-command", TABLE, lambda t: cmd(t, "ADD_AUDIO_MAPPINGS")["command"].update(per=0),
     False, "fail", ["schema: ADD_AUDIO_MAPPINGS: command per must be"]),
    ("per-null-command", TABLE, lambda t: cmd(t, "REMOVE_AUDIO_MAPPINGS")["command"].update(per=None),
     False, "fail", ["schema: REMOVE_AUDIO_MAPPINGS: command per must be"]),
    ("per-negative-command", TABLE, lambda t: cmd(t, "ADD_AUDIO_MAPPINGS")["command"].update(per=-8),
     False, "fail", ["schema: ADD_AUDIO_MAPPINGS: command per must be"]),
    ("per-bool-command", TABLE, lambda t: cmd(t, "ADD_AUDIO_MAPPINGS")["command"].update(per=True),
     False, "fail", ["schema: ADD_AUDIO_MAPPINGS: command per must be"]),
    ("per-float-command", TABLE, lambda t: cmd(t, "ADD_AUDIO_MAPPINGS")["command"].update(per=8.0),
     False, "fail", ["schema: ADD_AUDIO_MAPPINGS: command per must be"]),
    ("per-zero-response", TABLE, lambda t: cmd(t, "GET_AS_PATH")["response"].update(per=0),
     False, "fail", ["schema: GET_AS_PATH: response per must be"]),
    ("per-null-response", TABLE, lambda t: cmd(t, "GET_AUDIO_MAP")["response"].update(per=None),
     False, "fail", ["schema: GET_AUDIO_MAP: response per must be"]),
    ("per-negative-response", TABLE, lambda t: cmd(t, "GET_AVB_INFO")["response"].update(per=-4),
     False, "fail", ["schema: GET_AVB_INFO: response per must be"]),
    # round-3 item 2: documented GDI rows are semantic
    ("documented-gdi-opcode", TABLE, lambda t: doc(t, "GET_VIDEO_FORMAT").update(opcode="0x0070"),
     True, "fail", ["GET_VIDEO_FORMAT"]),
    # round-3 item 2: the declared limits (expected to PASS: held to nothing)
    ("declared-oversize-flip", TABLE, lambda t: cmd(t, "GET_CLOCK_SOURCE").update(oversize=True),
     True, "pass", []),
    ("declared-common-status-hides-own", TABLE,
     lambda t: (t["common_status"]["AEM"].append("BAD_ARGUMENTS"),
                cmd(t, "GET_CLOCK_SOURCE")["status"].remove("BAD_ARGUMENTS")),
     True, "pass", []),
    ("declared-engine-status-extra", TABLE,
     lambda t: cmd(t, "GET_DYNAMIC_INFO")["engine_status"].append("NOT_SUPPORTED"),
     True, "pass", []),
    ("declared-echo-entries-extra", TABLE,
     lambda t: t["echo_entries"].append("EAVL"), True, "pass", []),
    # round-3 item 1: registry exhaustiveness, both directions
    ("registry-table-field-unregistered", TABLE,
     lambda t: cmd(t, "GET_CLOCK_SOURCE").update(note="x"), False, "fail",
     ["fields: commands[].note: table field missing from registry"]),
    ("registry-common-status-new-message", TABLE,
     lambda t: t["common_status"].update(AVC=[]), False, "fail",
     ["fields: common_status.AVC: table field missing from registry"]),
    ("registry-entry-removed", FIELDS,
     lambda r: r.remove(reg(r, "commands[].command.per")), False, "fail",
     ["fields: commands[].command.per: table field missing from registry"]),
    ("registry-entry-stale", FIELDS,
     lambda r: r.append({"path": "commands[].nothing", "status": "held to nothing",
                         "reason": "probe"}), False, "fail",
     ["fields: commands[].nothing: registry entry has no such table field"]),
    ("registry-held-without-probe", FIELDS,
     lambda r: reg(r, "commands[].hazard").pop("probe"), False, "fail",
     ["fields: commands[].hazard: held needs consumer"]),
    ("registry-status-changed-no-write", FIELDS,
     lambda r: set_status(r, "commands[].opcode", "held to nothing"), False, "fail",
     ["registry reference differs"]),
    ("registry-reason-edited-no-write", FIELDS,
     lambda r: reg(r, "commands[].oversize").update(reason="Held: probe."), False, "fail",
     ["registry reference differs"]),
]


def run(tree: Path, args: list) -> tuple:
    p = subprocess.run([sys.executable, "-B", GATE] + args, cwd=tree,
                       capture_output=True, text=True, check=False)
    return p.returncode, (p.stdout + p.stderr)


def probe(src: Path, scratch: Path, item: tuple) -> dict:
    name, target, edit, regen, expect, words = item
    tree = scratch / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(src, tree, symlinks=True, ignore=shutil.ignore_patterns("obj_dir", "*.hex", "image.bin"))
    path = tree / target
    data = json.loads(path.read_text(encoding="utf-8"))
    edit(data)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    regen_rc, regen_out = (run(tree, ["--write"]) if regen else (None, ""))
    rc, out = run(tree, [])
    lines = out.splitlines()
    named = [ln for ln in lines if all(w in ln for w in words)] if words else []
    if expect == "fail":
        ok = rc == 1 and bool(named)
    elif expect == "refuse":
        ok = rc == 2 and bool(named)
    else:
        ok = rc == 0
    return {"probe": name, "target": target, "regenerated": regen, "regen_rc": regen_rc,
            "expect": expect, "rc": rc, "named": named, "as_expected": ok,
            "output": out[-3000:], "regen_output": regen_out[-1000:]}


def main() -> int:
    src, scratch, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    scratch.mkdir(parents=True, exist_ok=True)
    results = []
    rc0, out0 = run(src, [])
    results.append({"probe": "unmodified", "rc": rc0, "as_expected": rc0 == 0, "output": out0})
    if len(sys.argv) > 4:
        rc, o = run(src, ["--pr-body", str(Path(sys.argv[4]).resolve())])
        results.append({"probe": "published-pr-body-reference", "rc": rc,
                        "as_expected": rc == 0, "output": o})
    for item in PROBES:
        results.append(probe(src, scratch, item))
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    for r in results:
        print(f"{r['probe']}: rc={r['rc']} {'OK' if r['as_expected'] else 'UNEXPECTED'}"
              + (f"  | {r['named'][0].strip()}" if r.get("named") else ""))
    return 0 if all(r["as_expected"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
