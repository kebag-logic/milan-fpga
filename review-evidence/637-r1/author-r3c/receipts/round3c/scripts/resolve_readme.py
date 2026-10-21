import sys
p = sys.argv[1]
L = open(p).read().split('\n')
i = next(n for n, l in enumerate(L) if l.startswith('<<<<<<< '))
j = L.index('=======', i)
k = next(n for n in range(j, len(L)) if L[n].startswith('>>>>>>> '))
ours, theirs = L[i+1:j], L[j+1:k]
assert len(ours) == 3 and len(theirs) == 1
old = ("Then `[MAPREC]` (#637): the channel-map records written and restored across a planted power cycle, "
       "the EMPTY list in both directions included. Its planted controls are `make dynmap-mutants`; "
       "see [the section below](#the-658-power-on-audio-maps-obj_dynmap) |")
assert ours[0].endswith(old)
new = ("Then, on a fresh boot, `[762-DP]` (#762) on this shipping geometry, with the elaborated parameters logged. "
       "Then `[MAPREC]` (#637): the channel-map records written and restored across a planted power cycle, "
       "the EMPTY list in both directions included. Its planted controls are `make dynmap-mutants`; "
       "see [the section below](#the-658-power-on-audio-maps-obj_dynmap) |")
row = ours[0][:-len(old)] + new
assert len([n for n in range(len(L)) if L[n].startswith('<<<<<<< ')]) == 1
L[i:k+1] = [row] + ours[1:]
open(p, 'w').write('\n'.join(L))
