"""Run the current capture gate, then remove only D5's check in memory."""
import contextlib
import importlib.util
import io
import sys
from pathlib import Path
from unittest.mock import patch

root = Path.cwd()
packet = Path(__file__).resolve().parent
sys.path.insert(0, str(root / 'scripts'))
import check_nvm_capture as gate

assert gate.main() == 0
source = (root / 'tb/verilator/nvm_capture_cpu/run.py').read_text()
check = ("        if (spec.get('mutation', 'none') == 'none'\n"
         "                and row['sys_cycles'] * 2000 > HOLD_FLOOR_MS * spec['sys_hz']):\n"
         "            raise RuntimeError('worst measured copy exceeds half the 49 ms hold floor')\n")
assert source.count(check) == 1
copy = packet / 'scratch/d5/run.py'
copy.parent.mkdir(parents=True, exist_ok=True)
copy.write_text(source.replace(check, ''))
spec = importlib.util.spec_from_file_location('d5_removed', copy)
mutant = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutant)
sink = io.StringIO()
with patch.object(gate.capture, 'grade_rows', mutant.grade_rows), contextlib.redirect_stderr(sink):
    rc = gate.main()
print(f'D5 removal rc={rc}; {sink.getvalue().strip()}')
assert rc == 1 and 'OFF timing limit was ignored' in sink.getvalue()
print('PASS: original gate passes; removal of current-writer D5 check fails the unchanged gate')
