import hashlib, json, subprocess, sys
from pathlib import Path
out = Path(__file__).resolve().parent
root = Path('$LANES/387-media-rebase')
sys.path.insert(0, str(root/'scripts'))
from suite_tally import scan, log_reports_failure
commands = json.loads((out/'sweep-commands.json').read_text())
assert len(commands) == 44
receipts = [json.loads((out/f'sweep-{i:02d}.json').read_text()) for i in range(1,45)]
assert all(r['rc'] == 0 and r['command'] == command for r,command in zip(receipts,commands))
logs = ''.join((out/f'sweep-{i:02d}.log').read_text() for i in range(1,45))
assert not log_reports_failure(logs)[1], log_reports_failure(logs)
checks, failures, rows, unparsed, skips = scan(logs)
assert failures == 0
seconds = round(sum(r['elapsed_s'] for r in receipts),2)
(out/'sweep-summary.json').write_text(json.dumps(dict(commands=44,checks=checks,failures=failures,command_elapsed_s=seconds,rows=rows,unparsed=unparsed,skips=skips),indent=2)+'\n')
required = ['gmstep-mutants','tkdiag','docs-check','docs-check-no-git','em-dash','doc-style','toc','doc-paths','module-matrix','xvlog','rtl-source-lists','cpp-idiom','py-idiom','behave','builder-no-compiler','diff-check','diff-check-base','test-evidence','test-evidence-selftest','ci-events','freshness-make43','freshness-make44','freshness-both-legs','settime-render-control','settime-render-positive']
assert all(json.loads((out/(name+'.json')).read_text())['rc']==0 for name in required)
head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
assert head == '0f003fab3303858ba4db955ad3c0512e67a8018b'
assert not subprocess.check_output(['git','status','--short'],cwd=root,text=True)
assert all(hashlib.sha256((root/name).read_bytes()).hexdigest()==sha for name,sha in json.loads((out/'tested-inputs.json').read_text()).items())
summary = f'The default sweep passed all 44 expanded commands: {checks} checks, 0 failures. Their summed foreground durations were {seconds} seconds, excluding gaps between chunks. Every assigned gate exited 0.'
p = out/'HANDOFF.md'
text = p.read_text().replace('`VALIDATION_PENDING`',summary+"\n\nDocumentation passed in Git and no-Git modes. The style, TOC, cited-path, module-matrix, front-end, source-list, C++/Python idiom, behavior, and diff gates all exited 0. The behavior suite passed 344 scenarios and 1739 steps. The em-dash gate passed against the assigned base. The deadline contract passed 101 self-test checks, and the CI contract passed. Full commands and exclusions are retained in the per-gate receipts.")
p.write_text(text)
p = out/'PR-BODY.md'
text = p.read_text().replace('`VALIDATION_PENDING`','green').replace('`RESULTS_PENDING`',f'All 44 commands exited 0: {checks} checks, 0 failures. The gmstep leg passed 48/48; the full gmstep campaign passed 13/13; tkdiag passed 96/96 with four mutants caught. The true-ratio leg passed 143/143. Both documentation modes and all listed static checks passed. The behavior suite passed 344 scenarios. The full compiler-absent builder rejected 189/189 applicable mutations and reported its two expected exclusions. The settime omission control failed the named new checks. The nested freshness repro passed for both positive legs.')
text = text.replace('- [ ] Assigned local gates pass at the corrected head.','- [x] Assigned local gates pass at the corrected head.')
p.write_text(text)
results=[]
for file in sorted(out.glob('*.json')):
    data=json.loads(file.read_text())
    if isinstance(data,dict) and 'rc' in data:
        assert data['rc']==0,file.name
        results.append(dict(gate=file.stem,**data))
(out/'gate-results.json').write_text(json.dumps(results,indent=2)+'\n')
for name in ['HANDOFF.md','PR-BODY.md']:
    text=(out/name).read_text()
    assert text.startswith('[A277]') and '/home/' not in text and '\u2014' not in text
    assert '_PENDING' not in text
(out/'REVIEW-READY.md').write_text(f"""[A277] REVIEW READY

Commit: `{head}` (local head on `387-media-rebase`; not pushed).

Round 3 implements assignment [5820585975](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820585975): the 3600-second deadline and its contract, nested recipe freshness for both positive legs, the three documentation scope corrections, both requested RTL comments, the decided PR-body citations, and the live-CSR settime render check. The hosted shards already allow 120 minutes. No functional RTL changed this round.

Validation: all assigned commands exited 0. The chunked default `milan_dp` sweep ran 44 commands, {checks} checks, 0 failures; `gmstep-mutants` passed 13/13; tkdiag passed 96/96 with all four mutants caught. The reviewer's unchanged GNU make 4.3 repro prints `is_fresh: True` inside the parent recipe. Both positive legs also pass nested assertions, and the old behavior fails them. The settime omission control fails the named render check.

Both documentation CI modes, the requested static gates, and 344 behavior scenarios pass. The full builder without an RV32 compiler rejects 189/189 applicable mutations; compiler-dependent instruments and physical calibration remain explicitly NOT RUN. The deadline contract and its 101-check self-test pass. The em-dash gate used base `57456af96b3127b9d309a995bbbd35a6113ce52d`.

`HANDOFF.md`, the full replacement `PR-BODY.md`, and command/exit receipts are prepared in the assigned output packet. No PR edit or push was made. Independent re-review, publication, hosted/candidate validation, and merge remain pending. Issue #387 acceptance 4 remains the manager's #117 bench step after merge.
""")
print(summary)
print('Final handoff, PR body, and issue comment prepared for',head)
