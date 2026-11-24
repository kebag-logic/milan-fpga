[R913] NEGATIVE - exact head ed7df79c6f87a4172c885f268ad67629bd56c4eb

# R913-2: delta re-review of milan-fpga PR #992 (Closes #991), `20-lwsrp-pin-d1bb4f4` -> `dev-soft-core`

Exact head `ed7df79c6f87a4172c885f268ad67629bd56c4eb`, tree `9065222f25fa3e23aa73783effe26694949ceaea` (verified,
`receipts/checkout-integrity.txt`). Delta reviewed: `dbba60e6..ed7df79c`, two commits (`4ad6c164`, `ed7df79c`),
three files: `tb/verilator/milan_dp/twin_mrp.py`, `tb/verilator/milan_dp/README.md`,
`sw/firmware/ctrl/test/test_ctrl_firmware.py` (docstring only). Round-1 content outside the delta keeps its prior
lens verdicts; nothing in the delta changes what it depends on (no image input, no RTL, no grade code changed).

All five lenses were applied to the delta. Four are clean. `Docs` is unclean on one MINOR (F1): a sentence added
to the twin README, read plainly, claims self-test coverage of the Registrar-IN case for txLA! omission, and a
planted fault shows that case is not covered. That MINOR makes the verdict NEGATIVE. All three prior findings
are resolved at this head (R913-1-F1, R914-1-F1 fixed; R913-1-S1 taken). The required fix is one sentence of
README wording, or one more self-test check.

## Prior findings at this head

| ID | Status at ed7df79c | Evidence |
|---|---|---|
| R913-1-F1 (MINOR, Tests): self-test did not fail when the Registrar keeps IN across txLAF! | **RESOLVED** | R913-1's `twin_mutants.py`, sha256 `a3b9266a…` (equal to its round-1 manifest), run unchanged: control PASS `OK (11 checks)`; 9 of 9 CAUGHT; `txlaf-registrar-kept` CAUGHT by `omission-from-full-registrar-in` and `joinin-after-omission-from-full` (`receipts/r913-1-twin-mutants.txt`). My own mutants agree, 7 of 7 caught (below). `make twin` 0 findings, `make twin-plants` 16 of 16 |
| R914-1-F1 (MINOR, Tests+Docs): printed "10 checks" for 9 executed | **RESOLVED** | `twin_mrp.py:413-422` appends each name as `check` runs; `:464-466` prints `len(checks)`. R914-1's `probe_twin.py`, sha256 `1e9f97dd…` (equal to its manifest), unchanged: profile census 11 calls, 11 distinct names, `selftest failures: []`, then its pinned `== 9` assert stops (rc 1), as expected (`receipts/r914-1-probe-twin.txt`). With only that constant set to 11 (`receipts/probe-twin-11.diff`): rc 0, 72 table probes, 1492/1497 decoded boundary, 5 of 5 mutations caught (`receipts/probe-twin-11.txt`). No total is written in the source. PR body row 37 now says 11, and that 9 ran under the old fixed 10 |
| R913-1-S1 (SUGGESTION, Docs): `srp` entry did not describe the own-LeaveAll arms | **TAKEN** | `test_ctrl_firmware.py:80-85` matches `srp_own_leaveall.cpp:2-12, 18, 240-247` (withdrawal 5 to 200 ms after the own LeaveAll, Lv within 240 ms, none deregistered when none is withdrawn, lwSRP MSRP peer) and `srp_arms.py:116-122` (8x8/1if every input, 1x1/1if). One wording RESIDUE (R2) |

## Findings

### F1 - MINOR - Docs - `tb/verilator/milan_dp/README.md:1406-1408`

