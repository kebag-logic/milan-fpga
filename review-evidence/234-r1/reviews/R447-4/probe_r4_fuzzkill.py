#!/usr/bin/env python3
"""Would the round-4 generative test alone catch a removed barrier, converter or name rule?

Usage: probe_r4_fuzzkill.py <repo checkout> <scratch dir> [jobs]
Each mutant edits exactly one unique span of a copy of pp_resource_gate.py or
pp_baseline_rank.py (with the self-test beside them). For each mutant three runs:
  fuzz500  - gate.fuzz(500, 234) alone, the self-test's generated block
  fuzz5k   - gate.fuzz(5000, 447) alone, a second seed
  selftest - the shipped --selftest (arms and the 500 cases)
A run that exits 0 did not detect the mutant. The script never writes inside the checkout.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess
import sys

GATE, RANK, SELF = "pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py"
MUTANTS = {
    "barrier catches Refusal only": (GATE, "    except Exception as error:  # the barrier",
                                     "    except Refusal as error:  # the barrier"),
    "barrier returns 1": (GATE, "        return 2\n\n\nif __name__", "        return 1\n\n\nif __name__"),
    "check-baseline problems exit 1": (GATE, "            return 2 if problems else 0", "            return 1 if problems else 0"),
    "whole() unbounded": (RANK, 'f"[0-9]{{1,{DIGITS}}}"', '"[0-9]+"'),
    "whole() takes any int() text": (RANK, "    if not re.fullmatch((", "    if False and not re.fullmatch(("),
    "real() keeps non-finite": (GATE, "    if not math.isfinite(value):", "    if False:"),
    "JSON ints bypass whole()": (GATE, "parse_int=integer)", "parse_int=int)"),
    "JSON floats bypass real()": (GATE, "parse_float=decimal,", "parse_float=float,"),
    "duplicate keys kept": (GATE, "        if key in table:", "        if False:"),
    "key name class removed": (GATE, "        if not SCOPE_NAME.fullmatch(key):", "        if False:"),
    "brackets allowed in endpoint names": (GATE, 'for name in baseline["endpoints"] if not NAME.fullmatch(name)]',
                                           'for name in baseline["endpoints"] if not SCOPE_NAME.fullmatch(name)]'),
    "policy figure names unchecked": (GATE, "        elif not all(NAME.fullmatch(figure) for figure in entry.get(field, {})):",
                                      "        elif False:"),
    "emit prints raw": (GATE, '    print("".join(char if char == "\\n" or " " <= char <= "~" else ascii(char)[1:-1] for char in text))',
                        "    print(text)"),
    "route status via int()": (GATE, 'whole(value, f"route status row {label!a}")', "int(value)"),
    "timed endpoints via int()": (GATE, "paths = [whole(value, name)", "paths = [int(value)"),
    "utilization count via int()": (GATE, "else whole(value, what)", "else int(value)"),
    "half tile via float()": (GATE, 'real(value, what) if "." in value', 'float(value) if "." in value'),
    "hierarchy count via int()": (RANK, '(whole(value.strip(), f"hierarchy count of {key!a}")', "(int(value.strip())"),
    "slack via float()": (GATE, 'return {"WNS_ns": real(values[0], "WNS"), "WHS_ns": real(values[4], "WHS")}',
                          'return {"WNS_ns": float(values[0]), "WHS_ns": float(values[4])}'),
    "budget cell via float()": (GATE, 'real(value[1], f"budget policy cell {cell!r}")', "float(value[1])"),
    "manifest via json.loads": (GATE, "    images = strict(", "    images = json.loads("),
    "unknown endpoint refusal removed": (GATE, '        if args.command == "check" and args.endpoint not in baseline["endpoints"]:',
                                         "        if False:"),
    "record catch narrowed to OSError": (GATE, "    except (OSError, ValueError, KeyError, IndexError, TypeError, RecursionError) as error:",
                                         "    except OSError as error:"),
}
RUNS = {
    "fuzz500": ["-c", "import sys, pp_resource_gate as g; sys.exit(g.fuzz(500, 234))"],
    "fuzz5k": ["-c", "import sys, pp_resource_gate as g; sys.exit(g.fuzz(5000, 447))"],
    "selftest": [GATE, "--selftest"],
}


def run(name, target, spans, here, tmp):
    folder = tmp / name.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    for module in (GATE, RANK, SELF):
        shutil.copy(here / module, folder / module)
    text = (folder / target).read_text()
    if text.count(spans[0]) != 1:
        return name, {"apply": f"NOT-UNIQUE ({text.count(spans[0])})"}
    (folder / target).write_text(text.replace(*spans))
    out = {}
    for label, argv in RUNS.items():
        result = subprocess.run([sys.executable, "-B", *argv], capture_output=True, text=True, timeout=1800,
                                cwd=folder)
        lines = (result.stdout + result.stderr).strip().splitlines()
        tail = next((line for line in reversed(lines) if "Error" in line or "FAILURE" in line or "failures" in line),
                    lines[-1] if lines else "")
        out[label] = ("DETECTED" if result.returncode else "passed", result.returncode, tail[:200])
    return name, out


def main():
    here = Path(sys.argv[1]).resolve() / "syn/ooc"
    tmp = Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    control = run("control", GATE, ("BASELINE = ", "BASELINE = "), here, tmp)
    print("control: " + ", ".join(f"{k} rc={v[1]}" for k, v in control[1].items()))
    if any(v[1] != 0 for v in control[1].values()):
        sys.exit("the unmutated control must pass every run")
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda item: run(item[0], item[1][0], item[1][1:], here, tmp), MUTANTS.items()))
    for name, out in results:
        if "apply" in out:
            print(f"{name}: {out['apply']}")
            continue
        print(f"{name}: " + "; ".join(f"{k} {v[0]} rc={v[1]}" for k, v in out.items()))
        for k, v in out.items():
            print(f"    {k}: {v[2]}")
    selftest_killed = sum(1 for _, out in results if out.get("selftest", ("",))[0] == "DETECTED")
    fuzz_any = sum(1 for _, out in results if "apply" not in out and
                   (out["fuzz500"][0] == "DETECTED" or out["fuzz5k"][0] == "DETECTED"))
    print(f"round-4 structural mutants: {len(results)}; self-test killed {selftest_killed}; "
          f"generative block alone detected {fuzz_any}")


if __name__ == "__main__":
    main()
