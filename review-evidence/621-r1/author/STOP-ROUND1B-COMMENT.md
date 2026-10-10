[A576] STOP

Parent head: `034e2e30f225f3fcd755cac8ad01c60dda5b366a`.
Donor head: `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9` (unchanged).

The separate harness commit requested by the [round 1b ruling](https://github.com/kebag-logic/milan-fpga/issues/621#issuecomment-6087415319) is complete. Only `tb/verilator/nvm_capture_cpu/run.py` changed. The production bound remains 24.5 ms; byte-only retains the shared capture checks and 1.5x ratio. Both new fixtures pass: a valid 25 ms byte-only measurement is accepted, and the same production measurement is rejected. The existing three ratio/scenario controls pass. In-memory plants that restore the original timing defect or disable the production bound are both rejected. Python idiom and whitespace checks exit 0.

A required gate now needs another file outside the authorized scope:

```sh
python3 scripts/check_nvm_capture.py
```

It exits 1: `measurement harness changed; refresh measured evidence`. At `scripts/check_nvm_capture.py:61`, the gate hashes every harness Python/C++ file. `tb/verilator/nvm_capture_cpu/measurements.json:46` still pins the previous `run.py` hash. The resumed assignment authorizes the extra change in `run.py`; it does not authorize updating that receipt, and the ruling prohibits changing recorded measurements. Neither the receipt nor its enforcement was changed.

A scope decision on the receipt refresh is needed before the full bar can pass. The capture campaign, 61-suite sweep and vendor stages were not restarted after this STOP; no new measurement or complete gate pass is claimed. HANDOFF.md and PR-BODY.md contain the change, control coverage, gate result and both hashes. The worktrees are clean, no background jobs were started, and nothing was pushed or opened as a PR. The later physical repeat still closes #621.
