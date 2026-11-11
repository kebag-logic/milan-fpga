"""Every AECP and ACMP response a group's log committed: (cycle, channel, interface, kind, seq, type, status)."""
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import grade
log_path = Path(sys.argv[2])
text = log_path.read_text()
log = grade.parse(text, 100_000_000, 100_000_000)
for c, ch, i, fr in log.tx:
    if len(fr) < 36 or fr[12:14] != b'\x22\xf0':
        continue
    sub, mt, status = fr[14], fr[15] & 0xF, fr[16] >> 3
    if sub == 0xFB:
        seq = int.from_bytes(fr[34:36], 'big')
        if mt == 1:
            cmd = int.from_bytes(fr[36:38], 'big')
            print(f'{c} ch{ch} if{i} AEM_RESPONSE seq={seq:x} u={cmd >> 15} cmd={cmd & 0x7fff:04x} status={status} len={len(fr)}')
        elif mt == 7:
            cmd = int.from_bytes(fr[42:44], 'big')
            print(f'{c} ch{ch} if{i} MVU_RESPONSE seq={seq:x} cmd={cmd:04x} status={status} len={len(fr)}')
        else:
            print(f'{c} ch{ch} if{i} AECP mt={mt} seq={seq:x} status={status}')
    elif sub == 0xFC:
        seq = int.from_bytes(fr[62:64], 'big') if len(fr) > 63 else -1
        print(f'{c} ch{ch} if{i} ACMP mt={mt} seq={seq:x} status={status}')
