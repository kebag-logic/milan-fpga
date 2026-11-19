# receipts_spec.py: the round's receipts, run by receipts.py (keep, put, lines, run, S, L in scope).
import hashlib as _h
from pathlib import Path as _P

BASE, CODE, FIRST = '0839453f6d', '4224df639a', 'e5dee83b6d'

# --- the change
put('change/commits.txt', run('git', 'log', '--format=%H %s', f'{BASE}..HEAD', cwd=L))
put('change/diffstat.txt', run('git', 'diff', '--stat', BASE, 'HEAD', cwd=L))
put('change/firmware.diff', run('git', 'diff', BASE, 'HEAD', '--', 'sw/firmware/ctrl/srp/srp_mbx.c', cwd=L))
put('change/tests-and-plants.diff', run('git', 'diff', BASE, 'HEAD', '--', 'sw/firmware/ctrl/test', cwd=L))
put('change/docs.diff', run('git', 'diff', BASE, 'HEAD', '--', 'docs', 'sw/firmware/ctrl/srp/README.md',
                            'tb/verilator/ctrl_service_budget/README.md', cwd=L))
put('change/after-the-code-head.txt',
    f'# files changed after {CODE} (the code head every gate ran at): docs only\n' +
    run('git', 'diff', '--name-only', CODE, 'HEAD', cwd=L))

# --- tests: the restated tests, and the hold-off before #951 put back
for arm in sorted((S / 'fw/talker-head').glob('*.log')):
    keep(f'tests/restated-at-{FIRST[:8]}/{arm.name}', arm)
for arm in sorted((S / 'fw/talker-oldvalue').glob('*.log')):
    keep(f'tests/old-value-planted/{arm.name}', arm)
put('tests/old-value-planted/PLANT.diff', run('git', 'diff', cwd=S / 'clones/oldvalue'))
keep('tests/width-check-planted/PLANT.diff', S / 'fw/narrow-plant.diff')
keep('tests/width-check-planted/compile.txt', S / 'fw/narrow.log',
     lambda t: lines(r'error|held_cs|REFUSED', t, '# ctrl_srp_image.py at 1x1/1if on a scratch copy of 4224df63 with '
                                                  'held_cs planted uint8_t: refused at compile time\n'))

# --- gates, at the code head 4224df63 (and the first run at e5dee83b), condensed
GATE = (r'^(HEAD |END |suite verdicts|test_ctrl_firmware:|mutants:|planted|\[ok\]|\[FAIL\] mutant|ESCAPED|REFUSED|'
        r'== .*checks:|\s+verdict:|.*not caught|    named plants)')
for tag, unit in ((CODE[:8], 'fw-head2'), (FIRST[:8], 'fw-head')):
    for k in range(4):
        keep(f'gates/{tag}/firmware-gate-shard{k}.txt', S / f'units/{unit}-{k}.log',
             lambda t, k=k, tag=tag: lines(GATE, t, f'# test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 '
                                                    f'--shard {k}/4 on {tag}, condensed (verdicts, plant lines, '
                                                    f'result)\n'))
for tag, unit in ((CODE[:8], 'cov-head2'), (FIRST[:8], 'cov-head')):
    keep(f'gates/{tag}/fw-coverage.txt', S / f'units/{unit}.log')
TWIN = r'^(HEAD |== |END |twin:|twin rc|plant |\[LEDGER\]|\[OWED\]|\[DIFF\]|.*REFUSED|.*finding)'
for tag, unit in ((CODE[:8], 'twin-head2'), (FIRST[:8], 'twin-head')):
    keep(f'gates/{tag}/twin.txt', S / f'units/{unit}.log',
         lambda t, tag=tag: lines(TWIN, t, f'# make twin twin-plants twin-maps twin-maps-plants (tb/verilator/milan_dp) '
                                           f'on {tag}, condensed\n'))
BUILDER = r'^(HEAD |END |ALL GATES|.*DID NOT RUN|  - \[gate|\s*\[gate [0-9a-z]+\] [0-9]+ .* pass)'
for leg in (0, 1):
    for tag, unit in (('final', f'builder-final-{leg}'), (FIRST[:8], f'builder-{leg}')):
        p = S / f'units/{unit}.log'
        if p.is_file():
            keep(f'gates/{tag}/builder-leg-{leg}.txt', p, lambda t: lines(BUILDER, t))
p = S / 'units/builder-final-0-shared-clone.log'
if p.is_file():
    keep('gates/final/builder-leg-0-first-run-shared-clone.txt', p,
         lambda t: lines(BUILDER + r'|builder legs refused', t, '# leg 0\'s first run at 0d1eb8e4, in the clone the '
                         'docs steps ran in: refused at its end while check_entity_shape.py --self-test held a '
                         'planted control in tb/verilator/csr/Makefile; re-run in its own clone: builder-leg-0.txt\n'))
for tag, d in (('final', S / 'docs-steps/final'),):
    if (d / 'steps.txt').is_file():
        keep(f'gates/{tag}/docs-workflow-steps.txt', d / 'steps.txt')

