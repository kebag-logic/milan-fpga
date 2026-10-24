"""Recompute every figure the round 2 docs state for #773 and require each to appear in the page that states it.

usage: python3 -I round2_bounds.py <repo> [<capture_coherence dp log> ...]
The method is the one R690-1's check_bounds.py uses (rational periods, the RTL's own term formulas), extended to the
grid-live and start-up bounds, the render-queue margins, the supported range and the MAC-level figures. Given dp logs,
it also requires every [HOLD] maximum they print at 2 ms to be at or below the stated start-up bound.
"""
from fractions import Fraction as F
from math import ceil, floor
from pathlib import Path
import re, sys

repo = Path(sys.argv[1])
logs = [Path(p) for p in sys.argv[2:]]
ps = F(10**9, 48000)
cyc = 20                                   # ns, the 50 MHz datapath clock at both shipping shapes
lead = ceil(8 * ps)                        # 166,667 ns
five = ceil(5 * ps)                        # 104,167 ns, a PDU's last event after its first
ofs = 2_000_000
rnd = lambda x: (x.numerator * 2 + x.denominator) // (2 * x.denominator)
out, facts = [], {}


def say(key, value, text):
    facts[key] = value
    out.append(f'{key} = {value:,}  ({text})')


shapes = {'1x1': dict(slots=8, loop=4, audio=24_576_000, queue=2_656_119, k=2),
          '8x8': dict(slots=32, loop=1, audio=98_304_000, queue=2_650_942, k=1)}
for name, s in shapes.items():
    marker = rnd(F(256 * 10**9, s['slots'] * 32 * 48000)) + rnd(F(10**9, s['audio'])) + 90
    # grid live, earliest hand-over after the frame's instant: five periods, the marker, age 0, the walk to talker 0's
    # last pair (4 + LOOP + 26 x 3) and the packetizer (57 cycles for talker 0)
    walk0 = 4 + s['loop'] + 26 * 3
    early = 5 * ps + marker + (walk0 + 57) * cyc
    say(f'{name} grid-live earliest hand-over', round(early), f'5 Ps + marker {marker} + ({walk0} + 57) cycles')
    say(f'{name} grid-live lead', floor(ofs + lead - early), 'offset + 8 Ps - earliest hand-over')
    say(f'{name} grid-live last event', floor(ofs + lead - early) + five, '+ 5 Ps')
    say(f'{name} grid-live margin', s['queue'] - facts[f'{name} grid-live last event'], 'queue - last event')
    say(f'{name} pre-773 grid-live last event', floor(ofs - early) + five, 'stamp M + offset, + 5 Ps')
    # supported range for this talker (lead = offset + 8 Ps - transit)
    low = s['k'] * ps - marker + ps / 2
    say(f'{name} range floor', round(low), 'K x Ps - event latency + Ps / 2')
    say(f'{name} transit bound', ofs + lead - round(low), 'offset + 8 Ps - floor')
    say(f'{name} offset bound', s['queue'] - lead, 'queue - 8 Ps (first event)')
    say(f'{name} whole-PDU offset bound', s['queue'] - lead - five, 'queue - 8 Ps - 5 Ps')

# start-up: base = live PHC at the PDU's first pair; five tick spacings (>= 5,208 cycles), the walk on to the last
# pair (26 x 3 cycles), the packetizer (57 for talker 0)
ticks = floor(5 * F(50_000_000, 48000))
startup = (ticks + 26 * 3 + 57) * cyc
say('start-up earliest hand-over', startup, f'({ticks} + 78 + 57) cycles')
say('start-up lead', ofs + lead - startup, 'offset + 8 Ps - hand-over')
say('start-up lead at 125 us', 125_000 + lead - startup, '')
say('start-up last event', ofs + lead - startup + five, '+ 5 Ps')
for name, s in shapes.items():
    say(f'{name} start-up margin', s['queue'] - facts['start-up last event'], 'queue - last event')
say('Eq. (1) lead ceiling', startup + 125_000, 'earliest hand-over + TUmax')

# MAC level, 1 Gb/s: 8 ns an octet; a maximum tagged frame 1,522 octets with FCS + preamble 8 + gap 12
octet = 8
maxf, crf_f, aaf_f = (1522 + 20) * octet, (60 + 4 + 20) * octet, (234 + 4 + 20) * octet
say('max frame on the wire', maxf, '1,542 octets')
spare = {'AAF 1x1': 17_816, 'AAF 8x8': 18_912, 'CRF 1x1': 20_503, 'CRF 8x8': 15_326}
for k, v in spare.items():
    say(f'{k} after one frame ahead', v - maxf, 'spare - 12,336')
