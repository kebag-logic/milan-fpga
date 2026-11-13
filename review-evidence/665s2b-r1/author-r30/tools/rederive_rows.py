"""An independent re-derivation of the rows by every source (#665: R4, R5, R6 at 1x1/1if and 8x8/2if), written apart
from rows_grade.py: every count from the rules as the tree states them, the header constants from a compiled C probe
of the firmware's own headers (not rows_grade's parser), the contract's rates read from mailbox.yaml, and the stated
costs taken as given (load_grade.stated at the pin, poll_grade.stated_us, rows_grade.ROW_COSTS for a LINK event).

The rules, each from the tree:
  THE DRAIN (ctrl_loop.c): SRP first, a pass taking more than CTRL_LOOP_RX_PER_PASS SRP records takes no other
    channel's while under CTRL_LOOP_DRAIN_US; so every SRP record that arrives before R4's record is taken is ahead.
  SRP's window in R4: W less R4's own record (an SRP record arriving while that record runs is not ahead of it).
  The retained retry (srp_mbx.c: retry_spent spent by the poll, given back by the centisecond's consumer): at most one
    before the window's first centisecond and one after each centisecond the window holds, and one a pass; R4 only
    (SRP's rows are solved with no SRP record refused for storage: a refusal holds SRP's channel, SRP_RX_RETRY_MS).
  Everything else as the method states it (rows_grade's docstring): records at burst + floor(W / refill), the TICKs,
    the timer slots bounded by their protocol timers and one a pass, the grandmaster event's 802.1AS-2011 intervals,
    the passes' base, the poll items by their sources, THE RETRY's rounds, THE TRANSMIT's builds and THE STEP.
usage: python3 -I rederive_rows.py CHECKOUT OUT_DIR [RETRY_EXTRA [WINDOW]]
  RETRY_EXTRA  retries a window holds past floor(W / tick_ms): 2 (the rule above, default) or 1 (no retry before the
               window's first centisecond, both reviewers' count)
  WINDOW       SRP's window in R4: less-own (default) or whole (W itself)
"""
import json
import math
import subprocess
import sys
from pathlib import Path

co, out = Path(sys.argv[1]), Path(sys.argv[2])
EXTRA = int(sys.argv[3]) if len(sys.argv) > 3 else 2
WINDOW = sys.argv[4] if len(sys.argv) > 4 else 'less-own'
out.mkdir(parents=True, exist_ok=True)
H = co / 'tb/verilator/ctrl_service_budget'
sys.path[:0] = [str(H)]
import load_grade  # noqa: E402  (the stated costs and the contract parser only)
import poll_grade  # noqa: E402
import rows_grade  # noqa: E402  (ROW_COSTS, the LINK event's stated cost, only)

NAMES = ('CTRL_LOOP_DRAIN_US', 'CTRL_LOOP_RX_PER_PASS', 'CTRL_LOOP_STEP_AGE', 'CTRL_LOOP_STEP_PASS_US',
         'CTRL_LOOP_BUILD_PASS_US', 'CTRL_LOOP_BUILD_ONE_PASS_US', 'CTRL_LOOP_SHARE_US', 'CTRL_LOOP_SHARE_MARGIN_US',
         'CTRL_LOOP_TICK_US', 'AECP_NOTICE_US', 'AECP_ROUND_COLD_US', 'AECP_ROUND_PACE_MS', 'AECP_ROUND_YIELD_PACE_MS',
         'AECP_ROUND_YIELD_NOTICES', 'AECP_ROUND_YIELDS', 'AECP_ROUND_FIRM_NOTICES', 'AECP_NOTICES_MOST')


def constants(n_if: int) -> dict:
    """The constants as the firmware's compiler sees them, at that many interfaces."""
    work = out / f'probe-if{n_if}'
    work.mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(co / 'sw/mailbox/gen_mailbox.py'), '--variant-interfaces', str(n_if),
                    '--out', str(work)], check=True, capture_output=True)
    src = work / 'probe.c'
    src.write_text('#include <stdio.h>\n#include "ctrl_loop.h"\n#include "aecp.h"\n#include "aecp_mbx.h"\n'
                   'int main(void){\n' + ''.join(f'printf("{n} %lu\\n",(unsigned long)({n}));\n' for n in NAMES)
                   + 'return 0;}\n')
    inc = [f'-I{co / d}' for d in ('sw/firmware/ctrl/mbx', 'sw/firmware/ctrl/loop', 'sw/firmware/ctrl/aecp',
                                   'sw/firmware/ctrl/port', 'sw/firmware/ctrl/app', 'third_party/tsn-c-stack/include')]
    subprocess.run(['gcc', '-std=c11', *inc, '-include', str(work / 'mbx_contract.h'), str(src), '-o',
                    str(work / 'probe')], check=True)
    got = subprocess.run([str(work / 'probe')], check=True, capture_output=True, text=True).stdout.split()
    return {got[i]: int(got[i + 1]) for i in range(0, len(got), 2)}


