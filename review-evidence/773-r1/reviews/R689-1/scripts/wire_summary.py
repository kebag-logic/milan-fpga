"""Summarise capture_coherence dp [WIRE]/[GRID]/[HOLD] info lines and the final verdict."""
import re, sys
pat = re.compile(r'\[(?P<run>[^\]]+)\] \[WIRE\] offset (?P<ofs>\d+) ns: (?P<na>\d+) AAF PDUs, avtp_timestamp - offset - hand-over (?P<alo>-?\d+)\.\.(?P<ahi>-?\d+) ns; (?P<nc>\d+) CRF PDUs, timestamp - (?P<capp>\d+) ns applied - hand-over (?P<clo>-?\d+)\.\.(?P<chi>-?\d+) ns; \[GRID\] AAF (?P<aon>\d+) on, (?P<aoff>\d+) off, CRF (?P<con>\d+) on, (?P<coff>\d+) off; \[HOLD\] avtp_timestamp - hand-over max (?P<hold>-?\d+) ns')
rows = []
for l in open(sys.argv[1], errors='replace'):
    m = pat.search(l)
    if m: rows.append(m.groupdict())
    if 'checks:' in l and 'failures' in l: print(l.strip())
for r in rows:
    print("%-20s ofs=%7s AAF n=%4s margin %6s..%6s  CRF n=%3s margin %6s..%6s  GRID aaf %s/%s crf %s/%s  HOLD %s" % (
        r['run'], r['ofs'], r['na'], r['alo'], r['ahi'], r['nc'], r['clo'], r['chi'], r['aon'], r['aoff'], r['con'], r['coff'], r['hold']))
for ofs in sorted({r['ofs'] for r in rows}):
    rs = [r for r in rows if r['ofs'] == ofs]
    print("offset %s: %d runs, AAF margin %d..%d, CRF margin %d..%d, HOLD max %d, GRID off aaf %d crf %d, AAF PDUs %d CRF PDUs %d" % (
        ofs, len(rs), min(int(r['alo']) for r in rs), max(int(r['ahi']) for r in rs),
        min(int(r['clo']) for r in rs), max(int(r['chi']) for r in rs), max(int(r['hold']) for r in rs),
        sum(int(r['aoff']) for r in rs), sum(int(r['coff']) for r in rs), sum(int(r['na']) for r in rs), sum(int(r['nc']) for r in rs)))
