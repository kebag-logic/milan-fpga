"""Disposable mutation probes for the round-5 controls of PR #1026 at a given head.

usage: python3 -I mutants.py REPO_CLONE WORK_DIR OUT_JSON [NAME_PREFIX...]

The clone's checked-out submodules are copied (not linked) into the base, since some self-tests read them.

Archives the clone's HEAD into WORK_DIR/base, then for each mutant hard-links a copy, replaces the one mutated file
(a new inode, so the base is untouched), runs the named self-test there and records its exit status. A mutant is
CAUGHT when the self-test exits non-zero. The unmutated base is run first for each self-test and must exit 0.
"""
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

D = 'tb/verilator/ctrl_service_budget'
MUTANTS = {
    'M1 sr_frames drops the CRF frame (return aaf)': (f'{D}/egress_mii.py', '    return aaf + crf\n', '    return aaf\n',
                                                        'egress_mii.py --selftest'),
    'M2 CRF_AVTPDU = 0': (f'{D}/egress_mii.py', 'CRF_AVTPDU = 28\n', 'CRF_AVTPDU = 0\n', 'egress_mii.py --selftest'),
    'M3 crf = ()': (f'{D}/egress_mii.py', "    crf = (SR_HEADER + CRF_AVTPDU,) if", "    crf = () if",
                    'egress_mii.py --selftest'),
    'M4 CRF frame 86 octets (six timestamps a PDU)': (f'{D}/egress_mii.py', 'CRF_AVTPDU = 28\n', 'CRF_AVTPDU = 68\n',
                                                      'egress_mii.py --selftest'),
    'M5 point_name maps the 4x4 config to arty-1x1': (f'{D}/record_classes.py', "'endstation_arty_split_4x4': 'arty-4x4'}",
                                                      "'endstation_arty_split_4x4': 'arty-1x1'}",
                                                      'record_classes.py --selftest'),
    'M6 ARTY_CLOCKS arty-4x4 at 80 MHz': (f'{D}/record_classes.py', "'arty-4x4': 100_000_000}",
                                          "'arty-4x4': 80_000_000}", 'record_classes.py --selftest'),
    'M7 poll_grade reads arty-1x1 record.acmp at (1,5,5)': (f'{D}/poll_grade.py',
                                                            "shape_costs.Shape(1, 5, 5): 'arty-4x4'}",
                                                            "shape_costs.Shape(1, 5, 5): 'arty-1x1'}",
                                                            'record_classes.py --selftest'),
    'M8 egress_ledger CLOCK_KHZ arty-4x4 at 80 MHz': (f'{D}/egress_ledger.py', "'arty-4x4': 100_000}",
                                                      "'arty-4x4': 80_000}", 'egress_ledger.py --selftest'),
    'M9 egress_fixed whole-ps check removed': (f'{D}/egress_fixed.py', ' or 10**12 % int(text):', ':',
                                               'egress_fixed.py --selftest'),
    'M10 egress_fixed over() never over': (f'{D}/egress_fixed.py', '    return ps > egress_mii.MII_FIXED_NS * 1000\n',
                                           '    return False\n', 'egress_fixed.py --selftest'),
    'M11 STREAM_LOAD restated without the CRF frame': (f'{D}/egress_mii.py', "'arty-4x4': (90, 90, 90, 90, 46)}",
                                                       "'arty-4x4': (90, 90, 90, 90)}", 'egress_mii.py --selftest'),
}


def run(tree: Path, cmd: str) -> tuple[int, str]:
    script, *args = cmd.split()
    p = subprocess.run([sys.executable, '-I', str(tree / D / script), *args], cwd=tree, capture_output=True, text=True,
                       timeout=1800)
    return p.returncode, (p.stdout + p.stderr)[-1500:]


def one(name: str, spec: tuple, base: Path, work: Path) -> dict:
    path, old, new, cmd = spec
    tree = work / name.split()[0]
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(base, tree, copy_function=os.link)
    target = tree / path
    text = target.read_text()
    if text.count(old) != 1:
        return dict(mutant=name, applied=False, note=f'pattern found {text.count(old)} times')
    target.unlink()
    target.write_text(text.replace(old, new))
    rc, tail = run(tree, cmd)
    shutil.rmtree(tree)
    return dict(mutant=name, applied=True, command=cmd, rc=rc, caught=rc != 0, tail=tail)


def main(repo: str, work: str, out: str, *only: str) -> int:
    chosen = {n: s for n, s in MUTANTS.items() if not only or n.split()[0] in only}
    work_p, base = Path(work), Path(work) / 'base'
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    archive = subprocess.run(['git', '-C', repo, 'archive', 'HEAD'], check=True, capture_output=True).stdout
    subprocess.run(['tar', '-x', '-C', str(base)], input=archive, check=True)
    for sub in ('protocol-processor', 'gptp-processor', 'third_party/tsn-c-stack', 'third_party/lwSRP',
                'third_party/verilog-axis'):
        src = Path(repo) / sub
        if src.is_dir():
            shutil.rmtree(base / sub, ignore_errors=True)
            shutil.copytree(src, base / sub, ignore=shutil.ignore_patterns('.git'))
    head = subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'], check=True, capture_output=True, text=True).stdout
    result = dict(head=head.strip(), baseline={}, mutants=[])
    with concurrent.futures.ThreadPoolExecutor(max_workers=14) as pool:
        cmds = sorted({s[3] for s in chosen.values()})
        base_f = {c: pool.submit(run, base, c) for c in cmds}
        mut_f = [pool.submit(one, n, s, base, work_p) for n, s in chosen.items()]
        for c, f in base_f.items():
            rc, tail = f.result()
            result['baseline'][c] = dict(rc=rc, tail=tail[-300:])
        result['mutants'] = [f.result() for f in mut_f]
    Path(out).write_text(json.dumps(result, indent=1))
    ok = all(v['rc'] == 0 for v in result['baseline'].values())
    for m in result['mutants']:
        print(f"{'CAUGHT' if m.get('caught') else 'NOT-APPLIED' if not m['applied'] else 'SURVIVED'} {m['mutant']}"
              f" rc={m.get('rc')} {m.get('note', '')}")
    for c, v in result['baseline'].items():
        print(f'BASELINE {c} rc={v["rc"]}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
