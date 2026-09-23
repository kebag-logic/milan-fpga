#!/usr/bin/env python3
"""Read-only receipts that need the review clone, the pinned archive and (for
the GitHub ones) the public API through an authenticated `gh` CLI.

usage: misc_checks.py CLONE_AT_HEAD EVIDENCE_ROOT OUTDIR
"""
import sys, os, re, json, subprocess, statistics, difflib, hashlib, datetime
clone, root, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
REPO = 'kebag-logic/milan-fpga'
HEAD = 'f547a49bee5966a901d1e11981eb4dc94d038711'
BASE = 'ede8d48ecd7c7f589a14b957951f040d92c99c70'


def gh(*a):
    return json.loads(subprocess.run(['gh', 'api', '--paginate', *a], capture_output=True, check=True).stdout)


def w(name, lines):
    with open(os.path.join(out, name), 'w') as f:
        f.write('\n'.join(lines) + '\n')


# identity gate: reference CRC table, on-board readback, grader, grader hash
L = []
exp = open(os.path.join(root, 'bench-a200/identity/expected-crc.txt')).read()
L.append('reference CRC table byte-identical in both packets: %s' % (
    exp == open(os.path.join(root, 'bench-a202/identity/expected-crc.txt')).read()))
asl = exp.split('== build_ax7101_asl_tdm8devede8d48e')[1].split('==')[0]
L.append('asl row: ' + ' '.join(re.findall(r'(rom|bitpay|aem|bitfile)\s+len=\s*(\d+) crc32=([0-9a-f]+)', asl).__str__().split()))
for pk in ('bench-a200', 'bench-a202'):
    t = open(os.path.join(root, pk, 'identity/console-identity.txt'), encoding='latin-1').read()
    L.append('%s on-board CRC32 %s VERSION %s' % (pk, sorted(set(re.findall(r'CRC32: ([0-9a-f]{8})', t))),
                                                sorted(set(re.findall(r'VERSION=([0-9a-f]+)', t)))))
    g = open(os.path.join(root, pk, 'identity/uart-smoke-identity.log')).read().strip().splitlines()[-1]
    L.append('%s grader: %s' % (pk, g))
blob = subprocess.run(['git', '-C', clone, 'show', BASE + ':scripts/baremetal_uart_smoke.py'], capture_output=True, check=True).stdout
L.append('grader sha256 at %s: %s' % (BASE[:8], hashlib.sha256(blob).hexdigest()))
# the page's peer firmware-field hash, recomputed from the published ENTITY
# READ_DESCRIPTOR payload (4-octet configuration prefix, firmware_version at
# descriptor offset 116, 64 octets); only the hash and the octet count print
pl = json.loads(open(os.path.join(root, 'bench-a200/bench/peer-aem-1.jsonl')).read().splitlines()[1])['payload']
fw = bytes.fromhex(pl)[4 + 116:4 + 180]
L.append('peer ENTITY firmware_version field: sha256 %s, %d non-zero octets' % (hashlib.sha256(fw).hexdigest(), len(fw.rstrip(b'\0'))))
w('identity_gate_check.txt', L)

# register rows the page decodes
L = []
for i, l in enumerate(open(os.path.join(clone, 'docs/reference/REGISTER_MAP.md')).read().splitlines(), 1):
    if re.match(r'\|\s*`(0x(?:77C|750|764|774|780|720|7F0|624|628|62C|730|734|6E4))`\s*\|\s*`[A-Z]', l):
        c = [x.strip() for x in l.split('|')]
        L.append('L%d %s %s %s :: %s' % (i, c[1], c[2], c[3], ' | '.join(c[4:])[:420]))
w('register_rows.txt', L)

# tool files published redacted versus the page's tool-revision paragraph
m = json.load(open(os.path.join(root, 'MANIFEST.json')))
page = open(os.path.join(clone, 'docs/findings/117_GPTP_SILICON_EVIDENCE.md')).read().splitlines()
quoted = set(p for l in page for p in re.findall(r'`([0-9a-f]{8})\.\.\.`', l))
tools = [e for e in m if '/tools/' in e['file']]
red = [e for e in tools if e['original_sha256'] != e['published_sha256']]
L = ['packet tool files at the pinned commit: %d; published redacted: %d' % (len(tools), len(red))]
for e in red:
    p = e['original_sha256'][:8]
    L.append('  %-40s as-run %s published %s quoted-on-page=%s identity_redacted=%s' % (
        e['file'], p, e['published_sha256'][:8], p in quoted, bool(e.get('identity_redacted'))))
