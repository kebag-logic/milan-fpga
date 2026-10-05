#!/usr/bin/env python3
"""Probe nonidentical corrupt reads and permanent read refusal.

Only the disposable flash model changes. Production store/codec/port bytes
are checked against the checkout before compiling. A probe exit of 1 means
at least one acknowledged saved value was lost at the next clean boot.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=2)
    args = ap.parse_args()
    assert 1 <= args.jobs <= 16
    packet = Path(__file__).resolve().parents[1]
    scratch = packet / 'scratch/read-agreement'
    receipts = packet / 'receipts/read-agreement'
    scratch.mkdir(parents=True, exist_ok=True)
    receipts.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(args.repo / 'sw/firmware/ctrl_nvm/test'))
    import nvm_bench as nb
    import nvm_checks as checks

    def shape(stem):
        work = scratch / stem
        if work.exists():
            shutil.rmtree(work)
        inp = nb.shape_inputs(args.repo / 'configs' / (stem + '.yaml'), work)
        tree = work / 'tree'
        shutil.copytree(nb.TREE, tree, ignore=shutil.ignore_patterns('__pycache__'))
        model = tree / 'host/nvm_fmodel.c'
        original = model.read_text()
        old = '\tif (addr <= fm.fault_at && fm.fault_at - addr < len && fm_take(NVM_F_READ_FLIP_AT))\n\t\tdst[fm.fault_at - addr] ^= 0x08u;'
        new = '''\tif (addr <= fm.fault_at && fm.fault_at - addr < len && fm_take(NVM_F_READ_FLIP_AT)) {
\t\tunsigned int mask = fm.fault_count ? 0x08u : 0x10u;
\t\tdst[fm.fault_at - addr] ^= (uint8_t)mask;
\t\tprintf("PROBE_READ addr=%u len=%u offset=%u xor=%u returned=%u\\n",
\t\t       addr, len, fm.fault_at - addr, mask, dst[fm.fault_at - addr]);
\t}'''
        assert original.count(old) == 1
        model.write_text(original.replace('#include <string.h>', '#include <string.h>\n#include <stdio.h>').replace(old, new))
        identities = {}
        for source in nb.SOURCES:
            if source == 'host/nvm_fmodel.c':
                continue
            assert (tree / source).read_bytes() == (nb.TREE / source).read_bytes()
            identities[source] = hashlib.sha256((tree / source).read_bytes()).hexdigest()
        (receipts / (stem + '.source-hashes.json')).write_text(json.dumps(identities, indent=2) + '\n')
        bench = nb.make_bench(inp, work / 'bench', tree)
        rows = []
        controls = []
        raw = []
        def run(label, *command):
            result = bench.run(*command)
            raw.append({'label': label, 'args': command, 'stdout': result.out})
            return result
        for slot in (0, 1):
            for seq in (1, 5, 0x80000000, 0xffffffff):
                for location, offset in [('header', 0), ('body', 0x100)]:
                    label = f'{stem}-slot-{slot}-seq-{seq}-{location}'
                    golden = bench.assemble(bench.frames, seq)
                    rid = max(bench.frames)
                    value = bytes([0xa5]) * (len(bench.frames[rid]) - 8)
                    address = nb.JOURNAL['offset'] + slot * nb.SLOT + offset
                    control = run(label + '-one-corruption-control', '--slot-a' if slot == 0 else '--slot-b',
                                  bench.file('golden.bin', golden), '--boot-fault',
                                  f'read-flip-at:1:0:{address}', '--boot', '--set', f'{rid}:{value.hex()}',
                                  '--until-idle', '--dump-slot-a', 'control-a.bin', '--dump-slot-b', 'control-b.bin')
                    control_boot = run(label + '-control-clean-reboot', '--slot-a', str(bench.work / 'control-a.bin'),
                                       '--slot-b', str(bench.work / 'control-b.bin'), '--boot', '--dump-state', 'control-state.txt')
                    control_expected = checks.rid_payloads(bench, golden)
                    control_expected[rid] = value
                    assert control.s['ok'] == 1 and control.s['unread'] == 0
                    assert control.s['seq'] == (seq + 1) & 0xffffffff
                    assert not checks.state_matches(bench, bench.work / 'control-state.txt', control_expected)
                    controls.append({'case': label, 'one_corruption_then_clean_read': 'PASS',
                                     'committed_seq': control.s['seq'], 'reboot_seq': control_boot.s['seq']})
                    before = run(label + '-fault-and-commit', '--slot-a' if slot == 0 else '--slot-b',
                                 bench.file('golden.bin', golden), '--boot-fault',
                                 f'read-flip-at:2:0:{address}', '--boot', '--set', f'{rid}:{value.hex()}',
                                 '--until-idle', '--dump-slot-a', 'post-a.bin', '--dump-slot-b', 'post-b.bin')
                    after = run(label + '-clean-reboot', '--slot-a', str(bench.work / 'post-a.bin'),
                                '--slot-b', str(bench.work / 'post-b.bin'), '--boot', '--dump-state', 'state.txt')
                    expected = checks.rid_payloads(bench, golden)
                    if before.s['ok']:
                        expected[rid] = value
                    state = nb.read_state(bench.work / 'state.txt')
                    wrong = [r for r, val in expected.items() if state[r] != (1, val)]
                    traces = [s for s in before.out.splitlines() if s.startswith('PROBE_READ')]
                    assert len(traces) == 2 and 'xor=8 ' in traces[0] and 'xor=16 ' in traces[1]
                    row = {'case': label, 'seq_before': seq, 'unread': before.s['unread'],
                           'faults_reported': before.s['read_faults'], 'commits_ok': before.s['ok'],
                           'committed_seq': before.s['seq'], 'seq_clean_reboot': after.s['seq'],
                           'changed_record_lost': state[rid] != (1, value),
                           'changed_record': rid, 'expected_value': value.hex(),
                           'observed_valid': state[rid][0], 'observed_value': state[rid][1].hex(),
                           'wrong_records_after_reboot': wrong, 'differing_reads': traces}
                    rows.append(row)
        # The permanent-failure arm uses the unmodified read-failure fault.
        # Heal the medium without reboot: HELD must remain, status/loop live.
        live = run(stem + '-permanent-read-failure', '--slot-a', bench.file('live.bin', bench.assemble(bench.frames, 5)),
                   '--boot-fault', 'read-fail:999999', '--boot', '--set-pattern', '77', '--run-ms', '5000',
                   '--commit-try', '--fault', 'none:0', '--run-ms', '5000', '--commit-try')
        s = live.s
        assert s['unread'] == 3 and s['read_faults'] == 6 and s['releases'] == 1
        assert s['phase'] == 10 and s['dirty'] == 1 and s['erases'] == 0 and s['programs'] == 0
        assert s['calls'] >= 100000 and s['commit_refused'] == 2
        (receipts / (stem + '.permanent.json')).write_text(json.dumps(s, indent=2) + '\n')
        (receipts / (stem + '.results.json')).write_text(json.dumps(rows, indent=2) + '\n')
        (receipts / (stem + '.controls.json')).write_text(json.dumps(controls, indent=2) + '\n')
        output = '\n'.join(json.dumps(r) for r in raw) + '\n'
        output = output.replace(str(packet), '<packet>').replace(str(args.repo), '<repo>')
        (receipts / (stem + '.runs.jsonl')).write_text(output)
        failures = sum(bool(r['wrong_records_after_reboot']) for r in rows)
        print(json.dumps({'shape': stem, 'read_disagreement_cases': len(rows), 'lost_saved_values': failures,
                          'one_corruption_controls_passed': len(controls),
                          'permanent_read_failure_liveness': 'PASS'}), flush=True)
        return failures

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        counts = list(pool.map(shape, ['endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8']))
    return int(any(counts))


if __name__ == '__main__':
    sys.exit(main())
