[R285] POSITIVE - exact head e65dccfe586bea9455cf1e10397d275c220c740a

# R285-3: external re-review of PR #549 (Closes #530), docs-only correction round 2

- Round: R285-3, external, cleared context, own detached clone.
- Head: `e65dccfe586bea9455cf1e10397d275c220c740a`, tree `31f4188287b90a87a31c17b4e330b61c3f657038`.
- The head adds four one-line commits (`461e8c34`, `724a6bf2`, `03f26b19`, `e65dccfe`) on `446e79b977640d13fa1e5dc0f9896d6c5a70391d`, which R285-2 reviewed. The commit bodies are empty.
- Source base: `50e78097564244c124e1ec30dd8821f83951ab06`. The gitlinks are unchanged since `c593cbef`: protocol processor `09f9bf38`, gPTP `c1b61743`, verilog-axis `48ff7a7e`, `external` `efeb541a`.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open under any lens at this head.
  - R284-2 F1 = R285-2 F1 (MINOR, RTL and Docs) is fixed at every named site and in the PR body.
  - The `hdl/` delta is comments only. With comments stripped, `milan_datapath.sv` is identical to `c593cbef`, so the silicon image built from `c593cbef` stays the image this head builds.
  - One SUGGESTION (S1) is recorded. It does not affect coverage.

## Reconstruction (public state only)

1. Contract: AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #530:
   - The body. Its frozen acceptance is: a root cause for items 1 and 2, with a simulation reproduction and a fix; a silicon rerun showing continuous streaming with no self-Leave and no emission before Listener Ready; and item 3 explained or fixed.
   - Every comment, including:
     - the A205 DECISION and BLOCKED comments;
     - the manager's DECISION and the processor #106 evidence;
     - the A229, A236 and A238 assignments and REVIEW READY comments;
     - the SILICON RERUN note, the [A237] PASS on `c593cbef`, and the archive note (`1b3fa460`).
   - The A238 assignment scopes this round: comments and docs only. The corner must state the refused branch's full effect and name the CRF output's status bits, and FR_NFR's grant sentence must be corrected. The design question is split to #551, which is Backlog.
3. Authorities at pin `09f9bf38`:
   - `KL_srp_top.sv:445,742-748,772-779,850-862`
   - `KL_srp_talker_fsm.sv:432-442,539-542,634-639,684-710,796-803`
   - `KL_srp_admission.sv:150-154,179-200,205-214`
4. Authorities in the parent:
   - `milan_datapath.sv:1646-1666,1858-1889,2502-2508,3057,5278-5320,6576-6650`
   - `KL_pp_shadow.sv:626-630`
   - `KL_talker_diag_ctx.sv:24-40,255-266`
   - `REGISTER_MAP.md` rows `0x694`, `0x698`, `0x750` and `0x82C`
   - `REQUIREMENTS.md` section 5
5. The round delta `git diff 446e79b9..e65dccfe` (six files) and its four commits, plus the whole-PR diff `50e78097..e65dccfe` for the touched pages.
6. Public evidence:
   - Tree `9d1b176c`, `review-evidence/530-r1`, which holds `author/`, `correction-a236/` and `reviews/`.
   - The silicon archive `1b3fa460`, `review-evidence/530-r1/silicon-a237/`. Its HANDOFF gives identity `c593cbef` with bitstream CRC `11a89d32`, and PASS on 3a and 3b.
   - I found no manager bank receipt for this head in either tree or in any comment. The manager's statement that the static/builder and native banks passed is recorded as the manager's. This round does not rely on it.

My independent pass over the diff and the authorities ran first. Its verdict and draft ledger were written to this file before I read any prior public review in full. The disposition of prior findings follows the ledger.

## Findings

No BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - lenses: RTL, Docs - the refused-branch indicator list overstates two of its bits

