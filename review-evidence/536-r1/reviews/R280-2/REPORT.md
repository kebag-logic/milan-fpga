[R280] POSITIVE - exact head fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad

Round R280-2, internal cleared-context review of issue #536 / PR #543.
Head `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad`, tree `24a2b1c9bd657d2d14b5e814f18ec349108ffc1f`, source base `26d855a9176d63625e6635a029a0c44e3d57ce9a`.
This round covers correction round 1: four commits on `612db13c2` (`8179587ee`, `3753b5749`, `bfe2e5c79`, `fb84de54e`).
All five lenses were applied at this head. Each is CLEAN. No BLOCKER, MAJOR or MINOR finding is open.
The R280-1 and R281-1 findings (F1 to F3 in each) are resolved at this head. The resolution was checked by executed probes.

## Result in one paragraph

The offline AECP model's MVU sub-decode and its `E_MVUINFO` program agree with the pinned engine (`424c688`) byte for byte.
This round replayed every frame that the MVU-region scenarios of `aecp_response_contract.feature` send (41 frames, feature lines 89 to 288) through a build of the pinned `tb/pp_top`.
Each RTL answer equals the model's answer, 41 of 41, Ethernet padding included (`receipts/rtl_vs_model_head.txt`).
That includes the three rows the author could only argue from RTL source:
- the @26 high-nibble row `00-1B-C5-0A-D1-00` (line 186)
- the @26 low-nibble row `00-1B-C5-0A-C2-00` (line 187)
- GET_MILAN_INFO at cdl 24 (line 197)

All three are now executed evidence and agree with the RTL.
The comparison is not vacuous:
- A one-octet change to the model answer on each of those three rows turns exactly those three rows into mismatches (`receipts/rtl_vs_model_control.txt`).
- Two RTL mutants each diverge from the model on exactly the rows built to catch them (`receipts/rtl_mutants.txt`):
  - @26 compared on its high nibble only: the C2 row.
  - The length floor made exact: the cdl 24 and cdl 112 rows.

On the model side, this reviewer designed 30 single-substitution arms plus a control. 29 arms fail exactly their predicted feature lines. The one exception is an equivalent mutant, explained below (`receipts/model_mutations.txt`).
Both prior rounds' public mutation scripts, run unmodified at this head, kill every arm except R280-1's R9. R280-1 already classified R9 as equivalent.

## What the round reconstructed, in order

