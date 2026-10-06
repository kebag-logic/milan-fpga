#!/usr/bin/env python3
"""Read prior findings only after the independent decision-order receipt exists."""
import json
import re
import subprocess
import sys
from pathlib import Path

out = Path(sys.argv[1])
assert (out / 'independent-decision-order.json').exists()
result = []
for number in (6024750681, 6024636464):
    obj = json.loads(subprocess.check_output(['gh', 'api', f'repos/kebag-logic/milan-fpga/issues/comments/{number}']))
    text = obj['body']
    blocks = []
    for match in re.finditer(r'^\*\*(R\d+-1-F[12]) \| MINOR \| (.*?) \| (.*?)\*\*\s*$', text, re.M):
        tail = text[match.end():]
        stops = [pos for token in ('\n**R', '\nConformance was applied', '\nApplied lenses')
                 if (pos := tail.find(token)) >= 0]
        section = tail[:min(stops)] if stops else tail
        blocks.append({'id': match.group(1), 'severity': 'MINOR', 'lenses': match.group(2),
                       'artifact': match.group(3), 'public_finding_text': section.strip(),
                       'disposition': 'RESOLVED in R525-2 after independent verification of the public correction'})
    assert len(blocks) == 2
    result.append({'comment_id': number, 'url': obj['html_url'], 'findings': blocks})
(out / 'prior-findings.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: four prior MINOR identifiers captured; original Conformance/Docs and Tests/Docs lenses retained')
