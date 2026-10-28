"""Run the engine mutation arm of an FPGA-gPTP tree in parallel.

usage: python3 engine_arm_parallel.py <tree> <outdir> <jobs>
Uses the arm's own MUTATIONS, stage/build/generate_image/run_harness,
verdict and named_verdict. Per mutant it records the arm's own answer and a
STRICT answer: every " | "-separated name in `breaks` must appear in a FAIL
line of the matching pass (the arm's _named_failure). STRICT is reported for
every mutant whose breaks are check names, including any the arm grades
leniently. Writes <outdir>/<idx>.log (all FAIL lines) and summary.tsv.
"""
import contextlib, io, importlib.util, sys, tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

tree, outdir, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), int(sys.argv[3])
spec = importlib.util.spec_from_file_location(
    "engine_mutants", tree / "tb/verilator/engine/mutants.py")
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
WORK = Path(tempfile.mkdtemp(prefix="emut-"))  # under $TMPDIR
STRICT_PREFIX = ("#82 ", "#84 ", "#85 ", "#88 ", M.P1_PREFIX)


def clean():
    src = M.stage(WORK, "clean")
    exe = M.build(src, WORK, "clean")
    ok = exe is not None and M.generate_image(src, WORK / "run_clean")
    rc, out = M.run_harness(exe, WORK / "run_clean")
    return exe, M.verdict(rc, out), out


def one(args):
    idx, mut, clean_exe = args
    name, fname, pattern, replacement, breaks = mut
    edits = M.edits_of(pattern, replacement)
    src = (M.HDL / fname).read_text(encoding="utf-8")
    if any(src.count(p) != 1 for p, _ in edits):
        return idx, name, "stale-pattern", "n/a", "n/a", breaks, ""
    tag = f"m{idx:03d}"
    srcdir = M.stage(WORK, tag, (fname, edits))
    rundir = WORK / f"run_{tag}"
    if not M.generate_image(srcdir, rundir):
        return idx, name, "image-refused", "n/a", "n/a", breaks, ""
    exe = clean_exe if fname == M.GENERATOR else M.build(srcdir, WORK, tag)
    if exe is None:
        return idx, name, "no-build", "n/a", "n/a", breaks, ""
    rc, out = M.run_harness(exe, rundir)
    base = M.verdict(rc, out)
    with contextlib.redirect_stdout(io.StringIO()):
        arm = M.named_verdict(base, breaks, out)
    failed = [l for l in out.splitlines() if l.startswith("FAIL ")]
    names = breaks.split(" | ")
    is_named = breaks.startswith(STRICT_PREFIX) or breaks.startswith("#87 ")
    if is_named:
        missed = [w for w in names if M._named_failure(failed, w) is None]
        strict = "all-named-fail" if (base == "caught" and not missed) else \
                 ("missed: " + "; ".join(missed) if missed else base)
    else:
        strict = "prose-breaks"
    graded = "strict" if breaks.startswith(STRICT_PREFIX) else (
        "slew" if breaks.startswith("slew:") else "any-failure")
    tally = next((l for l in out.splitlines() if " checks: " in l), "")
    (outdir / f"{idx:03d}.log").write_text(
        f"mutant: {name}\nfile: {fname}\nbreaks: {breaks}\narm grading: {graded}\n"
        f"arm answer: {arm}\nstrict answer: {strict}\n{tally}\n" + "\n".join(failed) + "\n")
    return idx, name, arm, graded, strict, breaks, tally


if __name__ == "__main__":
    outdir.mkdir(parents=True, exist_ok=True)
    exe, ans, out = clean()
    (outdir / "000-clean.log").write_text(out)
    print("clean:", ans, flush=True)
    jobs_list = [(i + 1, m, exe) for i, m in enumerate(M.MUTATIONS)]
    rows = []
    with ProcessPoolExecutor(max_workers=jobs) as ex:
        for r in ex.map(one, jobs_list):
            rows.append(r)
            print(r[0], r[1], "|", r[2], "|", r[3], "|", r[4], flush=True)
    with open(outdir / "summary.tsv", "w") as f:
        f.write("idx\tmutant\tarm_answer\tarm_grading\tstrict_answer\ttally\n")
        for r in rows:
            f.write(f"{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}\t{r[6]}\n")
    caught = sum(r[2] == "caught" for r in rows)
    print(f"clean={ans} mutants={len(rows)} arm-caught={caught}", flush=True)
    sys.exit(0 if ans == "pass" and caught == len(rows) else 1)
