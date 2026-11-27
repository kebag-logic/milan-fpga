"""Round 10: the link-rate census's primary observations as numbered, hash-bound, redacted text receipts."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('$SOURCE')
OLD = Path('$VALIDATION_STORAGE/r10')
OUT = Path('$LANE_TOOLS/artysplit-a829/round10/full-packet')
HEAD = '7bc47c0ee'  # replaced below by the full SHA of the census build head
HEAD = subprocess.check_output(['git', 'rev-parse', HEAD], cwd=ROOT, text=True).strip()
MERGE = HEAD
sys.path[:0] = [str(ROOT / 'tb/verilator/ctrl_service_budget'), '$LANE_TOOLS']
import privacy


def sha(data):
    return hashlib.sha256(data).hexdigest()


def scrub(data):
    data = data.replace(str(ROOT).encode(), b'$SOURCE').replace(str(OLD.parent).encode(), b'$VALIDATION_STORAGE')
    data = data.replace(b'$TOOLCHAIN', b'$TOOLCHAIN').replace(b'$SHARED_STORAGE', b'$SHARED_STORAGE')
    data = data.replace(b'$LANE_TOOLS', b'$LANE_TOOLS')
    data = data.replace(b'$HOME', b'$HOME')
    data = re.sub(rb'(?m)^(\|?\s*Host\s*:) .*$', rb'\1 <build-host>', data)
    return privacy.scrub_redact(data)


def parts(directory, name, data):
    directory.mkdir(parents=True, exist_ok=True)
    records, start = [], 0
    while start < len(data) or not records:
        end = min(start + 180_000, len(data))
        if end < len(data):
            cut = data.rfind(b'\n', start, end)
            if cut >= start:
                end = cut + 1
        piece = data[start:end]
        path = directory / (name if start == 0 and end == len(data) else f'{name}.part{len(records)+1:04d}.txt')
        path.write_bytes(piece)
        records.append(dict(file=path.name, bytes=len(piece), sha256=sha(piece)))
        start = end
        if not data:
            break
    return dict(bytes=len(data), sha256=sha(data), parts=records)


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1) + '\n')
    assert path.stat().st_size < 190_000, path


def timing():
    records = []
    grading = json.loads((OLD / 'images/graded-images.json').read_text())
    expected = {r['directive'] + '/' + Path(c['report']['path']).name: c['report']['sha256']
                for r in grading['candidates'] for c in r['corners']}
    for directive in ('ExtraTimingOpt', 'AltSpreadLogic_high', 'ExtraPostPlacementOpt'):
        for corner in ('Slow_0C', 'Slow_85C', 'Fast_0C', 'Fast_85C'):
            source = OLD / 'images' / directive / 'gateware' / f'digilent_arty_signoff_{corner}_timing.rpt'
            raw = source.read_bytes()
            assert sha(raw) == expected[directive + '/' + source.name]
            directory = OUT / 'timing-r7' / directive
            record = dict(original_bytes=len(raw), original_sha256=sha(raw),
                          published=parts(directory, source.name, scrub(raw)), source_head=MERGE)
            path = directory / (source.name + '.manifest.json')
            write(path, record)
            records.append(dict(manifest=str(path.relative_to(OUT)), sha256=sha(path.read_bytes())))
        for extra in ('digilent_arty_utilization_place.rpt', 'digilent_arty_signoff_check_timing.rpt'):
            source = OLD / 'images' / directive / 'gateware' / extra
            raw = source.read_bytes()
            record = dict(original_bytes=len(raw), original_sha256=sha(raw),
                          published=parts(OUT / 'timing-r7' / directive, extra, scrub(raw)), source_head=MERGE)
            write(OUT / 'timing-r7' / directive / (extra + '.manifest.json'), record)
    graded = scrub((OLD / 'images/graded-images.json').read_bytes())
    parts(OUT / 'timing-r7', 'graded-images.json', graded)
    write(OUT / 'timing-r7.json', records)


VALIDATION = []  # set from the round's receipts list (validation-list.json) at pack time


def validation():
    rows = []
    for name in VALIDATION or json.loads((OLD / 'validation-list.json').read_text()):
        source = OLD / name
        raw = source.read_bytes()
        label = name.replace('/', '-')
        record = dict(original_bytes=len(raw), original_sha256=sha(raw), published=parts(OUT / 'validation', label, scrub(raw)))
        rows.append(dict(name=label, **record))
    write(OUT / 'validation/manifest.json', rows)


def source():
    after = subprocess.check_output(['git', 'log', '-p', '575118facfe226054fe3339878712a3e77bd73ab..HEAD'], cwd=ROOT)
    parts(OUT / 'source', 'round10-commits.patch', after)
    for script in sorted(list(OLD.glob('*.py')) + list(OLD.glob('*.sh')) + sorted((OLD / 'tools').glob('*.py'))):
        parts(OUT / 'recipes', script.name + '.txt', scrub(script.read_bytes()))


def preview():
    """The derivation: round 10's census of costs, merged with round 9's maxima, and the rule's model."""
    rows = []
    for path in (OLD / 'derive/census.json', OLD / 'derive/merged-census.json', OLD / 'derive/derived-model.json',
                 Path('$VALIDATION_STORAGE/r9/derive/merged-census.json')):
        raw = path.read_bytes()
        name = ('round9-' if '/r9/' in str(path) else '') + path.name
        rows.append(dict(name=name, original_bytes=len(raw), original_sha256=sha(raw),
                         published=parts(OUT / 'derivation', name, scrub(raw))))
    write(OUT / 'derivation/manifest.json', rows)


