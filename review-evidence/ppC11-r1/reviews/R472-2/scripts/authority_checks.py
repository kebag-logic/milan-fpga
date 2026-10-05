#!/usr/bin/env python3
"""Independent documentation/interface/history and scope checks."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

def main():
    p=argparse.ArgumentParser();p.add_argument('repo',type=Path);a=p.parse_args();root=a.repo
    def show(rev,path):
        return subprocess.check_output(['git','-C',str(root),'show',rev+':'+path]).decode()
    port=re.compile(r'\b(?:input|output|inout)\s+(?:wire|logic|reg)\b[^;\n]*?\b(\w+_[io])\b')
    ports=set()
    for f in (root/'hdl').rglob('*.sv'):
        ports.update(port.findall(f.read_text()))
    names=set()
    for f in (root/'docs/architecture').glob('*.md'):
        # Leading-underscore wildcard fragments such as *_data_i are not names.
        names.update(re.findall(r'\b[A-Za-z][A-Za-z0-9_]*_[io]\b',f.read_text()))
    missing=sorted(names-ports)
    assert not missing,missing
    print('ARCHITECTURE_PORT_NAMES',len(names),'all declared', 'CONTROL rx_r472_err_i missing:', 'rx_r472_err_i' not in ports)
    base=show('c050d971','docs/architecture/02_interfaces.md')
    hist=(root/'docs/history/02-class-a-word-stream.md').read_text()
    fragment=base[base.index('Word-oriented stream'):base.index('The RX stream carries')].strip()
    assert fragment in hist
    for caption,code in re.findall(r'\*\*(F02\.[34] — [^\n]+)\*\*.*?```wavedrom\n(.*?)```',base,re.S):
        assert code in hist
        print('HISTORY_WAVEFORM_VERBATIM',caption,hashlib.sha256(code.encode()).hexdigest())
    print('HISTORY_PROSE_TABLE_VERBATIM',hashlib.sha256(fragment.encode()).hexdigest())
    head=(root/'docs/architecture/02_interfaces.md').read_text()
    before=show('3d5a201','docs/architecture/02_interfaces.md')
    def rule5(text):
        return text[text.index('5. Reset:'):text.index('## 3. Class A')].replace('<a id="sec-02-class-a"></a>\n','').strip()
    assert rule5(base)==rule5(before)
    assert rule5(head)==rule5(show('ead80360','docs/architecture/02_interfaces.md'))
    print('RESET_RULE5_UNCHANGED_BY_C11_AND_IDENTICAL_TO_MERGED_MAIN')
    assert 'P-EN-TALKER-DYN-MAPPINGS-RUNNING' not in '\n'.join(f.read_text(errors='replace') for f in (root/'docs').rglob('*.md'))
    assert 'P-EN-TALKER-DYN-MAPPINGS-RUNNING' not in show('c050d971','docs/architecture/06_aecp_engine.md')
    assert 'no RTL consumer' in next(x for x in (root/'docs/architecture/01_overview.md').read_text().splitlines() if x.startswith('| P-EN-PLAIN-IEEE-PROFILE'))
    assert not list((root/'docs/diagrams').glob('2[0-4]-*.png'))
    print('NO_STRAY_DYN_MAPPING_ID; PROFILE_NONCONSUMER_RECORDED; FIVE_PNGS_ABSENT')
    # A small independent waveform expansion makes held-byte and pulse timing reviewable.
    for anchor in ['fig-02-rxwave','fig-02-txwave','fig-02-memwave']:
        rest=head[head.index('<a id="'+anchor+'">'):]
        block=json.loads(re.search(r'```wavedrom\n(.*?)```',rest,re.S).group(1))
        print('WAVEFORM_SOURCE',anchor,json.dumps(block))

if __name__=='__main__':
    main()