- **Authority/evidence:**
  - AGENTS.md section 6, Docs lens: changed contracts must be reflected accurately in authoritative documentation.
    The twin README is the authority for what the grade and its self-test hold.
  - Added text: "The `leave-all-omission` plant holds the txLA! case. `twin_mrp.py --selftest` holds both cases,
    with the Registrar MT and with it IN, …". In this paragraph "both cases" are the txLA! omission (room left)
    and the txLAF! omission (full frame). Read plainly, the qualifier "with the Registrar MT and with it IN"
    applies to both of them.
  - The self-test exercises the Registrar IN only in the full-frame (txLAF!) case. Its own docstring says so
    (`twin_mrp.py:408-410`), and so does the author's REVIEW-READY ("the full-frame case with the Registrar MT
    and IN").
  - Its one txLA! omission case, `omission-with-room` (`:430-431`), runs with the Registrar MT.
  - Planted fault: Table 10-4's txLA! row (`twin_mrp.py:98`, `"txLA!": {"IN": "LV"}`) replaced by no transition.
    The self-test still prints `OK (11 checks)`, rc 0 (`receipts/txla-registrar-mutant.txt`). So "with it IN"
    is not held for the txLA! case. The twin's captures don't reach it either: no frame of the stimulus reaches
    either half, so the Registrar stays MT (README `:1411-1412`).
- **Impact:**
  - The README, read plainly, states coverage the gate does not have. This is the same class as R914-1-F1, a
    test claim the evidence does not support.
  - A regression in the Registrar half of txLA! would pass the self-test while the README says it is held.
  - The grade code itself is not faulted. The txLA! row predates this PR (`a9082fdd`, an ancestor of base
    `aa30d77f`).
- **Required outcome:** the README claims only the coverage the self-test has. Either scope the qualifier to the
  full-frame case, for example: "`twin_mrp.py --selftest` holds both cases, the full-frame one with the Registrar
  MT and with it IN, as well as …". Or add a self-test check that fails when txLA! does not take a Registrar IN
  to LV (see S2).
- **Verification:**
  - Reread README `:1404-1409` against `twin_mrp.py:398-455`.
  - If a check is added instead, rerun the txLA! mutant (one substitution at `twin_mrp.py:98`, recorded in
    `receipts/txla-registrar-mutant.txt`). It must then be CAUGHT, with R913-1's nine and my seven
    (`scripts/r2_mutants.py`) still CAUGHT.
  - Rerun the docs gates. `make twin` must stay at 0 findings and `make twin-plants` at 16 of 16.
- **Lens attribution:** Docs. The code is correct against Table 10-4 (Conformance clean). The delta's tests do
  what their own docstring claims (Tests clean for the delta). The untested txLA! Registrar row is pre-existing,
  so it is S2, not a delta finding.

### R1 - RESIDUE - Docs - PR #992 body, routed-image paragraph ("Round 2's images are byte-identical … so the route stands")

The conclusion is right, but the stated reason is not quite the right one.

- The routed 8x8/1if image embeds the builder's `sw/builder/out/endstation_ax7101_8x8/ctrl_app.elf`, sha256
  `a24015a4…` (`author-route/receipts/head/fw-identity.txt`). That ELF is not one of the 28 hashed in
  `author-r2/receipts/images/elf-hashes.txt`.
- The route stands because nothing any image recipe reads changed. The tree diff `dbba60e6..ed7df79c` is the
  three files above, none read by the builder, SoC or firmware recipes; gitlinks are unchanged
  (`receipts/image-inputs.txt`).

Exact fix: "Round 2 changes no image input (its three files are a twin grade script, its README and a gate
docstring, and the gitlinks are unchanged), and its images are byte-identical to `dbba60e6`'s (28 of 28
ELF/bin/hex), so the route stands for this head."

### R2 - RESIDUE - Docs - `sw/firmware/ctrl/test/test_ctrl_firmware.py:80-82`

"a Listener withdrawn 5 to 200 ms after the board's own LeaveAll sent as Lv within 240 ms" can be parsed as the
LeaveAll being "sent as Lv". The gate reads only the docstring's first line (argparse), so this is wording only.
`srp_arms.py:117` already has the clear form. Exact fix: "a Listener withdrawn 5 to 200 ms after the board's own
LeaveAll is sent as Lv within 240 ms".

### S1 - SUGGESTION - Tests/Robustness - `tb/verilator/milan_dp/twin_mrp.py:464-466`

When no check runs, `--selftest` prints `twin_mrp selftest: OK (0 checks)` and exits 1. The guard works: my
`census-not-counted` and `census-zero-checks` mutants exit 1 (`receipts/r2-mutants.txt`). But the line says OK
on a failing run. Suggested: print `FAILED no check ran (0 checks)` in that branch. Optional.