- **Where:** `hdl/milan/milan_datapath.sv:6613-6614`, REFUSED paragraph: "CRFT_CTRL[6]/[7], LWSRP_STATUS[6], [8] for source 0 and the 0x82C talker lobs pulse with it."
- **Evidence:**
  - `0x82C[2]` at index 0 is `listener_observed_w`, which is `cfg_acmp_lobs | (cfg_lwsrp_enable & lwsrp_listener_ready)` (`milan_datapath.sv:1861-1862,1882-1883`). That is source 0's registered Listener Ready or Ready Failed, not its ACTIVE. It does not pulse with the refused licence. Only index > 0 reads `lwsrp_stream_gate` (`:1885-1886`).
  - `LWSRP_STATUS[6]` is `|pp_cd_srp_active_w` (`:6647`). It pulses only when no other source is ACTIVE.
  - The authoritative row `REGISTER_MAP.md` `0x82C` states the index split exactly: "at idx 0 source 0's registered Listener Ready or Ready Failed, at idx > 0 that source's ACTIVE".
  - The same paragraph's ADMITTED branch already marks `[6]` as `(|ACTIVE)`.
  - Every other named bit is correct, on the CRF output (`CRFT_CTRL[6]`/`[7]`, `:5318-5319`) and on source 0 (`[8]`, `:2505`).
- **Why a SUGGESTION and not a MINOR:**
  - The claim is true for the CRF output the corner is written for (index 1 on the AX7101 1x1 shape).
  - The one document that defines `0x82C` is exact.
  - `0x82C` is snap-latched, so no controller reads a pulse of a few cycles off it except by coincidence. No reader action is misdirected.
  - The "lobs pulse" wording came from my own R285-2 required outcome, and the author followed it. I record it rather than let it pass unmarked.
- **Optional change:** "the 0x82C lobs at index > 0". `LWSRP_STATUS[6]` could carry `(|ACTIVE)` here as it does above. Comments only.

### Observations (not findings against this PR)

