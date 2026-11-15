#!/usr/bin/env python3
"""Run the two Talker shapes and the three new hold-off controls.

Usage: python3 -B probe_talker.py SOURCE PACKET
Builds stay in PACKET/scratch; two foreground child processes use eight
compiler jobs each. Published logs replace local source/build paths.
"""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys


def worker(source, packet, interfaces):
    sys.path[:0] = [str(source / 'sw/firmware/ctrl/test'), str(source / 'sw/firmware/gtest')]
    import ctrl_arms
    import fw_gtest
    import srp_arms
    import srp_mutants
    from ctrl_build import CTRL, Tree
    out = packet / 'scratch' / f'talker-if{interfaces}'
    out.mkdir(parents=True, exist_ok=True)
    config = source / 'configs' / ('endstation_ax7101_8x8.yaml' if interfaces == 2
                                  else 'endstation_ax7101_1x1_tdm8.yaml')
    tree = Tree(CTRL, out / 'baseline', out / 'reuse', fw_gtest.Build(jobs=8))
    result = srp_arms.arm_srp(tree, source / 'third_party/lwSRP', interfaces,
                            test='srp_talker.cpp', config=config)
    (packet / f'talker-if{interfaces}-baseline.log').write_text(
        result.log.replace(str(source), '<source>').replace(str(packet), '<packet>'))
    failed = ctrl_arms.report([result])
    names = {'talker-hold-off-drops-the-transmit-term',
             'talker-hold-off-rounds-the-transmit-term-down',
             'talker-hold-off-drops-the-join-and-transmit-terms'}
    srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in names)
    assert len(srp_mutants.DEFECTS) == 3
    failed |= srp_mutants.campaign(out / 'plants', source / 'third_party/lwSRP', 8, interfaces)
    print(f'point if{interfaces}: baseline plus three controls: {"FAIL" if failed else "PASS"}')
    return int(bool(failed))


def main():
    source, packet = map(lambda x: Path(x).resolve(), sys.argv[1:3])
    if len(sys.argv) == 4:
        return worker(source, packet, int(sys.argv[3]))
    def run(n):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        p = subprocess.run([sys.executable, '-B', __file__, str(source), str(packet), str(n)],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
        text = p.stdout.replace(str(source), '<source>').replace(str(packet), '<packet>')
        (packet / f'talker-if{n}.log').write_text(text)
        (packet / f'talker-if{n}.rc').write_text(str(p.returncode) + '\n')
        print(f'if{n}: rc {p.returncode}', flush=True)
        for path in (packet / 'scratch' / f'talker-if{n}' / 'plants').glob('*.log'):
            (packet / f'if{n}-{path.name}').write_text(path.read_text().replace(str(source), '<source>').replace(str(packet), '<packet>'))
        return p.returncode
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        return int(any(list(pool.map(run, (1, 2)))))


if __name__ == '__main__':
    raise SystemExit(main())
