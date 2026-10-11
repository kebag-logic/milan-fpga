"""Compare independent unsplit measurements with identical firmware inputs."""
import copy
import csv
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd() / 'sw/firmware/gtest'))
import fw_coverage as coverage

baseline, candidate, output = map(Path, sys.argv[1:])
raw=[]
kept=[]
raw_tallies=[]
kept_tallies=[]
for directory in (baseline, candidate):
    measured=coverage.collect([directory/'ctrl',directory/'ctrl_nvm'])
    raw.append(measured)
    raw_tallies.append(coverage.tally(measured))
    retained,findings=coverage.apply_exclusions(copy.deepcopy(measured),
                       coverage.exclusions(coverage.README.read_text()))
    assert not findings, findings
    kept.append(retained)
    kept_tallies.append(coverage.tally(retained))
    assert not coverage.compare(kept_tallies[-1],coverage.read_ratchet(coverage.RATCHET.read_text()))
assert raw[0].keys()==raw[1].keys()
def locations(source):
    return {str(number):dict(covered=line.count>0,arcs=[count>0 for count in line.arcs])
            for number,line in sorted(source.lines.items())}
def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()
def fraction(pair):
    return '%d/%d' % pair
rows=[]
for name in sorted(raw[0]):
    left,right=raw_tallies[0][name],raw_tallies[1][name]
    retained_left,retained_right=kept_tallies[0][name],kept_tallies[1][name]
    assert left==right and retained_left==retained_right, name
    assert locations(raw[0][name])==locations(raw[1][name]), name
    assert locations(kept[0][name])==locations(kept[1][name]), name
    rows.append(dict(file=name,baseline_raw_lines=fraction(left.lines),candidate_raw_lines=fraction(right.lines),
                     baseline_raw_branches=fraction(left.branches),candidate_raw_branches=fraction(right.branches),
                     baseline_kept_lines=fraction(retained_left.lines),candidate_kept_lines=fraction(retained_right.lines),
                     baseline_kept_branches=fraction(retained_left.branches),candidate_kept_branches=fraction(retained_right.branches),
                     covered_locations_equal=True,raw_locations_sha256=digest(locations(raw[0][name])),
                     kept_locations_sha256=digest(locations(kept[0][name]))))
with (output/'ROUND2-COVERAGE-COMPARISON.csv').open('w') as stream:
    writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
print(f'PASS: {len(rows)} files match in raw and retained fractions and covered line/branch locations')
