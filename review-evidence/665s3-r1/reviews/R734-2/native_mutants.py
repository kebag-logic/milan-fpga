#!/usr/bin/env python3
"""Plant defects into the split boot driver's NATIVE check, one at a time, in memory (the module keeps the
checkout's path, so its ROOT is the checkout's), and require the native controls to grade at least one control
WRONG for each. Lane helper, not part of the tree; nothing is written into the checkout.

usage: native_mutants.py CHECKOUT WORK
"""
import sys
import types
from pathlib import Path

checkout = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
path = checkout / "tb/verilator/ctrl_split_boot/run.py"
source = path.read_text()
MUTANTS = (
    ("exit-status-ignored", "    elif status != 0:\n        findings.append(f'NATIVE: the model exited {status}')",
     "    elif False:\n        findings.append(f'NATIVE: the model exited {status}')"),
    ("missing-tally-ignored", "    if suite_tally.is_nocount(checks, failures, matched, skipped):",
     "    if False:"),
    ("failed-tally-ignored", "    elif failed:\n        findings.append(f'NATIVE: the model\\'s log reports",
     "    elif False:\n        findings.append(f'NATIVE: the model\\'s log reports"),
    ("status-not-saved", "        (out / STATUS).write_text(f'{result.returncode}\\n')\n", ""),
    ("regrade-assumes-success", "                 saved_status(out))", "                 0)"),
    ("missing-status-read-as-success", "    except (OSError, ValueError):\n        return None",
     "    except (OSError, ValueError):\n        return 0"),
)
escaped = 0
for name, old, new in MUTANTS:
    if source.count(old) != 1:
        print(f"MUTANT {name}: its anchor occurs {source.count(old)} times")
        escaped += 1
        continue
    module = types.ModuleType(f"run_{name.replace('-', '_')}")
    module.__file__ = str(path)
    exec(compile(source.replace(old, new), str(path), "exec"), module.__dict__)
    wrong = module.native_controls(work / name, "endstation_ax7101_1x1_tdm8", 1)
    escaped += not wrong
    print(f"MUTANT {name}: {'caught' if wrong else 'ESCAPED'} ({wrong} control(s) graded WRONG)", flush=True)
print(f"native_mutants: {len(MUTANTS) - escaped} of {len(MUTANTS)} caught")
raise SystemExit(1 if escaped else 0)
