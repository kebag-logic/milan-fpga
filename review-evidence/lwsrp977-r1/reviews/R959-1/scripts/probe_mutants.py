# SPDX-License-Identifier: Apache-2.0
"""Reviewer probes: plant extra defects and ask the head's differential whether
any seed's trace shows them. Reuses the head's check_differential.py build,
trace and comparison functions unchanged; never edits the checkout.

usage: python3 -I probe_mutants.py <checkout> <new-work-dir> [--milan OFF|ON] [--seeds N]
"""
import argparse
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

MAD = "core/mrp_mad.c"
PDU = "core/mrp_pdu.c"

ONE_PORT_REFUSAL_KEPT = [(
    "    if (priv_of(app)->n_ports <= 1u) {\n        return 0; /* No other port to propagate to (LWSRP_ONE_PORT_MAP). */\n    }",
    "    if (priv_of(app)->n_ports <= 1u) {\n        void *probe = shlan_calloc(1, sizeof(struct mrp_map_work));\n"
    "        if (!probe) {\n            priv_of(app)->map_error = -SHLAN_ERROR_NO_MEMORY;\n"
    "            return -SHLAN_ERROR_NO_MEMORY;\n        }\n        shlan_free(probe);\n        return 0;\n    }")]
ONE_PORT_INERT = [
    ("    if (priv_of(app)->n_ports <= 1u) {\n        return 0; /* No other port",
     "    if (priv_of(app)->n_ports <= 0u) {\n        return 0; /* No other port"),
    ("indicated = indicated && priv_of(app)->n_ports > 1u;", "indicated = indicated && priv_of(app)->n_ports > 0u;")]
ONE_PORT_POLICY_CALLED = [("indicated = indicated && priv_of(app)->n_ports > 1u;", "(void)0;")]
LEAN_DELIVERED_UNZEROED = [("                if (on_attr) {\n                    memset(value, 0, sizeof(value));\n                }\n",
                            "")]

PROBES = [
    ("one-port-refusal-kept", MAD, ONE_PORT_REFUSAL_KEPT, "end"),
    ("one-port-refusal-kept-alone", MAD, ONE_PORT_REFUSAL_KEPT, "one"),
    ("one-port-inert", MAD, ONE_PORT_INERT, "end"),
    ("one-port-policy-called", MAD, ONE_PORT_POLICY_CALLED, "end"),
    ("lean-delivered-unzeroed", PDU, LEAN_DELIVERED_UNZEROED, "end"),
    ("lean-delivered-unzeroed-alone", PDU, LEAN_DELIVERED_UNZEROED, "lean"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("checkout", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--milan", default="OFF")
    ap.add_argument("--seeds", type=int, default=200)
    a = ap.parse_args()
    spec = importlib.util.spec_from_file_location("cd", a.checkout / "tests/check_differential.py")
    cd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cd)
    switches = {"end": cd.END_STATION, "one": cd.ONE_PORT, "lean": cd.LEAN}
    work = a.work.resolve()
    work.mkdir(parents=True)
    base = work / "base"
    base.mkdir()
    subprocess.run(["git", "-C", str(a.checkout), "archive", "-o", str(work / "base.tar"), cd.BASE, "src"], check=True)
    subprocess.run(["tar", "-xf", str(work / "base.tar"), "-C", str(base)], check=True)
    ref = cd.build(work, "base", base / "src", "mad", [], a.milan)
    steps = cd.PROGRAMS["mad"][2]
    expected = {}
    for seed in range(1, a.seeds + 1):
        rc, out = cd.trace(ref, seed, steps)
        expected[seed] = (cd.compared("mad", [], out), cd.compared("mad", cd.ONE_PORT, out))
    survived = 0
    for name, path, edits, sw in PROBES:
        extra = switches[sw]
        tree = work / f"probe-{name}"
        shutil.copytree(a.checkout / "src", tree / "src")
        target = tree / "src" / path
        text = target.read_text()
        for old, new in edits:
            if old not in text:
                print(f"TARGET-MISSING {name}")
                return 2
            text = text.replace(old, new, 1)
        target.write_text(text)
        exe = cd.build(work, f"probe-{name}", tree / "src", "mad", extra, a.milan)
        if not exe:
            print(f"BUILD-FAIL {name}")
            continue
        seen = None
        excused = 0
        for seed in range(1, a.seeds + 1):
            rc, out = cd.trace(exe, seed, steps)
            mine = cd.compared("mad", extra, out)
            ref_of = expected[seed][cd.one_port_build(extra)]
            if rc == 0 and mine is None and ref_of is None:
                excused += 1
                continue
            if rc != 0 or mine != ref_of:
                seen = seed
                break
        print(f"{'KILLED' if seen else 'SURVIVED'} {name} [{sw}] milan={a.milan}" +
              (f" at seed {seen}" if seen else f" over {a.seeds} seeds ({excused} excused)"), flush=True)
        survived += seen is None
    print(f"Probes: {len(PROBES)}; survived: {survived}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
