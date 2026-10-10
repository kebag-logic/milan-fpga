[A576] STOP

Parent head: `034e2e30f225f3fcd755cac8ad01c60dda5b366a`.
Donor head: `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`.
Both are unchanged. No round 1d commit was made.

The attribution required by the [round 1d correction](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6087655217) returns `requests=24690` at capture 2. That run uses the original parent base `5603c353137e90c1fa95429f6d00ef7a2298d9ee` with original donor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`. The correction classifies this result as harness drift and requires STOP.

The receipt and its recipe (`tb/verilator/nvm_capture_cpu/README.md:158`) name Verilator 5.052, not the pinned 5.050. The arm was therefore run on both simulators, with the receipt's own measured tree added as a positive control. Every run uses the same case: `endstation_ax7101_1x1_tdm8`, CPU 50 MHz, system 100 MHz, aligned edges, traffic ON, mutation none, 16 captures.

| Run | Simulator | Capture 2 requests | Rows differing from receipt |
|---|---|---:|---|
| Committed receipt, `measurements.json:95` | 5.052 | 24691 | (reference) |
| Receipt's measured tree `a2f17342`, protocol pin `b2db3a97` | 5.052 | 24691 | none of 16 |
| Original base, protocol pin `2ad2f845` | 5.050 | 24690 | 1 of 3 observed; cancelled, 143 |
| Original base | 5.052 | 24690 | 9 of 16 |
| Candidate | 5.052 | 24690 | the same 9 of 16 |

Only `requests` differs, by ±1. Every other row field equals the receipt in every observed row: `ok`, `sys_cycles`, `raw`, `records`, `mismatches`, `open`, `responses` and `reads`. Minimum, maximum and margin are also unchanged. All three 16-capture runs exit 0.

The source is now established:
- The measured tree reproduces all 16 receipt rows and summary fields. The receipt faithfully records that tree.
- The simulator version is not the cause. 5.050 and 5.052 rows agree wherever both were observed.
- The donor fix is not the cause. Base and candidate write byte-identical capture logs, although their gPTP ROMs differ (`78c8418a…` vs `fd3dad06…`).
- Between `a2f17342` and the base, 30 of the capture SoC's 116 source files changed on dev. Seven are parent RTL files, including `milan_datapath.sv`, `KL_maap.sv` and `KL_nvm_backend.sv`. The other 23 are protocol-processor files, from pin `b2db3a97` to `2ad2f845`. The harness, firmware and BIOS are unchanged. `scripts/check_nvm_capture.py` does not hash that RTL, so it cannot flag this drift. No single commit was isolated.

A refresh needs a disposition of this dev drift. It would also change receipt fields that neither ruling lists:
- each arm's `gptp_ucode_sha256`;
- `processor_pins`;
- the `base`, `tree`, `date` and `provenance` fields, which name `a2f17342`;
- `simulator`, recorded as 5.052 while the assignment pins 5.050.

Reproduce from each clean checkout. Use the recipe's offline environment with networking disabled and Verilator 5.052 first on `PATH`:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir "$RESULTS/1x1-50-on"
```

The receipt and its input gate are unchanged. The receipt diff has 0 added and 0 deleted lines, and its SHA-256 remains `ed871bdd09bde7ebde1ae021cd647e3cad354d3f8682c5b7308cda91e4cbd72a`. The remaining capture arms, controls, 61-suite sweep and vendor stages were not started.

HANDOFF.md and PR-BODY.md are updated. They hold the row-by-row deltas, the per-file source list and size/SHA-256 receipts. The worktrees are clean, no validation job remains, and nothing was pushed or opened as a PR. The later physical repeat still closes #621.
