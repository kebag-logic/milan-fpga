"""Drive the engine mutation arm's main() of two revisions over stubbed
controls that reach every branch of the per-mutant verdict code, and require
identical stdout, return code and stub call sequence.

usage: python3 -I verdict_equiv.py <old engine dir> <new engine dir>
No build or simulation runs: stage, generate_image, build and run_harness are
replaced; verdict() and everything after it are the revisions' own code.
"""
import contextlib, importlib.util, io, sys, tempfile
from pathlib import Path

P1 = "p1 255 "
TALLY_FAIL = "\n3 checks: 1 PASS, 2 FAIL\n"
# name -> (file, occurrences of the pattern, image ok, builds, rc, output, breaks)
G, RTL = "ucode/gen_gptp_ucode.py", "top/KL_gptp_engine.sv"
ROWS = [
    ("absent", RTL, 0, True, True, 1, "", "#82 a"),
    ("twice", RTL, 2, True, True, 1, "", "#82 a"),
    ("image refused", RTL, 1, False, True, 1, "", "#82 a"),
    ("no build", RTL, 1, True, False, 1, "", "#82 a"),
    ("generator, clean exe", G, 1, True, False, 1, "FAIL #82 a got 0 exp 1" + TALLY_FAIL, "#82 a"),
    ("survivor", RTL, 1, True, True, 0, "\n3 checks: 3 PASS, 0 FAIL\n", "#82 a"),
    ("masked", RTL, 1, True, True, 0, "FAIL x" + TALLY_FAIL, "#82 a"),
    ("abort", RTL, 1, True, True, 2, "no tally", "#82 a"),
    ("signal", RTL, 1, True, True, -11, "", "#82 a"),
    ("skipped", RTL, 1, True, True, 0, "SKIP: none", "#82 a"),
    ("plain catch", RTL, 1, True, True, 1, "FAIL other" + TALLY_FAIL, "an unnamed property"),
    ("slew named", RTL, 1, True, True, 1, "FAIL slew: s1 got 0\nFAIL slew: s1 again" + TALLY_FAIL, "slew: s1"),
    ("slew only in p1", RTL, 1, True, True, 1, f"FAIL {P1}slew: s1 got 0" + TALLY_FAIL, "slew: s1"),
    ("slew unrelated", RTL, 1, True, True, 1, "FAIL other" + TALLY_FAIL, "slew: s1"),
    ("82 all named", RTL, 1, True, True, 1, "FAIL #82 a got 0\nFAIL #82 b got 1\nFAIL #82 a dup" + TALLY_FAIL, "#82 a | #82 b"),
    ("82 one missing", RTL, 1, True, True, 1, "FAIL #82 a got 0" + TALLY_FAIL, "#82 a | #82 b | #82 c"),
    ("82 only in p1", RTL, 1, True, True, 1, f"FAIL {P1}#82 a got 0" + TALLY_FAIL, "#82 a"),
    ("p1 named", RTL, 1, True, True, 1, f"FAIL {P1}#82 a got 0\nFAIL #82 b" + TALLY_FAIL, f"{P1}#82 a | #82 b"),
    ("p1 only shipping", RTL, 1, True, True, 1, "FAIL p1 x " + f"{P1}#82 a" + TALLY_FAIL, f"{P1}#82 a"),
    ("82 not caught", RTL, 1, True, True, 0, "\n3 checks: 3 PASS, 0 FAIL\n", "#82 a | #82 b"),
]

def run(engine: Path, control_ok: bool):
    sys.path.insert(0, str(engine.parent.parent))
    spec = importlib.util.spec_from_file_location(f"m{id(engine)}{control_ok}", engine / "mutants.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    calls = []
    hdl = Path(tempfile.mkdtemp(prefix="hdl-"))
    rows = {}
    for i, (name, fname, count, img, builds, rc, out, breaks) in enumerate(ROWS):
        pat = f"PATTERN_{i}_"
        rows[name] = (fname, img, builds, rc, out)
    for fname in (G, RTL):
        (hdl / fname).parent.mkdir(parents=True, exist_ok=True)
        (hdl / fname).write_text("".join(f"PATTERN_{i}_" * r[2] + "\n"
                                         for i, r in enumerate(ROWS) if r[1] == fname))
    m.HDL = hdl
    by_tag = {"".join(c if c.isalnum() else "_" for c in r[0]): r for r in ROWS}
    def stage(work, tag, *edit):
        calls.append(("stage", tag, edit)); return Path(work) / f"src_{tag}"
    def generate_image(src, rundir):
        tag = src.name[4:]; calls.append(("image", tag, rundir.name))
        return True if tag == "clean" else by_tag[tag][3]
    def build(src, work, tag):
        calls.append(("build", tag))
        if tag == "clean": return Path("/exe/clean")
        return Path(f"/exe/{tag}") if by_tag[tag][4] else None
    def run_harness(exe, rundir):
        calls.append(("run", str(exe), rundir.name))
        if exe.name == "clean" and rundir.name == "run_clean":
            return (0, "\n3 checks: 3 PASS, 0 FAIL\n") if control_ok else (1, "FAIL c" + TALLY_FAIL)
        tag = rundir.name[4:]
        r = by_tag[tag]
        return r[5], r[6]
    m.stage, m.generate_image, m.build, m.run_harness = stage, generate_image, build, run_harness
    m.MUTATIONS = [(r[0], r[1], f"PATTERN_{i}_", "x", r[7]) for i, r in enumerate(ROWS)]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = m.main()
    sys.path.pop(0)
    return buf.getvalue(), rc, [c for c in calls]

old, new = Path(sys.argv[1]), Path(sys.argv[2])
ok = True
for control_ok in (True, False):
    a, b = run(old, control_ok), run(new, control_ok)
    same = a[0] == b[0] and a[1] == b[1] and [c[:2] for c in a[2]] == [c[:2] for c in b[2]]
    ok &= same
    print(f"== control {'passes' if control_ok else 'fails'}: rc old {a[1]} new {b[1]}; "
          f"stdout identical {a[0] == b[0]}; stub calls identical {[c[:2] for c in a[2]] == [c[:2] for c in b[2]]}")
    print(a[0])
print("EQUIVALENT" if ok else "DIFFERENT")
sys.exit(0 if ok else 1)
