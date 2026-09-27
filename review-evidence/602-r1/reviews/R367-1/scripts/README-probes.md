# R367-1 probe scripts

All probes run on disposable copies. Nothing here edits the reviewed checkout.

## Probe tree

Clone the review checkout with `--shared`, detach it at `49012143b335ea48d6a71c441a05d0c1796887ff`, and clone each submodule at its gitlink:

- `gptp-processor` at `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`
- `protocol-processor` at `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`
- `third_party/verilog-axis` at `48ff7a7e2ef782cf778d47910cf85835c64b1bce`

Do the same for a base tree at `6d5ebd7357c1e468e446f18a61527c5be6118a04`. Set `VERILATOR` to a Verilator 5.050 binary.

## Commands

- `make -C TREE/tb/verilator/milan_dp gmstep` runs the clean leg.
- `TREE/tb/verilator/milan_dp/obj_gmstep/Vmilan_dp_gmstep obj_gmstep/aemi.bin D` runs one feed delay; the sweep ran D = 0..41, 8 at a time.
- `python3 run_mutants.py TREE WORK RECEIPTS --clean` builds the positive controls.
- `python3 run_mutants.py TREE WORK RECEIPTS --set author --only 0,...,7` runs the lane's inventory; run it again for 8,...,15.
- `python3 run_mutants.py TREE WORK RECEIPTS --set reviewer` runs the reviewer's mutants RV1-RV7.
- `python3 pin_probe.py TREE/hdl/milan/milan_datapath.sv PLANTED...` checks copies against the builder pin.
- `bash cone_synth.sh TREE OUTDIR` needs `sv2v` and `yosys`.
- `python3 artifact_identity.py BASE_TREE HEAD_TREE OUTDIR` compares the generated artifacts.
- `make -C TREE/tb/verilator/tkdiag` runs the tkdiag suite.
- `python3 TREE/scripts/lint_rtl.py --check --jobs 8 --verilator $VERILATOR` runs the lint gate.

## Stale-document scan (F1/F2)

Run from the checkout root, excluding submodules and `docs/history/**`:

```sh
grep -rn -i -E "(step|settime|adjtime|re-?base)[^|]{0,80}\b(mr\b|MEDIA_RESET|media.clock restart)|(\bmr\b|MEDIA_RESET)[^|]{0,80}(PHC step|settime|adjtime|re-?base)" \
  --include=*.md --include=*.py --include=*.sv --include=*.cpp --include=Makefile . \
  | grep -v -E '^\./(external|third_party|protocol-processor|gptp-processor)/' | grep -v '#602'
```

Separately, check `docs/testing/TESTING.md` against `gmstep_mutants.py` `CONTROLS`.

Redaction: in receipts/gmstep_clean_delay0.log and receipts/tkdiag.log the host path of the pinned Verilator 5.050 image root is replaced by $PINNED_VERILATOR_IMAGE; nothing else is altered.
