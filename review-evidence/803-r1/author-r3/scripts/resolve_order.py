"""resolve_order.py <file> <order>...: resolve each conflict hunk of <file> in turn by concatenating both sides,
'ot' = ours (HEAD) then theirs (dev), 'to' = theirs then ours, 'm' = leave the markers for a hand edit.
Refuses a count mismatch and any diff3 base section."""
import sys

path, orders = sys.argv[1], sys.argv[2:]
lines = open(path, encoding='utf-8').read().split('\n')
out, i, hunk = [], 0, 0
while i < len(lines):
    if not lines[i].startswith('<<<<<<< '):
        out.append(lines[i])
        i += 1
        continue
    j = lines.index('=======', i)
    k = next(n for n in range(j, len(lines)) if lines[n].startswith('>>>>>>> '))
    ours, theirs = lines[i + 1:j], lines[j + 1:k]
    assert not any(x.startswith('||||||| ') for x in ours), 'diff3 base section'
    order = orders[hunk]
    if order == 'ot':
        out += ours + theirs
    elif order == 'to':
        out += theirs + ours
    else:
        out += lines[i:k + 1]
    hunk += 1
    i = k + 1
assert hunk == len(orders), (hunk, len(orders))
open(path, 'w', encoding='utf-8').write('\n'.join(out))
print(path, hunk, 'hunks')
