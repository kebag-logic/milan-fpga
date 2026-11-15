"""In-process probes of load_grade.py's own-ADP rule (argument: the harness directory of the tree under review).

No file is written: each probe patches the imported module and reads --check's findings.
P6: the measurement one rule step dearer (12,500 cycles, 135 us) with the statement left at 130: must be refused.
P7: the merge of a NEAREST point's own statements removed from stated(): the tsn-c-stack#32 column then states 125 us
    for 8x8/1if's ADP record, under its measurement's 130: must be refused.
P8: the head as is: no own-ADP finding.
"""
import sys
from pathlib import Path
from unittest import mock

HERE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(HERE))
import load_grade  # noqa: E402

root = HERE.parents[2]
base = [f for f in load_grade.own_findings(root)]
print('P8 head own_findings:', base or 'none')
with mock.patch.dict(load_grade.OWN_MEASURED, {'8x8/1if': {'record.adp': (12_500, 'probe')}}):
    got = load_grade.own_findings(root)
    print('P6 dearer measurement refused:', bool(got), got[:2])
real = load_grade.stated


def no_merge(r, point, table=None):
    with mock.patch.dict(load_grade.OWN, {'8x8/1if': {}}):
        return real(r, point, table)


with mock.patch.object(load_grade, 'stated', no_merge):
    got = load_grade.own_findings(root)
    print('P7 own statement not merged refused:', bool(got), got[:2])
print('rule_us(12210) =', load_grade.rule_us(12_210), '; rule_us(11905) =', load_grade.rule_us(11_905),
      '; rule_us(11906) =', load_grade.rule_us(11_906))
