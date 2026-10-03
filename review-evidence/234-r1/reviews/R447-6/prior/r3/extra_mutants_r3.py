#!/usr/bin/env python3
"""Reviewer mutants for the round-3 validator and parsers of the #234 resource gate.

Usage: extra_mutants_r3.py <repo checkout> <scratch dir>
Each mutant edits exactly one unique span of a copy of syn/ooc/pp_resource_gate.py or of
syn/ooc/pp_baseline_rank.py and runs the shipped self-test against the copy. A mutant the
self-test still passes is SURVIVED. The script never writes inside the checkout.
"""
import ast
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess
import sys

GATE, RANK = "pp_resource_gate.py", "pp_baseline_rank.py"
MUTANTS = {
    "routing-error row may repeat": (GATE, '    if len(counts.get("nets with routing errors", [])) != 1:\n',
                                     '    if not counts.get("nets with routing errors"):\n'),
    "undecodable budget page escapes": (GATE, "    except (OSError, ValueError, Refusal) as error:\n",
                                        "    except (OSError, Refusal) as error:\n"),
    "undecodable route status escapes": (GATE, "    except (OSError, ValueError) as error:\n        raise Refusal(f\"unreadable route",
                                         "    except OSError as error:\n        raise Refusal(f\"unreadable route"),
    "bool scope counts accepted": (GATE, "type(count) is int and count >= 0", "isinstance(count, int) and count >= 0"),
    "standalone clock items unchecked": (GATE, 'for key in ("flow", "standalone_clock_ns") for item',
                                         'for key in ("flow",) for item'),
    "flow items unchecked": (GATE, 'for key in ("flow", "standalone_clock_ns") for item',
                             'for key in ("standalone_clock_ns",) for item'),
    "digest of any length": (GATE, 're.fullmatch(r"[0-9a-f]{64}"', 're.fullmatch(r"[0-9a-f]+"'),
    "identity may hold extra keys": (GATE, "not isinstance(identity, dict) or sorted(identity) != sorted(IDENTITY)",
                                     "not isinstance(identity, dict) or not set(IDENTITY) <= set(identity)"),
    "only TNS endpoints counted": (GATE, 'if name in ("TNS Total Endpoints", "THS Total Endpoints")]',
                                   'if name in ("TNS Total Endpoints",)]'),
    "only THS endpoints counted": (GATE, 'if name in ("TNS Total Endpoints", "THS Total Endpoints")]',
                                   'if name in ("THS Total Endpoints",)]'),
    "load refusal reaches judge": (GATE, "    if problems:\n        raise Refusal(f\"baseline {path} is malformed",
                                   "    if problems and False:\n        raise Refusal(f\"baseline {path} is malformed"),
    "hierarchy counts from the fourth cell": (RANK, "for value in fields[2:]):\n",
                                              "for value in fields[3:]):\n"),
    "hierarchy counts end early": (RANK, "for value in fields[2:]):\n", "for value in fields[2:-1]):\n"),
}


def run(name, target, change, here, tmp):
    source = (here / target).read_text()
    old, new = change
    if source.count(old) != 1:
        return name, "NOT-UNIQUE", f"{source.count(old)} matches"
    changed = source.replace(old, new)
    ast.parse(changed)
    folder = tmp / name.replace(" ", "_")
    folder.mkdir()
    for sibling in (GATE, RANK, "pp_resource_gate_selftest.py"):
        shutil.copy2(here / sibling, folder / sibling)
    (folder / target).write_text(changed)
    result = subprocess.run([sys.executable, "-B", str(folder / GATE), "--selftest"],
                            capture_output=True, text=True, timeout=600, cwd=folder)
    lines = (result.stdout + result.stderr).strip().splitlines()
    why = next((line for line in reversed(lines) if "AssertionError" in line or "Error" in line), lines[-1] if lines else "")
    return name, "KILLED" if result.returncode else "SURVIVED", f"rc={result.returncode} {why[:170]}"


def main():
    here = Path(sys.argv[1]) / "syn/ooc"
    tmp = Path(sys.argv[2]).resolve()
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    control = run("control", GATE, ("BASELINE = ", "BASELINE = "), here, tmp)
    print(f"control: {'PASS' if control[1] == 'SURVIVED' else 'FAIL'} {control[2]}")
    if control[1] != "SURVIVED":
        sys.exit("the unmutated control must pass the self-test")
    with ThreadPoolExecutor(max_workers=13) as pool:
        results = list(pool.map(lambda item: run(item[0], *item[1][:1], item[1][1:], here, tmp), MUTANTS.items()))
    for name, verdict, detail in results:
        print(f"{verdict:<10} {name}: {detail}")
    print(f"round-3 extra mutants: {sum(v == 'KILLED' for _, v, _ in results)} killed, "
          f"{sum(v == 'SURVIVED' for _, v, _ in results)} survived, "
          f"{sum(v == 'NOT-UNIQUE' for _, v, _ in results)} not unique, of {len(results)}")


if __name__ == "__main__":
    main()
