import pathlib
import subprocess
import sys
source = pathlib.Path('/repo/scripts/act_ci.py').read_text()
platform = '        *(word for label in RUNS_ON_LABELS for word in ("--platform", f"{label}={RUNNER_IMAGE}")),\n'
mutants = {
 'drop-2404-from-platform-map': (platform, '        "--platform",\n        f"ubuntu-latest={RUNNER_IMAGE}",\n'),
 'map-2404-to-act-default-image': (platform, '        "--platform",\n        f"ubuntu-latest={RUNNER_IMAGE}",\n        "--platform",\n        "ubuntu-24.04=node:16-bullseye-slim",\n'),
 'accept-any-ubuntu-prefix': ('if runs_on not in RUNS_ON_LABELS:', 'if not (isinstance(runs_on, str) and runs_on.startswith("ubuntu-")):'),
}
name = sys.argv[1]
old, new = mutants[name]
assert source.count(old) == 1
path = pathlib.Path('/work/act_ci.py')
path.write_text(source.replace(old, new))
path.chmod(0o555)
print('MUTANT', name, '\nREPLACED', repr(old), '\nWITH', repr(new), flush=True)
result = subprocess.run([sys.executable, '-I', str(path), '--selftest', '--worktree', '/repo'], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(result.stdout, end='')
failures = [line.strip() for line in result.stdout.splitlines() if 'FAIL ' in line]
expected = "act's platform list maps ubuntu-latest and ubuntu-24.04" if name != 'accept-any-ubuntu-prefix' else 'a job on ubuntu-26.04 is refused before act'
assert result.returncode == 1 and any(expected in line for line in failures), (result.returncode, failures)
print('MUTANT_DETECTED', name, 'child_rc', result.returncode, 'named_failures', failures)
