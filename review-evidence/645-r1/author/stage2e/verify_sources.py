import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--candidate', type=Path, required=True)
parser.add_argument('--candidate-route', type=Path, required=True)
parser.add_argument('--evidence', type=Path, required=True)
args = parser.parse_args()
comparison = json.loads((args.evidence / 'source-comparison.json').read_text())
old_comment = b'//! queues (depth 8 = one PDU + margin) popped one event per media tick -'
new_comment = b'//! queues (depth 16 = one PDU + margin) popped one event per media tick -'


def resolve(name, repo, route):
    resolved = Path(name.replace('$REPO', str(repo)).replace('$WORK', str(route))
                    .replace('$HOME', str(Path.home())))
    if resolved.exists():
        return resolved
    for prefix, suffix in (('$REPO/configs/generated/', 'roms/'),
                           ('$REPO/sw/builder/out/', 'builder/')):
        if name.startswith(prefix):
            return route / (suffix + name.removeprefix(prefix))
    raise FileNotFoundError(name)


rows = []
for expected in comparison['source_files']:
    name = expected['path']
    base = resolve(name, args.work / 'base', args.work / 'route').read_bytes()
    candidate = resolve(name, args.candidate, args.candidate_route).read_bytes()
    base_hash = hashlib.sha256(base).hexdigest()
    candidate_hash = hashlib.sha256(candidate).hexdigest()
    assert base_hash == expected['base_sha256'], name
    assert candidate_hash == expected['candidate_sha256'], name
    prior_candidate = candidate
    if name == '$REPO/hdl/ieee1722/aaf/KL_chan_map_capture.sv':
        assert candidate.count(new_comment) == 1 and old_comment not in candidate
        prior_candidate = candidate.replace(new_comment, old_comment)
    prior_hash = hashlib.sha256(prior_candidate).hexdigest()
    assert prior_hash == expected['prior_candidate_sha256'], name
    rows.append({'path': name, 'base_bytes': len(base), 'base_sha256': base_hash,
                 'candidate_bytes': len(candidate), 'candidate_sha256': candidate_hash,
                 'matches_before_run': True, 'matches_prior_candidate_except_comment': True})
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.candidate,
                               text=True).strip()
base_head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.work / 'base',
                                    text=True).strip()
assert base_head == comparison['base_head']
assert len(rows) == 134
result = {'candidate_head': head, 'base_head': base_head, 'inputs_rechecked': len(rows),
          'all_match': True,
          'comment_normalization': 'Only the named depth comment is restored in memory '
                                   'to compare with the prior candidate hash.',
          'files': rows}
(args.evidence / 'final-source-verification.json').write_text(
    json.dumps(result, indent=2) + '\n')
print('PASS: all 134 base and candidate inputs match; only the ruled comment differs '
      'from the prior candidate input hashes')
