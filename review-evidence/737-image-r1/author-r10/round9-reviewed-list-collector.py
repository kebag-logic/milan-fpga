"""Collect every unprovenanced interpreter program from traced step logs, identified as the round-nine audit
identifies it: inline and streamed texts and job-written scripts by their masked digest (scratch).

Usage: unpinned9.py OUTPUT.json CLONE LOGDIR...
Each entry: digest -> kind, interpreter, names, paths, steps, count, and the masked text.
"""
import collections, hashlib, json, re, subprocess, sys
from pathlib import Path, PurePosixPath
sys.path.insert(0, '$LANES/737-image/ci/image')
import exec_audit

CHECKOUT = '/work'


def masker(clone: str):
    """An Origin carrying only what masking reads, for the clone's tracked files at /work (the audit's own code)."""
    files = subprocess.run(['git', '-C', clone, 'ls-files', '--recurse-submodules'], capture_output=True, text=True,
                           check=True).stdout.split('\n')
    origin = object.__new__(exec_audit.Origin)
    origin.root = Path(CHECKOUT)
    origin.present = {CHECKOUT}
    for name in filter(None, files):
        path = PurePosixPath(CHECKOUT) / name
        origin.present |= {str(path), *map(str, path.parents)}
    origin.written = re.compile(rf"{exec_audit.WORD}{re.escape(CHECKOUT)}(?:{exec_audit.COMPONENT})+".encode())
    return origin


def mask(origin, data: bytes, scratch: tuple) -> str:
    """The audit's masked digest, with this instance's job scratch roots."""
    roots = '|'.join(re.escape(r) for r in ('/tmp', *scratch))
    origin.temporary = re.compile(rf"{exec_audit.WORD}(?:{roots})(?![A-Za-z0-9_.-])(?:{exec_audit.COMPONENT})*".encode())
    return origin.masked(data), origin.written.sub(origin.held, origin.temporary.sub(b'/tmp/<job>', data))


ORIGIN = masker(sys.argv[2])
out, other = {}, collections.Counter()
for directory in sys.argv[3:]:
    for log in sorted(Path(directory).glob('step-*.jsonl')):
        for line in log.read_text().splitlines():
            instance = json.loads(line)
            provenance = instance.get('provenance')
            if provenance not in ('none', 'unreadable', 'not a file on a path', 'checkout file changed before it ran',
                                  'refused'):
                continue
            what = exec_audit.invocation(instance)
            if provenance != 'none':
                other[(provenance, what['kind'], what['name'], what['path'], what.get('reason'))] += 1
                continue
            scratch = tuple(dict.fromkeys(re.findall(r'/out/scratch/job-[^/ ]+', json.dumps(instance))))
            text = what.get('text') if what['kind'] == 'inline' else instance.get('text')
            if text is None:
                other[('no text', what['kind'], what['name'], what['path'], None)] += 1
                continue
            digest, masked = mask(ORIGIN, str(text).encode('utf-8', 'surrogateescape'), scratch)
            assert hashlib.sha256(masked).hexdigest() == digest
            entry = out.setdefault(digest, {'kind': what['kind'], 'interpreter': what.get('family') or 'program',
                                            'program': Path(instance['program']).name, 'names': [], 'paths': [],
                                            'steps': [], 'count': 0, 'text': masked.decode('utf-8', 'surrogateescape')})
            entry['count'] += 1
            for key, value in (('names', what['name']), ('paths', what['path']),
                               ('steps', f'{Path(directory).name}/{log.name}')):
                if value not in entry[key] and len(entry[key]) < 6:
                    entry[key].append(value)
Path(sys.argv[1]).write_text(json.dumps(out, indent=1, sort_keys=True))
print('distinct', len(out), dict(collections.Counter((e['kind'], e['interpreter']) for e in out.values())))
for key, count in other.most_common():
    print('OTHER', count, key)
