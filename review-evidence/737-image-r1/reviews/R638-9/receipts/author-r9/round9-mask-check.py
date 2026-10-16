"""Digest generated texts under the /tmp mask alone and with job-written checkout paths masked (scratch).

Usage: mask_check2.py LOGDIR...   (checkout presence approximated by the tracked files of the lane head at /work)
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path, PurePosixPath
lane = '$LANES/737-image'
files = subprocess.run(['git', '-C', lane, 'ls-files', '--recurse-submodules'], capture_output=True, text=True,
                       check=True).stdout.split('\n')
present = set()
for f in filter(None, files):
    path = PurePosixPath('/work') / f
    present.add(str(path))
    present.update(str(p) for p in path.parents)
NAME = '[A-Za-z0-9_.-]'
COMPONENT = rf'/(?!\.\.?(?!{NAME})){NAME}+'
reviewed = json.load(open(f'{lane}/ci/image/exec-audit.json'))['generated_programs']


def tmp_mask(data, scratch):
    roots = '|'.join(re.escape(r) for r in ('/tmp', *scratch))
    return re.sub(rf'(?:{roots})(?!{NAME})(?:{COMPONENT})*'.encode(), b'/tmp/<job>', data)


def written(match):
    path = match.group(0).decode()
    if path in present:
        return match.group(0)
    parts = path.split('/')
    for cut in range(len(parts) - 1, 1, -1):
        if '/'.join(parts[:cut]) in present:
            return ('/'.join(parts[:cut]) + '/<job>').encode()
    return b'/work/<job>'


def checkout_mask(data):
    return re.sub(rf'/work(?:{COMPONENT})+'.encode(), written, data)


changed, used, total = [], set(), 0
for d in sys.argv[1:]:
    for log in sorted(Path(d).glob('step-*.jsonl')):
        for line in log.open():
            i = json.loads(line)
            if i.get('provenance') not in ('generated', 'none') or 'text' not in i:
                continue
            scratch = tuple(dict.fromkeys(re.findall(r'/out/scratch/job-[^/ ]+', json.dumps(i))))
            base = tmp_mask(i['text'].encode('utf-8', 'surrogateescape'), scratch)
            a, b = hashlib.sha256(base).hexdigest(), hashlib.sha256(checkout_mask(base)).hexdigest()
            total += 1
            if a in reviewed:
                used.add(a)
                if a != b:
                    changed.append((log.name, i['argv'][:2]))
print('instances', total, 'reviewed digests seen', len(used), 'reviewed digests that would change', len(changed), changed[:4])
