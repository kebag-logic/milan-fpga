[R401] NEGATIVE - exact head b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745

# R401-1: independent external review of processor PR #135 (lane C2, MAAP; issues #66, #67, #68)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745`, tree `7916d0854d52eecb28b03ac5e665d05355b7be08`
- Base: `c951a9ff0cb5851fb159d33e966e5a2a9a188fe3` (4 commits: `15de8b5`, `14b6caa`, `3407c84`, `b03d36f`)
- Round: R401-1, the first public review round on this PR. The review ran in a cleared context in an isolated detached clone.
- Verdict: **NEGATIVE**. One open MINOR (R401-1-F1) leaves the RTL, Tests and Docs lenses unclean. Every acceptance item of #66, #67 and #68 is met and reproduced at the head. The negative verdict comes from the Release! arm the PR rewrote. That arm's documented seed semantics disagree with the RTL, and the PR neither reconciles them nor tracks the gap.

## 1. What was reconstructed, in order

1. The repository has no AGENTS.md or CONTRIBUTING.md at this head. The conventions come from `README.md`, `docs/README.md` (single-source and editing rules) and `docs/guides/hdl-engineer.md`.
2. The acceptance lists in the issue bodies of #66, #67 and #68. The lane assignment on #66 (comment 5884446021) adds one rule: an RTL defect a new test exposes is fixed in-lane with a failing arm. It also sets a STOP before any port or parent-visible change, and requires a parent-visible list. #67 and #68 carry only the pointer comments to that assignment.
3. The PR body, including its parent-visible list and its "What remains" disclosure.
4. The authority for the engine: `docs/architecture/11_maap_engine.md` (sections 2, 3 and 6) and the `KL_pp_maap.sv` banner. IEEE 1722-2016 Annex B is cited through the clause references the engine and the issues carry. The standard's text is not distributed with the repository, so no standard wording is quoted here beyond what those documents quote.
5. The full diff `c951a9ff..b03d36f` (25 files, +823/-56) and each commit.
6. The public evidence at milan-fpga `82c7bcb1…/review-evidence/ppC2-r1`. Its 53 files match their published sha256 in `MANIFEST.json`, with 0 mismatches. That tree contains author receipts only. No manager bank receipts were present in it, and none appeared on the issues or the PR (see section 8).
7. Hosted checks at `b03d36f2` (section 6).

## 2. Acceptance, item by item

