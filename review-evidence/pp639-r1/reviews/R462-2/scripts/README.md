# Reviewer scripts, R462-2 (processor PR #155, milan-fpga #639)

Every probe runs on a tree exported with `git archive <rev> | tar -x`, never on a checkout,
and writes only under the directories it is given. Builds need Verilator 5.050 first on PATH.

| Script | What it does |
|---|---|
| `bin/verilator` | Runs the pinned Verilator 5.050 (`PINNED_VERILATOR`, default `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`). The only change it makes is to cap a build's own `-j 0` at `VJOBS` (default 2), so that concurrent builds stay inside the reviewer's budget. Put `bin/` first on PATH. |
| `launch.sh LOGDIR NAME CMD...` | Starts one command detached, writing `NAME.log`, `NAME.time` (`/usr/bin/time -v`) and, when the command ends, `NAME.rc`. |
| `aq_gen_mutant.sh HDL_TREE TB_TREE WORK NAME TABLE_PY` | Copies `hdl/` from HDL_TREE and `tb/common`, `tb/pp_top` from TB_TREE. It plants control NAME from TABLE_PY's `MUTANTS` table (`name -> (old, new)`, exactly one occurrence in `protocol_processor_top.sv`) and builds `make gsi-build`. Then it runs `--arm-queue-only`. NAME `none` plants nothing. TABLE_PY is R462-1's `scripts/lockstep_armq/gen.py`, imported unchanged, or `own_mutants.py`. |
| `own_mutants.py` | Six further arm-queue controls, outside `acmp_mutants.py`: count or drop counter not reset, saturation at 0xFFFE, a full pop+push writing one past the head, a drop counted on a full face that pops, and a write-first read on a full pop+push. |
| `edit_identity.py TREE GEN_PY` | Checks that each `armq_*` arm in `tb/pp_top/acmp_mutants.py` plants a top byte-identical to the one the matching `gen.py` control plants. |

R462-1's `scripts/aq_probe.sh` and `scripts/lockstep_armq/gen.py` are used unchanged from
milan-fpga `pp639-review-evidence` `b95bc644` (`review-evidence/pp639-r1/reviews/R462-1/scripts/`).

## Reproducing

```sh
P=<this packet>; export PATH=$P/scripts/bin:$PATH
git -C <processor> archive 1cba30c9 | tar -x -C head
git -C <processor> archive 07b1469 | tar -x -C main      # main's RTL (the shift queue)
git -C <processor> archive 9e869910 | tar -x -C r1       # the round-1 bench (red proof)
GEN=<R462-1>/scripts/lockstep_armq/gen.py
bash <R462-1>/scripts/aq_probe.sh head w/probe-write_refused write_refused   # expect rc 1, AQ3
bash <R462-1>/scripts/aq_probe.sh head w/probe-wr_wrap_hi wr_wrap_hi         # expect rc 1, AQ3
$P/scripts/aq_gen_mutant.sh head head w/gen-X X $GEN    # X in gen.py MUTANTS: rc 1 except hd_not_reset
$P/scripts/aq_gen_mutant.sh main head w/main none $GEN  # rc 0, same AQ lines as head
$P/scripts/aq_gen_mutant.sh head r1 w/r1-X X $GEN       # the four full-queue controls: rc 0 (AQ 2 of 2)
$P/scripts/aq_gen_mutant.sh head head w/own-Y Y $P/scripts/own_mutants.py
python3 $P/scripts/edit_identity.py head $GEN
python3 head/tb/pp_top/acmp_mutants.py --output w/acmp --verilator $P/scripts/bin/verilator --jobs 7
```

The published lockstep benches (milan-fpga `b95bc644`,
`review-evidence/pp639-r1/author-r2/lockstep/`) were regenerated with their own README's
steps. The arm-port matrix was then re-run with `dut.sv` and the controls re-cut from the
`1cba30c9` top, using `VALIDATION_STORAGE` pointed at an export of `5c71928a` for the
redacted `build.sh` path.