1. `AGENTS.md` and `CONTRIBUTING.md`: the lane, the lenses, the ledger rules and the section 6 wording rules. Then `docs/README.md`.
2. Issue #536: the body, with its three acceptance criteria (frozen), the A10 assignment, and the A223 TAKEN / REVIEW READY comments. Also the A10 correction-round assignment and the A230 REVIEW READY comment (`receipts/public_state.txt`).
3. PR #543: the body at this head, the three A10 review-start notices, and the head OID. The PR has no review objects.
4. Linked authorities:
   - `docs/reference/FR_NFR.md` FR-MVU-01/03.
   - `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 1.3/1.4 and `docs/reference/milan_feature_status.json` `served_mvu_operations`.
   - The pinned engine: `protocol-processor/hdl/aecp/KL_aecp_engine.sv` (`MVU_*_C` at :702-713; the `aem_w` guard and the RX-validator bucket note at :1133-1141; `mvu_get_milan_info_w` at :1290-1296; the walk captures and `pid_lo_r` at :3180-3195).
   - `protocol-processor/tb/pp_top/sim_main.cpp` M1 to M8 (:2190-2440).
   - `protocol-processor/docs/architecture/06_aecp_engine.md` 6.9.
5. `git diff 26d855a9..fb84de54` (5 files, +405/-26) and the six one-line commits. Each commit has one parent and no trailers.
6. Public evidence at `765cb958`, `review-evidence/536-r1`:
   - The correction-round packet: `gates.log`, `mutations.py/.log`, `xcheck_rows_vs_rtl.py/.log`, and the two review-script rerun logs.
   - Each file was checked against the published `MANIFEST.json` hashes. HANDOFF.md differs from its original only by the recorded path redaction.

The two prior review reports were read only after this round's independent pass and its results were complete.

## Independent results at this head

| Check | Result | Receipt |
|---|---|---|
| `cd tests && behave --no-capture -f plain` | 14 features / 343 scenarios / 1736 steps passed, exit 0 | `receipts/behave_full_head.txt` |
| contract feature alone | 59 scenarios / 435 steps passed, exit 0 | `receipts/behave_contract_head.txt` |
| `check_py_idiom`, `docs_check`, `check_feature_status` | every ratchet held; 0 findings; 0 findings | `receipts/static_gates.txt` |
| `check_em_dash --base 26d855a9` | 0 findings over 2 added lines in 2 pages, arms 57/57 | `receipts/static_gates.txt` |
| `git diff --check`; diff over `protocol-processor gptp-processor hdl firmware third_party` | clean; empty (no RTL, processor, firmware or gitlink change) | `receipts/static_gates.txt`, `receipts/public_state.txt` |
| Every MVU-region frame, model vs pinned RTL | 41/41 byte-identical answers | `receipts/rtl_vs_model_head.txt`, `.in`, `.sim.log`, `receipts/contract_frames_head.jsonl` |
| Negative control (model answer altered on rows 186, 187, 197) | exactly those 3 rows mismatch | `receipts/rtl_vs_model_control.txt` |
| RTL mutants: @26 high nibble only; length floor exact | only row 187 diverges; only rows 197 and 198 diverge | `receipts/rtl_mutants.txt` |
| Reviewer model arms (30 + control) | 29 exact, 1 equivalent (below) | `receipts/model_mutations.txt` |
| R280-1 `r280_mutations.py`, unmodified | R1 to R8, R10, R11 red; R9 survives (equivalent, as classified in R280-1); control green before and after | `receipts/prior_r280_1_arms_rerun.txt` |
| R281-1 `mutate_model.py`, unmodified | baseline green; all nine arms killed | `receipts/prior_r281_1_arms_rerun.txt` |
| Hosted check runs at the exact head (read-only) | all seven required contexts `success`; Verilator 5/5 and Yosys 4/4 shards executed; `bdd-conformance` executed; `Physical gPTP (nightly and manual)` **skipped**, not executed | `receipts/hosted_check_runs.tsv` |
| Clone after all probes | HEAD, tree, index and worktree exact; 872 superproject and 222 processor blobs re-hash to their index IDs; gitlinks unchanged; no ignored residue | `receipts/clone_restore_verify.txt` |

### The equivalent arm

`over-length step sends no extra octets` replaces the step's `bytes(range(cdl - 20))` with nothing.
Row 198 (cdl 112) fails, as predicted. Row 197 (cdl 24) does not.
`build_command` pads every frame to the 60-octet Ethernet minimum. A cdl 24 command ends at frame octet 50, so its four octets past Figure 5.3 are present either way, as padding zeros instead of `00 01 02 03`.
The sub-decode does not read them. The pinned RTL serves both frames identically: this round executed the head frame, and pp_top's own zero-filled builder sends the other form.
So the row's claim, that a longer GET_MILAN_INFO is still served with the 20-octet body, holds for both frames. The step docstring's claim, that the frame holds every octet its length claims, is also true for both. This is not a test gap.

## Findings

No BLOCKER, MAJOR or MINOR finding at this head.

Two suggestions are retained from R280-1 and remain optional. Neither affects coverage.

- **R280-S1 - SUGGESTION - Tests - `tests/steps/aecp_engine_steps.py:907`.**
  - The MVU RTL gate parses only `localparam logic [15:0] MVU_(GET|SET)_*_C = 16'hXXXX;`.
  - A later pin could declare a served command type at `[14:0]` or with a `16'd` literal. The gate would then stay green while GET_MILAN_INFO still parses.
  - Failing closed on any unparsed `MVU_(GET|SET)_` localparam would close this.
  - The regex is unchanged at this head.
- **R280-S2 - SUGGESTION - Tests, Docs.**
  - `SERVED_MVU` is not tied to the ledger's `served_mvu_operations`. Both hold only `GET_MILAN_INFO` today (`docs/reference/milan_feature_status.json:37-39`).
  - The PR records this as a known limitation.

## Clean-lens result

