"""The heaviest SRP records of each log (srp_mbx:receive SPAN cycles), largest first. usage: srpmax.py LOG..."""
import sys
for path in sys.argv[1:]:
    spans = []
    with open(path, errors='replace') as f:
        for line in f:
            if line.startswith('SPAN ') and line.rstrip().endswith('srp_mbx:receive'):
                w = line.split()
                spans.append(int(w[3]))
    spans.sort(reverse=True)
    print(f'{path}: {len(spans)} records, heaviest {spans[:6]}')
