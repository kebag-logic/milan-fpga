#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe (round 4): would the generative test alone catch a removed barrier or converter?

Each mutant edits one span of the gate or the hierarchy parser in a copy of the
three modules (as the shipped campaign copies them). For each, two runs:
  fuzz500  - only the generative test, `fuzz(500, 234)` on the self-test fixtures
             (the seeded arm the self-test runs), rc 0 = the contract held;
  selftest - the whole `--selftest` (arms plus the 500 cases).
DETECTED means rc != 0. A mutant whose fuzz500 misses is rerun at fuzz 5000.
Controls run unmutated. "barrier holds" mutants remove an inner handler; the
barrier is expected to keep the contract, so fuzz500 rc 0 is the expected result.

Usage: probe_r4_generative.py <checkout> <scratch-dir> [--jobs N]
"""

import concurrent.futures
from pathlib import Path
import shutil
import subprocess
import sys

REPO, SCRATCH = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
HERE = REPO / "syn/ooc"
GATE, RANK = "pp_resource_gate.py", "pp_baseline_rank.py"
MUTANTS = {
    # (file, old, new, expected fuzz outcome: "detect" or "hold")
    "control": (GATE, None, None, "hold"),
    "barrier narrowed to Refusal": (GATE, "    except Exception as error:  # the barrier",
                                    "    except Refusal as error:  # the barrier", "detect"),
    "barrier narrowed to Refusal and OSError": (GATE, "    except Exception as error:  # the barrier",
                                                "    except (Refusal, OSError) as error:  # the barrier", "detect"),
    "emit prints raw text": (GATE, '    print("".join(char if char == "\\n" or " " <= char <= "~" else '
                                   'ascii(char)[1:-1] for char in text))', "    print(text)", "detect"),
    "whole(): no grammar": (RANK, '    if not re.fullmatch(("-?" if signed else "") + f"[0-9]{{1,{DIGITS}}}", text):',
                            "    if False:", "detect"),
    "whole(): no digit bound": (RANK, 'f"[0-9]{{1,{DIGITS}}}"', '"[0-9]+"', "detect"),
    "whole(): any Unicode digit": (RANK, 'f"[0-9]{{1,{DIGITS}}}"', 'rf"\\d{{1,{DIGITS}}}"', "detect"),
    "real(): no finiteness": (GATE, "    if not math.isfinite(value):\n        raise ValueError(f\"{what} is not finite",
                              "    if False:\n        raise ValueError(f\"{what} is not finite", "detect"),
    "strict(): plain json.loads": (GATE, "    return json.loads(text, object_pairs_hook=named, parse_constant=constant, "
                                         "parse_float=decimal,\n                      parse_int=integer)",
                                   "    return json.loads(text)", "detect"),
    "strict(): parse_int=int": (GATE, "parse_int=integer)", "parse_int=int)", "detect"),
    "strict(): parse_float=float": (GATE, "parse_float=decimal,", "parse_float=float,", "detect"),
    "named(): no repeated-key refusal": (GATE, "        if key in table:\n", "        if False:\n", "detect"),
    "named(): no name class": (GATE, "        if not SCOPE_NAME.fullmatch(key):\n", "        if False:\n", "detect"),
    "named(): NAME class for every key (no bracket exception)": (
        GATE, "        if not SCOPE_NAME.fullmatch(key):\n", "        if not NAME.fullmatch(key):\n", "detect"),
    "load(): endpoint names not held to NAME": (GATE, "for name in baseline[\"endpoints\"] if not NAME.fullmatch(name)]",
                                                "for name in baseline[\"endpoints\"] if False]", "detect"),
    "routing(): int() not whole()": (GATE, 'append(whole(value, f"route status row {label!a}"))',
                                     "append(int(value))", "detect"),
    "utilization(): float/int not real/whole": (GATE, "real(value, what) if \".\" in value else whole(value, what)",
                                                "float(value) if \".\" in value else int(value)", "detect"),
    "timing(): float() slack": (GATE, 'return {"WNS_ns": real(values[0], "WNS"), "WHS_ns": real(values[4], "WHS")}',
                                'return {"WNS_ns": float(values[0]), "WHS_ns": float(values[4])}', "detect"),
    "timing(): int() endpoint counts": (GATE, "    paths = [whole(value, name) for name", "    paths = [int(value) for name",
                                        "detect"),
    "hierarchy(): int() counts": (RANK, '(whole(value.strip(), f"hierarchy count of {key!a}") for value in fields[2:])',
                                  "(int(value.strip()) for value in fields[2:])", "detect"),
    "barrier holds: record() handler removed": (
        GATE, "    except (OSError, ValueError, KeyError, IndexError, TypeError, RecursionError) as error:\n"
              "        raise Refusal(f\"unreadable measurement",
        "    except ZeroDivisionError as error:\n        raise Refusal(f\"unreadable measurement", "hold"),
    "barrier holds: load() handler removed": (
        GATE, "    except (OSError, ValueError, RecursionError) as error:\n        raise Refusal(f\"baseline {path} is unreadable",
        "    except ZeroDivisionError as error:\n        raise Refusal(f\"baseline {path} is unreadable", "hold"),
}


def run(name: str) -> str:
    target, old, new, expect = MUTANTS[name]
    folder = SCRATCH / name.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_").replace(":", "")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for sibling in (GATE, RANK, "pp_resource_gate_selftest.py"):
        shutil.copy2(HERE / sibling, folder / sibling)
    if old is not None:
        source = (folder / target).read_text()
        if source.count(old) != 1:
            return f"NOT-APPLIED {name}: span found {source.count(old)} times"
        (folder / target).write_text(source.replace(old, new))
    results = []
    for cases in (500, 5000):
        fuzz = subprocess.run([sys.executable, "-B", "-c", f"import sys, pp_resource_gate as g; sys.exit(g.fuzz({cases}, 234))"],
                              cwd=folder, capture_output=True, text=True, timeout=1800)
        failures = next((line for line in fuzz.stdout.splitlines() if line.startswith("resource gate fuzz: ") and
                         "cases at seed" in line), fuzz.stderr.strip().splitlines()[-1:] or ["?"])
        results.append((cases, fuzz.returncode, failures if isinstance(failures, str) else failures[0]))
        if fuzz.returncode != 0 or expect == "hold":
            break
    selftest = subprocess.run([sys.executable, "-B", GATE, "--selftest"], cwd=folder, capture_output=True, text=True,
                              timeout=1800)
    detected = results[-1][1] != 0
    ok = detected == (expect == "detect")
    fuzz_text = "; ".join(f"fuzz{cases} rc={rc} [{line[-60:]}]" for cases, rc, line in results)
    return (f"{'ok ' if ok else 'BAD'} {name}: expected {expect}; {fuzz_text}; selftest rc={selftest.returncode}"
            f" ({'DETECTED' if selftest.returncode else 'passes'})")


def main() -> None:
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        lines = list(pool.map(run, MUTANTS))
    for line in lines:
        print(line)
    print(f"probe_r4_generative: {len(lines)} runs, {sum(line.startswith('BAD') for line in lines)} BAD, "
          f"{sum(line.startswith('NOT-APPLIED') for line in lines)} not applied")


if __name__ == "__main__":
    main()