### S2 - SUGGESTION - Tests - `tb/verilator/milan_dp/twin_mrp.py:98`, self-test `:398-455`

Table 10-4's txLA! Registrar transition (IN to LV) has no self-test or capture coverage: planted fault, rc 0
(`receipts/txla-registrar-mutant.txt`). It predates this PR. A check like the new Registrar-IN pair, at a
LeaveAll MRPDU with room, would close it and would also settle F1. Out of scope as a delta finding; a new Issue
or this lane at the author's choice.

No comment-rule residue in the delta. The 34 added lines carry no bench lane labels, lane names, review rounds,
reviewer IDs, issue-comment IDs, tool or model names, or host details. No U+2014. Longest added line 110 columns
(`receipts/residue-scan.txt`).

## Lens results (delta, exact head ed7df79c)

- `[R913] PASS Conformance` — `twin_mrp.py:436-442` against `:90-98`, `:180-190`.
  - The new expectations follow IEEE 802.1Q Table 10-4 (rLA!: IN to LV, leavetimer to MT) and Table 10-3
    (txLAF!: QA to VP; tx! from VP sends sJ, JoinMt with the Registrar not IN). So
    `{(AA, LV), (AA, MT)}` with 0 findings is right for the omission plus JoinMt, and JoinIn there is illegal.
  - R914-1's 72-combination table probe passes (`receipts/probe-twin-11.txt`).
  - `test_ctrl_firmware.py:80-85` matches `srp_own_leaveall.cpp:7-12, 18` (Milan v1.2 Table 4.3 joinTime 240 ms).
- `[R913] PASS RTL` — `receipts/image-inputs.txt`, `author-r2/receipts/images/elf-hashes.txt`,
  `plat_ledger-*.log`, `author-route/receipts/head/summary.txt`.
  - The delta touches no RTL, HDL, config, firmware source or gitlink.
  - The author's 28 of 28 ELF/bin/hex are IDENTICAL. The two ledger logs differ only in the `b-base`/`b-head`
    path (`receipts/ledger-normalized.diff`, empty after normalising); plat_ledger PASS, 0 findings.
  - The routed 8x8/1if condition at `dbba60e6` (LUT 43,068 / FF 51,015, worst WNS +0.194, WHS +0.032, all four
    corners 0 failing) therefore stands at this head.
- `[R913] PASS Robustness` — `twin_mrp.py:413-422`, `:460-466`; `receipts/r2-mutants.txt`.
  - Zero checks counted exits 1 (two mutants).
  - A raising check propagates as a non-zero exit before the print.
  - The new cases exercise the full-frame boundary with a prior received event (Registrar IN) and an illegal
    follow-up message.
  - `ran=None` keeps `selftest()`'s old call shape, which R914-1's probe uses unchanged.
- `[R913] PASS Tests` — `twin_mrp.py:398-455`; `receipts/r2-mutants.txt`, `r913-1-twin-mutants.txt`,
  `r914-1-probe-twin.txt`, `probe-twin-11.txt`, `twin.log`, `twin-plants.log`, `twin-plants-refusals.txt`.
  - My 7 mutants are all CAUGHT, control PASS: Registrar kept, Registrar to MT, Applicant kept, txLAF! outcome
    dropped, rJoinIn! not registering, census not counted, census zeroed.
  - R913-1's 9 of 9 are CAUGHT.
  - Census: printed 11 = profiled 11, distinct.
  - `make twin` with Verilator 5.050 (identity checked) in a copy at this head: rc 0, self-test `OK (11 checks)`,
    `twin: 0 finding(s)`.
  - `make twin-plants`, a single invocation: rc 0, 16 of 16 plants REFUSED, 32 refusals.
  - Each new check can fail for its defect.