L += ['page L%d: %s' % (i, page[i - 1]) for i in range(216, 228)]
w('tool_redaction_vs_page.txt', L)

# steady state (step 2/4) and step 5
L = []
def status(p):
    t = open(p, encoding='latin-1').read()
    return [dict(re.findall(r'(\w+)=([0-9a-fA-Fx]+)', x)) for x in re.findall(r"cmd='milan_status'.*?\n(.*?)litex", t, flags=re.S)]
tot, pd = 0, []
for name, p in (('runA', 'bench/runA/console.txt'), ('runB', 'bench/runB/console.txt'),
                ('identity', 'identity/console-identity.txt'), ('final', 'bench/final/console-final.txt')):
    S = status(os.path.join(root, 'bench-a200', p))
    ok = all(s.get('SYNC') == '1' and s.get('ASCAPABLE') == '1' and s.get('TU') == '0' for s in S)
    pd += [int(s['PDELAY_NS']) for s in S if 'PDELAY_NS' in s and name != 'identity']
    L.append('%s milan_status samples %d, all SYNC=1 ASCAPABLE=1 TU=0 %s, GM %s, CLKV_STAT %s' % (
        name, len(S), ok, sorted(set(s.get('GPTP_GM') for s in S)), sorted(set(s.get('CLKV_STAT') for s in S))))
    tot += len(S)
L.append('total samples %d; console PDELAY_NS min %d max %d median %s' % (tot, min(pd), max(pd), statistics.median(pd)))
W = [json.loads(l) for l in open(os.path.join(root, 'bench-a200/bench/runA/pw1-watch.jsonl'))]
ai = [x for x in W if x.get('cmd') == 'GET_AVB_INFO' and x.get('target') == '020000fffe000001']
L.append('Run A GET_AVB_INFO DUT polls %d, AS_CAPABLE all %s, flags %s, propagation delay %d..%d median %s' % (
    len(ai), all(x['decoded']['as_capable'] == 1 for x in ai), sorted(set(x['decoded']['flags'] for x in ai)),
    min(x['decoded']['pdelay_ns'] for x in ai), max(x['decoded']['pdelay_ns'] for x in ai),
    statistics.median(x['decoded']['pdelay_ns'] for x in ai)))
rc = os.path.join(root, 'bench-a200/bench/runC')
a = open(os.path.join(rc, 'counters-probe-020000fffe000001.log')).read().splitlines()
b = open(os.path.join(rc, 'counters-probe-3cc0c60102030000.log')).read().splitlines()
norm = lambda X: [re.sub(r'0x[0-9a-fA-F]{16}|[0-9a-f]{16}', '<EID>', re.sub(r'\d{2}:\d{2}:\d{2}[.\d]*', '<T>', x)) for x in X]
d = [x for x in difflib.unified_diff(norm(a), norm(b), lineterm='', n=0) if not x.startswith(('---', '+++', '@@'))]
L.append('counters probe transcripts: %d and %d lines; differing after masking entity ids and times: %d' % (len(a), len(b), len(d)))
e = open(os.path.join(rc, 'a200-enum.log'), encoding='latin-1').read()
for pat in ('5.3.8.10', 'Milan mandatory counters missing for STREAM_INPUT', 'Entity not fully Milan compliant',
            'flags=IEEE17221 ', 'flags=IEEE17221|Milan'):
    L.append('enumeration log contains %-52r %d' % (pat, e.count(pat)))
w('rederive_steps4_5.txt', L)

# GitHub-side receipts
L = []
c117 = {x['id']: x['body'] for x in gh('repos/%s/issues/117/comments' % REPO)}
for cid, vals in ((5794859125, ['f0725eef7a361bd7dc6d692c369868f25e5d4f49f6b7267562a0b5f949ada33d',
                                '9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404',
                                '71e798fc401ed3fbaac4cd43a299f23498beafa466aaa17d6773590a62fa93e2']),
                  (5584039577, ['95d64fd5', 'ad579e18', '0e9faf30', '8ef4b008'])):
    for v in vals:
        full = re.findall(r'\b' + v + r'[0-9a-f]*\b', c117[cid])
        L.append('issue comment %d: %s %s' % (cid, v[:8], ('present, %d hex' % len(full[0])) if full else 'ABSENT'))
