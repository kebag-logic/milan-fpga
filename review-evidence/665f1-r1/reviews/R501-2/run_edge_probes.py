#!/usr/bin/env python3
"""Focused fault probes against unchanged source. Exit zero means probes ran."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys


def probe(repo, packet, stem):
    import nvm_bench as nb
    import nvm_checks as nc
    work = packet / 'scratch' / ('edge-' + stem)
    work.mkdir(parents=True, exist_ok=True)
    inputs = nb.shape_inputs(repo / 'configs' / (stem + '.yaml'), work)
    b = nb.make_bench(inputs, work / 'store')
    log = []

    def run(name, *args):
        r = b.run(*args)
        log.extend([name, 'ARGS ' + json.dumps(args).replace(str(packet), '<packet>'), r.out])
        return r

    old = b.file('old.bin', b.assemble(b.frames, 5))
    rid = max(b.frames)
    new = bytes([0xA6]) * (len(b.frames[rid]) - 8)
    first = run('transient_refusal_then_verified_commit', '--slot-a', old,
                '--boot-fault', 'read-fail:1', '--boot', '--set', f'{rid}:{new.hex()}',
                '--until-idle', '--dump-slot-a', 'after-a.bin', '--dump-slot-b', 'after-b.bin')
    second = run('clean_reboot_after_verified_commit', '--slot-a', str(b.work / 'after-a.bin'),
                 '--slot-b', str(b.work / 'after-b.bin'), '--boot', '--dump-state', 'state.txt')
    restored = nb.read_state(b.work / 'state.txt')[rid][1]
    assert first.s['ok'] == 1 and first.s['seq'] == 1 and first.s['auth'] == 1
    assert second.s['seq'] == 5 and second.s['auth'] == 0 and restored != new
    log.append('REPRODUCED verified_generation_1_loses_to_previously_refused_generation_5')

    for count in (2, 261):
        r = run(f'progressing_controller_{count}_delayed_TX_waits', '--litespi', '--slot-b', old,
                '--boot', '--set', f'{rid}:{new.hex()}', '--until-phase', '7',
                '--ls-stall', f'tx:{count}:0:4000', '--until-idle')
        log.append('OBSERVED ' + json.dumps({'slow_waits': count, 'max_call_us': r.s['max_call_us'],
                                            'ok': r.s['ok'], 'failed': r.s['failed'],
                                            'stalled': r.s['ls_stalled'], 'hung': r.s['ls_hung']}))
        assert r.s['ok'] == 1 and r.s['failed'] == 0 and r.s['ls_hung'] == 0

    r = run('fresh_change_during_retry_backoff', '--slot-b', old, '--boot',
            '--fault', 'program-drop:1', '--set', f'{rid}:{new.hex()}', '--run-ms', '2000',
            '--mark', '--set', '0:1234', '--until-idle')
    log.append('OBSERVED new_change_to_retry_erase_us=' + str(r.erases[1] - r.marks[0]))
    dest = packet / 'receipts' / ('edge-' + stem + '.log')
    dest.write_text('\n'.join(log) + '\n')
    dest.with_suffix('.rc').write_text('0\n')
    return dest.name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, default=Path.cwd())
    ap.add_argument('--packet', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--jobs', type=int, default=2)
    args = ap.parse_args()
    repo, packet = args.repo.resolve(), args.packet.resolve()
    sys.path.insert(0, str(repo / 'sw/firmware/ctrl_nvm/test'))
    assert 1 <= args.jobs <= 16
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(probe, repo, packet, stem) for stem in
                   ('endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8')]
        for future in futures:
            print(future.result())


if __name__ == '__main__':
    main()
