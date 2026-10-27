#!/usr/bin/env python3
"""Run selected engine mutants in parallel against a disposable copy of the tree.

usage: probe_mutants.py TREE OUTDIR JOBS [receipt|own|all]
Reuses the tree's own mutants.py staging/build/grading; each mutant's
verdict text goes to OUTDIR/<tag>.txt and a summary TSV to OUTDIR/summary.tsv.
"""
import contextlib, io, sys, tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

tree, outdir, jobs, which = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
eng = tree / "tb/verilator/engine"
sys.path.insert(0, str(eng))
import mutants as M  # noqa: E402
from mutation_verdict import verdict  # noqa: E402

G = "ucode/gen_gptp_ucode.py"
OWN = [
    ("OWN1 the asCapable rise keeps the aged mark", G,
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_SRTO, fmt=FMT_Q)\n    p.emit(\"BR\", label=\"done\")\n",
     "    p.emit(\"BR\", label=\"done\")\n", ""),
    ("OWN2 the gmPresent threshold is priority1 254", G,
     "SRTO_PASSED_C = 0xFF << 16\n", "SRTO_PASSED_C = 0xFE << 16\n", ""),
    ("OWN3 a master pair keeps the aged mark", G,
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_SRTO, fmt=FMT_Q)     # not aged\n",
     "", ""),
    ("OWN4 a Sync is taken on an incapable port", G,
     "    p.emit(\"CMP\", ra=RT, rb=0, fmt=FMT_D, imm=0)\n    p.emit(\"BRS\", cnd=BRS_Z, label=\"out\")\n    p.emit(\"WRST\", ra=RTS0, imm=RG_SCR | S_SYNCTS, fmt=FMT_Q)\n",
     "    p.emit(\"CMP\", ra=RT, rb=0, fmt=FMT_D, imm=0)\n    p.emit(\"WRST\", ra=RTS0, imm=RG_SCR | S_SYNCTS, fmt=FMT_Q)\n", ""),
]

def one(args):
    work, clean_exe, mut = args
    tag = "".join(c if c.isalnum() else "_" for c in mut[0])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        if mut[4]:
            ok = M.run_mutant(Path(work), Path(clean_exe), mut)
            res = "CAUGHT" if ok else "NOT-CAUGHT"
        else:
            # own probe: no named check; report raw verdict and the failing lines
            src = (M.HDL / mut[1]).read_text()
            if src.count(mut[2]) != 1:
                res = f"PATTERN-COUNT-{src.count(mut[2])}"
            else:
                sd = M.stage(Path(work), tag, (mut[1], mut[2], mut[3]))
                rd = Path(work) / f"run_{tag}"
                if not M.generate_image(sd, rd):
                    res = "GENERATOR-REFUSED"
                else:
                    rc, out = M.run_harness(Path(clean_exe), rd)
                    res = verdict(rc, out).upper()
                    print("\n".join([l for l in out.splitlines() if l.startswith("FAIL ")][:40]))
                    print(out.splitlines()[-1] if out else "")
    (outdir / f"{tag}.txt").write_text(f"{mut[0]}\n{res}\n{buf.getvalue()}")
    return mut[0], res

def main():
    outdir.mkdir(parents=True, exist_ok=True)
    sel = {"receipt": M.RECEIPT_MUTATIONS, "own": OWN, "all": list(M.RECEIPT_MUTATIONS) + OWN}[which]
    with tempfile.TemporaryDirectory(prefix="r720-mut-", dir=str(outdir.parent)) as td:
        w = Path(td)
        cs = M.stage(w, "clean"); cr = w / "run_clean"; ce = M.build(cs, w, "clean")
        assert ce and M.generate_image(cs, cr), "clean build failed"
        ctl = verdict(*M.run_harness(ce, cr))
        rows = [("CONTROL unmutated", ctl.upper())]
        with ProcessPoolExecutor(jobs) as ex:
            rows += list(ex.map(one, [(str(w), str(ce), m) for m in sel]))
    (outdir / "summary.tsv").write_text("".join(f"{n}\t{r}\n" for n, r in rows))
    print("".join(f"{n}\t{r}\n" for n, r in rows))

if __name__ == "__main__":
    main()
