"""Audit immutable public measurements; this does not run a simulation."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / 'public' / 'R239-1'
REF = '7795e487048867fde07a224ec1a5885acfb4375b'
PREFIX = 'review-evidence/372-r1/review/R239-1/'
argv = ['rtk', 'proxy', 'gh', 'api', f'repos/kebag-logic/milan-fpga/git/trees/{REF}?recursive=1']
result = subprocess.run(argv, capture_output=True, check=False)
assert result.returncode == 0, result.stderr.decode()
tree = json.loads(result.stdout)
assert not tree['truncated']
entries = {row['path'][len(PREFIX):]: row for row in tree['tree'] if row['path'].startswith(PREFIX)}
downloaded = []
for path in sorted(PUBLIC.rglob('*')):
    if not path.is_file():
        continue
    name = path.relative_to(PUBLIC).as_posix()
    raw = path.read_bytes()
    oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    assert entries[name]['sha'] == oid, name
    downloaded.append({'path': name, 'git_blob': oid, 'sha256': hashlib.sha256(raw).hexdigest()})
reset = (PUBLIC / 'raw/probe-reset-R1.log').read_text()
reset_lines = reset.splitlines()
selected = [{'line': i + 1, 'text': line} for i, line in enumerate(reset_lines) if 104 <= i + 1 <= 123]
assert 'edge  9 RESET edge, s0 still offering beat1' in reset
assert 'edge 10 pass-action TOP.axis_mux_rr_2in_1out.u_sva.u_s0_stimulus.ap_tvalid_held_until_handshake flag=0' in reset
assert 'edge 10 pass-action TOP.axis_mux_rr_2in_1out.u_sva.u_m_dut.ap_tvalid_held_until_handshake flag=0' in reset
past = (PUBLIC / 'raw/pastprobe-run.log').read_text()
assert 'PROBE ap_past_is_initial FAILED at 5' in past
assert 'PROBE ap_stable_initial FAILED at 5' in past
summary = (PUBLIC / 'raw/pastprobe-summary.txt').read_text()
assert 'build exit=0\nrun exit=0\n' in summary
groups = []
rows = []
for line in (PUBLIC / 'raw/focused-witness-and-tallies.txt').read_text().splitlines():
    match = re.fullmatch(r'witness (\S+)\s+nonvacuous=(\d+) harness=(\d+) \(([^)]+)\)', line)
    if match:
        name, seen, port, relation = match.groups()
        rows.append({'name': name, 'nonvacuous': int(seen), 'harness': int(port), 'relation': relation})
    tally = re.fullmatch(r'== ptp_ts mux sva w(8|64): checks: (\d+)\s+failures: (\d+) ==', line)
    if tally:
        width, checks, failures = map(int, tally.groups())
        relations = dict(Counter(row['relation'] for row in rows))
        assert relations == {'equal': 15, 'at least': 2, 'both above zero': 4}
        groups.append({'width': width, 'checks': checks, 'failures': failures, 'relations': relations, 'rows': rows})
        rows = []
assert len(groups) == 2
tool = Path('$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator')
selector_sha = hashlib.sha256(tool.read_bytes()).hexdigest()
assert selector_sha == '905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f'
receipt = {
    'attribution': 'Unchanged R239-1 public measurements at source 60c5225fe5f93209bf313c51b7a722f25f9aaa7d, pinned Verilator 5.050. No probe, positive harness or campaign was rerun by A175.',
    'evidence_commit': REF, 'tree_fetch_argv': argv, 'tree_fetch_exit': result.returncode,
    'downloaded_git_blob_matches': downloaded,
    'reset_R1_lines': selected,
    'pastprobe_recorded_build_exit': 0, 'pastprobe_recorded_run_exit': 0,
    'pastprobe_log': past, 'witness_groups': groups,
    'tool_selector_sha256': selector_sha,
    'upstream_changelog_receipt': (PUBLIC / 'raw/verilator-v5.050-Changes.txt').read_text(),
    'original_changelog_digest_is_not_receipt_digest': True,
}
(ROOT / 'public-measurement-audit.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(f'{len(downloaded)} public files match Git blobs at immutable evidence commit {REF}.')
print('R239 R1: reset edge 9, s0 stalled; edge 10 s0/m TVALID pass actions flag=0.')
print('R239 pastprobe: build/run exits 0; declared constant one=1; first-edge past/stable checks report failure at time 5.')
for group in groups:
    print({key: value for key, value in group.items() if key != 'rows'})
print(f'Supplied selector digest matches the public tool receipt: {selector_sha}')
print('No new tool-semantic result, simulation execution, or formal result is claimed.')
