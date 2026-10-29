#!/usr/bin/env python3
"""Scratch: two harness runs' behaviour with the timing taken out, group by group.

usage: logcmp.py RESULTS_A RESULTS_B [GROUP ...]

Per group, from each log (sim_main.cpp's lines):
- WIRE: every egress frame, per mailbox channel and interface in order, as frame bytes (which interface of two goes
  first at boot is timing);
- the firmware's mailbox register writes (the W fields of the PASS lines): each register's own sequence of values
  (how writes to different registers interleave is timing), without the registers whose values carry the time:
  TMR_DEADLINE and TMR_CMD (milliseconds), MAAP_BASE_LO/HI (the clock-seeded address below) and EVT_TAIL (the event
  ring's acknowledgements, which count the TICK events a run of that length coalesces);
- MAAP's requested and conflict start addresses (MAAPDU octets 26-31 and 34-39) are masked in its frames and in the
  script's replies, which copy them: the stack seeds MAAP's generator with the clock at start (tsn-c-stack
  src/maap.c:191), so the address follows boot timing;
- REPLY/RXS: the frames the script offered and replied, as (interface, bytes) in order (the stimulus, which a reply
  to a firmware frame can follow);
- the grader's probe verdicts' count, and SUMMARY's bus_errors and traps.
Prints IDENTICAL or the first difference of each part, then the differing registers by channel and area (the
build's own mbx_contract.h: each channel's RX and TX ring and its register block)."""
import re
import sys
from pathlib import Path

GROUPS = ('backlog', 'backlog-adp', 'backlog-adp-refill', 'backlog-owed')


def mask(frame: str) -> str:
    """A MAAPDU (ethertype 22f0, subtype fe) with its requested and conflict start addresses masked (hex digits 52-63
    and 68-79); any other frame unchanged."""
    if frame[24:30] != '22f0fe' or len(frame) < 80:
        return frame
    return frame[:52] + 'x' * 12 + frame[64:68] + 'x' * 12 + frame[80:]


def parts(log: Path) -> dict:
    wire: dict[int, list] = {}
    writes, stimulus, summary = [], [], {}
    for line in log.read_text().splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == 'WIRE':
            wire.setdefault((int(f[3]), int(f[2])), []).append(mask(f[4]))
        elif f[0] == 'PASS' and ' W' in line:
            for w in line.split(' W', 1)[1].split():
                _, word, value = w.split(':')
                writes.append((int(word, 16), int(value, 16)))
        elif f[0] in ('RXS', 'REPLY'):
            stimulus.append((f[0], f[2], mask(f[-1])))
        elif f[0] == 'SUMMARY':
            summary = dict(kv.split('=', 1) for kv in f[1:] if kv.split('=', 1)[0] in ('bus_errors', 'traps'))
    return dict(wire=wire, writes=writes, stimulus=stimulus, summary=summary)


def areas(contract: Path):
    """word -> 'CHANNEL TX ring' / 'CHANNEL RX ring' / 'CHANNEL registers' / 'other', from the contract header."""
    text = contract.read_text()
    rings = [(m.group(1), m.group(2), int(m.group(3), 16)) for m in
             re.finditer(r'#define MBX_CH_(\w+)_(RX|TX)_BASE 0x([0-9A-Fa-f]+)u', text)]
    words = {(n, d): int(re.search(rf'#define MBX_CH_{n}_{d}_WORDS (\d+)u', text).group(1)) for n, d, _ in rings}
    names = re.search(r'#define MBX_CH_RX_BASE_TBL \{([^}]*)\}', text).group(1)
    order = [re.search(r'MBX_CH_(\w+)_RX_BASE', x).group(1) for x in names.split(',')]
    ch_base = int(re.search(r'#define MBX_CH_BASE 0x([0-9A-Fa-f]+)u', text).group(1), 16)
    stride = int(re.search(r'#define MBX_CH_STRIDE 0x([0-9A-Fa-f]+)u', text).group(1), 16)

    def area(word: int) -> str:
        b = word * 4
        for n, d, base in rings:
            if base <= b < base + 4 * words[(n, d)]:
                return f'{n} {d} ring'
        if ch_base <= b < ch_base + stride * len(order):
            return f'{order[(b - ch_base) // stride]} registers'
        return 'other'
    return area


def first_difference(a: list, b: list) -> str:
    for k, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return f'item {k}: {str(x)[:120]} != {str(y)[:120]}'
    return f'lengths {len(a)} != {len(b)}' if len(a) != len(b) else ''


def main() -> int:
    ra, rb = Path(sys.argv[1]), Path(sys.argv[2])
    groups = sys.argv[3:] or GROUPS
    differ = 0
    for g in groups:
        a, b = parts(ra / f'{g}.log'), parts(rb / f'{g}.log')
        # mbx_contract.h: MAAP_BASE_LO/HI 0x2C/0x30, TMR_DEADLINE 0x38, TMR_CMD 0x3C, EVT_TAIL 0x64.
        timed = {0x2C // 4, 0x30 // 4, 0x38 // 4, 0x3C // 4, 0x64 // 4}
        assert TMR_CMD_WORD == 0x3C // 4
        per = lambda ws: {w: [v for x, v in ws if x == w] for w in {x for x, _ in ws} - timed}
        pa, pb = per(a['writes']), per(b['writes'])
        wa = sorted((w, v) for w, vs in pa.items() for v in vs)
        wb = sorted((w, v) for w, vs in pb.items() for v in vs)
        diff = [w for w in sorted(set(pa) | set(pb)) if pa.get(w) != pb.get(w)]
        out = []
        for ch in sorted(set(a['wire']) | set(b['wire'])):
            d = first_difference(a['wire'].get(ch, []), b['wire'].get(ch, []))
            out.append(f'wire ch{ch[0]} if{ch[1]} ({len(a["wire"].get(ch, []))} frames): {d or "IDENTICAL"}')
        d = ', '.join(f'word 0x{w:x}: {first_difference(pa.get(w, []), pb.get(w, []))}' for w in diff[:4])
        out.append(f'register writes ({len(wa)} to {len(pa)} registers, per register): {d or "IDENTICAL"}')
        d = first_difference(a['stimulus'], b['stimulus'])
        out.append(f'stimulus ({len(a["stimulus"])}): {d or "IDENTICAL"}')
        out.append(f'bus errors/traps: {a["summary"]} vs {b["summary"]}')
        if diff:
            out.append('differing registers by area: ' + ', '.join(f'{k} {v}' for k, v in sorted(
                __import__('collections').Counter(AREA(w) for w in diff).items())))
        differ += sum('IDENTICAL' not in o for o in out if not o.startswith(('bus errors', 'differing'))) + \
            (a['summary'] != b['summary'])
        print(f'## {g}')
        for o in out:
            print('-', o)
    print(f'{differ} part(s) differ')
    return 1 if differ else 0


TMR_CMD_WORD = None
AREA = None
if __name__ == '__main__':
    # budget_config.hpp's tmr_cmd_word for this build, beside the results directory.
    cfg = (Path(sys.argv[1]).parent / 'budget_config.hpp').read_text()
    TMR_CMD_WORD = int(re.search(r'tmr_cmd_word = 0x([0-9a-f]+)u', cfg).group(1), 16)
    # A two-interface build carries its own contract; a one-interface build uses the tree's.
    variant = Path(sys.argv[1]).parent / 'image/variant/mbx/mbx_contract.h'
    AREA = areas(variant if variant.is_file() else
                 Path('$LANES/665-s2b-cycles/sw/firmware/ctrl/mbx/mbx_contract.h'))
    raise SystemExit(main())
