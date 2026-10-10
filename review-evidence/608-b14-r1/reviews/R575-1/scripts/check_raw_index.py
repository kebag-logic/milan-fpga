#!/usr/bin/env python3
"""Sum the archived raw-capture index per group: count and bytes of .pcap entries, and hash coverage."""
import json, sys, glob, os
pk = sys.argv[1]
for f in sorted(glob.glob(pk + '/author/raw-index/*.jsonl')):
    ents = [json.loads(l) for l in open(f)]
    pc = [e for e in ents if e['path'].endswith('.pcap')]
    nohash = [e['path'] for e in pc if not e.get('sha256')]
    print(os.path.basename(f), 'entries', len(ents), 'pcaps', len(pc), 'pcap bytes', sum(e['bytes'] or 0 for e in pc),
          '(%.3g GB / %.1f MB)' % (sum(e['bytes'] or 0 for e in pc) / 1e9, sum(e['bytes'] or 0 for e in pc) / 1e6), 'pcaps without sha256', len(nohash))
