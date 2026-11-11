"""decode_arm.py <tree>: run only ctrl_memory_decode.arms (the CPU decode arm of test_ctrl_memory.py) from <tree>'s
sw/litex, printing each graded fact and the failure count. Nothing is generated or written."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'sw/litex'))
import ctrl_memory_decode as decode  # noqa: E402
problems = []
decode.arms(problems)
for p in problems:
    print('FAIL:', p)
print(f'decode arm: {len(problems)} failure(s)')
sys.exit(1 if problems else 0)
