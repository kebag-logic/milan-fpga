"""Repeat the reviewer's fault campaign and require every expected outcome."""
from pathlib import Path
import io
import json
import os
import subprocess
import sys
import tarfile

ROOT = Path('$LANES/395-timing-grade')
WORK = Path('$VALIDATION_STORAGE/395-a390-work')
OUT = Path('$MANAGEMENT/2026-09-23/395-a390')
REVIEW = Path('$REVIEWS/395-r372-1-packet')
PYTHON = '$WORKSPACE_HOME/litex-milan/venv/bin/python'
results = []

def run(name, argv, cwd=ROOT):
    result = subprocess.run(['timeout', '--foreground', '900', *argv], cwd=cwd,
                            text=True, capture_output=True, check=False)
    (OUT / (name + '.log')).write_text(result.stdout + result.stderr)
    print(name, 'rc=', result.returncode, flush=True)
    print(result.stdout, flush=True)
    assert result.returncode == 0, result.stderr
    return result.stdout

text = run('reviewer-mutations', ['python3', '-B', str(REVIEW/'scripts/mutation_probes.py'),
                               str(ROOT), str(WORK/'mutants'), PYTHON])
assert text.rstrip().endswith('unexpected=0'), text
assert 'UNEXPECTED' not in text and 'PLANT-FAILED' not in text, text
text = run('hook-refusals', ['python3', '-B', str(REVIEW/'scripts/hook_refusal_probe.py'), str(ROOT)])
assert text.count('hook rc=1') == 4 and 'hook rc=0' not in text, text

# The real builder enters test_commercial_timing_grade first. Export only
# its Python inputs and verify the complete entry point refuses all five
# report mutants before reaching any other bank arm.
paths = ['sw/builder', 'sw/litex', 'scripts', 'configs', 'avdecc']
archive = subprocess.run(['git', 'archive', 'HEAD', *paths], cwd=ROOT,
                         capture_output=True, check=True).stdout
required = ['reports-no-leading-check', 'reports-corner-setup-only',
            'reports-corner-no-unconstrained', 'reports-all-no-check-verbose',
            'reports-clock-interaction-setup-only']
for label in required:
    dest = WORK/'bank-mutants'/label
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(dest, filter='data')
    (dest/'sw/litex/timing_grade.tcl').write_bytes((WORK/'mutants'/label/'sw/litex/timing_grade.tcl').read_bytes())
    result = subprocess.run(['timeout', '--foreground', '300', 'python3', '-B',
                             'sw/builder/test_builder.py', '--require-rv32', '--require-elaboration'],
                            cwd=dest, text=True, capture_output=True, check=False)
    (OUT/(label+'-bank.log')).write_text(result.stdout+result.stderr)
    assert result.returncode == 1 and 'AssertionError' in result.stderr, (label,result)
    assert 'test_timing_grade.py' in result.stderr, (label,result)
    results.append({'fault':label,'returncode':result.returncode,'reason':result.stderr.strip().splitlines()[-1]})
    print(label, 'full bank rc=1, timing-grade assertion', flush=True)

# Prove the new derived-PLL check detects restoring the old literal.
for label, literal in [('pll-control',False),('pll-literal',True)]:
    dest=WORK/label
    dest.mkdir(parents=True,exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(dest,filter='data')
    path=dest/'sw/litex/milan_soc.py'
    source=path.read_text()
    # Resolve pinned dependencies from the registered lane, without copying
    # or linking submodules into the disposable fixture. Both arms use this.
    anchor='REPO_ROOT = SOC_DIR.parent.parent'
    assert source.count(anchor)==1
    path.write_text(source.replace(anchor, 'REPO_ROOT = Path('+repr(str(ROOT))+')'))
    if literal:
        old='S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)[1]))'
        source=path.read_text()
        assert source.count(old)==1
        path.write_text(source.replace(old,'S7PLL(speedgrade=-2)'))
    probe='import sys; sys.path.insert(0,"sw/builder"); from test_timing_grade import test_pll_grade; test_pll_grade('+repr(PYTHON)+')'
    result=subprocess.run(['timeout','--foreground','300','python3','-B','-c',probe],cwd=dest,
                          text=True,capture_output=True,check=False)
    (OUT/(label+'.log')).write_text(result.stdout+result.stderr)
    assert result.returncode == int(literal), (label,result)
    if literal:
        assert 'AssertionError' in result.stderr and "speedgrade=-2" in result.stderr, result
    print(label,'rc=',result.returncode,flush=True)
(OUT/'planted-faults.json').write_text(json.dumps(results,indent=2)+'\n')
print('All planted faults detected for their intended assertions; controls pass.')
