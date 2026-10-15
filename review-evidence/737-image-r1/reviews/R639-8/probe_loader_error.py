"""Exercise the loader-error branch without leaving a blocked tracee."""
import errno
import json
import os
from pathlib import Path
import sys

ROOT = Path(sys.argv[1]).resolve()
PACKET = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'ci/image'))
import exec_audit as audit

base = PACKET / 'scratch/loader-error'
base.mkdir(parents=True, exist_ok=True)
script = base / 'no-shebang'
script.write_text('exit 0\n')
script.chmod(0o755)
target_result = ('run', (str(script), str(script)), [str(script)])
loaded = audit._loaded(str(script), str(script), [str(script)], str(base))
assert loaded == ('errno', errno.ENOEXEC, [])
saved_target, saved_respond = audit._target, audit._respond
responses = []
audit._target = lambda *args: target_result
audit._respond = lambda *args: responses.append(args)
tracer = object.__new__(audit._Trace)
tracer.listener = -1
try:
    tracer.executed(1, os.getpid(), audit.NR_EXECVE, [])
    error = None
except Exception as exc:
    error = {'type': type(exc).__name__, 'message': str(exc)}
finally:
    audit._target, audit._respond = saved_target, saved_respond
result = {'target_result': target_result, 'actual_loaded_result': loaded,
          'executed_error': error, 'responses': responses,
          'method': 'real _loaded on a temporary executable text file; stub only target lookup and kernel response'}
(PACKET / 'loader-error.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
