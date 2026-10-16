"""Turn unprovenanced interpreter programs into reviewed-list entries (scratch tool; the lists are reviewed data).

Usage: pins.py UNPINNED.json RULES.py OUT.json
Each inline or streamed text gets its source (the tracked file holding it, found by its lines) and the reason
of the first matching text rule; each job-written script gets the generator and reason of its path rule.
Entries no rule covers are listed and refuse the output.
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path('$LANES/737-image')
unpinned = json.loads(Path(sys.argv[1]).read_text())
rules = {}
exec(Path(sys.argv[2]).read_text(), rules)


def source(text: str) -> str | None:
    """A tracked file holding the program's text: tried line by line, longest first."""
    lines = sorted({l.strip() for l in text.splitlines() if len(l.strip()) >= 12}, key=len, reverse=True)
    for line in lines[:8]:
        for candidate in (line, line.replace('\\', '\\\\')):
            found = subprocess.run(['git', '-C', str(ROOT), 'grep', '-F', '-l', '--recurse-submodules', '-e',
                                    candidate, '--', '.', ':!ci/image/exec-audit*.json', ':!ci/image/*receipt*'],
                                   capture_output=True, text=True).stdout.split()
            if found:
                return found[0]
    return None


inline, generated, missing = {}, {}, []
for digest, entry in sorted(unpinned.items()):
    if entry['kind'] in ('inline', 'stream'):
        text = entry.get('text')
        rule = next((r for r in rules['TEXTS'] if text is not None and
                     (text == r[0][1:] if r[0].startswith('=') else r[0] in text)), None)
        where = rule[1] if rule else (source(text) if text is not None else None)
        reason = rule[2] if rule else rules['SOURCES'].get(where)
        if text is None or where is None or reason is None:
            missing.append((digest, entry['kind'], entry['interpreter'], where, (text or '')[:100], entry['steps'][:2]))
            continue
        inline[digest] = {'interpreter': entry['interpreter'], 'form': entry['kind'], 'source': where,
                          'reason': reason, 'text': text}
        if rule and len(rule) > 3:
            # A long variant of a tracked script is kept as its exact difference from that script.
            import difflib
            base = (ROOT / rule[3]).read_text()
            diff = ''.join(difflib.unified_diff(base.splitlines(True), text.splitlines(True), rule[3], 'variant', n=0))
            inline[digest].pop('text')
            inline[digest].update({'variant_of': rule[3], 'diff': diff})
    else:
        path = entry['paths'][0]
        rule = next(((r, m) for r in rules['SCRIPTS'] if (m := re.search(r[0], path))), None)
        if rule is None:
            missing.append((digest, entry['kind'], entry['interpreter'], path, entry['steps'][:2]))
            continue
        (pattern, generator, reason), match = rule
        generated[digest] = {'kind': 'script' if entry['kind'] == 'script' else 'program',
                             'interpreter': entry['interpreter'], 'name': entry['names'][0],
                             'generator': generator, 'reason': reason.format(**match.groupdict())}
Path(sys.argv[3]).write_text(json.dumps({'inline_programs': inline, 'generated_programs': generated},
                                        indent=1, sort_keys=True))
print(f'{len(inline)} inline or streamed, {len(generated)} generated, {len(missing)} without a rule')
for row in missing:
    print('MISSING', row)
sys.exit(1 if missing else 0)
