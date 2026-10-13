"""Reviewer probes for R582-1 (PR #736, F3b): plant disposable defects in COPIES of
sw/firmware/ctrl and the stack (the repository's own ctrl_mutants.plant), run the
named arms, and report every [FAIL] line. A probe is "caught" when any arm fails
with at least one [FAIL] line; "ESCAPED" otherwise. Nothing in the checkout or
the submodule is written.

usage: python3 -I probe_f3b.py REPO WORKDIR JOBS [probe-name ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3])
only = set(sys.argv[4:])
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import Outcome, Refusal, Tree  # noqa: E402
from ctrl_mutant import ACMP_C, Mutant  # noqa: E402

MAAP = "maap/maap_mbx.c"
PROBES = (
    # (name, path, old, new, arms)
    ("p-timer-no-refresh", MAAP, "\t\t\trefresh_demand(m);\n\t\t\tmaap_timer_expired", "\t\t\tmaap_timer_expired",
     ("maap", "maap_if2", "acmp")),
    ("p-rx-no-refresh", MAAP, "\trefresh_demand(m);\n\tmaap_rx(", "\tmaap_rx(", ("maap", "maap_if2", "acmp")),
    ("p-link-no-refresh", MAAP, "\t\t\trefresh_demand(m);\n\t\t\tmaap_port_operational",
     "\t\t\tmaap_port_operational", ("maap", "maap_if2", "acmp")),
    ("p-no-expiry-retire", MAAP, "\t\t\t(void)acmp_declaring(m->acmp, s);\n", "", ("maap", "acmp")),
    ("p-poll-no-refresh", MAAP, "\tbool owed = false;\n\trefresh_demand(m);\n", "\tbool owed = false;\n",
     ("maap", "acmp")),
    ("p-poll-never-republish", MAAP, "if (gate != m->published_gate[k])", "if (false)", ("maap", "acmp")),
    ("p-ignore-source-interface", MAAP, "m->acmp->cfg.source_interface[s] == interface && ",
     "(m->acmp->cfg.source_interface[s] == interface || s < 32u) && ", ("maap", "maap_if2")),
    ("p-fresh-14999", "acmp/acmp_mbx.c", "config.da_fresh_ms = 15000u;", "config.da_fresh_ms = 14999u;",
     ("acmp",)),
    ("p-stop-keeps-gate", MAAP, "\tm->published_gate[interface] = declaring(m, interface, count, valid);",
     "\tm->published_gate[interface] = valid ? declaring(m, interface, count, valid) : m->published_gate[interface];",
     ("maap", "maap_if2")),
    ("p-stack-dest-fail-no-demand", ACMP_C,
     "((frame[O_STATUS] >> 3) == ACMP_STATUS_SUCCESS ||\n\t     (frame[O_STATUS] >> 3) == ACMP_STATUS_TALKER_DEST_MAC_FAIL))",
     "((frame[O_STATUS] >> 3) == ACMP_STATUS_SUCCESS))", ("maap", "acmp")),
)


def main() -> int:
    arms = {"maap": ctrl_arms.arm_maap, "maap_if2": ctrl_arms.arm_maap_if2, "acmp": ctrl_arms.arm_acmp,
            "acmpif2": ctrl_arms.arm_acmpif2}
    build = fw_gtest.Build(jobs=jobs)
    reuse = work / "reuse"
    results = []
    for name, path, old, new, use in PROBES:
        if only and name not in only:
            continue
        m = Mutant(name, path, old, new, use[0], "", "")
        try:
            ctrl, stack = ctrl_mutants.plant(m, work)
        except Refusal as exc:
            print(f"[REFUSED] {name}: {exc}", flush=True)
            results.append((name, "REFUSED"))
            continue
        tree = Tree(ctrl, work / "work" / "build", reuse, build, stack)
        fails: list[str] = []
        rcs = []
        for arm in use:
            try:
                outcome = arms[arm](tree)
            except Refusal as exc:
                outcome = Outcome(arm, 2, f"refused: {exc}")
            rcs.append(f"{arm}=rc{outcome.rc}")
            fails += [f"{arm}: {ln.strip()}" for ln in outcome.log.splitlines() if "[FAIL]" in ln]
            if outcome.rc not in (0, 1):
                fails.append(f"{arm}: BUILD/RUN rc {outcome.rc}: {outcome.log.strip().splitlines()[-1:]}")
        verdict = "caught" if any("[FAIL]" in f for f in fails) else "ESCAPED"
        print(f"[{verdict}] {name} ({', '.join(rcs)}): {len(fails)} failing line(s)", flush=True)
        for f in fails[:6]:
            print(f"    {f}", flush=True)
        results.append((name, verdict))
    print("SUMMARY " + " ".join(f"{n}={v}" for n, v in results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
