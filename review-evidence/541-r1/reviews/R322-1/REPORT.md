[R322] NEGATIVE - exact head 2734b771bcf0b383ea62ef05744452827bafe9e4

# R322-1: internal independent review of issue #541 / PR #562

- Head: `2734b771bcf0b383ea62ef05744452827bafe9e4`, tree `34cb4d208c6681af5405dd4da79fe7c5fe6fbc5e`, single commit, parent `5b73d3f47dfed519eb988c13d6beb1db664ef1e0` (source base = live dev at review time).
- Role: internal reviewer [R322]. This is a cleared-context session. The executor is [A304].
- Scope reconstructed from AGENTS.md, CONTRIBUTING.md and docs/README.md. It also draws on the #541 body, the decision in issue comment 5827373589 and the executor's TAKEN/REVIEW READY comments (5827406716, 5827529280). Other sources: the PR body, the diff `5b73d3f4..2734b771`, the receiver RTL, the CSR/datapath consumers, the receiver/servo harnesses, and the public evidence tree `a7f7e57a:review-evidence/541-r1`.
- Prior public review findings on PR #562 or issue #541: **none exist** (0 PR reviews, 0 inline comments; the only other comments are review-start notices). There is nothing to resolve or retain.

## Verdict summary

The decision's reading holds, and the RTL is functionally unchanged. The comment-stripped `KL_crf_rx.sv` is token- and line-identical to the base. The header and the `CRF_CTRL` row now describe the implemented behaviour accurately. The new locked-sink check does what the acceptance asks: it starts LOCKED, has a failing arm, and the named mutant fails it. The #546 legs, the connected talker-step leg, the servo suite and the campaign are all green at this head.

One MINOR finding remains open, so the verdict is NEGATIVE. The newly documented claim is "a validation error does not refresh the timeout". The decision's own rationale says the same thing: "the timeout already bounds how long invalid data can be followed". No shipped check grades this. A reviewer mutant that lets a rejected PDU refresh the timeout passes every receiver harness and the campaign. The RTL itself behaves correctly: a reviewer probe shows the head unlocking under malformed-only traffic, and the mutant does not.

## Findings

### R322-1-F1: MINOR: Tests, Robustness: documented "does not refresh the timeout" behaviour is ungraded; a timeout-refresh-on-reject mutant survives

- **Where:** `tb/verilator/crf_rx/sim_discontinuity.cpp:180-224` (`locked_validation_error`, the only new check). Its comment at `:182` reads "only silence expires lock". The campaign table is `tb/verilator/crf_rx/mutants.py:19-31`. The claim itself is at `hdl/ieee1722/crf/KL_crf_rx.sv:37-39` ("does not refresh the timeout") and `docs/reference/REGISTER_MAP.md:837` ("It does not refresh the timeout."). The behaviour is implemented at `hdl/ieee1722/crf/KL_crf_rx.sv:354` and `:531-533`.
- **Authority/evidence:**
  - The #541 decision (comment 5827373589) says a sink "unlocks only after 100 ms without valid PDUs", and justifies retention because "the timeout already bounds how long invalid data can be followed". This PR writes that property into the authoritative register map. AGENTS.md section 6, Tests lens: positive, negative and boundary behaviour must be covered, and each test must be able to fail for the defect it claims to detect.
  - Reviewer probe P2 changes `wire w_acc_run_w = w_acc && !stop_i;` to `w_hit && !stop_i`, so any matched PDU, including a rejected one, refreshes the timeout. P2 **SURVIVES**: the unit harness gives 13,836 checks with 0 failures and the discontinuity harness gives 1,932 checks with 0 failures (`receipts/probe-mutants.txt`, `receipts/probe-results.json`). The new check cannot see this defect. Its only timeout leg runs after valid traffic resumes and measures true silence. The existing unit and integration legs send isolated malformed PDUs, never a malformed-only stream across 100 ms.
  - Reviewer probe `scripts/probe_drought.cpp` locks the sink, then sends only matched-but-malformed PDUs at the 2 ms cadence. The head passes all 9 checks: lock is held for 98 ms, drops by 110 ms, exactly one MEDIA_UNLOCKED is scored, and UNSUPPORTED_FORMAT moves once per interval. P2 fails 4 checks: lock is still held after 110 ms and after 230 ms, and no unlock is scored (`receipts/probe-drought.txt`). So the RTL is correct today and the gap is test-only.
