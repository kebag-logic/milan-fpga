#!/usr/bin/env python3
"""The struct-ends layout of a checkout (#665, round 16 item 2; [A683t]'s X4-8 extended to this head): every field
THE RETRY and THE TRANSMIT added, moved to the end of its struct, so the image's other data keep the offsets they had
before them. THE RETRY's age and its count, THE TRANSMIT's two counts (out of struct ctrl_loop_stats, to the end of
struct ctrl_loop) and AECP's earliest held retry's time (to the end of struct aecp). THE TRANSMIT's client, its age,
its context, the loop's ordinary-pass count, tx_pass and rx_cap already end struct ctrl_loop, and SRP's hold, its age
and resent_pass end struct srp_mbx. A labelled scratch layout, never the measurement of record.

usage: struct_ends.py CHECKOUT   (edits it; prints the diff's files)
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
ctrl = root / 'sw/firmware/ctrl'


def edit(path: Path, pairs: list[tuple[str, str]]) -> None:
    text = path.read_text()
    for old, new in pairs:
        if text.count(old) != 1:
            raise SystemExit(f'{path}: {text.count(old)} sites for {old!r}')
        text = text.replace(old, new)
    path.write_text(text)
    print(path.relative_to(root))


edit(ctrl / 'loop/ctrl_loop.h', [
    ('\tctrl_retry_aged_fn retry_aged;  // its age\n', ''),
    ('\tuint32_t retry_aged_passes;  // passes given whole to an aged retry (THE RETRY)\n'
     '\tuint32_t transmit_passes;    // passes that called THE TRANSMIT\'s client\n'
     '\tuint32_t transmit_aged_passes;  // passes given whole to an aged transmit (THE TRANSMIT)\n', ''),
    ('\tuint32_t rx_cap;                // the records of a channel this pass takes at most (THE TICK)\n};',
     '\tuint32_t rx_cap;                // the records of a channel this pass takes at most (THE TICK)\n'
     '\tctrl_retry_aged_fn retry_aged;\n\tuint32_t retry_aged_passes;\n\tuint32_t transmit_passes;\n'
     '\tuint32_t transmit_aged_passes;\n};'),
])
loop_c = ctrl / 'loop/ctrl_loop.c'
text = loop_c.read_text()
for name in ('retry_aged_passes', 'transmit_aged_passes'):
    text = text.replace(f'l->stats.{name}++', f'l->{name}++')
text = text.replace('l->stats.transmit_passes++', 'l->transmit_passes++')
loop_c.write_text(text)
print(loop_c.relative_to(root))
aecp_h = ctrl / 'aecp/aecp.h'
text = aecp_h.read_text()
line = '\tuint32_t retry_since; // with retry_held, the earliest held retry\'s time (aecp_retry_aged)\n'
if text.count(line) != 1:
    raise SystemExit(f'{aecp_h}: no single retry_since')
text = text.replace(line, '')
end = '\tuint8_t held[AECP_HELD_BYTES];\n};'
if text.count(end) != 1:
    raise SystemExit(f'{aecp_h}: no single end of struct aecp')
aecp_h.write_text(text.replace(end, '\tuint8_t held[AECP_HELD_BYTES];\n' + line + '};'))
print(aecp_h.relative_to(root))
