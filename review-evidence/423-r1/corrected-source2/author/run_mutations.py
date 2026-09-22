"""Restoration controls in disposable copies, never in the source lane."""
from pathlib import Path
import datetime
import json
import shutil
import subprocess
import sys
import tempfile
import time

SOURCE = Path('$CANDIDATE/scripts')
OUT = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parent
OUT.mkdir(exist_ok=True)
CHANGES = {
    'shared-decode': ('check_merge_containment.py', 'os.fsdecode(p.stdout)', 'p.stdout.decode("utf-8", "surrogateescape")'),
    'patch-inverse': ('check_merge_containment.py', 'input=os.fsencode(patch)', 'input=patch.encode("utf-8", "surrogateescape")'),
    'retention-decode': ('merge_containment_replay.py', 'path = os.fsdecode(name)', 'path = name.decode("utf-8", "surrogateescape")'),
    'entry-name-check': ('merge_containment_replay.py', 'name != os.fsencode(path)', 'name != path.encode("utf-8", "surrogateescape")'),
}
RUNNER = '''import merge_containment_selftest_locale as test
from merge_containment_selftest_scratch import quiet_git
class Fixture:
    leftovers = []
    failures = 0
    count = 0
    def case(self, name, got, want, why):
        self.count += 1
        if got != want:
            self.failures += 1
            print("FAIL", name, repr(got), repr(want))
fx = Fixture()
with quiet_git():
    test.locale_cases(fx)
print("RESULT", fx.count, fx.failures, fx.leftovers)
raise SystemExit(bool(fx.failures or fx.leftovers))
'''
results = []
for name in ['baseline', *CHANGES]:
    with tempfile.TemporaryDirectory(prefix='containment-locale-mutation-') as directory:
        work = Path(directory)
        for file in ['check_merge_containment.py', 'merge_containment_replay.py',
                     'merge_containment_selftest_locale.py', 'merge_containment_selftest_scratch.py']:
            shutil.copy2(SOURCE / file, work / file)
        if name in CHANGES:
            file, before, after = CHANGES[name]
            path = work / file
            body = path.read_text()
            assert body.count(before) == 1
            path.write_text(body.replace(before, after))
        (work / 'run.py').write_text(RUNNER)
        started = time.monotonic()
        command = ['python3', '-B', str(work / 'run.py')]
        result = subprocess.run(command, cwd=work, capture_output=True)
        (OUT / f'mutation-{name}.stdout').write_bytes(result.stdout)
        (OUT / f'mutation-{name}.stderr').write_bytes(result.stderr)
        row = dict(name=name, argv=command, exit_code=result.returncode,
                   seconds=round(time.monotonic()-started, 3),
                   expected_exit=0 if name == 'baseline' else 1)
        results.append(row)
        (OUT / 'mutations.json').write_text(json.dumps(dict(
            at=datetime.datetime.now().astimezone().isoformat(), results=results), indent=2)+'\n')
        print(json.dumps(row), flush=True)
        assert b'NOT RUN' not in result.stdout, 'Latin-1 mutation coverage did not run'
        assert result.returncode == row['expected_exit']
(OUT / 'mutations.json').write_text(json.dumps(dict(
    at=datetime.datetime.now().astimezone().isoformat(), results=results), indent=2)+'\n')