- **Impact:** a regression that lets rejected PDUs keep the timeout alive would leave the sink reporting LOCKED indefinitely while accepting no timestamps. That means `CRF_CTRL[31]`=1 and MEDIA_LOCKED = MEDIA_UNLOCKED + 1 on GET_COUNTERS. `crf_locked_w` would never fall, so the 4.4.4.3 disruption trigger (`hdl/milan/milan_datapath.sv:3112-3113`) and the servo's CRF-unlock HOLDOVER entry (`docs/design/TIME_SYNC.md:148`) would never engage. That is exactly the failure the decision's rationale relies on the timeout to prevent, and every shipped gate would stay green.
- **Required outcome:**
  - Add a self-checking check at the receiver layer. It holds a LOCKED, started sink on matched-but-malformed-only traffic across the 100 ms boundary. It grades lock retained before the boundary, and after it grades lock cleared plus exactly one MEDIA_UNLOCKED.
  - Add a named campaign mutant in which a rejected PDU refreshes the timeout. It must fail that check by name.
  - Correct the comment at `:182`: lock expires after 100 ms without a consumed accepted PDU, not only on silence.
- **Verification:** the campaign prints the new mutant's named rejection and the clean control still passes. Probe P2, re-run against the new harness, must be DETECTED. Tests and Robustness are then re-covered at the new head.

### R322-1-S1: SUGGESTION: Docs: `CRF_CTRL` row qualifiers (optional, does not affect coverage)

`docs/reference/REGISTER_MAP.md:837` says "Eight clean consecutive PDUs establish lock". It drops the header's "consumed while started" qualifier (`KL_crf_rx.sv:34`, RTL `:571-574`). It also does not mention that a not-bound-to-bound edge or a reset clears lock without scoring MEDIA_UNLOCKED (`KL_crf_rx.sv:125-137`, `:670`). The row is not wrong, and the header is complete. Adding both would make the row self-sufficient.

## Lens results (reviewer-owned)

```text
[R322] PASS Conformance - hdl/ieee1722/crf/KL_crf_rx.sv:34-44,:354,:531-581; docs/reference/REGISTER_MAP.md:837; issue 541 comments 5827373589/5827406716 - clause reading and all three acceptance items checked
[R322] PASS RTL - receipts/rtl-comment-strip.txt; hdl/ieee1722/crf/KL_crf_rx.sv:309-676 - no functional RTL change; the unlock and validation paths read against the new text
[R322] MINOR Robustness - receipts/probe-drought.txt; receipts/probe-mutants.txt P2 - malformed-only timeout path correct in RTL but ungraded (R322-1-F1)
[R322] MINOR Tests - tb/verilator/crf_rx/sim_discontinuity.cpp:180-224; mutants.py:19-31; receipts/probe-mutants.txt - new check sound, one documented claim ungraded (R322-1-F1)
[R322] PASS Docs - hdl/ieee1722/crf/KL_crf_rx.sv:34-44; docs/reference/REGISTER_MAP.md:837,842; hdl/milan/milan_datapath.sv:2574-2576,3556; receipts/doc-idiom-checks.txt, receipts/doc-md-venv-checks.txt - every new sentence traced to RTL/CSR/wire
```

**Conformance: CLEAN.**
- Clause: Milan v1.2 5.3.8.10 / Table 5.6 makes MEDIA_LOCKED/MEDIA_UNLOCKED event counters whose pair reads as state. It leaves what "synchronized"/"unsynchronized" means to the manufacturer. The in-repo quotations agree: `KL_crf_rx.sv:661-663` and `milan_datapath.sv:3430`, plus the published clause evidence.
- UNSUPPORTED_FORMAT is an observation-interval counter with an interval of at most 1 s. Milan 7.3.2-7.3.4 fixes the profile and says nothing about unlock-on-error. IEEE 1722-2016 10.6 has the media clock free-wheel through CRF packet loss.
- No clause requires unlock on a validation error, so the stop condition does not trigger and the decision stands.
- Acceptance 1: the clause is recorded on #541.
- Acceptance 2: the RTL, header and row agree (see RTL/Docs). The new check has a failing arm (`validation_error_unlocks` gives rc=1 with the named failure, `receipts/crf_rx-head-make-all.log`).
- Acceptance 3: the focused gates I re-ran are green; the hosted and candidate state is below. F1 is a test-strength gap, not an acceptance failure.