[R280] PASS Conformance - issue #536 acceptance 1-3; tests/features/aecp_response_contract.feature:98-233; tests/steps/aecp_engine_model.py:76-91, :542-555, :660-695; tests/steps/aecp_engine_steps.py:76-98; receipts/rtl_vs_model_head.txt - checked against the three frozen acceptance criteria, the pinned engine (KL_aecp_engine.sv:1290-1296, :3190-3195), pp_top M1-M8, and the Milan figure lengths and quotations recorded from the specification text in the R280-1 and R281-1 public receipts. Acceptance 1: 0x0000 is served in Figure 5.3 (SUCCESS, cdl 32, protocol_version 1, features_flags 0, certification_version 0), and 0x0001-0x0004 are each sent in their own Figure 5.5/5.3/5.6/5.7 form (cdl 28/20/92/20) and echoed NOT_IMPLEMENTED exactly as the RTL answers them: 41/41 executed frames are byte-identical. Acceptance 2: every row has a failing arm (receipts/model_mutations.txt). Acceptance 3: behave and the docs gates pass. The MVU citations at the head read: Milan Table 5.19 and IEEE 1722.1-2021 9.6 / Table 9-6 for status 1 (feature:105-110, steps:91-98), the command-length echo stated as the engine's choice, 9.3.5.3.3 named as the AEM rule, and the protocol_version SHALL attributed to Section 4.2.4 beside 5.4.4.1's own sentence (model:81-84). The Figure 5.6 builder (clock_domain_index @30; flags, reserved, default_mcr_prio, user_mcr_prio @32-35; a reserved quadlet; a 64-octet name) matches the layout the prior rounds quoted.

[R280] PASS RTL - protocol-processor gitlink 424c688 (unchanged base..head); KL_aecp_engine.sv:702-713, :1133-1141, :1290-1296, :3180-3195; KL_pp_rx_validator.sv 6/7 -> MVU bucket; tests/steps/aecp_engine_model.py:317-406 (deliver), :448-467 (_mvu_program), :542-555 (_mvu_command_type) - the model's mirror of the RTL was checked against the source and then executed against a build of the pinned tb/pp_top with the pinned simulator (Verilator 5.050). The sub-decode's six conjuncts, the @26 whole-byte compare, the >= 8-octet floor on the trimmed payload, the 16-bit r+command_type word, the disjoint message_type guards (AEM arms on type 0 only, MVU on type 6 only), the restated 20-octet body and the command-length echo all agree with the RTL: 41/41 identical frames. The two RTL mutants show the replay detects an RTL divergence at the nibble and length rows. The diff contains no HDL, processor, firmware or gitlink change.

[R280] PASS Robustness - tests/features/aecp_response_contract.feature:178-198 (sub-decode outline), :208-225 (message_type outline), :131-139 (per-figure lengths), plus the existing drop and foreign-entity rows - covered: malformed and foreign input (one row per protocol_id octet @22-@27, both @26 nibbles, a one-bit @27 change, r = 1); minimum and maximum (one octet short of Figure 5.3 at cdl 19; over-length cdl 24 and cdl 112 served with the fixed body; the longest MVU echo at cdl 92); invalid ordering and type (the served octets under message_type 0/2/4/8/10/12/14, each echoed under its own type); junk reserved restated as zero; feature-disabled (`mvu_served` is a required keyword with no default, and an undeclared command type falls to the echo). Every one of these rows was executed against the RTL and agrees. Reset during activity and backpressure are not reachable in this stateless offline model, and the RTL's own pp_top M7 owns the post-MVU descriptor path.

[R280] PASS Tests - receipts/model_mutations.txt, receipts/prior_r280_1_arms_rerun.txt, receipts/prior_r281_1_arms_rerun.txt, receipts/rtl_mutants.txt - each new row can fail for the defect it names. Checks: each protocol_id octet's compare dropped fails exactly that octet's row; @26 cut to either nibble fails exactly the other nibble's row; @27 bit 0 ignored fails only the C1-01 row; the r bit, the command_type read, the length floor (-1), the exact length, and a Figure 5.3+4 cap each fail exactly their rows; message_type 0 or 10 accepted fails exactly that type's row; an MVU echo capped at 8 octets fails rows 0x0001 and 0x0003; each figure's builder shortened or lengthened fails exactly its row; a forwarded reserved field, each Figure 5.4 quadlet, and a short body fail their rows; declaring 0x0002 served fails row 0x0002 and the RTL gate (line 233); a step that leaves message_type 6 fails all seven type rows. One arm is equivalent, with the reason given. The controls are green. The expected values come from the executed RTL, not from the model.

