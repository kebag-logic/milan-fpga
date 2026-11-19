# receipts_spec_r2.py: round 2's receipts, run by receipts.py OUT receipts_spec_r2.py 'round 2'.
R1, R2 = '0d1eb8e4c5', 'f09d82e052'
put('change/commits.txt', run('git', 'log', '--format=%H %s', '0839453f6d..HEAD', cwd=L))
put('change/round2.diff', run('git', 'diff', R1, R2, cwd=L))
keep('change/non-comment-lines.txt', S / 'r2/non-comment-lines.txt')
put('images/budget-hashes.txt', '# the CPU budget harness images (point arm sha256)\n## round 1, 4224df63 (equal to e5dee83b)\n'
    + (S / 'img/budget-head2/hashes.txt').read_text() + '## round 2, e7b0272b\n' + (S / 'img/budget-r2/hashes.txt').read_text()
    + ('## EQUAL\n' if (S / 'img/budget-head2/hashes.txt').read_text() == (S / 'img/budget-r2/hashes.txt').read_text()
       else '## DIFFERENT\n'))
put('images/platform-and-fixture-hashes.txt', '# the platform and size-fixture images (sha256 path)\n## round 1, 4224df63\n'
    + (S / 'img/plat-head2.hashes').read_text() + '## round 2, e7b0272b\n' + (S / 'img/plat-r2.hashes').read_text()
    + ('## EQUAL\n' if (S / 'img/plat-head2.hashes').read_text() == (S / 'img/plat-r2.hashes').read_text()
       else '## DIFFERENT\n'))
keep('images/platform-ledger-r2.txt', S / 'img/plat-r2/plat_ledger.log',
     lambda x: lines(r'^(POINT|plat_ledger|LINK|KEY|TILES|LEDGER)', x))
keep('images/rodata-shifts.txt', S / 'r2/rodata-shifts.txt')
for arm in sorted((S / 'fw/talker-r2').glob('*.log')):
    keep(f'tests/talker-arms-r2/{arm.name}', arm)
for tag, d in (('e7b0272b', S / 'docs-steps/r2'), ('f09d82e0', S / 'docs-steps/r2b')):
    if (d / 'steps.txt').is_file():
        keep(f'gates/{tag}/docs-workflow-steps.txt', d / 'steps.txt')
put('change/after-the-image-check.txt',
    '# files changed after e7b0272b, where the 20 images were checked byte-identical: a design page and a harness '
    'docstring, neither linked into any image\n' + run('git', 'diff', '--name-only', 'e7b0272ba4', 'f09d82e052', cwd=L))
put('review/ctrl_service_budget-README-261.txt',
    '# tb/verilator/ctrl_service_budget/README.md line 261 at e7b0272b (F2 asked whether it claims more): the formal '
    'pass\'s completeness rule, unchanged\n' + run('sed', '-n', '261p', 'tb/verilator/ctrl_service_budget/README.md', cwd=L))
put('review/pr952-review-starts.txt', run('gh', 'pr', 'view', '952', '--json', 'comments', '--jq',
    '.comments[] | select(.body | test("INDEPENDENT REVIEW STARTED")) | .createdAt + " " + (.body | split("\\n")[0])', cwd=L))
for name in ('receipts.py', 'receipts_spec_r2.py', 'budget_images.py', 'plat_images.sh', 'docs_steps.py', 'talker_arms.py',
             'clone.sh', 'bgunit.sh', 'unit.sh', 'launch_when_free.sh', 'env.sh'):
    keep(f'tools/{name}', S / 'bin' / name)