**RTL: CLEAN.**
- `scripts/strip_compare.py`: stripped sha256 is `f0081e18...` at both base and head, with 278 lines and 1,187 tokens identical. A negative control on a changed file reports a difference.
- The only RTL hunk is the comment block at `:34-42`.
- I read the text against the RTL:
  - Lock needs 8 consumed accepts: `settle_r` 0..7, then lock on the 8th (`:575-581`).
  - A sequence discontinuity and a reject both reset `settle_r` (`:564`, `:569-570`).
  - A reject leaves `locked_o` alone and does not touch `tout_r`, which is cleared only by `w_acc_run_w` (`:354`, `:531-533`).
  - The timeout fires at `tout_r == CLK/10`, with a single MEDIA_UNLOCKED (`:533-538`).
  - The reject sets `iv_uf_r`, which commits once per tick (`:374`, `:480-481`, `:503`).
- Reviewer probes P1, P3, P5, P6, P7, P8, P9 and P4b are all DETECTED. Their fault classes are unlock-and-count, settle-not-broken, unlock at commit, timeout ±50 clk, never-count, delayed unlock, and reject raising FRAMES_RX.

**Robustness: UNCLEAN (R322-1-F1).**
- The malformed-input, timeout, idempotence and stopped-state paths were read in the RTL. The head behaves correctly: the drought probe passes 9/9.
- The malformed-only timeout path has no graded regression, because P2 survives.
- Already graded elsewhere: repeat rejects within one interval count once (unit `5 malformed: ONE interval tick`), and a reject never counts FRAMES_RX (P4b detected).

**Tests: UNCLEAN (R322-1-F1).**
- The new check is sound:
  - The precondition is LOCKED with one lock event.
  - Counters are snapshotted after an interval commit.
  - Lock is checked on the rejection edge and on every cycle through the commit, so P9 (delayed unlock) is caught.
  - It verifies one count, no FRAMES_RX, no lock or unlock events, no recount on an empty interval, and resumption without a new lock event.
  - The timeout window is 19,992 to 20,012 clk, which catches P6 and P7 at ±50 clk.
- `validation_error_unlocks` fails the named check. Its anchor is unique, and the campaign enforces the anchor count (`mutants.py:87`).
- Head results: 13,836 unit, 1,932 discontinuity and 69 talker-step checks, and 9/9 campaign controls, all with 0 failures. The servo suite gives 85 unit, 8 rail and 113 PHC-step checks, all with 0 failures. These match the author's published counts.
- Open gap: F1.

**Docs: CLEAN.**
- The header (`KL_crf_rx.sv:34-44`) and row (`REGISTER_MAP.md:837`) state the timeout-based unlock, and every claim traces to the RTL or its consumers:
  - A reject breaks settling, retains lock, does not refresh the timeout, and is counted once per interval as UNSUPPORTED_FORMAT via `fmt_err_o`.
  - `CRF_STATUS[15:8]` carries `crf_fmterr_w[7:0]` (`milan_datapath.sv:2574-2575`, `milan_csr.sv:2358`, row `:842`).
  - GET_COUNTERS @32 carries the full 32-bit `crf_fmterr_w` (`milan_datapath.sv:3556`).
  - `CRF_CTRL[31]` is `i_crf_locked` (`milan_csr.sv:2355`).
- The stale "|delta jitter| within window" lock criterion, which the RTL never implemented, was removed.
- The only remaining "validation error ... to unlock" text is in `docs/history/v1/design/TIME_SYNC.md:351`. It is obsolete history by `docs/README.md:120-124` and was not restored.
- Doc gates at head: docs_check 0 findings; doc style OK; doc paths OK; em-dash 0 findings vs base; TOC check and anchors OK. The em-dash and TOC checks ran with the pre-existing pinned Markdown venv. SV, C++ and Python idiom gates are OK, and `git diff --check` is clean.
- The TOC summary at `REGISTER_MAP.md:185` ("drops after 100 ms of silence") is consistent. S1 is optional.

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|------|---------------|--------------------|----------------|------------|
| Conformance | CLEAN | Issue #541 body and comments 5827373589, 5827406716, 5827529280; `KL_crf_rx.sv:34-44,125-137,354,531-581,661-663`; `milan_datapath.sv:3430`; `REGISTER_MAP.md:837`; public `author/CLAUSE-EVIDENCE.md` @ `a7f7e57a`; campaign log | R322-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |
| RTL | CLEAN | `receipts/rtl-comment-strip.txt`; `KL_crf_rx.sv:309-676`; probes P1,P3,P4b,P5-P9 in `receipts/probe-mutants*.txt` | R322-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |
| Robustness | UNCLEAN (F1) | `KL_crf_rx.sv:354,531-609`; `receipts/probe-drought.txt`; `receipts/probe-mutants.txt` (P2 survives) | R322-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |
| Tests | UNCLEAN (F1) | `sim_discontinuity.cpp:180-224`; `mutants.py:19-31,87`; `sim_main.cpp:440-469`; `receipts/crf_rx-head-make-all.log`; `receipts/mmcm_servo-head-make.log`; `receipts/probe-mutants*.txt` | R322-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |
| Docs | CLEAN | `KL_crf_rx.sv:34-44`; `REGISTER_MAP.md:185,822-842`; `milan_datapath.sv:2574-2576,3556`; `milan_csr.sv:2355,2358`; `docs/history/v1/design/TIME_SYNC.md:351`; `receipts/doc-idiom-checks.txt`; `receipts/doc-md-venv-checks.txt` | R322-1 | `2734b771bcf0b383ea62ef05744452827bafe9e4` |