- `[R913] UNCLEAN Docs` — README `:1404-1409` (F1 open). Checked clean apart from F1:
  - `twin_mrp.py:398-411` docstring.
  - `test_ctrl_firmware.py:80-85`.
  - README `:1404-1405`, `:1409` ("counted as they run").
  - PR #992 body counts: row 37 (11 checks, 9 and 9 of 9 faults), row 38 (0 findings), row 39 (16, 32).
  - The route table matches `author-route/receipts/{base,head}/summary.txt` and `HANDOFF-route.md:12-20`:
    base 43,145 / 51,005, +0.193 / +0.036; head 43,068 / 51,015 (-77 / +10), +0.194 / +0.032; 78 / 33 / 11
    both.
  - The live body differs from `author-r2/PR-BODY.md` only in that route block (packet "pending", live filled
    from author-route; `receipts/pr-body-vs-packet.diff`).
  - `check_py_idiom.py` rc 0 and `docs_check.py` 0 findings at this head.
  - R1 and R2 are RESIDUE.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | twin_mrp.py:90-98, :180-190, :436-442; test_ctrl_firmware.py:80-85 vs srp_own_leaveall.cpp; probe-twin-11.txt | R913-2 | ed7df79c6f87a4172c885f268ad67629bd56c4eb |
| RTL | CLEAN | image-inputs.txt (no RTL/HDL/config/firmware/gitlink change); author elf-hashes 28/28; ledger logs normalized-equal; author-route summaries | R913-2 | ed7df79c6f87a4172c885f268ad67629bd56c4eb |
| Robustness | CLEAN | twin_mrp.py:413-422, :460-466; r2-mutants.txt census guards; full-boundary Registrar-IN cases | R913-2 | ed7df79c6f87a4172c885f268ad67629bd56c4eb |
| Tests | CLEAN | twin_mrp.py:398-455; r2-mutants (7/7), r913-1-twin-mutants (9/9), r914-1 probe census 11; make twin 0 findings; twin-plants 16/16, 32 refusals | R913-2 | ed7df79c6f87a4172c885f268ad67629bd56c4eb |
| Docs | UNCLEAN (F1 MINOR open) | README.md:1404-1409; twin_mrp.py:398-411; test_ctrl_firmware.py:80-85; PR #992 body vs packet and author-route | R913-2 (applied, not clean) | ed7df79c6f87a4172c885f268ad67629bd56c4eb |

## Real limits

- `check_em_dash.py` could not run here: the pinned Markdown renderer is absent and installing it is not
  allowed. I relied on my own scan of the added lines (no U+2014) and on the author's receipt
  (`author-r2/receipts/docs/summary.txt`, docs-gates-0#12 rc 0 at `ed7df79c`).
- I did not rebuild the firmware images or re-route. Image identity rests on the author's published 28-hash
  receipt and on my unchanged-input check.
- I did not re-run the firmware gate, the reproduction (`srp_own_leaveall.cpp`), the budget model or the docs
  workflow steps: the delta does not change them. Those stand from the author's receipts and round 1.
- Hosted checks at this head were in flight when sampled (22 success, 1 skipped, 34 queued or in progress, none
  failed; `receipts/hosted-checks.txt`). That is not an acceptance claim.
- No manager source bank ran at this head. None is claimed or inferred.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry F1 to the author lane. Re-review Docs (and Tests, if a check is added) at the corrected head.
- Carry R1 and R2 to the residue checklist.
- At the merge turn, build and validate the current-dev merge candidate: source base
  `aa30d77f75cd97b3a29878ca0ed68010a7629266`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, builder and
  native banks. Publish its receipts, and own hosted and act acceptance.

## Receipts and scripts

All paths are relative to this packet and listed in `MANIFEST.sha256`.

- `scripts/r2_mutants.py`: my seven round-2 mutants and the control.
- `scripts/checkout_integrity.sh`: the exact-head blob, mode, index and gitlink check.
- `scripts/probe_twin_census11.py`: R914-1's probe with its one constant set to 11.
- `receipts/`: mutants, prior probes (with their hashes), twin build, twin and plants logs and rc files, image
  inputs, the normalised ledger diff, PR body live copy and diff, residue scan, idiom and docs gates, hosted
  check snapshot, checkout integrity.
- The local toolchain path in the build logs is replaced by `$PINNED_VERILATOR_IMAGE`.
- The clone was restored and verified: 1937 tracked blobs byte- and mode-identical, index equal to HEAD, no
  untracked or ignored file, gitlinks as recorded (`receipts/checkout-integrity.txt`).

R913-2 FINISHED
