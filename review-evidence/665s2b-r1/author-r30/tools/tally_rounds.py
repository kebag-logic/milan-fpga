"""Every round of THE RETRY in every leg's finished group logs (round_grade.rounds, the harness's own parse), tallied by
notices n and refused attempts k: the count, the dearest in CPU cycles, and the implied cold cost, the round less
n x AECP_NOTICE_US and k x AECP_ATTEMPT_US at its point (365/34 us at two interfaces, 255/34 at one), against
the trigger (183.1 us at two interfaces; the stated 85 us at one). A leg's group is taken from the first of its runs
(results, its helpers' and stealers') whose log is finished. usage: python3 -I tally_rounds.py HARNESS_DIR OUT_JSON LEG:POINT..."""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, sys.argv[1])
import grade  # noqa: E402
import round_grade  # noqa: E402

B = Path('/data-2/milan/tmp/665s2b-a683zo/builds')
W = {1: 255, 2: 365}
A = 34
LIMIT = {1: 85.0, 2: 183.1}


def finished(path: Path) -> bool:
    with open(path, 'rb') as f:
        f.seek(0, 2)
        f.seek(max(0, f.tell() - 5000))
        return b'SUMMARY' in f.read()


def logs(leg: str) -> list[Path]:
    chosen = {}
    for run in ('results', 'results-h1', 'results-h2', 'results-h3', 'results-h4', 'stolen-h5', 'stolen-h6',
                'stolen-h7'):
        for p in sorted((B / leg / run).glob('*.log')):
            if p.stem not in chosen and finished(p):
                chosen[p.stem] = p
    return [chosen[k] for k in sorted(chosen)]


def one(args):
    path, n_if = args
    log = grade.parse(path.read_text(errors='replace'), 100_000_000, 100_000_000)
    out = []
    for r in round_grade.rounds(log):
        n, k = r['notices'], r['refused']
        out.append((n, k, r['cycles'], r['cycles'] / 100 - n * W[n_if] - k * A))
    return path.parent.name + '/' + path.name, out


def main() -> int:
    out_json = Path(sys.argv[2])
    report, worst = {}, []
    for spec in sys.argv[3:]:
        leg, point = spec.split(':')
        n_if = 2 if point == '8x8' else 1
        files = logs(leg)
        tally = {}
        with ProcessPoolExecutor(8) as pool:
            for name, rounds in pool.map(one, [(p, n_if) for p in files]):
                for n, k, cycles, cold in rounds:
                    t = tally.setdefault(f'n={n} k={k}', dict(rounds=0, dearest=0, cold_us=-1e9, group=''))
                    t['rounds'] += 1
                    if cycles > t['dearest']:
                        t['dearest'] = cycles
                    if cold > t['cold_us']:
                        t['cold_us'], t['group'] = round(cold, 2), name
        report[leg] = dict(point=point, groups=len(files), limit_us=LIMIT[n_if], tally=tally)
        print(f'{leg} ({point}, {len(files)} groups, implied cold limit {LIMIT[n_if]} us)')
        for key in sorted(tally, key=lambda s: tuple(int(x.split('=')[1]) for x in s.split())):
            t = tally[key]
            flag = '  OVER' if t['cold_us'] > LIMIT[n_if] else ''
            print(f"  {key:10s} {t['rounds']:6d} rounds, dearest {t['dearest']:>7,} cycles, implied cold "
                  f"{t['cold_us']:7.2f} us ({t['group']}){flag}")
            if flag:
                worst.append(f'{leg} {key} {t["cold_us"]} us {t["group"]}')
    out_json.write_text(json.dumps(report, indent=1))
    print('TRIGGER 1: ' + ('OVER: ' + '; '.join(worst) if worst else 'no implied cold cost over its limit'))
    return 1 if worst else 0


if __name__ == '__main__':
    sys.exit(main())
