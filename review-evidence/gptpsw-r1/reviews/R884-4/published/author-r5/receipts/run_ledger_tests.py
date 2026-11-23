from functools import partial
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path.cwd() / "sw/litex"))
import test_ctrl_memory as tests

problems = []
with tempfile.TemporaryDirectory(prefix="gptpsw-a814-r5-ledger-") as name:
    tmp = Path(name)
    tests.run_arm(problems, "rules and ledger", partial(tests.check_arms, tmp=tmp))
    green = {"checks"} if not problems else set()
    tests.run_arm(problems, "planted ledgers", partial(tests.ledger_plant_arms, tmp=tmp, green=green))
    tests.run_arm(problems, "out-of-context mapper", partial(
        tests.ledgers.mapper_arms, check=tests.check, tmp=tmp,
        write=partial(tests.ledger_elf, tmp),
        rebuild=partial(tests.mutated, tests.ledgers.mapper(), "main")))
for problem in problems:
    print(f"FAIL: {problem}")
print(f"focused ledger tests: {len(problems)} failure(s)")
raise SystemExit(bool(problems))