| # | Acceptance item | Evidence at head | Result |
|---|---|---|---|
| #66.1 | The reject arm is forced deterministically, the engine redraws, and the block ends at or below `91:E0:F0:00:FD:FF` | `tb/maap` U17 (`sim_main.cpp` `overhanging_draws_are_redrawn_until_the_block_fits`): count 255 and a kind-7 stub in `maap_wrap.sv` scripting `0xFDFF`, `0xFD02`, `0xFD01`. Three draws are consumed, the PROBE is byte-exact at `…:FD:01`, and the block ends at `…:FD:FF`. The stub latches the kind at the PRNG's own acceptance condition and passes kinds 5 and 6 through. | MET, reproduced |
| #66.2 | A seed above `0xFE00 - count` probes the clamped offset byte-exact | U18: seed `0xFFFF`, count 8. The byte-exact PROBE is at `0xFDF8`, no kind-7 draw is made, and the last source is granted `…:FD:FF`. | MET, reproduced |
| #66.3 | The compare at `:587` forced true and the seed clamp removed each turn the suite red, recorded in the README | `fit-compare-forced-true` (the compare is now at `:594`) and `seed-clamp-removed` are both KILLED with named U17 and U18 failures. The ledger is in `tb/maap/README.md`. | MET, reproduced |
| #66 fix | A Release! mid-draw clears the draw mark (`KL_pp_maap.sv:569-577`) | U17b kills `release-keeps-draw-mark` (phases 1 to 3). Both of the reviewer's own mutants are KILLED (section 4). The fix is safe at the top: the owner mux in `protocol_processor_top.sv:2707-2780` routes the abandoned answer only to MAAP, where it is ignored, and the shared busy blocks a new request until that answer lands. It leaves no stale claim or timer, because `pstate` is INITIAL, the yield already cancelled the running timer, and W_ADDR arms nothing. It re-uses no seed, because `seed_used_r` is untouched. But see **F1** for seed re-arm. | Fix correct. F1 open on the same arm |
| #67.1 | `tb/rx_validator`: maap_version 2 and 0 are accepted, go to `PP_PROTO_MAAP`, and the status lane carries the version | F28a/b/c (versions 2, 0 and 31) are checked against the suite's independent `classify()` oracle (`status = f[16] >> 3`), with field-by-field header beats | MET, reproduced (453/453) |
| #67.2 | `pp_top` MP: a version-2 PROBE conflicting with a DEFEND-state claim gets a byte-exact DEFEND | MP7: version 2, then version 0, each answered by a byte-exact unicast DEFEND carrying version 1 and the B.3.6.6 overlap, with the claim kept. The DEFEND itself proves DEFEND state, because a PROBE-state rProbe! from that MAC would be ignored by compare_MAC. | MET, reproduced (33/33) |
| #67.3 | A `maap_version == 1` mutation turns both suites red | `validator-maap-version-1-only`: rx_validator 47 FAIL (F28), pp_top MP7 4 FAIL | MET, reproduced |
| #68.1 | Tie-break MAC pairs disagree forward vs reversed, in both directions, for PROBE/rProbe!, DEFEND/rAnnounce! and DEFEND/rDefend! | `WIN_MAC 00:11:22:33:44:FF` and `LOSE_MAC F2:11:22:33:44:01` against `OWN 02:AA:BB:CC:DD:EE`. The reviewer computed both premises independently: WIN is forward-lower and reversed-higher, LOSE is forward-higher and reversed-lower. Every scenario asserts its premise. The cells are U9/U19, U7/U8 and U20/U21. | MET |
| #68.2 | New cells: PROBE/rProbe! from a rev-lower peer yields and re-randomizes; DEFEND/rDefend! from a rev-lower peer yields and from a rev-higher peer is ignored; PROBE/rAnnounce! from a rev-higher peer yields | U19, U21, U20 and U22. Each yield is graded by one helper: one re-address, the claim invalid, and a fresh in-pool byte-exact PROBE that is not the contested range. | MET, reproduced |
| #68.3 | The forward-compare mutation turns `tb/maap` red, and at least one pp_top MP scenario uses a disagreeing pair | `compare-mac-forward` gives maap 9 FAIL and MP4 5 FAIL. MP4's winner `F2:11:22:33:44:01` is reversed-lower and forward-higher than `0A:0B:0C:0D:0E:0F`, with a premise check. | MET, reproduced |
| #68.4 | A mutation ledger in `tb/maap/README.md` | Present. Its tallies match the reviewer's re-run exactly. | MET |
| b03d36f | The parent C++ rule-11 fix | The parent's own `check_cpp_idiom.py` `scan()` (dev 57b8c867) run on every touched C++ file: `tb/rx_validator/sim_main.cpp` has 1 multi-declarator at `3407c84` and 0 at head. `tb/maap` and `tb/pp_top` have 0 at base and at head. `receipts/cpp-idiom-delta.txt`. | Correct |
| Parent list | Complete: one RTL behaviour change, dark in the parent | No port, parameter or interface change is in the diff. The top wires `cfg_en_i` to `cfg_maap_internal_i` (`protocol_processor_top.sv:2090`), and `eng_w` requires `cfg_en_i`, so with the tie-off the walker never leaves W_OFF and the changed arm is unreachable. The parent at dev `57b8c867` ties it to `1'b0` (`hdl/milan/milan_datapath.sv:7695`, read-only fetch). The new entry points and the optional test-evidence budget are listed. The pp_top tally changes from 7,751 to 7,756, so any parent pin of processor check counts would move. No such pin could be searched reliably (section 8). | Complete, as far as could be checked |

## 3. Reproduction at the exact head (pinned simulator)

