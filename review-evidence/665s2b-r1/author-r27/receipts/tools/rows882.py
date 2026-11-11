"""#882's changed rows, before (round 26's aecp group) and after (this round's, arm A and arm B), at both points: each
row's label, status, interval (ms), its measured bound (ms), its taking pass (CPU cycles), and each group's heaviest
AECP record (aecp_mbx:frame SPAN, CPU cycles). usage: rows882.py NAME=RESULTS_DIR..."""
import json, sys
ROWS = ('get_counters', 'get_avb_info', 'unknown_command')
for arg in sys.argv[1:]:
    name, d = arg.split('=', 1)
    r = json.load(open(f'{d}/aecp.json'))
    frames = sorted((int(l.split()[3]) for l in open(f'{d}/aecp.log', errors='replace')
                     if l.startswith('SPAN ') and l.rstrip().endswith('aecp_mbx:frame')), reverse=True)
    print(f'## {name}: heaviest AECP records {frames[:3]}')
    for p in r['probes']:
        if any(f'.{row}.' in p['probe'] for row in ROWS):
            print(f"{p['probe']} | {p['row']} | {p['status']} | {p.get('ms')} ms (bound {p.get('bound_ms')}) | "
                  f"pass {p.get('pass_cycles')} cycles")