# the same frame through the arbiters first: its 190 beats, then its wire time, then the other output's PDU; the
# PDU's own uncontended egress is its last beat (nb - 1 cycles after its first)
aaf_w = 189 * cyc + maxf + crf_f - 29 * cyc
crf_w = 189 * cyc + maxf + aaf_f - 7 * cyc
say('AAF egress past uncontended', aaf_w, 'F 190 beats, F wire, CRF PDU wire, less the AAF 30 beats')
say('CRF egress past uncontended', crf_w, 'F 190 beats, F wire, AAF PDU wire, less the CRF 8 beats')
for k, v in spare.items():
    say(f'{k} after the arbitrated frame', v - (aaf_w if k.startswith('AAF') else crf_w), 'spare - egress delay')
say('max frame at 100 Mb/s', maxf * 10, '')

mcf = (repo / 'docs/design/MEDIA_CLOCK_FOLLOWING.md').read_text()
mat = (repo / 'docs/reference/MILAN_COMPLIANCE_MATRIX.md').read_text()
need = {
    mcf: ['2,038,676', '2,054,392', '2,059,807', '184,807', '106,860', '5,343', '5,208', '2,163,974', '492.1 us',
          '487.0 us', '2,142,843', '2,158,559', '513.3', '492.4', '1,976,176', '1,991,892', '231.8 us',
          '2,135,548', '2,140,725', '2,489,452', '2,484,275', '2,385,285', '2,380,108', '12,336', '5,480', '6,576',
          '8,167', '2,990', '16,208', '18,040', '1,608', '2,704', '2,463', '2,714', '123,360', '127,991', '112,275'],
    mat: ['2,054,392', '2,038,676', '2,059,807'],
}
derived = {
    '2,038,676': facts['1x1 grid-live lead'], '2,054,392': facts['8x8 grid-live lead'],
    '2,059,807': facts['start-up lead'], '184,807': facts['start-up lead at 125 us'],
    '106,860': facts['start-up earliest hand-over'], '5,343': facts['start-up earliest hand-over'] // cyc,
    '5,208': ticks, '2,163,974': facts['start-up last event'],
    '492.1 us': round(facts['1x1 start-up margin'] / 100) / 10, '487.0 us': round(facts['8x8 start-up margin'] / 100) / 10,
    '2,142,843': facts['1x1 grid-live last event'], '2,158,559': facts['8x8 grid-live last event'],
    '513.3': round(facts['1x1 grid-live margin'] / 100) / 10, '492.4': round(facts['8x8 grid-live margin'] / 100) / 10,
    '1,976,176': facts['1x1 pre-773 grid-live last event'], '1,991,892': facts['8x8 pre-773 grid-live last event'],
    '231.8 us': floor(facts['Eq. (1) lead ceiling'] / 100) / 10,
    '2,135,548': facts['1x1 transit bound'], '2,140,725': facts['8x8 transit bound'],
    '2,489,452': facts['1x1 offset bound'], '2,484,275': facts['8x8 offset bound'],
    '2,385,285': facts['1x1 whole-PDU offset bound'], '2,380,108': facts['8x8 whole-PDU offset bound'],
    '12,336': maxf, '5,480': facts['AAF 1x1 after one frame ahead'], '6,576': facts['AAF 8x8 after one frame ahead'],
    '8,167': facts['CRF 1x1 after one frame ahead'], '2,990': facts['CRF 8x8 after one frame ahead'],
    '16,208': aaf_w, '18,040': crf_w, '1,608': facts['AAF 1x1 after the arbitrated frame'],
    '2,704': facts['AAF 8x8 after the arbitrated frame'], '2,463': facts['CRF 1x1 after the arbitrated frame'],
    '2,714': -facts['CRF 8x8 after the arbitrated frame'], '123,360': facts['max frame at 100 Mb/s'],
    '127,991': facts['1x1 grid-live earliest hand-over'], '112,275': facts['8x8 grid-live earliest hand-over'],
}
fail = 0
print('\n'.join(out))
print()
for text, items in need.items():
    page = 'MEDIA_CLOCK_FOLLOWING.md' if text is mcf else 'MILAN_COMPLIANCE_MATRIX.md'
    for item in items:
        num = float(item.split()[0].replace(',', ''))
        ok = item in text and abs(num - derived[item]) < 1e-9
        fail += not ok
        print(f'{"PASS" if ok else "FAIL"} {page}: "{item}" stated, derived {derived[item]:,}')
for log in logs:
    holds = [int(x.replace(',', '')) for x in re.findall(r'\[HOLD\][^\n]*?max(?:imum)?[^\n0-9]*([0-9,]+) ns', log.read_text())]
    big = [h for h in holds if h > 1_000_000]
    ok = bool(big) and max(big) <= facts['start-up lead']
    fail += not ok
    print(f'{"PASS" if ok else "FAIL"} {log.name}: {len(big)} 2 ms [HOLD] maxima, largest {max(big) if big else None:,} '
          f'<= stated start-up bound {facts["start-up lead"]:,}')
print(f'\n{"PASS" if not fail else "FAIL"}: {fail} failure(s)')
sys.exit(1 if fail else 0)
