"""Collect every unprovenanced interpreter program, script and program from traced step logs (scratch).

Usage: unpinned.py OUTPUT.json LOGDIR...
Each entry: digest -> kind, interpreter, names, paths, steps, count, and the text for inline/stream programs.
"""
import collections, json, sys
from pathlib import Path
sys.path.insert(0, '$LANES/737-image/ci/image')
import exec_audit
from exec_operands import EXEC_ONLY

out = {}
other = collections.Counter()
for directory in sys.argv[2:]:
    for log in sorted(Path(directory).glob('step-*.jsonl')):
        for line in log.read_text().splitlines():
            instance = json.loads(line)
            provenance = instance.get('provenance')
            if provenance not in ('none', 'unreadable', 'not a file on a path', 'checkout file changed before it ran'):
                continue
            what = exec_audit.invocation(instance)
            if provenance != 'none':
                other[(provenance, what['kind'], what['name'], what['path'])] += 1
                continue
            digest = what.get('sha256') if what['kind'] in ('inline', 'stream') else \
                (instance.get('sha256_masked') or instance.get('sha256'))
            entry = out.setdefault(digest, {'kind': what['kind'], 'interpreter': what.get('family') or 'program',
                                            'program': Path(instance['program']).name, 'names': [], 'paths': [],
                                            'steps': [], 'count': 0})
            entry['count'] += 1
            for key, value in (('names', what['name']), ('paths', what['path']), ('steps', f'{Path(directory).name}/{log.name}')):
                if value not in entry[key] and len(entry[key]) < 6:
                    entry[key].append(value)
            if what['kind'] == 'inline' and 'text' not in entry:
                read = exec_audit.operands(what['family'], instance['argv'])
                entry['text'] = read.get('text')
            if what['kind'] in ('stream', 'script') and 'text' not in entry:
                entry['text'] = instance.get('text')
Path(sys.argv[1]).write_text(json.dumps(out, indent=1, sort_keys=True))
kinds = collections.Counter((e['kind'], e['interpreter']) for e in out.values())
print('distinct', len(out), dict(kinds))
for k, v in other.most_common():
    print('OTHER', v, k)