The instructed launcher `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. Every other pinned launcher on the host execs the same overlay binary, so the reviewer built a private scratch wrapper around it. It reports `Verilator 5.050 2026-07-01 rev v5.050`, and `verilator_bin` has sha256 `44898b22…bfdd` (`receipts/head/verilator-version.txt`). The author's receipts were built with 5.052. All runs used a `git archive` export of the head under `scratch/`, never the clone.

| Run | Result | Receipt |
|---|---|---|
| `tb/maap` run | rc 0, 114/114 | `receipts/head/maap-run.log` |
| `tb/rx_validator` run | rc 0, 453/453 | `receipts/head/rx_validator-run.log` |
| `tb/pp_top` `maap-internal` | rc 0, 33 checks, 0 failures | `receipts/head/pp_top-maap-internal.log` |
| `make -C tb/maap mutants` (the PR's campaign) | rc 0: 3 controls PASS, 13/13 arm runs KILLED, `16 checks: 16 PASS`. Tallies identical to the author's receipt. | `receipts/campaign/` |
| Lint of `KL_pp_maap` (the `lint_hdl.sh` flags) | rc 0, 0 warnings | `receipts/static/lint-KL_pp_maap.log` |
| `scripts/gen_matrix.py --check` | rc 0 | `receipts/static/gen_matrix-check.log` |
| `git diff --check c951a9ff b03d36f` | rc 0 | `receipts/static/diff-check.log` |
| Parent Python idiom `scan()` on the new `tb/maap/mutants.py` | 0 findings | `receipts/py-idiom-mutants.txt` |

The full processor bank, `make check`, Yosys and the SRP campaign were not re-run, as the review scope requires. The hosted runs executed lint and every suite (section 6).

## 4. Reviewer-owned mutants against the Release! fix

Both mutants are planted in scratch copies, and the unmodified `tb/maap` suite must finish red with a named U17b failure (`scripts/03_own_mutants.sh`, `scripts/mutations/`).

| Mutant | Planted defect at `KL_pp_maap.sv:576` | Result |
|---|---|---|
| `r401-release-clears-mark-after-request-only` | `if (!draw_req_r) draw_act_r <= 1'b0;`: the mark survives a fall on the request-presentation cycle | **KILLED**: `FAIL: U17b: phase 1`, 1 FAIL of 114 |
| `r401-release-keeps-mark-on-coincident-answer` | `if (!prng_draw_valid_i) draw_act_r <= 1'b0;`: the mark survives a fall that coincides with the answer | **KILLED**: `FAIL: U17b: phase 3`, 1 FAIL of 114 |

Each mutant is killed by exactly the phase predicted from the PRNG handshake (request, then busy, then answer, a 4-cycle loop). This shows that each U17b phase carries weight on its own.

## 5. Findings

### R401-1-F1: MINOR. Lenses: RTL, Tests, Docs

