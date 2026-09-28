#!/usr/bin/env python3
"""R394-1 CRF lock-phase probe for tb/verilator/capture_coherence (#617).

The committed junction harness locks CRF at sixteen TDM start offsets 260
steps (about 65 axis cycles) apart. This probe copies the suite into a
sibling directory, replaces only its scenario list with CRF scenarios at the
start delays given, builds it through the suite's own Makefile recipe, and
runs it. Every check and print of the committed harness is unchanged.

  python3 r394_crf_phase_probe.py <suite-dir> <probe-name> <plan> <columns> <delay> [<delay> ...]

<plan> is "true" (the 391/1591 plan) or an integer ppm. The tree the suite
lives in must be a disposable copy: the probe directory is created beside it.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    suite = Path(sys.argv[1]).resolve()
    name, plan, cols = sys.argv[2], sys.argv[3], int(sys.argv[4])
    delays = [int(x) for x in sys.argv[5:]]
    probe = suite.parent / f"cc_probe_{name}"
    if probe.exists():
        shutil.rmtree(probe)
    shutil.copytree(suite, probe, ignore=shutil.ignore_patterns("obj_*", "obj_dir"))
    src = (probe / "sim_main.cpp").read_text()
    plan_expr = "true_plan()" if plan == "true" else f"ppm_plan({int(plan)})"
    body = "\n".join(
        f'    list.push_back({{"P{name}-d{d}", {plan_expr}, true, {d}L, {cols}, false}});' for d in delays)
    new = ("std::vector<Scenario> scenarios(bool quick) {\n"
           "    (void)quick;\n    std::vector<Scenario> list;\n" + body + "\n    return list;\n}\n")
    src2, n = re.subn(r"std::vector<Scenario> scenarios\(bool quick\) \{.*?\n\}\n", new, src, count=1,
                      flags=re.S)
    if n != 1:
        print("scenario list not found")
        return 2
    (probe / "sim_main.cpp").write_text(src2)
    # information only: per-pair frame continuity in the CRF tail, so a
    # crossing on pairs 1..3 (the pre-#617 law) is visible too; no check changes
    bench = (probe / "coherence_bench.hpp").read_text()
    hooks = [
        ("        t_.states[key]++;\n",
         "        t_.states[key]++;\n"
         "        for (int p = 0; p < kPairs; p++) {\n"
         "            const long fp = frame[static_cast<size_t>(2 * p)];\n"
         "            if (have_pp_ && tail_ && fp - prev_pp_[static_cast<size_t>(p)] != 1) r394_pp_[static_cast<size_t>(p)]++;\n"
         "            prev_pp_[static_cast<size_t>(p)] = fp;\n"
         "        }\n"
         "        have_pp_ = true;\n"),
        ("        in_cluster_ = false;\n    }\n\n    //! one accepted AXIS beat",
         "        in_cluster_ = false;\n        have_pp_ = false;\n        r394_pp_ = {};\n    }\n\n"
         "    //! one accepted AXIS beat"),
        ("    bool live_ = false;\n",
         "    bool live_ = false;\n"
         "    bool have_pp_ = false;\n"
         "    std::array<long, kPairs> prev_pp_{};\n"
         "  public:\n"
         "    std::array<long, kPairs> r394_pp_{};\n"
         "  private:\n"),
    ]
    for pat, rep in hooks:
        if bench.count(pat) != 1:
            print("bench hook not found:", pat)
            return 2
        bench = bench.replace(pat, rep)
    (probe / "coherence_bench.hpp").write_text(bench)
    sm = (probe / "sim_main.cpp").read_text()
    pat = "    bench_.print_table();\n"
    if sm.count(pat) != 1:
        print("print hook not found")
        return 2
    sm = sm.replace(pat, pat + "    std::printf(\"  [r394] tail per-pair slips: %ld %ld %ld %ld\\n\", bench_.r394_pp_[0],"
                    " bench_.r394_pp_[1], bench_.r394_pp_[2], bench_.r394_pp_[3]);\n")
    (probe / "sim_main.cpp").write_text(sm)
    b = subprocess.run(["make", "-s", "-C", str(probe), "build"], capture_output=True, text=True, check=False)
    if b.returncode != 0:
        print(b.stdout[-3000:], b.stderr[-3000:])
        return 3
    r = subprocess.run([str(probe / "obj_dir" / "Vcoherence_sim")], cwd=probe, capture_output=True, text=True,
                       check=False)
    print(r.stdout)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
