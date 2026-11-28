#!/usr/bin/env python3
"""Reviewer mutation probes for PR #1026 at head 47f2a3d7 (round R968-2).

usage: python3 -I mutants_r968_2.py PRISTINE_TREE WORK_DIR OUT_DIR [JOBS [NAME...]]

PRISTINE_TREE is an untouched copy of the exact head's working tree (no .git needed). Each mutant gets its own
hard-linked copy under WORK_DIR, one exact-string edit (the edited file's link is broken first), and one command.
A mutant is CAUGHT when the command exits non-zero, ESCAPED when it exits 0. `verilator` must be on PATH for the
bench mutants (5.050 was used). Nothing outside WORK_DIR and OUT_DIR is written.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

H = 'tb/verilator/ctrl_service_budget'
MII = ['python3', '-I', '-B', f'{H}/egress_mii.py', '--selftest']
REC = ['python3', '-I', '-B', f'{H}/record_classes.py', '--selftest']
LED = ['python3', '-I', '-B', f'{H}/egress_ledger.py', '--selftest']
FIX = ['python3', '-I', '-B', f'{H}/egress_fixed.py', '--selftest']
FIX100 = ['python3', '-I', '-B', f'{H}/egress_fixed.py', 'BUILD_DIR', '100000000']
REGRADE = ['python3', '-I', '-B', f'{H}/egress_mii.py', 'EXTRACT_BUILDS']
FIXBAD = ['python3', '-I', '-B', f'{H}/egress_fixed.py', 'BUILD_DIR', '\u00b2']
STRUCT = ['python3', '-I', '-B', f'{H}/egress_mii.py', '--structural', '--point', 'arty-4x4']

#: name: (file, old, new, command, what it plants)
MUTANTS = {
    'clean-mii': (None, '', '', MII, 'unchanged tree'),
    'clean-rec': (None, '', '', REC, 'unchanged tree'),
    'clean-led': (None, '', '', LED, 'unchanged tree'),
    'clean-fix': (None, '', '', FIX, 'unchanged tree'),
    'A1-crf-not-in-sources': (f'{H}/egress_mii.py', '    return aaf + crf\n', '    return aaf\n', MII,
                              "sr_frames leaves the CRF output's frame out"),
    'A2-crf-octet-short': (f'{H}/egress_mii.py', 'CRF_AVTPDU = 28\n', 'CRF_AVTPDU = 27\n', MII,
                           'the CRF AVTPDU an octet short'),
    'A4-4x4-point-reads-1x1-config': (f'{H}/egress_mii.py', "'arty-4x4': 'endstation_arty_split_4x4'}\n#: Each point",
                                      "'arty-4x4': 'endstation_arty_split'}\n#: Each point", MII,
                                      "the 4x4 point's queue read from the 1x1 product configuration"),
    'A5-python-queue-drops-last-frame': (f'{H}/egress_mii.py', 'self.others.extend(p.sr_bytes)',
                                         'self.others.extend(p.sr_bytes[:4])', MII,
                                         "the grade's queue model carries only four SR frames"),
    'A6-testbench-queue-drops-last-frame': (
        f'{H}/egress_queue.hpp', 'for (const unsigned bytes : p_.sr_bytes) others_.push_back(bytes);',
        'for (std::size_t i = 0; i < p_.sr_bytes.size() && i < 4; ++i) others_.push_back(p_.sr_bytes[i]);', MII,
        "the testbench's queue carries only four SR frames"),
    'A8-structural-ignores-point': (f'{H}/egress_mii.py', "print('\\n'.join(structural(params(point_spec(point)))))",
                                    "print('\\n'.join(structural(params(arty_spec()))))", MII,
                                    '--structural --point prints the 1x1 queue under the named point'),
    'A9-packet-ignores-point': (f'{H}/egress_mii.py',
                                "        p = params(point_spec(point))\n        ok, lines = verdict(",
                                "        p = params(arty_spec())\n        ok, lines = verdict(", MII,
                                '--packet --point grades at the 1x1 queue'),
    'B1-4x4-clock-80': (f'{H}/record_classes.py', "'arty-4x4': 100_000_000}\nARTY_POINTS",
                        "'arty-4x4': 80_000_000}\nARTY_POINTS", REC, 'the 4x4 point held at 80 MHz'),
    'B2-4x4-config-named-1x1': (f'{H}/record_classes.py', "'endstation_arty_split_4x4': 'arty-4x4'}",
                                "'endstation_arty_split_4x4': 'arty-1x1'}", REC,
                                "the 4x4 configuration named to the 1x1 point"),
    'B3-4x4-no-reboot-path': (f'{H}/record_classes.py', "REBOOT_PATH_POINTS = ('1x1/1if', 'arty-1x1', 'arty-4x4')",
                              "REBOOT_PATH_POINTS = ('1x1/1if', 'arty-1x1')", REC,
                              'the 4x4 point not held to its REBOOTs and GET_AS_PATH'),
    'B4-4x4-not-complete': (f'{H}/record_classes.py', "COMPLETE = ('1x1/1if', '8x8/1if', 'arty-1x1', 'arty-4x4')",
                            "COMPLETE = ('1x1/1if', '8x8/1if', 'arty-1x1')", REC,
                            'the 4x4 point not among the points a pass is held complete at'),
    'B5-4x4-label-1x1': (f'{H}/record_classes.py', "'arty-1x1': 'arty-1x1', 'arty-4x4': 'arty-4x4'}",
                         "'arty-1x1': 'arty-1x1', 'arty-4x4': 'arty-1x1'}", REC, "the 4x4 point's run label the 1x1's"),
    'B6-poll-shape-155-named-1x1': (f'{H}/poll_grade.py', "shape_costs.Shape(1, 5, 5): 'arty-4x4'}",
                                    "shape_costs.Shape(1, 5, 5): 'arty-1x1'}", REC,
                                    "the (1,5,5) shape's kept-record cost read at the 1x1 point"),
    'B8-4x4-clock-not-checked': (f'{H}/record_classes.py',
                                 "if leg.point in ARTY_POINTS and (leg.cpu_hz, leg.sys_hz) !=",
                                 "if leg.point == 'arty-1x1' and (leg.cpu_hz, leg.sys_hz) !=", REC,
                                 "a 4x4 leg's clock never checked"),
    'C1-ledger-4x4-cycle-80': (f'{H}/egress_ledger.py', "'arty-1x1': 80_000, 'arty-4x4': 100_000}",
                               "'arty-1x1': 80_000, 'arty-4x4': 80_000}", LED, "the 4x4's planted cycle the 80 MHz one"),
    'C3-ledger-plant-ignores-table': (f'{H}/egress_ledger.py', 'cycle_ms = 1 / CLOCK_KHZ[point]',
                                      'cycle_ms = 1 / 80_000', LED,
                                      'the plant uses a 12.5 ns cycle at every point, whatever the table'),
    'D1-build-flag-fixed': (f'{H}/egress_fixed.py', '-DEGRESS_FIXED_SYS_PS={sys_ps}', '-DEGRESS_FIXED_SYS_PS=12500',
                            FIX, 'build() passes the default period whatever it is given'),
    'D3-no-whole-ps': (f'{H}/egress_fixed.py', " or 10**12 % int(text):", ":", FIX,
                       'a SYS_HZ with a fractional-ps period accepted'),
    'D2-bench-ignores-define-selftest': (f'{H}/egress_fixed_main.cpp',
                                         'constexpr std::uint64_t kSysPs = EGRESS_FIXED_SYS_PS;',
                                         'constexpr std::uint64_t kSysPs = 12500;', FIX,
                                         'the bench ignores the sys period the build names (self-test)'),
    'D2-bench-ignores-define-run100': (f'{H}/egress_fixed_main.cpp',
                                       'constexpr std::uint64_t kSysPs = EGRESS_FIXED_SYS_PS;',
                                       'constexpr std::uint64_t kSysPs = 12500;', FIX100,
                                       'the bench ignores the sys period the build names (documented 100 MHz run)'),
    'A8-structural-ignores-point-print': (f'{H}/egress_mii.py',
                                          "print('\\n'.join(structural(params(point_spec(point)))))",
                                          "print('\\n'.join(structural(params(arty_spec()))))", STRUCT,
                                          'what --structural --point arty-4x4 prints under that mutant'),
    'M1-crf-empty-tuple': (f'{H}/egress_mii.py', "    crf = (SR_HEADER + CRF_AVTPDU,) if ", "    crf = () if ", MII,
                           "round 1's M1: the CRF output's frame never added"),
    'M1b-crf-zero-length': (f'{H}/egress_mii.py', 'CRF_AVTPDU = 28\n', 'CRF_AVTPDU = 0\n', MII,
                            'the CRF AVTPDU at zero length'),
    'B5b-1x1-label-ax': (f'{H}/record_classes.py', "'arty-1x1': 'arty-1x1', 'arty-4x4': 'arty-4x4'}",
                         "'arty-1x1': '1x1', 'arty-4x4': 'arty-4x4'}", REC,
                         "the same label defect at the 1x1 point, for comparison"),
    'E1-census-regrade-without-crf': (f'{H}/egress_mii.py', '    return aaf + crf\n', '    return aaf\n', REGRADE,
                                      'the published census-4 extract regraded by a model with no CRF frame'),
    'E2-census-regrade-crf-octet-short': (f'{H}/egress_mii.py', 'CRF_AVTPDU = 28\n', 'CRF_AVTPDU = 27\n', REGRADE,
                                          'the published census-4 extract regraded with the CRF frame an octet short'),
    'E3-census-regrade-queue-drops-crf': (f'{H}/egress_mii.py', 'self.others.extend(p.sr_bytes)',
                                          'self.others.extend(p.sr_bytes[:4])', REGRADE,
                                          'the published extract regraded by a queue that states five frames and '
                                          'carries four'),
    'X1-fixed-superscript-digit': (None, '', '', FIXBAD, 'unchanged tree, SYS_HZ a superscript digit (U+00B2)'),
}


def one(name: str, pristine: Path, work: Path, out: Path) -> dict:
    """Plant one mutant in its own copy, run its command, record the verdict."""
    file, old, new, cmd, what = MUTANTS[name]
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    subprocess.run(['cp', '-al', str(pristine), str(tree)], check=True)
    if file:
        target = tree / file
        text = target.read_text()
        if text.count(old) != 1:
            return dict(name=name, verdict='NOT-PLANTED', found=text.count(old))
        target.unlink()
        target.write_text(text.replace(old, new))
    argv = [str(tree / 'build-fixed') if a == 'BUILD_DIR' else a for a in cmd]
    if 'EXTRACT_BUILDS' in argv:  # the published census-4 extract's variant directories (R968_EXTRACT)
        builds = sorted(str(d) for d in Path(os.environ['R968_EXTRACT']).iterdir() if d.is_dir())
        argv = argv[:-1] + builds
    done = subprocess.run(argv, cwd=tree, capture_output=True, text=True, timeout=1500)
    lines = [ln for ln in (done.stdout + done.stderr).splitlines() if not ln.startswith(('%Warning', ' ', '...'))]
    (out / f'{name}.log').write_text('\n'.join(lines).replace(str(tree), '<TREE>') + '\n')
    verdict = ('PASS' if done.returncode == 0 else 'FAIL') if file is None else (
        'ESCAPED' if done.returncode == 0 else 'CAUGHT')
    keep = [ln for ln in lines if not ln.startswith('GRADED') or 'refused' in ln or '"agree_ps": 0' not in ln]
    (out / f'{name}.log').write_text('\n'.join(keep).replace(str(tree), '<TREE>').replace(
        os.environ.get('R968_EXTRACT', '\0'), '<EXTRACT>') + '\n')
    shutil.rmtree(tree)
    return dict(name=name, file=file, plant=what, old=old, new=new, command=' '.join(cmd), rc=done.returncode,
                verdict=verdict)


def main(argv: list[str]) -> int:
    pristine, work, out = (Path(a).resolve() for a in argv[:3])
    jobs = int(argv[3]) if len(argv) > 3 else 8
    names = argv[4:] or list(MUTANTS)
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(jobs) as pool:
        rows = list(pool.map(lambda n: one(n, pristine, work, out), names))
    name = 'mutants.json' if not argv[4:] else 'mutants-' + '-'.join(n.split('-')[0] for n in names) + '.json'
    (out / name).write_text(json.dumps(rows, indent=1) + '\n')
    for r in rows:
        print(f"{r['verdict']:<11} {r['name']} rc={r.get('rc')}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
