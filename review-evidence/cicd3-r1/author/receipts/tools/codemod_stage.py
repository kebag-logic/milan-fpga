"""Rewrite each milan-fpga mutation driver's staging directory to scripts/mutant_stage.py."""
import re, sys
from pathlib import Path
ROOT = Path('/data-2/milan/lanes/cicd-1')
SKIP_CALL = '.gsi-uc-'   # a run directory for a microcode image, not a model build
TD = re.compile(r'tempfile\.TemporaryDirectory\(prefix=("[^"]+")(?:, dir=os\.environ\.get\("TMPDIR"\))?\)')
TDD = re.compile(r'tempfile\.TemporaryDirectory\(prefix=("[^"]+"), dir=([^)]+\)?)\)')
MK = re.compile(r'tempfile\.mkdtemp\(prefix=("[^"]+"), dir=(HERE)\)')
for path in sys.argv[1:]:
    p = ROOT / path; s = p.read_text(); orig = s
    n = 0
    def td(m):
        global n
        if SKIP_CALL in m.group(0): return m.group(0)
        n += 1; return f'mutant_stage.directory({m.group(1)})'
    s = TD.sub(td, s)
    def tdd(m):
        global n
        if SKIP_CALL in m.group(0): return m.group(0)
        n += 1; return f'mutant_stage.directory({m.group(1)}, dir={m.group(2)})'
    s = TDD.sub(tdd, s)
    def mk(m):
        global n
        n += 1; return f'mutant_stage.mkdtemp({m.group(1)}, dir={m.group(2)})'
    s = MK.sub(mk, s)
    if n == 0:
        print(f'{path}: NO SITE'); continue
    lines = s.split('\n')
    # where to import
    ins = [i for i, l in enumerate(lines) if l.startswith('sys.path.insert(0,') and 'scripts' in l]
    if ins:
        i = ins[0] + 1
        while i < len(lines) and lines[i].startswith(('from ', 'import ')) and 'E402' in lines[i]:
            i += 1
        lines.insert(i, 'import mutant_stage  # noqa: E402')
        how = 'after its scripts path'
    else:
        here = [i for i, l in enumerate(lines) if re.match(r'^HERE = Path\(__file__\)\.resolve\(\)\.parent$', l)]
        if not here:
            print(f'{path}: NO HERE, manual'); continue
        lines[here[0] + 1:here[0] + 1] = ['sys.path.insert(0, str(HERE.parents[2] / "scripts"))',
                                          'import mutant_stage  # noqa: E402']
        how = 'new scripts path'
        if not any(l == 'import sys' for l in lines):
            j = next(i for i, l in enumerate(lines) if l.startswith('import ') or l.startswith('from '))
            # keep alphabetical-ish: put before the first import after 'import s' sorted position
            imports = [i for i, l in enumerate(lines[:here[0]]) if l.startswith('import ')]
            pos = next((i for i in imports if lines[i] > 'import sys'), imports[-1] + 1)
            lines.insert(pos, 'import sys')
            how += ' + import sys'
    s = '\n'.join(lines)
    if 'tempfile.' not in s:
        s = s.replace('import tempfile\n', '', 1)
        how += ', tempfile import dropped'
    p.write_text(s)
    print(f'{path}: {n} site(s), {how}')