- **The refused-branch licence (#551).** A declaration that the admission round refuses inside the optimistic window keeps ACTIVE, and so the licence, for up to three rounds. This is a narrow exception to FR-SRP-03's "on failure the stream MUST NOT transmit".
  - This PR created that exception when the gate moved from the raw verdict to ACTIVE. The manager's #530 DECISION required that move.
  - It is now stated openly at `FR_NFR.md:207-219` and on every corner site.
  - It is published as a decision-pending conflict in #551 (Backlog), as AGENTS.md section 2 requires for a requirement and implementation conflict.
  - It needs a registering Listener event decoded within a window of at most 3 x `N_SOURCES` cycles after a declaration. #530's acceptance ("no emission before Listener Ready") holds in both branches.
  - I do not raise it as a finding of this PR. The design decision belongs to the manager and the owner in #551.
- **A related pre-existing port comment.** `hdl/milan/KL_pp_shadow.sv:629` ("RAW Sigma-slope verdict; lags srp_active_o by up to three admission rounds") predates the PR and describes only the admitted branch. It is optional for #551's lane.

## Independent evidence at this head

Receipts are under `receipts/` and scripts under `scripts/`. Local paths are redacted to placeholders. The simulator is the scoped 5.050 build: wrapper sha256 `905795b9...`, version string in `receipts/00-tool-identity.txt`. Builds used 8 jobs, in a disposable shared clone under `scratch/` only.

**`hdl/` delta is comments only**
- Result: `446e79b9..e65dccfe` has 54 changed lines and `c593cbef..e65dccfe` has 113. None is a non-comment line and none carries a metacomment token. `milan_datapath.sv`, stripped (string-aware, `//` and `/* */` with metacomments kept, whitespace-normalised), is IDENTICAL at `446e79b9`, `c593cbef` and `e65dccfe` (sha256 prefix `df597781949b1278`, this script's normalisation).
- Canary: `50e78097` vs `c593cbef` reports DIFFERENT, so the comparator can fail.
- Receipt: `receipts/03-hdl-comment-only.txt`, `scripts/hdl_comment_only.py`.

**Scope of the delta**
- Result: `c593cbef..e65dccfe` touches only `CHANGELOG.md`, `EGRESS_QUEUE_MAP.md`, `FR_NFR.md`, `REGISTER_MAP.md`, `ieee8021q.md` and `milan_datapath.sv`. No gitlink changes, and the commit bodies are empty.
- Receipt: same receipt.

**Processor citations in the new text**
- Every cited line range matches. They show:
  - opt aging on the third round strobe (`KL_srp_top.sv:772-779`);
  - `opt_r`/`opt_cnt_r = 2` set on the gate accept (`:855-858`);
  - that accept is the same handshake the talker FSM uses (`:489-492,746-748`);
  - the registrar is cleared to MT with `lstn_val_r = 0` on gate re-open (`KL_srp_talker_fsm.sv:705-709`);
  - ACTIVE is `declaring & !fail_r & {Ready, ReadyFailed} & sr_admitted_i`, where `sr_admitted_i = opt_r | admitted` (`:800-803`; top `:445,501`);
  - `fail_r` follows `sr_admitted_i` only (`:440-441,541`);
  - refusal: `refuse_w` sets `over_r`, and `sr_admitted_o = grant_r & req` (`KL_srp_admission.sv:152-154,186,207-214`);
  - the round walks one source per cycle (`:179-200`).
- Receipt: `receipts/02-rtl-citations.txt`.

**Status bits named in the new text**
- `LWSRP_STATUS` packs `[6]` `|ACTIVE`, `[7]` over_limit, `[8]` `lwsrp_stream_gate[0]` and `[9]` `|sr_admitted` (`milan_datapath.sv:2502-2508`, widths `:1646-1666`).
- `CRFT_CTRL[6]` is `crft_res_active_w`, the top ACTIVE slot, and `[7]` is `crft_emit_en_w` (`:5280-5281,5305-5307,5318-5319`).
- `tkd_streaming_w = {crft_emit_en_w, aaf_stream_en_w}` (`:3057`).
- STREAM_START and STREAM_STOP count its edges, and a start zeroes MEDIA_RESET, TIMESTAMP_UNCERTAIN and FRAMES_TX (`KL_talker_diag_ctx.sv:25-37,255-266`).
- The processor and datapath share one clock (`KL_pp_shadow.sv:243`), so the window is not stretched by a crossing. It lasts at most 3 x `ACMP_SRC_C` cycles, which is shorter than any PDU interval, so "at most one PDU per source" holds.
- The exception is S1.
- Receipt: `receipts/02-rtl-citations.txt`.

**Residual-claim search**
- Result: 75 hits for "registered at declaration", "already registered", "outlived", "whole/only effect", "status skew", "inside the window", "optimistic window" and "three rounds", outside the processor and history. I read every PR-relevant hit:
  - "status skew" and "whole effect" appear only in the admitted branch (`REGISTER_MAP.md:1120`, `ieee8021q.md:61`, `CHANGELOG.md:43`, `milan_datapath.sv:6593`);
  - "inside the window" appears only as "does not fall inside the window" or as the rise condition;
  - "registered at the declaration" and "outlived" appear nowhere in PR text.
- The remaining hits are unrelated uses elsewhere in the repository.
- Receipt: `receipts/06-residual-claim-search.txt`.

**Docs and source gates on the head bytes**
- All of these return rc 0:
  - `docs_check`;
  - `check_em_dash --base 50e78097`;
  - `check_doc_style`;
  - `gen_toc --check` and `--verify-anchors`;
  - `check_doc_paths`;
  - `check_rtl_source_lists`;
  - `check_feature_status`;
  - `check_sv_idiom`;
  - `git diff --check 50e78097 HEAD`.
- Receipt: `receipts/01-docs-gates.txt`.

**`obj_crflic` leg at head, unmodified**
- Result: 85 checks, 0 failures, RESULT PASS.
- Receipt: `receipts/04-crflic.log`.

**BDD suite at head**
- Result: 14 features, 317 scenarios and 1518 steps passed, 0 failed. The licence steps read the gate source text and `REGISTER_MAP.md`.
- Receipt: `receipts/05-behave.log`.

**PR body at this head (read only)**
- Result:
  - It says "Closes #530".
  - Its Known limitations state both branches, the right bits (CRF: `CRFT_CTRL[6]`/`[7]`, `LWSRP_STATUS[6]`; `[8]` source 0 only) and #551.
  - The disposition row marks R284-2/R285-2 F1 fixed.
  - The PR is not a draft, and its base is `dev`.
- Receipt: read with the `gh` CLI; not archived.

**Hosted runs at the exact head (read only, 06:50Z)**
- Result: 0 check runs and 0 workflow runs recorded for `e65dccfe`, combined status `pending` with 0 statuses. There was no hosted evidence at this head to read.
- Receipt: `receipts/07-hosted-check-runs.tsv`.

**Clone integrity after all work**
- Result:
  - HEAD, tree and index tree equal the head.
  - All 874 tracked blobs match in bytes and mode, with 0 assume-unchanged or skip-worktree flags.
  - 0 untracked or ignored leftovers. A `scripts/__pycache__/` created by this round's gate runs was removed before the final check.
  - The gitlinks `protocol-processor 09f9bf38`, `gptp-processor c1b61743` and `third_party/verilog-axis 48ff7a7e` are checked out at their pins and clean. `external` is not initialised, as in the clone.
- Receipt: `receipts/08-verify-clone.txt`, `scripts/verify_clone.sh`.

## Per-lens results (R285-3, exact head `e65dccfe`)

```text
[R285] PASS Conformance - receipts/03-hdl-comment-only.txt (comment-free milan_datapath.sv identical to c593cbef; no tb/ tests/ scripts/ syn/ sw/ file or gitlink changed), receipts/04-crflic.log (85/0 at head), milan_datapath.sv:1886,1916,2026,5280-5307,6632 against KL_srp_talker_fsm.sv:800-803 and Milan v1.2 5.3.7.3/5.3.7.7 Table 5.4 - behaviour byte-identical to the c593cbef logic R285-1 covered and the silicon rerun passed on; the new text states the 5.3.7.3 licence and the Table 5.4 effects of the refused branch correctly, and FR_NFR.md:207-219 now quotes FR-SRP-03 and records the window exception against #551 instead of claiming ACTIVE needs the grant
[R285] PASS RTL - milan_datapath.sv:6576-6636 comment block (OPENING EDGE, ADMITTED, REFUSED, later-lane note) read line by line against KL_srp_top.sv:445,489-492,746-748,772-779,855-858, KL_srp_talker_fsm.sv:440-441,541,638,686-710,800-803, KL_srp_admission.sv:152-154,179-214, and the parent wiring :1861-1886,2502-2508,3057,5280-5319,6632,6647 (receipt 02); logic unchanged (receipt 03, canary DIFFERENT); only S1 (a SUGGESTION) remains
[R285] PASS Robustness - receipts/03 (no logic, harness or step change since c593cbef), receipts/04 (leg phases [A]..[E], [INV] at head, 85/0), KL_srp_top.sv:772-779 and KL_srp_talker_fsm.sv:705-710 - the optimistic-window corner re-derived for both branches: reachable only with a registering Listener event within 3 x N_SOURCES cycles of a declaration, one clock domain (KL_pp_shadow.sv:243), at most one PDU per source, no emission before a registered Listener Ready or Ready Failed; escape terms at milan_datapath.sv:1913-1916,5305-5307 unchanged
[R285] PASS Tests - receipts/03 (sim_crf_licence.cpp, crflic_mutants.py, Makefile, tests/features, tests/steps untouched since c593cbef), receipts/04-crflic.log (85 checks, 0 failures), receipts/05-behave.log (317/0) - round-1 coverage (three mutants caught, gate-reverted arm 23/85, old-pin arm 17/85, BDD pin fails on a planted gate) applies unchanged
[R285] PASS Docs - CHANGELOG.md:29-58; EGRESS_QUEUE_MAP.md:64-101; FR_NFR.md:144,205-219; REGISTER_MAP.md:1105-1133,1167-1168 and rows 0x750/0x82C; ieee8021q.md:50-69,98-99; milan_datapath.sv:6576-6636 comments; the PR body - both branches, the cleared-registrar premise, the window-end fall, the Table 5.4 pair and reset, at most one PDU, the CRF output's bits and #551 are stated consistently at every site; receipts 01 (gates green) and 06 (residual search); S1 is a SUGGESTION
```

## Ledger (reviewer-owned)

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:1886,1916,2026,5280-5307,6632`; processor `KL_srp_talker_fsm.sv:800-803`; Milan v1.2 5.3.7.3 and 5.3.7.7 Table 5.4 (spec readings from round 1); `FR_NFR.md:205-219`; receipts 03 and 04 | R285-3 (re-applied; first covered R285-1) | `e65dccfe586bea9455cf1e10397d275c220c740a` |
| RTL | CLEAN | `milan_datapath.sv:1646-1666,1858-1889,2502-2508,3057,5278-5320,6576-6650`; `KL_pp_shadow.sv:243,626-630`; processor `KL_srp_top.sv:442-445,489-501,742-748,770-780,850-862`, `KL_srp_talker_fsm.sv:432-442,539-542,634-639,684-710,796-803`, `KL_srp_admission.sv:150-214`; receipts 02 and 03 | R285-3 | `e65dccfe586bea9455cf1e10397d275c220c740a` |
| Robustness | CLEAN | `sim_crf_licence.cpp` phases `[A]`..`[E]`, `[INV]` (receipt 04); the optimistic window re-derived for both branches from the processor sources; escape terms `milan_datapath.sv:1913-1916,5305-5307` | R285-3 (re-applied; first covered R285-1 at `c593cbef`, logic unchanged since) | `e65dccfe586bea9455cf1e10397d275c220c740a` |
| Tests | CLEAN | `sim_crf_licence.cpp`, `crflic_mutants.py`, `Makefile`, `tests/features/milan_streaming_licence.feature`, `tests/steps/milan_streaming_licence_steps.py` (untouched since `c593cbef`, receipt 03); receipts 04 (85/0) and 05 (317/0) at head | R285-3 (re-applied; mutant and arm coverage from R285-1 at `c593cbef`, an ancestor whose Tests scope is untouched since) | `e65dccfe586bea9455cf1e10397d275c220c740a` |
| Docs | CLEAN | `CHANGELOG.md`, `EGRESS_QUEUE_MAP.md`, `FR_NFR.md`, `REGISTER_MAP.md`, `ieee8021q.md`, the in-RTL comments of `milan_datapath.sv`, the PR body; receipts 01 and 06 | R285-3 | `e65dccfe586bea9455cf1e10397d275c220c740a` |

Every lens is clean at the exact head. S1 is a SUGGESTION and does not affect coverage.

## Prior public findings on this PR, resolved or retained at this head

I read these after the verdict and ledger above were drafted.

| item | disposition at `e65dccfe` | basis |
|---|---|---|
| **R285-2 F1**, MINOR (RTL, Docs): false "registered at the declaration / re-declaration outlived" premise; "ACTIVE falls inside the window"; "status skew is the whole/only effect" | **RESOLVED.** Each of the five sites states the cleared-registrar premise, and none keeps the old one. ACTIVE falls at the window's end. The refused branch's effect is stated: licence and Table 5.4 level for up to three rounds, a STREAM_START/STREAM_STOP pair, the interval counters reset, at most one PDU per source. "Status skew" is limited to the admitted branch. Q-9 now says ACTIVE is lost "when the three-round optimistic window ends". The PR body matches | `milan_datapath.sv:6581-6618`; `CHANGELOG.md:40-51`; `EGRESS_QUEUE_MAP.md:77-101`; `REGISTER_MAP.md:1105-1133`; `ieee8021q.md:56-69,98`; receipts 02 and 06 |
| **R284-2 F1**, MINOR (Docs, RTL), the same defect, plus: `LWSRP_STATUS[8]` named as showing the CRF output; `FR_NFR.md:210-213` said ACTIVE "needs ... the grant" | **RESOLVED.** Every site names `CRFT_CTRL[6]`/`[7]` and `LWSRP_STATUS[6]` for the CRF output and `[8]` as source 0 only. The `0x694[9]` and `0x698` rows say "trail the licensed source's ACTIVE (`[6]`, `[8]` for source 0, `CRFT_CTRL[6]` for the CRF output)". FR_NFR quotes FR-SRP-03, says the term "is the grant except inside the optimistic window", and records the refused-branch licence against #551. The PR body's Known limitations were rewritten the same way | `REGISTER_MAP.md:1130-1132,1167-1168`; `FR_NFR.md:207-219`; PR body |
| R285-2 S1 (RTL, Docs): `milan_datapath.sv:5294-5296` "rides the same bw-gate" | Retained as a SUGGESTION. Unchanged, and it predates the PR | read at head (`:5295-5296`) |
| R284-2 S1 (`milan_datapath.sv:1588` "stop consulting the admission verdict") and S2 (pre-existing bw-gate and slope-MUX terms) | Retained as SUGGESTIONS, not taken. The PR body records them for triage | PR body |
| R284-1 S1, R284-1 S2, R285-1 S1, R285-1 S3 (Tests-scope suggestions) | Retained as SUGGESTIONS, unchanged. No coverage effect | receipt 03 (Tests scope untouched) |
| Earlier F1/F2 of R284-1 and R285-1 | Stay RESOLVED, as recorded in round 2. The corner wording they prescribed is superseded by the R285-2/R284-2 F1 fix above | round-2 dispositions; receipt 06 |
| R285-2 out-of-scope builder remnants (`sw/builder/endstation_builder.py:332`, `test_builder.py:16811-16813`) | Unchanged. Not a finding against this PR; still a triage candidate for a new Issue | not in this PR's diff |

## Limits

- Physical calibration and hardware: NOT RUN by this round. The [A237] silicon PASS is on `c593cbef`. This round proves only that the head's `hdl/` logic is comment-identical to it (receipt 03). It did not audit the silicon archive beyond its HANDOFF identity and verdict lines. Field skips are not hardware proof.
- Both corner branches are established by reading RTL. No bench, including the `obj_crflic` leg, stages a refused declaration inside the window, and I built none.
- Not run, per scope:
  - the full parent, processor, gPTP, Yosys and builder banks;
  - the other `milan_dp` legs, `pp_shadow` and the mutant campaign;
  - the failing arms, which are unchanged since round 1;
  - `lint_rtl` and `xvlog_gate`;
  - act, Docker and hardware.
- The specification text (Milan v1.2, 802.1Q) was not re-read this round. The readings are those of round 1.
- No hosted run existed at the exact head when I queried it (06:50Z). The manager's bank result at this head is the manager's statement. I found no public receipt for it.

## Pending manager duties

- Exact-head hosted evidence: `rtl-fast`, and after the PR is marked ready, `verilator-suites` (the shard carrying `obj_crflic`) and `yosys-portability`. Also act acceptance at this head.
- A second independent positive review at this head, from the internal lane (R284-3).
- Candidate-merge validation against live dev `f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f` (source base `50e78097`), then post-merge containment.
- Closing #530 through "Closes #530" on merge, and moving it to Done.
- Optional: triage S1 with the retained suggestions, and the builder remnants as a new Issue. #551 stays the owner of the refused-branch design question.

Publishable receipts and scripts are listed in `MANIFEST.sha256`. The disposable clone and fetched comment copies live only under `scratch/`.

R285-3 FINISHED
