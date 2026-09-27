#!/usr/bin/env python3
"""Probe the argument-level profile checks in sw/litex/milan_soc.py main().

LiteX/migen are not required: main() is parsed with ast and its body is cut
right after the last bare-metal profile refusal (`if args.with_fpu or ...`),
then executed with argparse and a no-op LiteX builder_args stub. The probe
reports, per argv, whether argparse/ap.error refuses it or the arguments pass
every check that precedes elaboration. Usage: probe_milan_soc_args.py <repo>
"""
import argparse, ast, contextlib, io, os, sys
repo = sys.argv[1]
src = open(os.path.join(repo, "sw/litex/milan_soc.py"), encoding="utf-8").read()
tree = ast.parse(src)
main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
cut = None
for i, st in enumerate(main.body):
    if isinstance(st, ast.If) and "with_fpu" in ast.unparse(st.test):
        cut = i
        break
assert cut is not None, "profile refusal not found"
main.body = main.body[:cut + 1] + [ast.parse("return args").body[0]]
print("executed main() prefix ends at source line", main.body[cut].lineno,
      "->", ast.unparse(main.body[cut].test))
mod = ast.Module(body=[main], type_ignores=[])
ns = {"argparse": argparse, "os": os, "sys": sys,
      "builder_args": lambda ap: None}
# Module-level constants used as argparse defaults: execute each top-level
# assignment/import that does not need LiteX; skip the ones that fail.
skipped = 0
for st in tree.body:
    if isinstance(st, (ast.Assign, ast.AnnAssign, ast.Import, ast.ImportFrom)):
        try:
            exec(compile(ast.Module(body=[st], type_ignores=[]), "milan_soc_top", "exec"), ns)
        except Exception:
            skipped += 1
print("top-level statements skipped (need LiteX or unavailable):", skipped)
exec(compile(mod, "milan_soc_main_prefix", "exec"), ns)
BASE = ["--cpu", "vexiiriscv", "--software-profile", "baremetal", "--xlen", "32",
        "--full", "--with-spiflash", "--flashboot", "baremetal",
        "--l2-bytes", "0", "--cpu-count", "1", "--milan-clk-freq", "50e6"]
def with_(k, v=None):
    a = list(BASE)
    if k in a:
        j = a.index(k)
        if v is None: del a[j:j + 2]
        else: a[j + 1] = v
    else:
        a += [k] + ([v] if v is not None else [])
    return a
CASES = [
    ("baseline_50e6", BASE),
    ("milan_75e6", with_("--milan-clk-freq", "75e6")),
    ("milan_100e6", with_("--milan-clk-freq", "100e6")),
    ("milan_200e6_gt_sys", with_("--milan-clk-freq", "200e6")),
    ("milan_absent", with_("--milan-clk-freq", None)),
    ("sys_150e6", with_("--sys-clk-freq", "150e6")),
    ("with_fpu", BASE + ["--with-fpu"]),
    ("scala_noncache", BASE + ["--scala-args", "alu-count=1"]),
    ("l2_4096", with_("--l2-bytes", "4096")),
    ("xlen_64", with_("--xlen", "64")),
    ("cpu_count_2", with_("--cpu-count", "2")),
    ("naxriscv", with_("--cpu", "naxriscv")),
    ("flashboot_linux", with_("--flashboot", "linux")),
    ("flashboot_none", with_("--flashboot", "none")),
    ("profile_linux", with_("--software-profile", "linux")),
]
for name, argv in CASES:
    sys.argv = ["milan_soc.py"] + argv
    err = io.StringIO()
    try:
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            args = ns["main"]()
        print(f"{name:22s} ACCEPTED milan_clk_freq={args.milan_clk_freq} sys_clk_freq={args.sys_clk_freq}")
    except SystemExit as e:
        last = err.getvalue().strip().splitlines()[-1] if err.getvalue().strip() else ""
        print(f"{name:22s} REFUSED rc={e.code} {last[:150]}")
