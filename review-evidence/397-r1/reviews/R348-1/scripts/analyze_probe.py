#!/usr/bin/env python3
"""Independent analysis of a reviewer probe run (stdout log + PROBE_LOG side file).

usage: analyze_probe.py <run.log> <run.probe> [aem_bytes]
Observers used here are independent of the harness grader:
  U/I  UART byte handshakes (text lines located by content, not EVENT markers)
  F    every flash command with its address (AEM reads, journal reads, erase, program)
  A    KL_nvm_backend alive_r / backed_r / stale_r (inside the fabric, after CDC)
  W    milan_csr writes with the unmasked address
Times are printed in ms of the 100 MHz system counter (cycles / 100000).
"""
import sys, json
log, probe = sys.argv[1], sys.argv[2]
aem = int(sys.argv[3]) if len(sys.argv) > 3 else None
U, I, F, A, W = [], [], [], [], []
for line in open(probe):
    p = line.split()
    if not p or p[0] not in 'UIFAW' or len(p) != {'U': 3, 'I': 3, 'F': 4, 'A': 6, 'W': 4}[p[0]]:
        continue  # a partial trailing line of a run still in progress
    k = p[0]; v = [int(x) for x in p[1:]]
    {'U': U, 'I': I, 'F': F, 'A': A, 'W': W}[k].append(v)
ms = lambda c: c / 100_000
out = {}
# UART text lines with start/end cycles
lines, cur, start = [], [], None
for c, b in U:
    if start is None and b != 13: start = c  # LiteX emits CR after LF; a line starts at its first non-CR byte
    cur.append(chr(b))
    if b == 10:
        lines.append((start if start is not None else c, c, ''.join(cur).rstrip('\n'))); cur, start = [], None
if cur and start is not None: lines.append((start, U[-1][0], ''.join(cur)))
def first_line(sub, after=0):
    return next((l for l in lines if sub in l[2] and l[0] >= after), None)
# boot -> entity enable, bracketed by UART text and by the enable write
en_line = first_line('fabric entity enabled')
aem_line = first_line('Milan baremetal: AEM')
en_w = [w for w in W if (w[1] & 0xffff) == 0x920 and w[2] & 1]
out['csr_write_addresses_seen'] = sorted({hex(w[1]) for w in W})
if en_line:
    out['boot'] = dict(enable_write_ms=ms(en_w[0][0]) if en_w else None,
                       prev_uart_line_end_ms=ms(aem_line[1]) if aem_line else None,
                       enable_uart_line_start_ms=ms(en_line[0]),
                       bracket_ok=bool(en_w and aem_line and aem_line[1] <= en_w[0][0] <= en_line[0]))
    if aem is not None:
        reads = [f for f in F if f[1] in (0x0b, 0x03) and 0x400000 <= f[2] < 0x400000 + aem]
        if reads:
            out['aem_copy_crc'] = dict(first_aem_flash_read_ms=ms(reads[0][0]), last_aem_flash_read_ms=ms(reads[-1][0]),
                                       aem_reads=len(reads),
                                       first_read_to_enable_ms=ms(en_w[0][0] - reads[0][0]) if en_w else None)
# console commands: input start (I) and prompt end (U) located independently
prompt = 'litex\x1b[0m> '
text = ''.join(chr(b) for _, b in U)
# prompt end cycles: index of each prompt occurrence end in U stream
ends, pos = [], 0
while True:
    j = text.find(prompt, pos)
    if j < 0: break
    ends.append(U[j + len(prompt) - 1][0]); pos = j + len(prompt)
# group input bytes into commands (newline-terminated)
cmds, buf, s0 = [], '', None
for c, b in I:
    if s0 is None: s0 = c
    buf += chr(b)
    if b == 10:
        cmds.append((s0, buf.strip())); buf, s0 = '', None
rows = []
for k, (s, name) in enumerate(cmds):
    e = next((x for x in ends if x > s), None)
    if e is None: break
    jr = [f for f in F if s <= f[0] <= e and f[1] in (0x0b, 0x03) and 0xee0000 <= f[2] < 0xf00000]
    rows.append(dict(index=k, command=name, ms=ms(e - s),
                     journal_reads=len(jr), journal_read_span_ms=ms(jr[-1][0] - jr[0][0]) if jr else 0.0,
                     erases=sum(1 for f in F if s <= f[0] <= e and f[1] == 0xd8),
                     programs=sum(1 for f in F if s <= f[0] <= e and f[1] == 0x02)))
out['commands'] = rows
# heartbeats seen by the fabric: alive_r reloads (A lines where alive rose)
kicks = [a for a in A if a[1] > a[4]]
hb_w = [w[0] for w in W if (w[1] & 0xffff) == 0x93c and w[2] == 1]
out['fabric_kicks'] = len(kicks); out['csr_heartbeat_writes'] = len(hb_w)
gaps = [(ms(b[0] - a[0]), ms(a[0]), ms(b[0]), b[4]) for a, b in zip(kicks, kicks[1:])]
end_c = max([e for e in ends] + [U[-1][0]]) if U else None
if kicks and end_c:
    gaps.append((ms(end_c - kicks[-1][0]), ms(kicks[-1][0]), ms(end_c), None))
gaps.sort(reverse=True)
out['max_fabric_kick_gaps_ms'] = gaps[:4]
out['min_alive_remaining_ms_at_kick'] = min((k[4] for k in kicks[1:]), default=None)
lapse = [a for a in A if a[2] == 0 and any(b[2] == 1 for b in A if b[0] < a[0])]
out['backed_lapses'] = [dict(cycle_ms=ms(a[0]), alive=a[1], stale=a[3],
                             since_last_kick_ms=ms(a[0] - max(k[0] for k in kicks if k[0] <= a[0]))) for a in lapse[:4]]
# commit brackets and heartbeat cadence during erase WIP
st = [w[0] for w in W if (w[1] & 0xffff) == 0x93c and w[2] == 4]
ack = [w[0] for w in W if (w[1] & 0xffff) == 0x93c and w[2] & 2 and not w[2] & 1]
out['commit_brackets_ms'] = [ms(b - a) for a, b in zip(st, ack)]
er = [f for f in F if f[1] == 0xd8]
for f in er:
    inside = [c for c in hb_w if f[0] <= c]
    nxt = next((g for g in F if g[0] > f[0] and g[1] == 0x02), None)
    win = [c for c in hb_w if f[0] <= c <= (nxt[0] if nxt else 10**18)]
    out.setdefault('erase_windows', []).append(dict(erase_ms=ms(f[0]), next_program_ms=ms(nxt[0]) if nxt else None,
        heartbeats_inside=len(win), max_hb_spacing_inside_ms=max((ms(b - a) for a, b in zip(win, win[1:])), default=None)))
out['final_uart_line'] = lines[-1][2][-60:] if lines else None
out['backed_status_prints'] = [l[2][:60] + ' ... ' + l[2][l[2].find('backed='):l[2].find('backed=') + 26] + f' @ {ms(l[0]):.3f} ms'
                               for l in lines if 'backed=' in l[2]]
print(json.dumps(out, indent=1))