On re-cover: a fix commit that touches only `tb/verilator/crf_rx/` leaves RTL, Conformance and Docs banked at this head, because nothing in their scope changed. Tests and Robustness must be re-covered at the new head.

## Commands (portable; all run in the foreground)

- RTL identity: `python3 scripts/strip_compare.py <clone> 5b73d3f4... 2734b771...`
- Suites: `git archive 2734b771 hdl tb | tar -x -C scratch/head`. Then run `make VERILATOR=<pinned> all` in `tb/verilator/crf_rx` (the suite's own `-j 0`), and `make` in `tb/verilator/mmcm_servo` with its builder capped at `-j 8`.
- Probes: `python3 scripts/probe_mutants.py scratch/head scratch/probes <pinned> 1` (P4b via `PROBES=P4b_error_flags_frames_rx`), and `sh scripts/run_drought.sh scratch/head scratch/drought <pinned>`.
- Tool: Verilator 5.050 rev v5.050, via the scoped wrapper (`receipts/verilator-identity.txt`).
- Clone integrity after the review (`receipts/clone-integrity.txt`):
  - HEAD, index write-tree, content and modes all equal the head tree.
  - No untracked or ignored files.
  - Gitlinks unchanged: `external efeb541a`, `gptp-processor e5dcea6e`, `protocol-processor 09f9bf38`, `third_party/verilog-axis 48ff7a7e`.
  - No probe edited the clone; every build and mutant ran on an archive copy under `scratch/`.

## Real limits

- I had no primary copy of Milan v1.2 or IEEE 1722-2016 in this environment. The clause check rests on:
  - the in-repo quotations;
  - the executor's published excerpts;
  - my own reading of Table 5.6 and 1722-2016 10.6.

  None of these contradicts the decision, but I did not re-open the standards' pages.
- The first `crf_rx` run used the suite's own `-j 0` builder parallelism. All later builds were capped at `-j 8`.
- Suites run: the receiver unit, discontinuity, talker-step and campaign legs, and the servo suite. Not run: milan_dp, the parent/PP/gPTP/Yosys/builder banks, act/Docker and hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The public evidence tree `a7f7e57a:review-evidence/541-r1` contains the author's logs only. I saw no manager bank receipts there; the manager's bank result is taken from the assignment and from my own reruns.
- Hosted checks at head (`receipts/hosted-checks-snapshot.tsv`, snapshot at review time):
  - Executed and successful: rtl-fast, full-ci-gate, docs-check, docs-check-no-git, elaborate, verilator-lint, wire-accountability, bdd-conformance, yosys-elaboration, Yosys shards 0-3, and Verilator shards 0, 2 and 3.
  - Still in progress: Verilator shards 1 and 4.
  - Skipped: Physical gPTP.
  - I did not observe the `verilator-suites` / `yosys-portability` aggregate contexts. The manager owns hosted and act acceptance.

## Pending manager duties

- Publish this report and its receipts.
- Route F1 to the executor. Re-review is required at the fix head, re-covering Tests and Robustness.
- A second, external positive review is required, per CONTRIBUTING.
- Build and validate the final current-dev candidate merge result at the merge turn (source base and live dev are both `5b73d3f4` at review time).
- Hosted exact-head `verilator-suites` / `yosys-portability` evidence and act acceptance.
- Merge only with explicit maintainer authorization; then post-merge containment and issue closure.

R322-1 FINISHED
