"""(#818) mutant_words.py <syn/ooc dir> <out.tsv>: run each route-set mutant and each rewritten mutant of
pp_resource_gate_mutants.py the way that harness does (a copy of the six modules, one span changed, the self-test
run) and record the self-test's exit status and the words of the failure that killed it.
"""
import concurrent.futures
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
REWRITTEN = ("all-fabric population not read", "all-fabric population judged in a printed record",
             "identical-input refusal", "identical-input figures", "timing floor", "timing floor boundary",
             "timing fall", "timing fall boundary", "route status of a route", "check reads the route status",
             "kind from the directory")
SIBLINGS = ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_resource_gate_selftest.py",
            "pp_resource_gate_set_selftest.py", "pp_placement.py", "pp_placement_selftest.py")
spec = importlib.util.spec_from_file_location("mutants", HERE / "pp_resource_gate_mutants.py")
mutants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutants)
table = {**{name: mutants.MUTANTS.get(name) or mutants.POPULATION_MUTANTS[name] for name in REWRITTEN},
         **mutants.SET_MUTANTS}


def words(text: str) -> str:
    """The failure's own words: the last AssertionError line, else the last non-empty line."""
    lines = [line for line in text.splitlines() if line.strip()]
    found = [line for line in lines if line.startswith("AssertionError")]
    return (found[-1] if found else lines[-1] if lines else "").replace("\t", " ")[:400]


def run(tmp: Path, name: str, change: tuple[str, str]) -> str:
    """Apply one mutant to a copy and run the self-test; return one TSV row."""
    folder = tmp / name.replace(" ", "_").replace("'", "")
    folder.mkdir()
    for sibling in SIBLINGS:
        shutil.copy2(HERE / sibling, folder / sibling)
    source = (HERE / "pp_resource_gate.py").read_text()
    if source.count(change[0]) != 1:
        return f"{name}\tNOT-UNIQUE\t"
    (folder / "pp_resource_gate.py").write_text(source.replace(*change))
    result = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                            capture_output=True, text=True, timeout=600)
    return f"{name}\t{result.returncode}\t{words(result.stdout + result.stderr)}"


with tempfile.TemporaryDirectory(prefix="mutant-words-") as tmp, \
        concurrent.futures.ThreadPoolExecutor(8) as pool:
    rows = list(pool.map(lambda item: run(Path(tmp), *item), table.items()))
OUT.write_text("mutant\tselftest rc\tfailing words\n" + "\n".join(rows) + "\n")
print(f"{len(rows)} mutants, {sum(1 for row in rows if row.split(chr(9))[1] not in ('0', 'NOT-UNIQUE'))} killed")
