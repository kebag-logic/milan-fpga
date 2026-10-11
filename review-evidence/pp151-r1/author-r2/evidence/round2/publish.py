#!/usr/bin/env python3
"""Publish bounded text receipts and the current guard refusal table."""
from pathlib import Path
import hashlib
import json
import re
import sys

HERE = Path(__file__).resolve().parent
LANE = Path('<lane>')
OUT = Path('$MANAGEMENT/2026-09-23/pp151-a593')
DEST = OUT / 'evidence/round2'
sys.path.insert(0, str(LANE / 'tb/elab_guards'))
import guards
import mutants


def clean(text: str) -> str:
    """Replace machine-specific roots in published text."""
    for old, new in ((str(LANE), '<lane>'),
                     ('<scratch>', '<scratch>'),
                     ('<tools>', '<tools>'),
                     ('<vendor>', '<vendor>'),
                     ('<host-bin>', '<host-bin>')):
        text = text.replace(old, new)
    return text


def cell(text: str) -> str:
    """Keep a single Markdown table cell readable."""
    return clean(text).replace('|', '\\|').replace('\n', ' ')


def records(path: Path) -> dict[tuple[str, str, str], str]:
    """Index the tool's own words by kind, front end and guard."""
    out = {}
    for line in path.read_text().splitlines():
        found = re.match(r'^(GUARD|ELAB)\s+(\w+)\s+(\S+)\s+.*?: (.*)$', line)
        if found:
            out[found.group(1), found.group(2), found.group(3)] = found.group(4)
    return out


def tables(include_mutants: bool = True) -> None:
    """Produce complete tables only after all required measured legs finish."""
    runs = [('V', 'verilator', HERE / 'head/mutant-logs/control.log'),
            ('Y12', 'yosys', HERE / 'head/mutant-logs/control.log'),
            ('Y13', 'yosys', HERE / 'head/mutant013-logs/control.log'),
            ('X', 'xsim', HERE / 'probes/vivado.log'),
            ('S', 'synth', HERE / 'probes/vivado.log')]
    read = [(label, frontend, records(path)) for label, frontend, path in runs]
    sites = {f'{s.module}.{s.block}': s for s in guards.inventory(LANE)}
    rows = ['| Guard and task location | Violating / passing parameters | V refusal | Y12 refusal | Y13 refusal | X refusal | S refusal | Passing side |',
            '|---|---|---|---|---|---|---|---|']
    for guard in guards.GUARDS:
        site = sites[guard.name]
        params = lambda values: ', '.join(f'{k}={v:#x}' if v > 0xFFFFFF else f'{k}={v}'
                                         for k, v in values) or 'defaults'
        shape = params(guard.bad) + ' / ' + params(guard.good)
        if guard.setup or guard.plant:
            shape += ' (scratch context; see fixture table)'
        bad = ["``" + data['GUARD', frontend, guard.name] + "``" for _, frontend, data in read]
        good = [data['ELAB', frontend, guard.name] for _, frontend, data in read]
        if not all(s.startswith('elaborates') for s in good):
            raise RuntimeError(f'{guard.name}: incomplete passing proof')
        passed = '5/5; lint only measured UNSIGNED' if guard.unsigned else '5/5, rc 0'
        row = [f'`{guard.name}` (`{site.path}:{site.line}`)', shape, *bad, passed]
        rows.append('| ' + ' | '.join(map(cell, row)) + ' |')
    (DEST / 'guard-table.md').write_text('\n'.join(rows) + '\n')
    if not include_mutants:
        return

    rows = ['| Guard | Original term(s) | Tightened term(s) and named failure | Loosened term(s) and named failure |', '|---|---|---|---|']
    for guard in guards.GUARDS:
        columns = []
        for kind in ('tightened', 'loosened'):
            arm = next(a for a in mutants.arms() if a.name == f'{guard.name}:{kind}')
            failures = []
            for folder, frontends in (('mutant-logs', ('verilator', 'yosys')),
                                      ('mutant013-logs', ('yosys',)),
                                      ('vivado-mutant-logs', ('xsim', 'synth'))):
                path = HERE / 'head' / folder / (arm.name.replace(':', '-') + '.log')
                text = path.read_text()
                label = 'ELAB' if kind == 'tightened' else 'GUARD'
                for frontend in frontends:
                    if not re.search(rf'^FAIL: {label}\s+{frontend}\s+{re.escape(guard.name)}\s', text, re.M):
                        raise RuntimeError(f'{arm.name}: no {frontend} named failure in {folder}')
                    failures.append(frontend)
            side = 1 if kind == 'tightened' else 2
            terms = '; '.join(f'`{term[side]}`' for term in mutants.BOUNDARIES[guard.name])
            columns.append(f'{terms}; `{arm.name}`: 5/5 (`FAIL: {label}`)')
        rows.append('| ' + ' | '.join(map(cell, [guard.name, '; '.join(f'`{term[0]}`' for term in mutants.BOUNDARIES[guard.name]), *columns])) + ' |')
    (DEST / 'boundary-mutants.md').write_text('\n'.join(rows) + '\n')


def main() -> None:
    """Copy text receipts, retaining only hashes and sizes for large files."""
    DEST.mkdir(parents=True, exist_ok=True)
    manifest = []
    for folder in ('base', 'head', 'probes'):
        for path in sorted((HERE / folder).rglob('*')):
            if not path.is_file() or path.suffix not in ('.log', '.rc', '.seconds', '.cmd'):
                continue
            rel = path.relative_to(HERE)
            raw = path.read_bytes()
            entry = {'path': str(rel), 'raw_bytes': len(raw), 'raw_sha256': hashlib.sha256(raw).hexdigest()}
            if len(raw) <= 200000:
                body = clean(raw.decode('utf-8', errors='replace')).encode()
                dest = DEST / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(body)
                entry.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
            else:
                entry['disposition'] = 'size and digest only'
            manifest.append(entry)
    for name in ('identities.txt', 'identity.txt', 'record.py', 'publish.py'):
        (DEST / name).write_text(clean((HERE / name).read_text()))
    encoded = json.dumps(manifest, separators=(',', ':')) + '\n'
    if len(encoded.encode()) > 200000:
        raise RuntimeError('receipt manifest exceeds the publication size limit')
    (DEST / 'MANIFEST.json').write_text(encoded)
    tables()
    print(f'Published {len(manifest)} receipts and both 31-guard tables')


if __name__ == '__main__':
    main()
