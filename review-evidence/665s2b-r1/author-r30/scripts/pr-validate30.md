At this head (round 30) the full pass did not run (STOP). What ran on a clean clone of it:

```sh
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/plat-ledger --self-test
python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --ledgered-point 8x8-two-interfaces --output /tmp/fixture-8x8-if2 \
  --flash-map /tmp/plat-ledger/endstation_ax7101_8x8/split-soc/flash-map \
  --libc /tmp/plat-ledger/runtime/libc.a --compiler-runtime /tmp/plat-ledger/runtime/libcompiler_rt.a
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 sw/litex/test_ctrl_memory.py
python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test
```

Expected result at this head:
- `plat_ledger.py` exits 0 with four `POINT ... PASS` lines, the 8x8/2if one at 59.5 RAMB36 under `platform-8x8-two-interfaces`, and `plat_ledger controls: 7 of 7 as required`.
- The fixture link at 8x8/2if exits 2: `REFUSED: allocation over budget: 58.5 RAMB36 (rom 123808 bytes in 124928, sram 113168 bytes in 114688) exceeds the 58-RAMB36 budget ledgered for 8x8, two interfaces`.
- `load_grade.py --check`: `RESULT: PASS`, 0.486 and 0.483. `--selftest`: 25 of 25. `flip_grade.py --selftest`: 132 of 132.
- `test_ctrl_memory.py`: PASS. Hooks self-test: 28 of 28 checks, 96 of 96 mutants.

At items 1 to 3 (`e27a4540`, before the merge), the harness self-test reported 0 failures and 213 mutants caught, and `fw_coverage.py --check` passed over 39 files. The SRP control (`run.py --point 8x8 --variant answering-every-port --mutation srp-compared-by-memcmp`) printed `CONTROL srp-compared-by-memcmp caught` at `ef913ca4`.

The rest of this section is round 29's, at `b2d39235`:

