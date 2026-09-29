#!/usr/bin/env python3
"""R394-2/R394-3 CRF engagement-phase probe for tb/verilator/capture_coherence (#617).

Copies a checkout's suite directory beside itself, replaces ONLY the
scenario and sweep lists of sim_main.cpp (every check, print and the bench are
the committed ones), builds it through the suite's own Makefile recipe
(optionally against a mutated wrapper via WRAP_SRC or crossbar via CMAP_SRC),
and runs the requested CRF engagements, split over up to 8 processes.

  python3 r394_probe.py <suite-dir> <tag> <plan> <columns> <spec> [--wrap F] [--cmap F] [--jobs N]

<plan>  "true" (the 391/1591 plan) or an integer ppm.
<spec>  "off:LO:HI:STEP" places engagements from LO to HI cycles of the
        crossing in STEP quarter-cycles (oscillator steps) using the harness's
        own calibration and delay_for(); "steps:A,B,..." gives raw hold steps.
Each engagement prints the harness's own [i] line; the probe prints the rc and
the check tally of every shard. Nothing in the source tree is written.
"""

import argparse
import concurrent.futures as cf
import re
import shutil
import subprocess
import sys
from pathlib import Path

PATCH = r'''
std::vector<Scenario> r394_list() {
    std::vector<Scenario> list;
    const char* f = std::getenv("R394_SCEN");
    if (!f) return list;
    std::FILE* fp = std::fopen(f, "r");
    char name[64], plan[16];
    long delay = 0, cols = 0, placed = 0;
    int has_placed = 0;
    while (fp && std::fscanf(fp, "%63s %15s %ld %ld %d %ld", name, plan, &delay, &cols, &has_placed, &placed) == 6) {
        const ClockPlan p = std::string(plan) == "true" ? true_plan() : ppm_plan(std::atoi(plan));
        list.push_back({name, p, true, delay, cols, false, false, has_placed ? placed : kUnplaced});
    }
    if (fp) std::fclose(fp);
    return list;
}

std::vector<Scenario> scenarios(Mode mode) {
    (void)mode;
    return r394_list();
}

std::vector<Sweep> sweeps(Mode mode) {
    (void)mode;
    return {};
}
'''


def patch_suite(src_suite: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src_suite, dst, ignore=shutil.ignore_patterns("obj_*", "obj_dir", "*.hex"))
    sm = (dst / "sim_main.cpp").read_text()
    new, n = re.subn(r"std::vector<Scenario> scenarios\(Mode mode\) \{.*?\n\}\n\nstd::vector<Sweep> sweeps\(Mode mode\) \{.*?\n\}\n",
                     PATCH.lstrip("\n"), sm, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("scenario/sweep lists not found")
    (dst / "sim_main.cpp").write_text(new)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("suite")
    ap.add_argument("tag")
    ap.add_argument("plan")
    ap.add_argument("columns", type=int)
    ap.add_argument("spec")
    ap.add_argument("--wrap")
    ap.add_argument("--cmap")
    ap.add_argument("--dp-src")
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    suite = Path(a.suite).resolve()
    probe = suite.parent / f"cc_r394_{a.tag}"
    patch_suite(suite, probe)
    make = ["make", "-s", "-C", str(probe), "build"]
    if a.wrap:
        make.append(f"WRAP_SRC={Path(a.wrap).resolve()}")
    if a.cmap:
        make.append(f"CMAP_SRC={Path(a.cmap).resolve()}")
    if a.dp_src:
        make.append(f"DP_SRC={Path(a.dp_src).resolve()}")
    b = subprocess.run(make, capture_output=True, text=True, check=False)
    if b.returncode != 0:
        print(b.stdout[-3000:], b.stderr[-3000:])
        return 3
    exe = probe / "obj_dir" / "Vcoherence_sim"
    # calibration: where the first close lands with the clock unheld (the
    # harness's own calibrate(), through a one-scenario run with no hold)
    scen = []
    if a.spec.startswith("steps:"):
        for d in a.spec[6:].split(","):
            scen.append((f"{a.tag}-s{d}", int(d), 0, 0))
    else:
        _, lo, hi, step = a.spec.split(":")
        cal = probe / "cal.txt"
        cal.write_text(f"cal {a.plan} 0 40 0 0\n")
        r = subprocess.run([str(exe)], cwd=probe, env={"R394_SCEN": str(cal), "PATH": "/usr/bin:/bin"},
                           capture_output=True, text=True, check=False)
        m = re.search(r"engaged ([+-]\d+) cycles from the crossing", r.stdout)
        if not m:
            print(r.stdout[-2000:])
            return 4
        unheld = int(m.group(1))
        frame_steps = 50e6 / 48000.0 * 4
        print(f"[r394] calibration {a.plan}: unheld engagement lands {unheld:+d} cycles from the crossing")
        q = int(float(lo) * 4)
        while q <= int(float(hi) * 4):
            off = q / 4.0
            d = ((off - unheld) * 4) % frame_steps
            scen.append((f"{a.tag}{off:+.2f}", int(round(d)), 1, int(round(off))))
            q += int(step)
    shards = [scen[i::a.jobs] for i in range(a.jobs) if scen[i::a.jobs]]

    def run_shard(i: int, sh) -> tuple[int, int, str]:
        f = probe / f"shard{i}.txt"
        f.write_text("".join(f"{n} {a.plan} {d} {a.columns} {hp} {pl}\n" for n, d, hp, pl in sh))
        r = subprocess.run([str(exe)], cwd=probe, env={"R394_SCEN": str(f), "PATH": "/usr/bin:/bin"},
                           capture_output=True, text=True, check=False)
        return i, r.returncode, r.stdout

    total_rc = 0
    outs = []
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for i, rc, out in ex.map(lambda t: run_shard(*t), enumerate(shards)):
            outs.append((i, rc, out))
    for i, rc, out in sorted(outs):
        tally = re.search(r"checks: (\d+)\s+failures: (\d+)", out)
        print(f"[r394] shard {i}: rc={rc} {tally.group(0) if tally else 'NO TALLY'}")
        for line in out.splitlines():
            if "engaged" in line or "[FAIL]" in line or "columns in" in line or "last slip" in line or "keep-off" in line:
                print("   ", line.strip())
        total_rc |= rc
    print(f"[r394] {len(scen)} engagements, overall rc={total_rc}")
    return total_rc


if __name__ == "__main__":
    sys.exit(main())
