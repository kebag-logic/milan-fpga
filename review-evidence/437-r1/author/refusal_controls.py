#!/usr/bin/env python3
"""Exercise existing refusal policy on new list-context fixtures."""
import json
import sys
import tempfile
from pathlib import Path
from receipt import HERE, identity

sys.path.insert(0, str(Path.cwd() / 'scripts'))
import check_em_dash as gate
import gen_toc as toc

# Independent spelling; CR belongs to the separately preserved reader-normalization controls.
CHARACTERS = '\v\f\x1c\x1d\x1e\x1f\x85\xa0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000'
heading = '## Old \u2014 heading\n'
tail = '\n## Alpha\n\nBody.\n\n## Beta\n\nBody.\n\n## Gamma\n\nBody.\n'
plain = '# Page\n\n' + heading + tail
navigation = toc.apply(Path('sample.md'), plain).replace(toc.TODO, 'Description.')
assert toc.generated_block(navigation, 'sample.md') is not None
rows = []
with tempfile.TemporaryDirectory(prefix='refusal-', dir=HERE) as tmp:
    repo = Path(tmp)
    gate._fixture_git(repo, 'init', '-q', '--initial-branch=main')
    for char in CHARACTERS:
        prefix = '- item\n\n  text' + char + '\n<span>\n'
        (repo / f'base-{ord(char)}.md').write_text('# Page\n\n' + prefix + heading + '</span>\n' + tail)
        (repo / f'head-{ord(char)}.md').write_text(plain)
    base = gate._commit(repo, 'Refusal baseline')
    for char in CHARACTERS:
        (repo / f'base-{ord(char)}.md').write_text(navigation)
        (repo / f'head-{ord(char)}.md').write_text(navigation + '\n- item\n\n  text' + char + '\n')
    gate._commit(repo, 'Refusal head')
    for char in CHARACTERS:
        for side in ('base', 'head'):
            name = f'{side}-{ord(char)}.md'
            verdict = gate.Verdict()
            gate.judge_page(repo, base, gate.Change(name, name), verdict)
            assert (len(verdict.findings), verdict.exempt) == (2, 0), (name, verdict)
            assert any(f'U+{ord(char):04X}' in finding and 'at column' in finding for finding in verdict.findings)
            if side == 'base':
                assert any('mirrors no heading' in finding for finding in verdict.findings)
            rows.append({'side': side, 'character': f'U+{ord(char):04X}', 'findings': verdict.findings,
                         'exempt': verdict.exempt})
    try:
        gate.judge(repo, 'no-such-base')
    except gate.Refusal as exc:
        rows.append({'invalid_base': str(exc)})
    else:
        raise AssertionError('invalid base was accepted')
(HERE / 'refusals-head.json').write_text(json.dumps({**identity(), 'rows': rows}, indent=2) + '\n')
print(f'PASS: {len(rows) - 1} base/head character refusals, zero exemptions; invalid base refused')
