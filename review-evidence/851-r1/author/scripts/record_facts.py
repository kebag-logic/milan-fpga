"""record_facts.py <dir> ...: for each Vivado measurement directory, its run rc and seconds, its log's SHA-256 and
bytes, the log's highest reported memory peak, its Synth 8-4445 and 8-6901 lines, whether every recorded memory image
still hashes as recorded, and the routed hierarchy rows the area budget names. Prints JSON; reads, never writes."""
import hashlib
import json
import re
import sys
from pathlib import Path

out = {}
for d in map(Path, sys.argv[1:]):
    r = {}
    rc = (d / 'baseline.log.rc').read_text().split()
    r['rc'], r['seconds'] = int(rc[0]), int(rc[1].rstrip('s'))
    log = (d / 'baseline.log').read_bytes()
    r['log_sha256'], r['log_bytes'] = hashlib.sha256(log).hexdigest(), len(log)
    text = log.decode(errors='replace')
    peaks = [float(x) for x in re.findall(r'Memory \(MB\): peak = ([0-9.]+)', text)]
    r['peak_mb'] = max(peaks) if peaks else None
    r['synth_8_4445'] = len(re.findall(r'(?:WARNING|ERROR|CRITICAL WARNING): \[Synth 8-4445\]', text))
    r['synth_8_6901'] = sorted(set(m.group(0)[:160] for m in re.finditer(r'WARNING: \[Synth 8-6901\][^\n]*', text)))
    imgs = d / 'baseline_images.json'
    if imgs.exists():
        ok = bad = 0
        for e in json.loads(imgs.read_text()):
            p = Path(e['path'])
            if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() == e['sha256']:
                ok += 1
            else:
                bad += 1
        r['images_match'], r['images_differ'] = ok, bad
    hier = d / 'baseline_hierarchy.rpt'
    if hier.exists():
        rows = {}
        for line in hier.read_text(errors='replace').splitlines():
            m = re.match(r'^\|\s+(\S+)\s+\|\s+(\S.*?)\s+\|\s+(\d+)\s+\|', line)
            if m and m.group(1) in ('alinx_ax7101', 'milan_datapath', 'pp_shadow', 'u_pp', 'u_maap', 'u_encoder') and m.group(1) not in rows:
                rows[m.group(1)] = {'module': m.group(2), 'lut': int(m.group(3)), 'depth': (len(line) - len(line[1:].lstrip()))}
        r['hierarchy'] = rows
    out[d.name] = r
print(json.dumps(out, indent=1))
