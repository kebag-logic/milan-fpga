#!/usr/bin/env python3
"""Reviewer probes on KL_aaf_clock_meter (disposable copies; no tracked file edited).
Each probe applies exact replacements (each anchor must occur exactly once),
builds the meter harness with METER_RTL/MDIR overrides and runs every case.
CAUGHT = build ok and harness exit 1 with at least one [FAIL]; SURVIVED = exit 0.
Usage: meter_probes.py <repo> <workdir>"""
import subprocess, sys, os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
suite = repo / 'tb/verilator/aaf_clock_meter'
rtl = (repo / 'hdl/ieee1722/crf/KL_aaf_clock_meter.sv').read_text()
PROBES = {
  'clean_control': [],
  'max_dev_not_cleared_at_era_start': [("        mr_toggle_p_o <= 1'b0;\n        max_dev_r     <= '0;\n",
                                        "        mr_toggle_p_o <= 1'b0;\n")],
  'tu_edge_clears_held_lock': [("wire lock_clr_w  = en_rise_w || en_fall_w || idx_chg_w || !en_w;",
                                "wire lock_clr_w  = en_rise_w || en_fall_w || idx_chg_w || !en_w || s2_tu_edge_w;")],
  'tu_edge_pulses_disrupt': [("      if (tout_fire_w && locked_o) begin\n",
                              "      if ((tout_fire_w && locked_o) || s2_tu_edge_w) begin\n")],
  'max_dev_no_saturation': [("          if (s2_abs_w > 32'd65535)            max_dev_r <= 16'hFFFF;\n          else if",
                             "          if")],
  'max_dev_includes_gap_pdus': [("        end else if (s2_gap_r || !grp_act_r || s2_tu_edge_w) begin\n          grp_act_r <= 1'b0;\n        end else begin\n",
                                 "        end else if (s2_gap_r || !grp_act_r || s2_tu_edge_w) begin\n          grp_act_r <= 1'b0;\n          if (16'(s2_abs_w) > max_dev_r) max_dev_r <= 16'(s2_abs_w);\n        end else begin\n")],
}
def run(name):
    src = rtl
    for a, b in PROBES[name]:
        n = src.count(a)
        if n != 1:
            return name, f'ANCHOR x{n}', ''
        src = src.replace(a, b)
    d = work / name; d.mkdir(parents=True, exist_ok=True)
    f = d / 'KL_aaf_clock_meter.sv'; f.write_text(src)
    b = subprocess.run(['make', '-s', '-C', str(suite), 'build', f'METER_RTL={f}', f'MDIR={d}/obj'],
                       capture_output=True, text=True)
    if b.returncode:
        return name, 'BUILD-FAIL', b.stderr[-2000:]
    r = subprocess.run([str(d / 'obj/Vmeter_sim')], capture_output=True, text=True, cwd=str(suite))
    fails = [l for l in r.stdout.splitlines() if 'FAIL' in l]
    (d / 'run.log').write_text(r.stdout + r.stderr)
    verdict = ('PASS(clean)' if r.returncode == 0 else 'UNEXPECTED-FAIL') if name == 'clean_control' else \
              ('CAUGHT' if r.returncode == 1 and fails else ('SURVIVED' if r.returncode == 0 else f'EXIT{r.returncode}'))
    return name, verdict, '\n'.join(fails[:6])
with ThreadPoolExecutor(max_workers=6) as ex:
    for name, verdict, detail in ex.map(run, PROBES):
        print(f'{verdict:12s} {name}')
        if detail: print('    ' + detail.replace('\n', '\n    '))
