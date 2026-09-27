"""Run assigned local gates synchronously at a clean committed head.

Usage: python3 run_gates.py CANDIDATE OUTPUT_DIRECTORY SCRATCH_PARENT [--resume]
Run with the pinned documentation dependencies in the active interpreter.
The scratch clone exists solely for the requested submodule-free gate.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def main():
    candidate, output, scratch_parent = [Path(p).resolve() for p in sys.argv[1:4]]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    def git(*args, cwd=candidate):
        return subprocess.run(['git', *args], cwd=cwd, env=env, capture_output=True, text=True, timeout=600, check=True).stdout.strip()
    head = git('rev-parse','HEAD')
    assert not git('status','--porcelain'), 'candidate must be clean'
    for line in git('submodule','status','third_party/verilog-axis','protocol-processor','gptp-processor').splitlines():
        assert not line.startswith(('-', '+', 'U')), 'required submodule missing or mismatched'
    resume = sys.argv[4:] == ['--resume']
    receipts = json.loads((output/'gates.json').read_text()) if resume else []
    assert all(r['head'] == head for r in receipts), 'resume head changed'
    def gate(name, args, cwd, context):
        previous = next((r for r in receipts if r['gate'] == name), None)
        if previous and previous['return_code'] == 0:
            print(name, 'rc 0 already recorded at this head', flush=True)
            return
        if previous:
            shutil.copyfile(output/f'gate-{name}.txt',output/f'gate-{name}-initial.txt')
            receipts.remove(previous)
        display = ['python3' if a in (sys.executable, sys._base_executable) else a for a in args]
        with (output/f'gate-{name}.txt').open('w') as log:
            log.write(f'Head: {head}\nContext: {context}\nCommand: ' + ' '.join(display)+'\n')
            log.flush()
            result = subprocess.run(args, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1800)
            log.write(f'\nReturn code: {result.returncode}\n')
        receipt = dict(gate=name, command=display,
                       head=head, context=context, return_code=result.returncode)
        receipts.append(receipt)
        (output/'gates.json').write_text(json.dumps(receipts, indent=2)+'\n')
        print(name, 'rc', result.returncode, flush=True)
        assert result.returncode == 0, name
    for name, args in [
        ('docs-submodules',['scripts/docs_check.py']),
        ('doc-style',['scripts/check_doc_style.py']),
        ('toc',['scripts/gen_toc.py','--check']),
        ('em-dash',['scripts/check_em_dash.py','--base','8bc97021']),
        ('doc-paths',['scripts/check_doc_paths.py']),
        ('ci-scope',['scripts/ci_scope.py','--selftest']),
        ('baremetal',['scripts/check_baremetal_only.py','--check']),
        ('feature-status',['scripts/check_feature_status.py','--self-test']),
    ]:
        interpreter = sys._base_executable if name == 'baremetal' else sys.executable
        context = 'physical candidate; pinned submodules present'
        if name == 'baremetal':
            context += '; base interpreter with PyYAML'
        gate(name, [interpreter, *args], candidate, context)
    gate('diff',['git','diff','--check'], candidate, 'physical candidate; committed head')
    gate('diff-committed',['git','diff','--check','8bc97021','HEAD'], candidate, 'physical candidate; full committed PR delta')
    with tempfile.TemporaryDirectory(prefix='75-a389-docs-', dir=scratch_parent) as temporary:
        scratch = Path(temporary)
        clone = scratch/'candidate'
        subprocess.run(['git','clone','--shared','--no-checkout',str(candidate),str(clone)],
                       capture_output=True, text=True, timeout=600, check=True)
        git('checkout','--detach',head,cwd=clone)
        assert git('rev-parse','HEAD',cwd=clone) == head
        assert not git('status','--porcelain',cwd=clone)
        assert all(line.startswith('-') for line in git('submodule','status',cwd=clone).splitlines())
        gate('docs-no-submodules',[sys.executable,'scripts/docs_check.py'], clone, 'exact-head validation clone; no submodules')
        (clone/'.git').rename(scratch/'git-metadata')
        env['GIT_CEILING_DIRECTORIES'] = str(scratch)
        gate('docs-no-git',[sys.executable,'scripts/docs_check.py'], clone, 'same validation tree; no submodules or Git metadata')
    assert git('rev-parse','HEAD') == head and not git('status','--porcelain')
    print('PASS: all assigned gates at',head,flush=True)


if __name__ == '__main__':
    main()
