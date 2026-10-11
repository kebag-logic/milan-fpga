#!/usr/bin/env python3
"""Reviewer probes for the AECP command gate (R608-2).

Each probe copies a pristine source tree (--src, an export of the exact head),
applies one edit to the table, the doc or the RTL, optionally regenerates
F06.14 with the gate's own --write, then runs the gate (no self-test) and
records rc and output. A probe "PASSES THE GATE" when rc == 0, which for a
semantic drift means the drift is held to nothing.

usage: python3 -I table_probes.py --src DIR --out DIR [--only NAME ...]
"""
import argparse
import difflib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TABLE = "hdl/aecp/ucode/aecp_commands.json"
DOC = "docs/architecture/06_aecp_engine.md"
ENGINE = "hdl/aecp/KL_aecp_engine.sv"


def tedit(fn):
    """A table edit as a probe action."""
    def act(root: Path) -> None:
        p = root / TABLE
        t = json.loads(p.read_text(encoding="utf-8"))
        fn(t)
        p.write_text(json.dumps(t, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return act


def sedit(rel, old, new, count=1):
    """An exact text edit as a probe action."""
    def act(root: Path) -> None:
        p = root / rel
        s = p.read_text(encoding="utf-8")
        if s.count(old) != count:
            raise SystemExit(f"probe edit site count {s.count(old)} != {count} in {rel}: {old!r}")
        p.write_text(s.replace(old, new), encoding="utf-8")
    return act


def cmd(t, name):
    return next(c for c in t["commands"] if c["name"] == name)


def _renumber(t):
    cmd(t, "GET_COUNTERS")["opcode"] = "0x002A"


def _drop(t):
    t["commands"] = [c for c in t["commands"] if c["name"] != "GET_COUNTERS"]


def _oversize(t):
    cmd(t, "GET_CONFIGURATION")["oversize"] = True
    cmd(t, "READ_DESCRIPTOR")["oversize"] = False


def _common(t):
    t["common_status"]["AEM"].append("STREAM_IS_RUNNING")
    for n in ("SET_CONFIGURATION", "SET_STREAM_FORMAT", "SET_STREAM_INFO"):
        cmd(t, n)["status"].remove("STREAM_IS_RUNNING")


def _common_add_unreachable(t):
    t["common_status"]["AEM"].append("NO_RESOURCES")


def _per_echo(t):
    for n in ("ADD_AUDIO_MAPPINGS", "REMOVE_AUDIO_MAPPINGS"):
        c = cmd(t, n)
        c["command"]["per"] = 4
        c["response"]["per"] = 4


def _per_echo_2(t):
    c = cmd(t, "ADD_AUDIO_MAPPINGS")
    c["command"]["per"] = 2
    c["response"]["per"] = 2


def _per_avb(t):
    cmd(t, "GET_AVB_INFO")["response"]["per"] = 2


def _entries_order(t):
    c = cmd(t, "GET_STREAM_INFO")
    c["entries"] = ["NSUPPE", "GSTRI", "BADARG"]


def _stub(t):
    cmd(t, "READ_DESCRIPTOR")["response"]["stub"] = 24


def _lock(t):
    cmd(t, "SET_NAME")["lock"] = False


def _status_drop(t):
    cmd(t, "SET_CONFIGURATION")["status"].remove("ENTITY_LOCKED")


def _gdi(t):
    cmd(t, "GET_CONTROL")["gdi"] = True


def _hazard_mvu(t):
    cmd(t, "GET_MILAN_INFO")["hazard"] = "MAP_CFG"


def _echo_entries_add(t):
    t["echo_entries"].append("GCTRS")


def _engine_status_any(t):
    cmd(t, "GET_DYNAMIC_INFO")["engine_status"].append("NO_RESOURCES")


def _shared_entry_add(t):
    t["shared_entries"]["GCFG"] = "reviewer probe: a served command's program declared shared"


def _mvu_floor(t):
    cmd(t, "GET_MILAN_INFO")["command"]["floor"] = 16


def _notify_kind(t):
    cmd(t, "LOCK_ENTITY")["notify"]["kind"] = "PP_UNS_CFG_C"


def _max(t):
    c = cmd(t, "GET_DYNAMIC_INFO")
    c["command"]["max"] = 600
    c["response"]["max"] = 600


PROBES = {
    # the issue's four planted drifts (manager's proof list)
    "accept-opcode-renumbered-table-only": ([tedit(_renumber)], False),
    "accept-size-changed-doc-only": ([sedit(DOC, "| 0x0017 | GET_CLOCK_SOURCE | shall | — | RO_SNAPSHOT | no | yes | no | — | 16 | 32 B (cdl 20) |",
                                            "| 0x0017 | GET_CLOCK_SOURCE | shall | — | RO_SNAPSHOT | no | yes | no | — | 16 | 36 B (cdl 24) |")], False),
    "accept-op-const-changed-rtl-only": ([sedit(ENGINE, "OP_GET_COUNTERS_C    = 16'h0029", "OP_GET_COUNTERS_C    = 16'h002A")], False),
    "accept-command-missing-from-table": ([tedit(_drop)], False),
    "accept-command-missing-from-table-doc-regenerated": ([tedit(_drop)], True),
    # reviewer probes: semantic table fields, each with F06.14 regenerated
    "oversize-flags-flipped": ([tedit(_oversize)], True),
    "common-status-hides-stream-is-running": ([tedit(_common)], True),
    "common-status-adds-unreachable": ([tedit(_common_add_unreachable)], True),
    "per-echo-8-to-4": ([tedit(_per_echo)], True),
    "per-echo-8-to-2-add-only": ([tedit(_per_echo_2)], True),
    "per-avb-4-to-2": ([tedit(_per_avb)], True),
    "entries-success-not-first": ([tedit(_entries_order)], True),
    "stub-20-to-24": ([tedit(_stub)], True),
    "lock-flag-dropped": ([tedit(_lock)], True),
    "status-locked-dropped": ([tedit(_status_drop)], True),
    "gdi-flag-added": ([tedit(_gdi)], True),
    "mvu-hazard-changed": ([tedit(_hazard_mvu)], True),
    "echo-entries-add-gctrs": ([tedit(_echo_entries_add)], True),
    "engine-status-add": ([tedit(_engine_status_any)], True),
    "shared-entry-add-gcfg": ([tedit(_shared_entry_add)], True),
    "mvu-floor-16": ([tedit(_mvu_floor)], True),
    "notify-kind-changed": ([tedit(_notify_kind)], True),
    "gdi-max-524-to-600": ([tedit(_max)], True),
}


def run_probe(name, src: Path, out: Path) -> dict:
    acts, regen = PROBES[name]
    with tempfile.TemporaryDirectory(prefix="r608-2-probe-") as tmp:
        root = Path(tmp)
        for d in ("hdl", "scripts", "tb/common", "tb/aecp_cmds", "docs"):
            shutil.copytree(src / d, root / d, ignore=shutil.ignore_patterns(
                "obj_dir", "*.hex", "image.bin", "__pycache__"))
        for a in acts:
            a(root)
        gate = [sys.executable, "-B", str(root / "scripts/check_aecp_commands.py")]
        wlog = ""
        if regen:
            w = subprocess.run(gate + ["--write"], capture_output=True, text=True)
            wlog = f"--write rc {w.returncode}: {w.stdout}{w.stderr}"
            diff = difflib.unified_diff(
                (src / DOC).read_text(encoding="utf-8").splitlines(),
                (root / DOC).read_text(encoding="utf-8").splitlines(), DOC, DOC + " (probe)", n=0, lineterm="")
            wlog += "\n# F06.14 as regenerated by the probe (diff against head)\n" + "\n".join(diff)
        r = subprocess.run(gate, capture_output=True, text=True)
    text = (f"# probe {name}\n{wlog}\n# gate rc {r.returncode}\n{r.stdout}{r.stderr}")
    (out / f"{name}.log").write_text(text, encoding="utf-8")
    return {"probe": name, "doc_regenerated": regen, "gate_rc": r.returncode,
            "first_lines": [x for x in (r.stdout + r.stderr).splitlines() if x.strip()][:4]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    res = [run_probe(n, a.src.resolve(), a.out) for n in PROBES if not a.only or n in a.only]
    (a.out / "summary.json").write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")
    for r in res:
        print(f"{r['probe']}: gate rc {r['gate_rc']}  {r['first_lines'][1:3] if r['gate_rc'] else r['first_lines'][-1:]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