def census():
    import collections
    import dataclasses
    import run
    import scenario
    cases = []
    completed = json.loads((OLD / 'final-census/completed.json').read_text())
    expected = {(r['variant'], r['group']): r['trace_sha256'] for r in completed}
    for directory in sorted((OLD / 'final-census').iterdir()):
        if not (directory / 'build.json').is_file():
            continue
        spec = json.loads((directory / 'build.json').read_text())
        groups = {g.name: g for g in run.all_groups(scenario.point('arty-1x1', spec), spec)}
        for log in sorted((directory / 'results').glob('*.log')):
            name = directory.name + '/' + log.stem
            target = OUT / 'census' / directory.name / log.stem
            group = groups[log.stem]
            original_hash, original_bytes, kept, omitted = hashlib.sha256(), 0, bytearray(), collections.Counter()
            with log.open('rb') as stream:
                for line in stream:
                    original_hash.update(line)
                    original_bytes += len(line)
                    kind = line.split(maxsplit=1)[0] if line.strip() else b''
                    if kind in (b'PC', b'FETCH', b'REPLY', b'FLASH') or not kind:  # TXREADY kept: egress_mii reads holds
                        omitted[kind.decode()] += 1
                    else:
                        kept.extend(line)
            assert original_hash.hexdigest() == expected[directory.name, log.stem]
            group_record = parts(target, 'scenario.json', json.dumps(dataclasses.asdict(group), indent=1).encode() + b'\n')
            manifest = dict(case=name, group=group_record, sys_hz=spec['sys_hz'], cpu_hz=spec['cpu_hz'], shape=[1, 1, 2],
                            native_status=int(log.with_suffix('.status').read_text()),
                            full_log=dict(bytes=original_bytes, sha256=original_hash.hexdigest()),
                            omitted=dict(omitted), executable_sha256=spec['executable_sha256'],
                            firmware_sha256=sha(Path(spec['elf']).read_bytes()),
                            extract=parts(target, 'observations.log', bytes(kept)),
                            grade=parts(target, 'original-grade.json', log.with_suffix('.json').read_bytes()),
                            stimulus=parts(target, 'stimulus.txt', log.with_suffix('.txt').read_bytes()))
            if group.save.get('journal'):
                journal = run.journal_of(directory / 'results', group)
                manifest['journal'] = parts(target, 'journal.hex.txt', journal.read_bytes().hex().encode() + b'\n')
            write(target / 'manifest.json', manifest)
            cases.append(dict(case=name, manifest=str((target / 'manifest.json').relative_to(OUT)),
                              sha256=sha((target / 'manifest.json').read_bytes())))
            print('PACKED', name, original_bytes, len(kept), flush=True)
    assert len(cases) == 159
    write(OUT / 'census.json', dict(source_head=HEAD, cases=cases))
    summaries = []
    for source in sorted((OLD / 'final-census').glob('*.log')):
        if source.name.endswith('-build.log'):
            continue
        summaries.append(dict(name=source.name, receipt=parts(OUT / 'qualification', source.name, scrub(source.read_bytes()))))
    for name in ('qualification.json', 'derived-model.json', 'census.json', 'merged-census.json'):
        source = OLD / 'final-census' / name
        summaries.append(dict(name=name, receipt=parts(OUT / 'qualification', name, scrub(source.read_bytes()))))
    write(OUT / 'qualification/manifest.json', summaries)
    (OUT / 'published-qualification.json').write_bytes(scrub((OLD / 'final-census/qualification.json').read_bytes()))


if __name__ == '__main__':
    for step in sys.argv[1:] or ['validation', 'source', 'preview', 'census']:
        globals()[step]()
        print('PACKED', step, flush=True)
