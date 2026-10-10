[A576] STOP

Parent head: `034e2e30f225f3fcd755cac8ad01c60dda5b366a`.
Donor head: `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`.
Both are unchanged. No round 1c commit was made.

The [round 1c ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6087498843) requires every production value to remain byte-identical and explicitly requires STOP otherwise. A fresh production run violates that condition.

Case: `endstation_ax7101_1x1_tdm8`, CPU 50 MHz, system 100 MHz, traffic ON, mutation none, 16 captures requested. The run rebuilt at the current parent head with the pinned donor and required environment. These are the complete before/after rows for capture 2:

| Source | index | ok | sys_cycles | raw | records | mismatches | open | requests | responses | reads |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Committed receipt | 2 | 1 | 396442 | 3290 | 54 | 0 | 0 | 24691 | 26 | 1006 |
| Fresh production run | 2 | 1 | 396442 | 3290 | 54 | 0 | 0 | 24690 | 26 | 1006 |

The recorded counter is at `tb/verilator/nvm_capture_cpu/measurements.json:95`. The new value also matches the saved earlier candidate run. The product firmware source and rebuilt BIOS match the committed receipt's hashes. The cause of the request-count difference is not established.

Reproduction, with the capture recipe's offline environment and external results directory:

```sh
unshare -Urn "$PRODUCT_PYTHON" tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic on --mutation none --build-dir "$RESULTS/round1c-capture/1x1-50-on"
```

The owned campaign was terminated after detecting the mismatch. Four complete rows were captured; cancellation is recorded as 143, and the production-value comparison exits 1. This is not a completed campaign or a gate pass. The remaining capture arms, 61-suite sweep and vendor stages were not started in this round.

The receipt and `scripts/check_nvm_capture.py` remain unchanged. Receipt diff: 0 added lines, 0 deleted lines. Its SHA-256 remains `ed871bdd09bde7ebde1ae021cd647e3cad354d3f8682c5b7308cda91e4cbd72a`. No aggregate refresh was performed.

HANDOFF.md and PR-BODY.md are updated. The local evidence includes the raw capture, complete before/after rows, input hashes, cancellation record and SHA-256/size receipts for larger artifacts. Both worktrees are clean, no validation job remains, and nothing was pushed or opened as a PR. The complete local bar remains blocked. The later physical repeat still closes #621.