[R280] PASS Docs - tests/README.md:90 (T1 row, 59); docs/MILAN_V12_ROADMAP.md:539 (proof-ladder row); tests/features/aecp_response_contract.feature:98-115, :156-168, :200-206, :227-231 (comment blocks); tests/steps/aecp_engine_steps.py:76-98, :262-278 (header and SERVED_MVU note); tests/steps/aecp_engine_model.py:76-91, :680-687 - checked for agreement with the behaviour, for counts and for the wording gates. The scenario count 59 matches behave. The roadmap row's "MVU_GET_*/MVU_SET_* constants" matches the gate's regex. The #510 and RECOMMENDED statements agree with MILAN_COMPLIANCE_MATRIX 1.4. docs_check, check_em_dash and check_feature_status report 0 findings. No obsolete document was restored, and the compliance-matrix and roadmap Section 3 rows owned by #537 are untouched. The PR body, the A230 REVIEW READY comment and the public packet carry enough evidence for a cold reviewer, and this round could reproduce every claimed gate.

## Per-lens coverage, this round

| Lens | Applied | Open BLOCKER/MAJOR/MINOR under it | Result |
|---|---|---|---|
| Conformance | yes | none | CLEAN |
| RTL | yes | none | CLEAN |
| Robustness | yes | none | CLEAN |
| Tests | yes | none | CLEAN |
| Docs | yes | none | CLEAN |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #536 acceptance; feature :98-233; model :76-91, :542-555, :660-695; steps :76-98; RTL replay 41/41 | R280-2 | fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad |
| RTL | CLEAN | KL_aecp_engine.sv :702-713, :1133-1141, :1290-1296, :3180-3195; model deliver/_mvu_program/_mvu_command_type; pinned pp_top replay + 2 RTL mutants | R280-2 | fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad |
| Robustness | CLEAN | feature :131-139, :178-198, :208-225; executed RTL agreement on every malformed, boundary and type row | R280-2 | fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad |
| Tests | CLEAN | 30 reviewer arms + control; R280-1 11 arms; R281-1 9 arms; RTL mutants; controls | R280-2 | fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad |
| Docs | CLEAN | tests/README.md:90; docs/MILAN_V12_ROADMAP.md:539; feature and step comment blocks; docs gates | R280-2 | fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad |

Every lens is covered at the merge-candidate source head itself, so no later commit has un-covered one.

## Prior public review findings on this PR

| Finding | Severity, lenses | Status at this head | Evidence |
|---|---|---|---|
| R280-F1 = R281-F1: the sub-decode outline pinned 3 of its guards | MINOR; Tests, Robustness | RESOLVED | Rows :181-189 (each octet @22-@27, both @26 nibbles, one-bit @27), :197-198 (over-length served), :219-225 (seven other message types). R280-1 R1-R5 red; R281-1 `mt_guard_dropped`, `len_exact_20`, `pid_head_22_23_dropped`, `pid_24_25_dropped`, `pid_26_dropped`, `pid_only_27` killed; this round's per-conjunct arms exact; all rows RTL-identical |
| R280-F2 = R281-F2: rows 0x0001/0x0003 sent a truncated Figure 5.3 frame | MINOR; Conformance, Tests, Robustness | RESOLVED | `MVU_COMMAND_FORMS` (model :680-695) sends Figures 5.5/5.3/5.6/5.7; rows assert cdl 28/20/92/20; the step refuses a row whose figure is not the command's (steps :392-407). R280-1 R10 red; the 8-octet echo cap fails exactly rows 0x0001 and 0x0003; the RTL answers these frames identically |
| R280-F3(a): IEEE 9.3.5.3.3 cited for the MVU echo | MINOR; Conformance, Docs | RESOLVED | feature :105-110 and steps :91-98 cite Milan Table 5.19 and IEEE 9.6 / Table 9-6, call the length echo the engine's choice, and name 9.3.5.3.3 as the AEM rule; the MVU text no longer relies on 9.3.5.3.3 |
| R280-F3(b) = R281-F3: a 4.2.4 quotation under a 5.4.4.1 heading | MINOR; Docs, Conformance | RESOLVED | model :81-84 quotes 5.4.4.1's "The value of this field is 1" and attributes the SHALL sentence to Section 4.2.4 |
| R280-S1, R280-S2 | SUGGESTION | RETAINED as suggestions | see Findings |
| R281-S1 = R280-O1 | SUGGESTION / observation | RETAINED, out of scope | see below |

