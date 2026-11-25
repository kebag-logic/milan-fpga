[A839] REVIEW READY
Commit: 9c62539365fea8316dae2b9fd7c68defeff5cb31
Changed: nine commits on `fcbc31f3` (PR #1001, now merged into `dev-soft-core` as `2f2a8152`). They run the Verilator preflight once per head, start each CI piece's longest case first, stage mutants at stable paths with one lock per slot, re-deal the Verilator sweep onto 26 workers within 1276 s each (leg A stated, #737), add `follow_ring`/`media_phase` as CI cases, and split rtl-fast's `firmware-boundary` into two capture legs and a judge. No RTL, firmware, test expectation or graded figure changed. Nothing changed since the round-6 head: this round explains a receipt difference and records the manager's ruling on the bound.
Validation:
- Local gates: 37 of 37 commands rc 0 at the head in a clean clone. The list is in the PR body's "How to validate", and it includes `python3 scripts/suite_shards.py --selftest`, `python3 scripts/ci_events.py --selftest` (5967 arms), `python3 scripts/ci_suite_pieces_selftest.py`, `python3 scripts/ci_gate_workflows.py --check` and `python3 scripts/check_py_idiom.py`.
- Hosted at the head: rtl-full 45528738040, rtl-fast 45528738009, elaborate 45528738049 and docs 45528737977, all success on their first attempt.
- Receipts against one base, for `milan_dp`'s `gptp`/`gptp-lat`:
  - Six local trees: the base alone, the head, and the pre-change head `45d5c35a`, each merged as GitHub merges into `2509db68` and into `e608f8d8`. Two tree ids equal the hosted merges `dd5cf579` and `241f036e`.
  - `make -s -C tb/verilator/milan_dp ci-prepare build-gptp build-gptp-lat`: within each base, both binaries and every input are byte-identical across the three trees.
  - `make -s -C tb/verilator/milan_dp exec-gptp` and `exec-gptp-lat`: 28 direct runs under three CPU loads.
  - `python3 scripts/ci_make_cases.py --suite milan_dp --shard {0/4,1/4,0/8,1/8} --jobs 2`: 12 pieces.
  - Result: each pin gives one output per case (old pin `767854b0…`/`699262f3…`, new pin `fded66ab…`/`691b82a4…`). Each equals the hosted receipt's `output_sha256` for that pin, and at one base every case's receipt is identical with and without the change, under both deals.
Acceptance criteria:
- #998 acceptance 1 (byte-identical output against the base): met. Every difference between the two hosted runs is accounted for, and nothing is masked.
  - `milan_dp`'s `gptp`/`gptp-lat` and `gptp_shadow` differed between the two hosted runs because #995 re-pinned the gPTP processor in the base between them (`1616fc8f` → `1213ac5b`).
  - At one base they are identical. `capture_coherence`'s per-leg tallies differ by construction, with equal totals.
- #998 acceptance 2 (as ruled for this PR): met. Every job the PR touches is within the bound with margin, and none is slower than its slowest earlier window except by noise: the preflight +3 s, and Yosys shard 1/4 +19 s from #995's ROM change.
  - Leg A projects 1530 s and is stated (#737).
  - The untouched jobs are #1008. The four fail-fast watchers and the nightly physical job are its documented exceptions.
Open risks/questions:
- No hosted run of the pre-change head on `e608f8d8` exists. The same-base comparison is local, tied to the hosted runs by tree ids and output digests.
- The first run after a workflow change rebuilds Yosys (split-cdc 14.2 min, Prepare pinned Yosys 12.7 min), once.
- Not run: the act replay and the full serial sweep (the candidate bank runs it).
- `ci/image/tool-inventory.json` and `exec-audit-receipt.json` name `firmware-boundary`'s old step indices. They belong to the image work to regenerate.
