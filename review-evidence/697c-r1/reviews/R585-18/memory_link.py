#!/usr/bin/env python3
"""Exercise the existing split-link and plan arms without SoC generation."""
from pathlib import Path
import sys

root = Path.cwd()
sys.path.insert(0, str(root / 'sw/litex'))
import test_ctrl_memory as memory

work = Path(__file__).resolve().parent / 'scratch/memory-link'
work.mkdir(parents=True, exist_ok=True)
problems = []
memory.bank_arms(problems)
memory.check_arms(problems, work)
assert memory.link_arms(problems, work)
memory.registry_arms(problems, work)
assert not problems, problems
print('memory bank, map, link and rule-registry arms: PASS')