## Out-of-scope observations (present at base `26d855a9`, not counted against this head)

- **O1** (= R281-S1). The "NOTE ON THE DECODE" at `aecp_response_contract.feature:32-36` has been stale since #83. The PR records it for its own Issue.
- **O2.** `tests/README.md:80` and `:128` still carry the dated total of 312 scenarios. The count is 343 at this head.
- **O3.** The 5.4.4.1 NOTE recommends that a PAAD-AE whose active configuration is not compliant not reply to GET_MILAN_INFO. The engine always replies, and so does the model. This is a processor/owner decision, and the PR lists it.
- **O4.** `protocol-processor/docs/architecture/06_aecp_engine.md:605` places `clock_domain_index` at @28 for SET/GET_MEDIA_CLOCK_REFERENCE_INFO.
  - Milan 5.4.3.2 puts r + command_type at @28, and the model and both prior rounds place `clock_domain_index` at @30.
  - The text is in the processor submodule's docs, not in this PR. It is a candidate for a processor-side Issue.

## Real limits of this round

- The RTL evidence comes from a copy of the pinned `tb/pp_top`, with a frame-replay probe spliced in at the point where the suite runs its MVU phase (`scripts/build_rtl_probe.sh`).
  - The copy runs every phase before that point and then exits.
  - It is not the processor's full pp_top run, and phases after the MVU phase were not run.
  - Frames were readdressed only: the MAC and entity_id were swapped to the harness's, and swapped back on the way out.
- The Milan v1.2 and IEEE 1722.1-2021 texts were not available to this round.
  - The figure lengths, and the quotations for Table 9-6, "an appropriate status code", 4.2.4 and 5.4.4.1, were checked against the specification extracts published in the R280-1 and R281-1 receipts, which identify the documents by hash.
  - The longer phrase at `feature:106-108` and `steps:93-95`, "the appropriate details from the command and an appropriate status code", has only its final clause attested there. Its first half was not verified against the primary text.
- No full parent, processor, gPTP, Yosys or builder bank was run. No act, no Docker, no hardware.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- Hosted runs were inspected read-only. `Physical gPTP (nightly and manual)` is skipped, not executed.
- Test runs created ignored byte-cache directories in the clone, all timestamped inside this round. They were removed, and the clone was re-verified exact afterwards.

## Pending manager duties

- Publish this packet and the verdict.
- The external review at this head is a separate required positive.
- Own hosted and local-replica acceptance for the exact head.
- Build and validate the final current-dev candidate at the merge turn: source base `26d855a9`, live dev `615b5a5d7de01b23f15502e3732c6f2cb81ce74b`. This round's evidence is source-head evidence and does not cover that candidate.
- Post-merge containment, and file Issues for O1/O2/O4 if wanted.
- Merge only with explicit maintainer authorization.

## Reproduce

All paths are relative to this packet. `<clone>` is a checkout at the head with `protocol-processor` and `gptp-processor` initialised at their pins. `<verilator>` is Verilator 5.050.

```sh
python3 -B scripts/record_frames.py <clone> receipts/contract_frames_head.jsonl
sh scripts/build_rtl_probe.sh <clone> scratch/pp <verilator>
python3 -B scripts/rtl_vs_model.py receipts/contract_frames_head.jsonl scratch/pp/tb/pp_top/obj_dir/Vpp_top_sim receipts/rtl_vs_model_head 89 300
sh scripts/rtl_mutants.sh "$PWD" <verilator>
python3 -B scripts/model_mutations.py <clone> scratch
sh scripts/verify_clone.sh <clone> fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad 24a2b1c9bd657d2d14b5e814f18ec349108ffc1f
```

R280-2 FINISHED
