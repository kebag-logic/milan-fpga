#!/usr/bin/env python3
"""Compare the earlier probes' outcomes, retaining all reading differences for inspection.
Usage: python r10_compare_probes.py PACKET OUT.json
"""
import json, re, sys
from pathlib import Path
root,out=map(Path,sys.argv[1:])
keys={"forms","detected","statuses","verdicts","escaped","escaping","row3200_insensitive",
      "row3200_polls_detected","not_meeting","any_statuses","not_detected","all_receipts","exceptions",
      "id_forms","id_detected","expect_fail","fail_detected"}
def diffs(a,b,path=""):
    if isinstance(a,dict) and isinstance(b,dict):
        return [d for k in sorted(a.keys()|b.keys()) for d in diffs(a.get(k),b.get(k),path+"/"+k)]
    return [] if a==b else [dict(path=path,before=a,after=b)]
def points(d):
    return sorted(set(re.findall(r"(MARKUP|UNCOVERED) (?:629_MEDIA_CLOCK_FOLLOWING_BENCH\.md|README\.md):(\d+)",json.dumps(d))))
records=[]
for old in sorted((root/'r9').glob('*-probe-rerun.json')):
    new=root/'r10'/old.name
    a,b=json.loads(old.read_text()),json.loads(new.read_text())
    x,y=a['reading'],b['reading']
    outcome=all(x.get(k)==y.get(k) for k in keys) and a['exit']==b['exit']
    records.append(dict(probe=old.name,unchanged_probe=a['probe_sha256']==b['probe_sha256'],
                        outcomes_equal=outcome,reading_differences=diffs(x,y),
                        diagnostic_points_before=points(a),diagnostic_points_after=points(b)))
r=dict(note="Round 9 to round 10: unchanged probe hashes, exits and outcome fields; all other reading differences retained, including appended source-line movement",probes=records,
       all_outcomes_equal=all(x['outcomes_equal'] and x['unchanged_probe'] for x in records))
out.write_text(json.dumps(r,indent=1)+'\n')
print(json.dumps({'probes':len(records),'all_outcomes_equal':r['all_outcomes_equal'],
                  'reading_differences':{x['probe']:len(x['reading_differences']) for x in records if x['reading_differences']}}))
raise SystemExit(0 if r['all_outcomes_equal'] else 1)