- **Where:** `hdl/maap/KL_pp_maap.sv:569-577`, the W_ADDR engage-fall exit this PR rewrote. It contradicts `docs/architecture/11_maap_engine.md:135-137`: "Release! = engage fall …: stop both timers, INITIAL, no PDU …, seed re-armed for the next engage". It also contradicts the banner at `KL_pp_maap.sv:294-299`: "only a Release!/engage fall re-arms it".
- **Evidence:** reviewer probe P1 (`scripts/probe_scenarios.inc`, `receipts/probes/probes.log`). The sequence is a seeded walk (seed `0x2000`), then a rProbe! from `LOSE_MAC` in PROBE (yield, seed consumed), then a Release! while generate_address redraws, then PortOperational!. The first PROBE goes to `91:E0:F0:00:8A:D6`, a random range, not the seed `91:E0:F0:00:20:00`. The control P1c runs the same yield with the Release! landing in W_IDLE, and the next engage probes the seed `…:20:00`. Whether an engage fall re-arms the seed therefore depends on which walker cycle it lands in. Only the W_IDLE exit (`:684`) re-arms it; the W_ADDR exit does not. This predates the PR on the non-in-flight cycle. The PR turned the in-flight case from a permanent wedge into this path, rewrote the arm, and added a comment describing its Release! semantics. The author disclosed the divergence ("Observation A", PR body "What remains"), but did not act on it, document it, or open a tracking issue.
- **Authority:** the engine's normative document (`11` §6) and the module banner, which `docs/guides/hdl-engineer.md` calls "the primary source". The assignment on #66 asks for this arm to be judged against the engine's documented behaviour. Annex B conformance itself is not at stake: the engine reads footnote a as permissive, so a random draw is a legal outcome.
- **Impact:** at the head, the normative documentation states a Release! behaviour that the RTL does not implement on the arm this PR changed. An integrator who relies on a provisioned seed (footnote a's reuse of a stored range) sees it silently skipped for one engagement after a Release! lands during a post-conflict redraw. No test pins either outcome, so the next change to this arm can move it again unobserved. There is no parent impact while `cfg_maap_internal_i` is tied to 0.
- **Required outcome:** reconcile the arm and its contract in this lane, in one of two ways:
  - (a) re-arm the seed in the W_ADDR engage-fall exit (`seed_used_r <= 1'b0`, matching `:684`), or
  - (b) state the exception in `11` §6 and in the banner at `:294-299` (and in the new comment at `:570-575`).

  Either way, add a failing-first scenario that pins the chosen outcome (P1's shape) and a mutant for it in the ledger. A tracking issue alone does not clear this. The head's normative text would still contradict the RTL on the rewritten arm.
- **Verification:** `scripts/04_probes.sh` with `CLONE` set. P1 must pass under outcome (a), or the suite's new scenario must pin the documented exception under outcome (b). `make -C tb/maap mutants` must stay green with the new arm KILLED.

### R401-1-F2: SUGGESTION. Lenses: RTL, Robustness (pre-existing, outside the diff and the acceptance)

- **Where:** `KL_pp_maap.sv:559-565` (W_OFF starts only on an edge, `eng_w && !eng_q_r`), `:680-686` and `:762-773` (a 2-cycle W_TEARDOWN between W_IDLE and W_OFF).
- **Evidence:** probe P2. An engage fall of 1 or 2 cycles seen in W_IDLE never re-probes: `state_o` stays 0 through 2 probe budgets. A fall of 3 or 4 cycles re-probes. The result is identical with the base RTL (`receipts/probes/probes-base-rtl.log`), so it predates the PR. The rising edge lands while the walker is in W_TEARDOWN. `eng_q_r` then already equals 1 when W_OFF looks, so the engine stays parked while engaged until another fall and rise. This is the same invariant the new comment asserts ("the next PortOperational! must still reach ReserveAddress!"), violated on the neighbouring arc.
- **Impact:** with `cfg_maap_internal_i = 1`, a short `link_up_i` or config glitch can leave the entity without a MAAP claim, so ALLOC_DA is refused indefinitely. It is dark in the parent.
- **Suggested outcome:** open a follow-up issue. For example, W_OFF could start on the level `eng_w` when arriving from teardown, or W_TEARDOWN could avoid consuming the edge. Pin it with P2's shape.

### R401-1-F3: SUGGESTION. Lenses: Conformance, RTL (pre-existing, disclosed by the author, outside the acceptance)

- **Where:** W_IVAL and the TX states (`KL_pp_maap.sv:610-657`) do not test `eng_w`. This contradicts `11` §6 ("no PDU") and the banner at `:57-58` (footnote c, as the engine reads it).
- **Evidence:** probe P3. A `cfg_en_i` fall 12 cycles into a fresh walk still lets 1 PROBE leave. The result is identical with the base RTL.
- **Suggested outcome:** open a follow-up issue, as the author's "Observation B" already proposes.

### R401-1-F4: SUGGESTION. Lens: Docs

- **Where:** the new comment at `KL_pp_maap.sv:570-575` and `tb/maap/README.md:87-92` both say the stale mark makes "the next walk's W_IVAL wait forever". That is true only for a seeded next walk (`:578-587`). For an unseeded next walk, which is the case U17b drives, the wait is in W_ADDR's `else if (draw_act_r)` arm (`:588-601`), which never requests again.
- **Suggested outcome:** name both states in the comment and the README when they are next touched.

**Prior public review findings:** this is the first public review round on PR #135. No earlier-round findings exist to resolve or retain at this head (checked after this report's verdict and ledger were written; see section 8).

## 6. Hosted checks at `b03d36f2`

Polled at 2026-09-29 08:35 UTC (`receipts/hosted-*.txt`, `receipts/hosted-check-runs.tsv`).

| Run (event) | Job | State |
|---|---|---|
| 36540841402 (push), 36540852737 (pull_request) | `docs-gates` | completed, **success** (both) |
| same | `portability` | completed, **success** (both) |
| same | `suites` | **in progress**. Steps: the pinned-simulator cache step executed and succeeded, and the build step was skipped on a cache hit. "Lint (zero tolerance) + every suite" **executed, success**. The SRP LeaveAll mutation campaign was running. **The MAAP mutation campaign, traceability and nvm_port figures were pending, not yet executed.** |

The overall commit status was `pending`. Hosted and act acceptance, including the new MAAP campaign step, belong to the manager.

## 7. Reviewer-owned lens ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (F3 is a pre-existing SUGGESTION) | Annex B clause references in #66/#67/#68 and `11` §3/§6 (B.1/Table B.9 fit, footnote-a clamp, B.2.3.2/B.2.3.4 versions, B.3.6.4 reversed compare_MAC, Table B.7 cells); `KL_pp_maap.sv` `row_decode`, the fit and seed clamps, the frame builder; MAC-pair premises recomputed independently; version handling in the validator oracle | R401-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |
| RTL | **UNCLEAN (F1)** | the `KL_pp_maap.sv` diff (`:569-577`) and the whole walker; the PRNG handshake (`KL_pp_prng.sv:167-187`); the top's PRNG owner mux and cfg_en wiring; the parent tie-off at 57b8c867; focused lint rc 0; two reviewer mutants KILLED; probes P1 to P3 at head and base | R401-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |
| Robustness | CLEAN (F2 is a pre-existing SUGGESTION) | Release!/PortOperational! arcs under draws in flight (U17b plus own mutants), short-bounce probe P2, top-level abandoned-draw routing, stale-timer and stale-claim reasoning; the `mutants.py` driver (controls first, named failures, build failure or missing tally = UNPROVEN, scratch isolation) | R401-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |
| Tests | **UNCLEAN (F1)** | `tb/maap` U17/U17b/U18/U19 to U22 and the kind-7 stub; `tb/rx_validator` F28 against the independent `classify()`; `tb/pp_top` MP4/MP7 and the `maap-internal` entry; all 13 campaign arms re-run (identical tallies); head suites re-run on the pinned simulator | R401-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |
| Docs | **UNCLEAN (F1)** | `11_maap_engine.md` (§6 and the §11 change), the `KL_pp_maap.sv` banner and the new comment, the `tb/maap`, `tb/rx_validator` and `tb/pp_top` READMEs and ledgers (numbers checked against the re-run), PR body claims, the `hdl.yml` step, `.gitattributes`; F4 is a SUGGESTION | R401-1 | b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745 |

## 8. Real limits and pending manager duties

**Limits:**

- The instructed launcher path was absent. The same pinned 5.050 binary was used through a scratch wrapper, with its identity recorded.
- The published evidence tree held author receipts only. No manager bank receipts were found there or in comments on #66, #67, #68, #135 or milan-fpga #76 since 2026-09-28, so the manager's source, static, builder and native banks could not be inspected. They are taken as the brief states them.
- The parent's code search returned nothing for processor tally pins. That search does not index non-default branches reliably, so the absence of parent pins on processor check counts is **not proven**.
- The standard's text was not consulted directly (not distributed). Annex B judgements follow the clause references and readings recorded in the issues and in `11`.
- The full processor, parent, Yosys and builder banks, the SRP campaign and `make check` were not run, as the scope requires.
- Physical calibration was **not run**. Field skips are not hardware proof.

**Pending manager duties:**

- Resolve F1 through the author, then re-review.
- Run the donor full bank and the 16-command parent consumer bank at milan-fpga dev `57b8c867`. The author's parent receipts were taken at `13eda870`.
- Accept the hosted `suites` job once its SRP campaign, MAAP campaign, traceability and figures steps complete.
- Decide on follow-up issues for F2 and F3.
- Build the final current-dev candidate at the merge turn (source base `c951a9ff`, live dev `57b8c867`).

**Clone integrity after the probes (`receipts/clone-verify.txt`):**

- HEAD `b03d36f2…` and tree `7916d085…`. The index writes back the same tree.
- The worktree and index equal HEAD, with 0 untracked or ignored entries.
- All 321 tracked blobs match in bytes and mode.
- No gitlinks are required at this head, and none exist.

Every probe ran in `scratch/` exports only. No source edit, commit, push or GitHub write was made.

R401-1 FINISHED