def solve(row: str, point: str) -> tuple:
    s = load_grade.POINTS[point]
    n_if, sinks, regs, ctrs = s['n_if'], s['sinks_per_if'], s['registrations'], s['counter_descriptors']
    k = constants(n_if)
    c = load_grade.stated(co, point, load_grade.STATED_US)
    polls = poll_grade.stated_us(n_if)
    for name in ('withdraw', 'rebuild', 'aecp'):
        c[f'item.{name}'] = polls[name]
    c['item.retained'] = max(c['item.retained'], c['record.srp'])
    c.update(rows_grade.ROW_COSTS[point])
    y = load_grade.parsed((co / 'sw/mailbox/mailbox.yaml').read_text())
    rate = {ch['name']: (ch['rate']['burst'], ch['rate']['refill_ms']) for ch in y['channels']}
    tick_ms, cap = y['tick_ms'], k['CTRL_LOOP_RX_PER_PASS']

    def arrive(ch, w):
        return rate[ch][0] + math.floor(w / rate[ch][1])

    def work(w):
        t = {}
        ticks = math.floor(w / tick_ms) + 1
        t['ticks'] = ticks * (c['event.TICK'] + max(c['centisecond'], k['CTRL_LOOP_TICK_US']))
        if row == 'R4':
            t['aecp'] = rate['aecp'][0] * c['record.aecp']
            t['srp'] = (rate['srp'][0] + math.floor(max(0.0, w - (c['record.aecp'] / 1000 if WINDOW == 'less-own' else 0)) / rate['srp'][1])) \
                * c['record.srp']
            fixed = math.ceil(rate['aecp'][0] / cap) + ticks + 1
        else:
            t['srp'] = rate['srp'][0] * c['record.srp']
            fixed = 1 + ((n_if + 1) if row == 'R5' else 0)
        both, one = n_if * k['CTRL_LOOP_BUILD_PASS_US'], 2 * n_if * k['CTRL_LOOP_BUILD_ONE_PASS_US']
        t['builds'], n_builds = (both, n_if) if both >= one else (one, 2 * n_if)
        passes = 1
        for _ in range(100):
            timers = n_if * (min(passes, 2 + math.floor(w / rate['adp'][1]) + sinks) * c['event.ADP'] +
                             min(passes, sinks) * c['event.ACMP'] + min(passes, 1) * c['event.MAAP']) + \
                min(passes, regs * n_if + ctrs + 2) * c['event.AECP']
            n = fixed + math.ceil((t['srp'] + t['ticks'] + timers) / k['CTRL_LOOP_DRAIN_US'])
            if n == passes:
                break
            passes = n
        t['timers'] = timers
        if row == 'R4':
            t['others'] = sum(min(arrive(o, w), passes * cap) * c[f'record.{o}'] for o in ('acmp', 'adp', 'maap'))
        else:
            light = math.floor((t['ticks'] + timers) / max(1, k['CTRL_LOOP_DRAIN_US'] - cap * c['record.srp'])) + \
                ((n_if + 1) if row == 'R5' else 0)
            t['others'] = sum(min(arrive(o, w), light * cap) * c[f'record.{o}'] for o in ('aecp', 'acmp', 'adp', 'maap'))
        t['gm'] = n_if * min(passes, sum(math.floor(w / ms) + 1 for ms in load_grade.GM_INTERVALS_MS)) * c['event.GM']
        t['steps'] = (math.floor(w / (10 * (k['CTRL_LOOP_STEP_AGE'] + 1))) + 1) * k['CTRL_LOOP_STEP_PASS_US']
        t['item.walk'] = min(passes * n_if, n_if * (ticks + n_builds)) * c['item.walk']
        t['item.reclaim'] = min(2 * n_if * passes, 2 * (arrive('srp', w) + n_builds)) * c['item.reclaim']
        if row == 'R4':
            t['item.retained'] = min(passes, math.floor(w / tick_ms) + EXTRA) * c['item.retained']
        t['item.mrpdu'] = min(passes, 2 * n_builds) * c['item.mrpdu']
        t['item.acmp'] = min(passes, arrive('acmp', w) + arrive('adp', w) + n_if * sinks) * c['item.acmp']
        t['item.aecp'] = min(passes, arrive('aecp', w) + n_if * regs) * c['item.aecp']
        if row == 'R5':
            t['item.withdraw'], t['item.rebuild'] = n_if * c['item.withdraw'], n_if * c['item.rebuild']
            t['links'] = n_if * c['event.LINK']
        t['passes'] = passes * (c['events_none'] + c['base'])
        # THE RETRY's rounds (aecp_mbx.h): the yielding rounds first, then firm ones, a pace apart, at most the queue
        room = k['CTRL_LOOP_SHARE_US'] - k['CTRL_LOOP_SHARE_MARGIN_US'] - k['AECP_ROUND_COLD_US']
        per = max(1, min(k['AECP_ROUND_FIRM_NOTICES'], room // k['AECP_NOTICE_US']))
        left, at, us = k['AECP_NOTICES_MOST'], 0.0, 0
        for i in range(10_000):
            if at > w or left <= 0:
                break
            yielding = i < k['AECP_ROUND_YIELDS']
            built = min(left, k['AECP_ROUND_YIELD_NOTICES'] if yielding else per)
            us += k['AECP_ROUND_COLD_US'] + built * k['AECP_NOTICE_US']
            left -= built
            at += k['AECP_ROUND_YIELD_PACE_MS'] if yielding else k['AECP_ROUND_PACE_MS']
        t['rounds'] = us
        return t, passes

    w = 0.01
    while w < 2000:
        t, passes = work(w)
        total = sum(t.values()) / 1000
        if total <= w + 1e-9:
            return round(w, 2), passes, {n: v / 1000 for n, v in t.items()}
        w = round(max(w + 0.01, math.ceil(total * 100 - 1e-6) / 100), 2)
    return None, None, {}


result = {}
for point in ('1x1/1if', '8x8/2if'):
    for row in ('R4', 'R5', 'R6'):
        w, passes, terms = solve(row, point)
        result[f'{point} {row}'] = dict(w_ms=w, passes=passes, terms=dict(sorted(terms.items(), key=lambda t: -t[1])))
        top = ', '.join(f'{n} {v:.2f}' for n, v in list(result[f'{point} {row}']['terms'].items())[:4])
        print(f'{point} {row}: {w} ms, {passes} passes; {top}')
(out / 'rederive.json').write_text(json.dumps(result, indent=1))
