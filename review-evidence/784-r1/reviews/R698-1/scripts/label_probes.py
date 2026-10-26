import contextvars
import importlib.util
import pathlib
import tempfile
import sys
from unittest import mock
spec = importlib.util.spec_from_file_location('runner', '/repo/scripts/act_ci.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
fixture = m.selftest_fixture()
resolved = m.ValidatedRun(fixture.pr, fixture.repository, fixture.base)
labels = ['ubuntu-latest', 'ubuntu-24.04', 'ubuntu-22.04', 'ubuntu-26.04', '${{ matrix.os }}', '[ubuntu-24.04]', '', '""', 'null', '{}', 'true', '42', 'Ubuntu-24.04', 'ubuntu-24.04-arm']
with mock.patch.object(m, 'BOOKED_CPU_RANGES', contextvars.ContextVar('booked', default=('0-15', '16-31', '32-47', '48-63'))):
    for label in labels:
        rc, refusal, transcript, entered = m.dry_run_replay(resolved, pathlib.Path('/repo'), label)
        print('LABEL', repr(label), 'RC', rc, 'BOUNDARIES', entered, 'REFUSAL', refusal)
        if label in ('ubuntu-latest', 'ubuntu-24.04'):
            assert rc == 0 and not refusal and entered == 1
            for accepted in ('ubuntu-latest', 'ubuntu-24.04'):
                assert transcript.count(' --platform ' + accepted + '=' + m.RUNNER_IMAGE + ' ') == 1
            assert ' --memory=8g --memory-swap=8g' in transcript
            print(transcript)
        else:
            assert rc is None and 'runs on ' in refusal and entered == 0 and '--platform' not in transcript
with tempfile.TemporaryDirectory(dir='/work') as raw:
    root = pathlib.Path(raw)
    count = 0
    for rel in m.WORKFLOWS.values():
        data = (pathlib.Path('/repo') / rel).read_text()
        count += data.count('runs-on: ubuntu-latest')
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(data.replace('runs-on: ubuntu-latest', 'runs-on: ubuntu-24.04'))
    m.validate_workflow_sandbox(root, tuple(m.WORKFLOWS))
    print('STEP2_SANDBOX_PASS', count, 'shipping jobs relabelled in disposable tree')
print('EXTRA_LABEL_PROBES_PASS')
