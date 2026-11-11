"""For a checkout (argv[1]), report whether each of the composed OUTSIDE/SUITES entries is found by
ctrl_configs.held()'s text finder (builder_texts) and is a program, i.e. whether dropping the entry would
make the TSN stack boundary gate refuse it by name. Exit 1 if an entry is not load-bearing or is missing."""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_configs as c  # noqa: E402
KEYS = ["scripts/nvm_layout3.py", "scripts/nvm_klj3.py", "scripts/check_nvm_klj3.py",
        "scripts/nvm_format_32x32_tables.py", "tb/verilator/milan_dp/srptx_grade.py",
        "tb/verilator/milan_dp/srptx_mutants.py"]
texts = {c.rel(p): (p, t) for p, t in c.builder_texts(None).items()}
bad = 0
print(f"builders found by text: {len(texts)}; OUTSIDE {len(c.OUTSIDE)}; SUITES {len(c.SUITES)}; "
      f"BUILDERS {len(c.BUILDERS)}; PART_OF {len(c.PART_OF)}")
for k in KEYS:
    where = "OUTSIDE" if k in c.OUTSIDE else "SUITES" if k in c.SUITES else "NONE"
    found = k in texts
    prog = found and c.program(*texts[k])
    other = k in {b.path for b in c.BUILDERS} or k in c.PART_OF
    load = found and not other
    print(f"{k}: listed in {where}; found by text {found}; program {prog}; otherwise covered {other}; "
          f"load-bearing {load}")
    bad += where == "NONE" or not load
unlisted = [n for n, (p, t) in texts.items() if n not in c.OUTSIDE and n not in c.SUITES and n not in c.PART_OF
            and n not in {b.path for b in c.BUILDERS}]
print(f"found by text and in no registry: {unlisted}")
sys.exit(1 if bad else 0)