L.append('comments carrying a full 64-hex value starting 8ef4b008: %d' % sum(
    1 for b in c117.values() if re.search(r'\b8ef4b008[0-9a-f]{56}\b', b)))
pre = [(cid, len(m_.group())) for cid, b in c117.items() for m_ in re.finditer(r'33f0e7f9[0-9a-f]*', b)]
L.append('peer firmware-field hash occurrences (comment, hex length): %s' % pre)
b14 = c117[5670665596]
L.append('2026-09-14 report fields published as hash prefixes: %s' % sorted(set(re.findall(r'"([a-z_]+)":\s*\{[^{}]*?"sha256_8"', b14))))
w('external_hash_sources.txt', L)

L = []
for n in (495, 529, 530):
    i = gh('repos/%s/issues/%d' % (REPO, n))
    cs = gh('repos/%s/issues/%d/comments' % (REPO, n))
    L.append('#%d %s: %s (%d comments)' % (n, i['state'], i['title'][:90], len(cs)))
    for x in cs:
        if n == 495 and '#117 silicon run' in x['body']:
            L += ['   ' + l for l in x['body'].splitlines()]
        if n == 530 and ('item 9' in x['body'] or 'items 1' in x['body']):
            L.append('   comment %d mentions item 9: %s' % (x['id'], 'item 9' in x['body']))
w('verify_followup_tracking.txt', L)

pr = json.loads(subprocess.run(['gh', 'pr', 'view', '531', '--repo', REPO, '--json', 'body,headRefOid'], capture_output=True, check=True).stdout)
tpl = open(os.path.join(clone, '.github/PULL_REQUEST_TEMPLATE.md')).read()
L = ['PR #531 head %s' % pr['headRefOid']]
for s in re.findall(r'^## (.+)$', tpl, flags=re.M):
    L.append('template section %-36s present=%s' % (s, bool(re.search(r'^#+\s*' + re.escape(s), pr['body'], flags=re.M))))
L += ['--- body ---', pr['body']]
w('pr_body_template_check.txt', L)
prs = json.loads(subprocess.run(['gh', 'pr', 'list', '--repo', REPO, '--state', 'merged', '--limit', '40', '--json', 'number,title,body'],
                                capture_output=True, check=True).stdout)
w('merged_pr_template_practice.tsv', ['%d\t%s\t%s\t%s' % (p['number'], p['title'][:70], '## Status' in p['body'], 'How to validate' in p['body']) for p in prs])

runs = gh('repos/%s/commits/%s/check-runs?per_page=100' % (REPO, HEAD))['check_runs']
L = ['read at %s - check runs at %s: %d' % (datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), HEAD[:8], len(runs))]
L += ['%-36s status=%-11s conclusion=%-9s id=%s' % (r['name'], r['status'], r['conclusion'], r['id']) for r in sorted(runs, key=lambda r: r['name'])]
names = {r['name']: r for r in runs}
for q in ('rtl-fast', 'docs-check', 'wire-accountability', 'docs-check-no-git', 'elaborate', 'verilator-suites', 'yosys-portability'):
    r = names.get(q)
    L.append('required %-20s %s' % (q, 'ABSENT' if not r else '%s/%s' % (r['status'], r['conclusion'])))
w('hosted_checks_head.txt', L)
if 'docs-check' in names:
    j = gh('repos/%s/actions/jobs/%d' % (REPO, names['docs-check']['id']))
    L = ['job %d %s %s head_sha %s' % (j['id'], j['status'], j['conclusion'], j['head_sha'])]
    from collections import Counter
    L.append('step conclusions %s' % dict(Counter(s['conclusion'] for s in j['steps'])))
    L += ['  step %d %s %s' % (s['number'], s['name'], s['conclusion']) for s in j['steps']]
    w('hosted_docs_check_steps.txt', L)
print('misc_checks: done')
