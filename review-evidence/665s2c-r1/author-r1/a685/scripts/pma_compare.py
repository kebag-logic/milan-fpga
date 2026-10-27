"""Compare the region decode (PMA) of two VexiiRiscv netlists, the fetch plugin's name folded.

usage: pma_compare.py A.v B.v
Every `assign` in the core module whose left side names a PMA builder or port
(pmaBuilder, onPma, pmaPort) is taken, with the fetch plugin's own prefix
(FetchCachelessPlugin_logic_onPma_port / FetchL1Plugin_logic_ctrl_pmaPort, and
their builders) folded to one name, so the cacheless and the cached fetch compare
line for line. The plugin's input address and the pipeline stages it carries
its answer through are left out: they are where the decode is read, not what
it decodes. Prints both line counts, the lines only in each, and exits 1 when
the decodes differ.
"""
import re
import sys
from pathlib import Path

FOLD = ((r'FetchCachelessPlugin_logic_onPma_port', 'FETCH_PMA'), (r'FetchL1Plugin_logic_ctrl_pmaPort', 'FETCH_PMA'),
        (r'FetchCachelessPlugin_pmaBuilder', 'FETCH_PMA_BUILDER'), (r'FetchL1Plugin_pmaBuilder', 'FETCH_PMA_BUILDER'))


def decode(path: Path) -> set[str]:
    text = path.read_text()
    core = text[text.index('\nmodule VexiiRiscv ('):]
    core = core[:core.index('\nendmodule')]
    lines = set()
    for line in core.splitlines():
        m = re.match(r'\s*assign (\S+) = (.*);$', line)
        # The decode itself, not the pipeline stage it is read at or carried to.
        if (m and re.search(r'pmaBuilder|onPma|pmaPort', m.group(1))
                and not m.group(1).endswith('_cmd_address') and not m.group(1).startswith('fetch_logic_ctrls_')):
            for old, new in FOLD:
                line = line.replace(old, new)
            lines.add(line.strip())
    return lines


a, b = (decode(Path(p)) for p in sys.argv[1:3])
print(f'{Path(sys.argv[1]).name}: {len(a)} decode lines; {Path(sys.argv[2]).name}: {len(b)} decode lines')
for line in sorted(a - b):
    print('only A:', line)
for line in sorted(b - a):
    print('only B:', line)
print('decode identical' if a == b else 'decode differs')
raise SystemExit(0 if a == b else 1)
