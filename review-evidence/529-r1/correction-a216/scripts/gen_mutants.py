#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""[A216] #529: write the mutant copies of hdl/milan/milan_datapath.sv.

Three sets, each a disposable copy with exact-text edits. Every anchor must
match exactly once, so no mutant can silently be a copy of the original.

  pw_<a>_<b>   all 45 pairwise exchanges of the ten KL_crf_rx Table 5.16
               output bindings at the instance port map (the mux untouched)
  r269/<id>    the external reviewer's set, written by their archived
               make_mutants.py (mx1-mx4, ma1-ma7)
  r268/<id>    the internal reviewer's set, written by their archived
               mutants.py make_copy() (ctl_marked, a1-a8, p1-p5, r1-r7)

usage: gen_mutants.py <milan_datapath.sv> <reviewer-scripts dir> <outdir>
"""
import hashlib
import importlib.util
import itertools
import pathlib
import subprocess
import sys

# the ten tally bindings, exactly as the port map spells them at the head
PORTS = [
    ("pdu", ".pdu_count_o (", "crf_pducnt_w"),
    ("fmt", ".fmt_err_o   (", "crf_fmterr_w"),
    ("seq", ".seq_err_o   (", "crf_seqerr_w"),
    ("mr", ".mr_cnt_o    (", "crf_mrcnt_w"),
    ("tu", ".tu_cnt_o    (", "crf_tucnt_w"),
    ("late", ".late_cnt_o  (", "crf_latecnt_w"),
    ("early", ".early_cnt_o (", "crf_earlycnt_w"),
    ("lock", ".cnt_locked_o   (", "crf_lockcnt_w"),
    ("unlock", ".cnt_unlocked_o (", "crf_unlockcnt_w"),
    ("intr", ".cnt_intr_o     (", "crf_intrcnt_w"),
]


def apply(src, edits):
    text = src
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"anchor matched {n} times: {old!r}")
        text = text.replace(old, new)
    if text == src:
        raise SystemExit("an edit set left the source unchanged")
    return text


def write(out, name, text, manifest):
    path = out / f"{name}.sv"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    manifest.append(f"{name} {hashlib.sha256(text.encode()).hexdigest()}")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    src_path = pathlib.Path(sys.argv[1])
    rs = pathlib.Path(sys.argv[2])
    out = pathlib.Path(sys.argv[3])
    src = src_path.read_text(encoding="utf-8")
    manifest = ["# name sha256"]

    for (na, pa, wa), (nb, pb, wb) in itertools.combinations(PORTS, 2):
        edits = [(f"{pa}{wa}),", f"{pa}{wb}),"), (f"{pb}{wb}),", f"{pb}{wa}),")]
        write(out, f"pw_{na}_{nb}", apply(src, edits), manifest)

    # the external reviewer's generator, run as archived
    r269 = out / "r269"
    subprocess.run([sys.executable, str(rs / "make_mutants.py"), str(src_path),
                    str(r269)], check=True, stdout=subprocess.DEVNULL)
    for p in sorted(r269.glob("*.sv")):
        manifest.append(f"r269/{p.stem} "
                        f"{hashlib.sha256(p.read_bytes()).hexdigest()}")

    # the internal reviewer's copy builder, imported as archived
    m268 = load(rs / "mutants.py", "r268_mutants")
    for mid, (_desc, edits) in m268.MUTANTS.items():
        write(out, f"r268/{mid}", m268.make_copy(src, edits), manifest)

    (out / "MUTANTS.sha256").write_text("\n".join(manifest) + "\n",
                                        encoding="utf-8")
    print("\n".join(manifest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
