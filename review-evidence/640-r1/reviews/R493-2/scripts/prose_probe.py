#!/usr/bin/env python3
"""Screen changed prose and reproduce the M3 table rendering; no source edits."""
from pathlib import Path
import re
import subprocess
import sys
import cmarkgfm

repo=Path(sys.argv[1]).resolve()
out=Path(sys.argv[2]).resolve()
sys.path.insert(0,str(repo/'scripts'))
import check_doc_style as style

observations=[]
for path in ['docs/design/MARK_II_AREA_PLAN.md','docs/design/AREA_BUDGET.md']:
    text=(repo/path).read_text()
    diff=subprocess.check_output(['git','diff','--unified=0','c4b8b7d3','HEAD','--',path],cwd=repo,text=True)
    changed=set()
    for m in re.finditer(r'^@@ .*? \+(\d+)(?:,(\d+))? @@',diff,re.M):
        start=int(m[1]); count=int(m[2] or 1)
        changed.update(range(start,start+count))
    for n,line in enumerate(text.splitlines(),1):
        if n in changed and not line.startswith(('|','#','- **[')):
            for finding in style.analyze(line):
                if finding.reason.startswith('sentence'):
                    observations.append(f'{path}:{n}: {finding.reason}: {finding.text}')
(out/'changed-sentence-audit.txt').write_text('Screening only: individual changed lines, with the repository tokenizer.\n'
    'Multiline prose and links containing code need manual interpretation.\n'+'\n'.join(observations)+'\n')
text=(repo/'docs/design/MARK_II_AREA_PLAN.md').read_text()
sample=text.split('Its basis uses these shares:')[1].split('### Cumulative')[0]
html=cmarkgfm.github_flavored_markdown_to_html(sample)
(out/'m3-table-render.html').write_text(html)
assert '<td>That displaces about 3,380 LUTs.</td>' in html
fixed=sample.replace('| AECP dispatch queue | 421 | 40 percent |\n',
                     '| AECP dispatch queue | 421 | 40 percent |\n\n')
rendered=cmarkgfm.github_flavored_markdown_to_html(fixed)
assert '<td>That displaces about 3,380 LUTs.</td>' not in rendered
assert '<p>That displaces about 3,380 LUTs.' in rendered
(out/'m3-table-fixed-render.html').write_text(rendered)
print('Screening observations:',len(observations))
print('M3 presentation defect confirmed: narrative is rendered as table rows.')
print('One blank line after the fourth data row restores narrative paragraphs.')
print('All text and numbers retained; no source file changed.')
