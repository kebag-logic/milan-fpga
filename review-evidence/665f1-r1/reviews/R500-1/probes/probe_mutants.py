#!/usr/bin/env python3
# R500-1 probe M: reviewer-planted defects, each graded by EVERY check of the
# lane's suite on every port the suite runs it on, at one shape. A defect no
# check reddens is a test gap. Usage: probe_mutants.py NAME [SHAPE]
from __future__ import annotations

import sys

from r500_common import bench, planted_tree

import test_ctrl_nvm  # noqa: E402  (the lane's driver: CHECKS, PORTS, grade)

STORE = "nvm_store.c"
LITESPI = "plat/nvm_flash_litespi.c"
MUTANTS = {
    # positive control: the lane's own no_verify seam, which its suite must catch
    "control_no_verify": [(STORE, "\t\tif (nvm_chunk[i] != nvm_stage[nvm.pos + i]) {", "\t\tif (0) {")],
    # the read-back skips the last stretch: a container whose trailer page did
    # not program would still move the authority
    "verify_skips_last_stretch": [(STORE,
        "\tfor (i = 0; i < n; ++i) {\n\t\tif (nvm_chunk[i] != nvm_stage[nvm.pos + i]) {",
        "\tfor (i = 0; i < n && nvm.pos + n < NVM_IMG_LEN; ++i) {\n\t\tif (nvm_chunk[i] != nvm_stage[nvm.pos + i]) {")],
    # the blank check reads only the first stretch of the erased slot
    "blankcheck_first_stretch_only": [(STORE,
        "\tnvm.pos += n;\n\tif (nvm.pos >= NVM_IMG_LEN) {\n\t\tnvm.pos = 0;\n\t\tnvm.st.phase = NVM_P_PROGRAM;",
        "\tnvm.pos = NVM_IMG_LEN;\n\tif (nvm.pos >= NVM_IMG_LEN) {\n\t\tnvm.pos = 0;\n\t\tnvm.st.phase = NVM_P_PROGRAM;")],
    # a sequence tie picks B instead of A (the stated tie rule inverted)
    "tie_picks_b": [(STORE, "((int32_t)(s->seq_a - s->seq_b) >= 0) ? 0 : 1;",
                     "((int32_t)(s->seq_a - s->seq_b) > 0) ? 0 : 1;")],
    # the LiteSPI port's time follows a backward PHC step instead of holding
    "time_not_held": [(LITESPI, "\tif (now < ls_last_us)\n\t\treturn ls_last_us;\n", "")],
    # a failed attempt no longer marks the claim stale
    "fail_not_stale": [(STORE, "\tnvm.st.stale = 1;\n\tif (nvm.st.attempts", "\tif (nvm.st.attempts")],
    # the program step ignores a refused page program
    "program_refusal_ignored": [(STORE,
        "\tif (f->program(f->ctx, nvm_slot_addr(nvm.target) + nvm.pos, nvm_stage + nvm.pos, n)) {\n\t\tnvm_fail(NVM_VD_PROGRAM);\n\t\treturn;\n\t}",
        "\t(void)f->program(f->ctx, nvm_slot_addr(nvm.target) + nvm.pos, nvm_stage + nvm.pos, n);")],
}



def main() -> None:
    name = sys.argv[1]
    stem = sys.argv[2] if len(sys.argv) > 2 else "endstation_ax7101_1x1_tdm8"
    tree = planted_tree(f"mut_{name}", MUTANTS[name])
    b = bench(stem, f"mut_{name}", tree)
    if test_ctrl_nvm.table_exists(stem):
        from nvm_bench import VECTOR_IDENT, make_bench
        from r500_common import SCRATCH, inputs
        b.vector = make_bench(inputs(stem), SCRATCH / "bench" / f"mut_{name}" / "vector", tree, VECTOR_IDENT)
    result = test_ctrl_nvm.grade(b, list(test_ctrl_nvm.CHECKS))
    red = {k: v for k, v in result.items() if v}
    print(f"MUTANT {name} shape={stem} reddened={len(red)} of {len(result)}: {sorted(red)}")
    for k, v in sorted(red.items()):
        print(f"  {k}: {v[0][:160]}")
    print("SURVIVED" if not red else "CAUGHT")


if __name__ == "__main__":
    main()
