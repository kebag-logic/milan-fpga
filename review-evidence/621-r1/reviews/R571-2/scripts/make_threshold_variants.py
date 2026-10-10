#!/usr/bin/env python3
"""Write donor-generator variants for the liveness boundary probes.

Usage: make_threshold_variants.py <gen_gptp_ucode.py> <outdir>

third  : asCapable falls when the lost count reaches 3 (one request early)
fifth  : asCapable falls when the lost count reaches 5 (one request late)
plants : the campaign's two liveness plants, recomputed independently, and
         whether their generator texts are byte-identical
"""
import hashlib
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
anchor = 'p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=LOST_N_C + 1)'
assert src.count(anchor) == 1, 'threshold anchor not unique'
(out / 'gen_third.py').write_text(src.replace(anchor, anchor.replace('LOST_N_C + 1', 'LOST_N_C')))
(out / 'gen_fifth.py').write_text(src.replace(anchor, anchor.replace('LOST_N_C + 1', 'LOST_N_C + 2')))

credit = '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n'
start = src.index('\ndef prog_leg_pdepoch(')
end = src.find('\ndef ', start + 1)
region = src[start:end]
assert region.count(credit) == 1
a = src[:start] + region.replace(credit, '') + src[end:]
tail = '    p.emit("END")\n    return p\n\n\ndef prog_leg_pdpair'
assert src.count(credit + tail) == 1
b = src.replace(credit + tail, tail)
for name, text in (('liveness-not-marked', a), ('r571-no-liveness', b)):
    print(name, hashlib.sha256(text.encode()).hexdigest())
print('plants byte-identical:', a == b)
print('credit occurrences in donor:', src.count(credit))