# --- images
keep('images/SUMMARY.txt', S / 'cmp/all/SUMMARY.txt',
     lambda t: f'# the 20 image pairs, base {BASE[:8]} against head {FIRST[:8]}: differing inputs, sized sections, the '
               'relinks, the canonical listings\n' + t)
for f in sorted((S / 'cmp/all').glob('*.txt')):
    if f.name != 'SUMMARY.txt':
        keep(f'images/pairs/{f.name}', f)
put('images/budget-hashes.txt',
    '# the CPU budget harness images (point arm sha256)\n## base 0839453f, built here\n' +
    (S / 'img/budget-base/hashes.txt').read_text() + '## the train record at step 12 (0839453f)\n' +
    _P('<mgmt>/2026-09-23/train1117-a794/round5/receipts/step12c/images/hashes.txt').read_text()
    + f'## head {FIRST[:8]}\n' + (S / 'img/budget-head/hashes.txt').read_text() +
    f'## code head {CODE[:8]} (the width check added)\n' + (S / 'img/budget-head2/hashes.txt').read_text())
put('images/platform-and-fixture-hashes.txt',
    f'# the platform and size-fixture images (sha256 path)\n## {FIRST[:8]}\n' + (S / 'img/plat-head.hashes').read_text()
    + f'## {CODE[:8]}\n' + (S / 'img/plat-head2.hashes').read_text())
for t in ('base', 'head', 'head2'):
    keep(f'images/platform-ledger-{t}.txt', S / f'img/plat-{t}/plat_ledger.log',
         lambda x: lines(r'^(POINT|plat_ledger|LINK|KEY|TILES|LEDGER)', x))
for r, t in (('0839453f6d7135063e904bcaf4ac1852ad6b522a', 'base'), ('e5dee83b6d610a215adc5bac03c1dc4b543635df', 'head')):
    keep(f'images/release-{t}.sha256', S / f'img/release/{r}/IMAGES.sha256')
    keep(f'images/release-{t}-run.txt', S / f'img/release/{r}/RUN.txt')

# --- the CPU rows
for unit in sorted((S / 'units').glob('mr-*.log')):
    keep(f'cpu/legs/{unit.stem}.txt', unit,
         lambda t: ''.join(l + '\n' for l in t.splitlines() if not l.startswith('COMMAND ')))
for f in sorted((S / 'cmp/rows').glob('*.txt')):
    if f.name != '1x1-armA-probes.txt':
        keep(f'cpu/compare/{f.name}', f)
for f in sorted((S / 'cmp/graders').glob('*.log')):
    keep(f'cpu/graders/{f.name.replace(".py_", "-").replace("__", "-")}', f)
put('cpu/graders/SAME.txt', '# each grader\'s output on base 0839453f and on the code head 4224df63\n' + ''.join(
    f'{"IDENTICAL" if (S / "cmp/graders" / f"base-{n}").read_bytes() == (S / "cmp/graders" / f"head2-{n}").read_bytes() else "DIFFER"} {n}\n'
    for n in sorted(p.name[5:] for p in (S / 'cmp/graders').glob('base-*.log'))))
keep('cpu/control/PLANT.diff', S / 'fw/nop-control.diff')
keep('cpu/control/listing-head-against-control.txt', S / 'cmp/relink-nop-vs-head.txt')
ctl = S / 'meas/nop/8x8-1if/valid-destinations/regrade-loss/results.json'
if ctl.is_file():
    import json as _j
    ctl_rows = []
    for tag, p in (('base', S / 'meas/base/8x8-1if/valid-destinations/results/results.json'),
                   ('head', S / 'meas/head/8x8-1if/valid-destinations/results/results.json'),
                   ('control', ctl)):
        for g in _j.load(open(p))['results']:
            if g['group'] == 'srp-talker-loss':
                ctl_rows += [f'{tag} {q["probe"]} {q["ms"]:.3f}' for q in g['probes']]
    put('cpu/control/srp-talker-loss-probes.txt',
        '# srp-talker-loss at 8x8/1if: every probe (ms) on the base image, the head image and the control (the base\'s '
        'value with a nop after its store: the head\'s placement)\n' + '\n'.join(ctl_rows) + '\n')
keep('cpu/control/srp-talker-and-loss-probes.txt', S / 'cmp/control-probes.txt',
     lambda x: '# every probe (ms) of srp-talker and srp-talker-loss at 8x8/1if: the base image, the head image and '
               'the control (the base value with a nop after its store: the head placement)\n' + x)
keep('cpu/control/srp-talker-passes.txt', S / 'cmp/control-passes.txt')
buckets = S / 'cmp/buckets.txt'
if buckets.is_file():
    keep('cpu/control/passes-per-second.txt', buckets)
big = []
for f in sorted((S / 'meas').rglob('results/*.log')) + sorted((S / 'meas').rglob('regrade-loss/*.log')):
    big.append(f'{f.stat().st_size} {_h.sha256(f.read_bytes()).hexdigest()} {f.relative_to(S / "meas")}')
put('cpu/simulation-logs.sha256', "# each leg's simulation log (bytes, sha256; not copied: over 200 KB)\n" +
    '\n'.join(big) + '\n')

# --- tools
for f in sorted((S / 'bin').iterdir()):
    if f.is_file():
        keep(f'tools/{f.name}', f)
