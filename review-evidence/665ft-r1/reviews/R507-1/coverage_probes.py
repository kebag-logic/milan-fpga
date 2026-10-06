#!/usr/bin/env python3
"""Independent coverage probes; only disposable sources are written."""
import argparse
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
a = p.parse_args()
repo = a.repo.resolve()
work = Path(__file__).resolve().parent / "scratch" / "coverage-probes"
work.mkdir(parents=True, exist_ok=True)
sys.path[:0] = [str(repo / "sw/firmware/gtest"), str(repo / "sw/firmware/ctrl_nvm/test")]
import fw_coverage as cov
import nvm_bench as bench

def run(argv, cwd):
    r = subprocess.run([str(x) for x in argv], cwd=cwd, capture_output=True, text=True, check=False)
    if r.returncode:
        raise RuntimeError(r.stdout + r.stderr)
    if r.stdout.strip():
        print(r.stdout.strip())
    return r

inputs = bench.shape_inputs(repo / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "inputs")
bench.write_headers(work / "gen", bench.shape_header(inputs.shape, inputs.donor, inputs.ident), inputs.clock_hz)
src = work / "short_loaded.c"
src.write_text('''#include <stdio.h>
#include <string.h>
#include "nvm_klj2.h"
int main(void) {
    static unsigned char whole[NVM_IMG_LEN];
    unsigned char header[NVM_KLJ2_HDR];
    nvm_klj2_blank(whole);
    int full = nvm_klj2_check(whole, sizeof whole);
    memcpy(header, whole, sizeof header);
    int short_result = nvm_klj2_check_body(header, NVM_IMG_LEN, sizeof header);
    printf("CRC-closed whole container: verdict=%d (OK=%d)\\n", full, NVM_VD_OK);
    printf("Public check_body with loaded=%u, img_len=%u: verdict=%d (REC=%d)\\n",
           (unsigned)sizeof header, (unsigned)NVM_IMG_LEN, short_result, NVM_VD_REC);
    return !(full == NVM_VD_OK && short_result == NVM_VD_REC);
}
''')
fw = repo / "sw/firmware/ctrl_nvm/nvm_klj2.c"
run(["gcc", "-std=c11", "-O0", "--coverage", "-I" + str(work / "gen"),
     "-I" + str(fw.parent), "-c", fw, "-o", work / "codec.o"], work)
run(["gcc", "-std=c11", "-O0", "-I" + str(work / "gen"), "-I" + str(fw.parent),
     src, work / "codec.o", "--coverage", "-o", work / "short_loaded"], work)
run([work / "short_loaded"], work)
measured = cov.collect([work])["sw/firmware/ctrl_nvm/nvm_klj2.c"]
for n, text in enumerate(fw.read_text().splitlines(), 1):
    if "pos + NVM_REC_HDR > loaded" in text:
        print(f"Original firmware line {n}: {text.strip()}, arcs={measured.lines[n].arcs}")
        print(f"Original firmware line {n+1}: executed {measured.lines[n+1].count} time(s)")
        assert all(measured.lines[n].arcs)
        assert measured.lines[n+1].count > 0

print("\nCompensating coverage swap against the real gcov reader:")
root = work / "synthetic"
rel = "sw/firmware/ctrl/swap.c"
source = root / rel
source.parent.mkdir(parents=True, exist_ok=True)
source.write_text('''int f(int x) {
    if (x == 7)
        return 7;
    if (x == 9)
        return 9;
    return 0;
}
''')
cov.ROOT = root
row = cov.Exclusion(rel, "f", "if (x == 7)", "1 arc, 1 line", "The accepted input population never supplies 7.")
floor = None
for tag, values in (("before", (0, 9)), ("after", (0, 7))):
    b = root / tag
    b.mkdir(exist_ok=True)
    (b / "main.c").write_text(f"int f(int); int main(void) {{ f({values[0]}); f({values[1]}); return 0; }}\n")
    run(["gcc", "-O0", "--coverage", "-c", source, "-o", b / "swap.o"], b)
    run(["gcc", "-O0", b / "main.c", b / "swap.o", "--coverage", "-o", b / "run"], b)
    run([b / "run"], b)
    merged = cov.collect([b])
    print(tag, "uncovered lines", [n for n, ln in merged[rel].lines.items() if ln.count == 0])
    print(tag, "uncovered arcs", [(n, ln.arcs) for n, ln in merged[rel].lines.items() if 0 in ln.arcs])
    kept, findings = cov.apply_exclusions(merged, [row], root)
    tallies = cov.tally(kept)
    if floor is None:
        floor = tallies
    findings += cov.compare(tallies, floor)
    print(tag, "gate findings:", findings, "coverage:", tallies[rel])
    assert not findings
print("REPRODUCED: a reachable public refusal is excluded; a different uncovered branch can inherit an exclusion.")
