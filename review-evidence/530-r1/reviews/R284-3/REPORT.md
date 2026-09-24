[R284] NEGATIVE - exact head e65dccfe586bea9455cf1e10397d275c220c740a

Round R284-3: internal, cleared-context, independent re-review of issue #530 / PR #549.

- Head: `e65dccfe586bea9455cf1e10397d275c220c740a`, tree `31f4188287b90a87a31c17b4e330b61c3f657038`.
- Source base: `50e78097564244c124e1ec30dd8821f83951ab06`. The silicon-tested head is `c593cbeffaffa647cda70fb1a233455bf9c80d55`. The round-2 head is `446e79b977640d13fa1e5dc0f9896d6c5a70391d`. This round adds four one-line commits on it (`461e8c34`, `724a6bf2`, `03f26b19`, `e65dccfe`), for fourteen in all.

**Summary.**
- The correction does what R284-2 F1 = R285-2 F1 asked, at every site:
  - both branches of the optimistic-window corner are stated;
  - the "registered at the declaration" premise is gone;
  - ACTIVE is said to fall at the window's end, not inside it;
  - the refused branch's STREAM_START/STREAM_STOP pair, counter reset and one-PDU bound are stated;
  - `LWSRP_STATUS[8]` is scoped to source 0;
  - the FR_NFR grant sentence is corrected.
- I checked each of those claims against the processor source at the pin and against the parent RTL, and each one holds.
- The `hdl/` change since `c593cbef` is comments only. I proved this independently, so the silicon image built from `c593cbef` stays valid for this head.
- The verdict is NEGATIVE on one new MINOR (F1). The rewritten `milan_datapath.sv` refused-branch paragraph says that "the 0x82C talker lobs pulse with it". On the AX7101 1x1 product shape that is false:
  - `0x82C` talker index 0's lobs bit is source 0's *registered Listener* level, not ACTIVE, so it does not fall when ACTIVE does;
  - the CRF output has no `0x82C` talker index at all.
- That wording came from the required outcome of R285-2 F1 ("`CRFT_CTRL[6]/[7]` and the lobs pulse"), and the author followed it. F1 corrects the prescription. It does not criticise the implementation.

## Reconstruction (public state only)

In order, I read:
1. `AGENTS.md`, `CONTRIBUTING.md` (sections 2, 3 and 6), `docs/README.md`.
2. The issue #530 body and every issue comment:
   - the A205 DECISION and BLOCKED;
   - the manager decisions of 2026-09-23;
   - the processor issue 106 note;
   - the A229 assignment and REVIEW READY;
   - the A236 assignment and REVIEW READY;
   - the manager's silicon-rerun note;
   - the A238 assignment (06:05Z), which names the required outcome: the refused branch's full effect, the right status bits, and the FR_NFR grant sentence, with behaviour unchanged and the design question split to #551;
   - the [A237] SILICON RERUN PASS on `c593cbef`, the manager's archive note (`1b3fa460`, `review-evidence/530-r1/silicon-a237/`) and A238 REVIEW READY.
3. The PR #549 body at this head: "Closes #530", not draft, base `dev`.
4. The authorities:
   - `REQUIREMENTS.md` section 5;
   - `FR_NFR.md` 2.5 and its scope note;
   - `EGRESS_QUEUE_MAP.md` "Credit-based shaping";
   - `REGISTER_MAP.md` `0x694`, `0x698`, `0x750`, `0x82C` and the slope-ordering paragraph;
   - `ieee8021q.md`: the second consequence, Q-9 and Q-10.
5. The processor at pin `09f9bf38`:
   - `KL_srp_top.sv:424-445,746-748,772-781,843-862`;
   - `KL_srp_admission.sv:1-216`;
   - `KL_srp_talker_fsm.sv:425-450,530-548,636-639,684-720,793-810`.
6. The parent RTL behind every status bit the new text names:
   - `milan_datapath.sv:1646-1666,1855-1890,1913-1916,2017-2027,2474-2511,3055-3059,5278-5320,5630-5631,6575-6650,6688-6696`;
   - `milan_csr.sv:348-351,2912-2921`;
   - `KL_talker_diag_ctx.sv:20-45,196-282`;
   - `KL_crf_tx.sv:480-530`;
   - `KL_aaf_packetizer.sv:305-330,730-740`.
7. `git diff 50e78097..e65dccfe`, `c593cbef..e65dccfe` and `446e79b9..e65dccfe`, with the commit history.
8. The public evidence:
   - the tree `9d1b176c` `review-evidence/530-r1`, whose manifest lists the author and correction-a236 packets;
   - the silicon archive `1b3fa460` `review-evidence/530-r1/silicon-a237/`, whose listing I read;
   - the exact-head hosted state.

I read the prior public review findings (R284-1, R285-1, R284-2, R285-2) only after my own pass. By then a draft verdict naming F1, S1 and S2, and a draft ledger, were already written to this file.

Scope, as frozen by the A238 assignment: a docs-only correction of R284-2 F1 = R285-2 F1, with no RTL logic, harness, Makefile or BDD step change.

## Findings

### F1 - MINOR - lenses: RTL, Docs - the refused-branch paragraph says the `0x82C` talker lobs pulse with ACTIVE; on the product shape they do not

**Where:** `hdl/milan/milan_datapath.sv:6613-6614`, in the new REFUSED paragraph of the OPENING EDGE block (added by `461e8c34`):

> CRFT_CTRL[6]/[7], LWSRP_STATUS[6], [8] for source 0 and the 0x82C talker lobs pulse with it.

No Markdown page repeats the lobs claim, and the PR body does not either.

**Authority and evidence.** Receipt `receipts/06-0x82c-lobs-trace.txt` (script `scripts/trace_0x82c_lobs.py`) prints and asserts each link at this head:
1. `0x82C` talker bit `[2]` is `i_tlk_lobs_v[snap_idx]` (`hdl/common/csr/milan_csr.sv:2918`), a snap-latched pack.
2. The window gets only the AAF indices: `.i_tlk_lobs_v (8'(acmp_lobs_v_w[N_STREAMS-1:0]))` (`milan_datapath.sv:2483`). On the AX7101 1x1 shape `N_STREAMS` = 1, and the CRF output is source 1 (`SRP_TALKERS_C = N_STREAMS + SRP_CRF_TK_C`, `:1628`). **The CRF output has no `0x82C` talker index.**
3. Index 0 is `listener_observed_w = cfg_acmp_lobs | (cfg_lwsrp_enable & lwsrp_listener_ready)` (`:1861-1862,1883`). Here `lwsrp_listener_ready` is source 0's *registered* Ready or Ready Failed (`:6690-6695`, from `pp_cd_srp_lstn_reg_state_w[1:0]`). Only indices > 0 take `lwsrp_stream_gate[gj]`, which is ACTIVE (`:1885-1886`).
4. `REGISTER_MAP.md:1522` (the `0x82C` row) says exactly this: "at idx 0 source 0's registered Listener Ready or Ready Failed, at idx > 0 that source's ACTIVE since #530".
5. In the refused branch, ACTIVE falls at the window's end because the admission term `sr_admitted_i` falls (`KL_srp_talker_fsm.sv:800-803`, `KL_srp_top.sv:445,772-779`). The registration does not fall:
   - the Talker Failed swap flips only `fail_r` (`KL_srp_talker_fsm.sv:540-541`);
   - the registrar is cleared only by a gate accept (`:706-710`), not by the swap.
   - So index 0's lobs bit rises with the registration and stays high after ACTIVE falls.

The claim therefore fails on both counts for the product shape:
- a refused source 0 does not pulse `0x82C[2]`;
- the CRF output never appears in `0x82C`.

It holds only for AAF indices > 0 on multi-stream shapes. The talker bit that does follow the composed gate at every index is `[3]` (`aaf_stream_en[idx]`, `milan_csr.sv:2917`).

**Provenance.** R285-2 F1's required outcome ends "... and `CRFT_CTRL[6]/[7]` and the lobs pulse". The author carried that into the RTL comment. The defect is in the review prescription. The same thing happened in round 2, where the corner wording came from R284-1 F1.

**Impact.**
- This paragraph is the lane's record of which bits reveal the corner, and the A238 assignment's required outcome was specifically to name the right status bits.
- A debugger on the product shape who watches `0x82C[2]` for a refused declaration will see it rise with the registration and stay high. For the CRF output there is nothing in `0x82C` to watch.
- The comment contradicts the authoritative `0x82C` register row.

**Required outcome.**
- The refused-branch bit list in `milan_datapath.sv:6613-6614` names only bits that pulse with ACTIVE for the source they belong to. Either drop the `0x82C` lobs, or scope them: indices > 0 only, never index 0, never the CRF output. Name `0x82C[3]` instead if a `0x82C` bit is wanted.
- No RTL logic change. The comment-free `milan_datapath.sv` stays identical to `c593cbef`.

**Verification.**
- A reviewer reads the revised line against `milan_csr.sv:2917-2918`, `milan_datapath.sv:1861-1886,2483,6690-6695` and `REGISTER_MAP.md:1522`.
- `scripts/hdl_comment_only.py` stays PASS, with its canary.
- The docs gates stay green.

### Suggestions (do not affect coverage)

- **S1 (Docs).** Three pages say "Both show on the licensed source's own bits" and then list `LWSRP_STATUS[6]` for the CRF output:
  - `REGISTER_MAP.md:1130-1131`;
  - `EGRESS_QUEUE_MAP.md:99-100`;
  - `ieee8021q.md:67-68`.

  `[6]` is `|ACTIVE` across all sources (`milan_datapath.sv:6647`), not the CRF output's own bit. With AAF source 0 ACTIVE at the same time, `[6]` does not show the CRF corner. The RTL comment says this correctly: "LWSRP_STATUS[6] (|ACTIVE)", `:6600`. Optional: say "`LWSRP_STATUS[6]` (the OR over sources)" on those pages.
- **S2 (Docs), PR body, manager-owned.** The Contents line for "Linked Issue / roles" still says "#530 stays open for the silicon rerun", while the section says "Closes #530" and the rerun has passed. The first Definition of Done box still reads "the silicon rerun is the manager's". Optional: bring both in line with "Closes #530".

## Round-2 claims checked at this head (all hold)

| claim (every site) | result | evidence |
|---|---|---|
| the window lasts until the end of the third round after a fresh declaration; a round is `N_SOURCES` cycles | holds. `opt_cnt_r <= 2` at declaration; decremented, then `opt_r` cleared, on `round_done`; `round_w` at `aidx_r == N_SOURCES_P-1` | `KL_srp_top.sv:772-779,855-858`; `KL_srp_admission.sv:155,181-198` |
| each declaration clears the source's talker-side Listener registrar, so ACTIVE is 0 after it | holds. On `gate_acc_w && gate_open_i`: `reg_r <= R_MT_C; lstn_val_r <= 0`. This is the later assignment in the block, so it beats a same-cycle registering event. `lstn_out_w = 0` in MT. `gate_valid_w = (svc_st_r == S_GATE)` and `gate_open_i = a_open_r` | `KL_srp_talker_fsm.sv:638,684-710`; `KL_srp_top.sv:491,746` |
| ACTIVE rises in the window only on a decoded New/JoinIn/JoinMt with Ready or Ready Failed | holds | `KL_srp_talker_fsm.sv:686-692,800-803` |
| refused: `over_limit` rises, `sr_admitted_o` stays 0, ACTIVE holds on `opt` and falls at the window's end, then the Talker Failed swap | holds. ACTIVE takes `sr_adm_fsm_w = opt_r \| adm_admitted_w`. `adm_fix_w` fires once `sr_admitted_i` = 0 and `fail_r` follows on the grant. ACTIVE falls combinationally first, so FR_NFR's "before the declaration swaps" is right | `KL_srp_top.sv:445,501`; `KL_srp_admission.sv:152-154,207-214`; `KL_srp_talker_fsm.sv:438-441,540-541,800-803` |
| a STREAM_START/STREAM_STOP pair; the start zeroes MEDIA_RESET, TIMESTAMP_UNCERTAIN and FRAMES_TX | holds. These are single-cycle edge counters with no debounce, on `tkd_streaming_w = {crft_emit_en_w, aaf_stream_en_w}` | `KL_talker_diag_ctx.sv:255-278`; `milan_datapath.sv:3055-3059` |
| at most one PDU per source, if its media event falls in the window | holds as an upper bound. CRF latches one PDU per media event while `enable_i`, at 500/s. AAF accepts pairs only while enabled and clears its accumulation when disabled, so a window of a few cycles cannot complete a frame from earlier samples | `KL_crf_tx.sv:497-510`; `KL_aaf_packetizer.sv:314-316,732-738` |
| CRF output bits `CRFT_CTRL[6]`/`[7]` and `LWSRP_STATUS[6]`; `[8]` is source 0 only | holds. `crft_stat_c[6] = crft_res_active_w = lwsrp_stream_gate[SRP_TALKERS_C-1]`, `[7] = crft_emit_en_w`. The `LWSRP_STATUS` pack, with `listener_decl` 2 bits wide, puts `[6]` = `\|ACTIVE`, `[7]` = over_limit, `[8]` = `lwsrp_stream_gate[0]` and `[9]` = `\|sr_admitted` | `milan_datapath.sv:1652-1658,2502-2508,5280-5281,5305-5319,6638-6647` |
| cited processor line numbers | every citation resolves to the stated content at `09f9bf38` | `receipts/07-processor-claims.txt` |
| no stale premise remains | none of "registered at the declaration", "already registered", "outlived", "only effect", "trail `[8]`" or "falls inside the window" survives in current-tense text. The only "whole effect" hits are scoped to the admitted branch | residual search over `*.md *.sv *.cpp *.py *.feature`, read at head |
| `KL_pp_shadow.sv:629` ("lags srp_active_o by up to three admission rounds") | pre-existing at base `50e78097`, not touched by this PR. It is imprecise for the refused branch, where the verdict never rises. Noted for triage only | read at base and head |

## What was independently verified at this head

The simulator is the scoped 5.050 build. The wrapper sha256 is `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`, and `--version` prints "Verilator 5.050 2026-07-01 rev v5.050". Builds used 8 jobs. Local paths in the receipts are redacted to placeholders.

| check | result | receipt |
|---|---|---|
| `hdl/` since the silicon-tested head is comments only | `c593cbef..e65dccfe` and `446e79b9..e65dccfe`: `milan_datapath.sv` is the only `hdl/` file. With `//` and `/* */` stripped (string-aware) and whitespace normalised it is identical (`327d63f941421dee`). The added and removed `hdl/` lines have 0 lines that are not `//` comments. The canary `50e78097..c593cbef` reports DIFFERENT. The metacomment grep's only hits are the prose word "keeps", with no `verilator`, `synthesis`, `pragma` or `translate` token | `receipts/01-hdl-comment-only.txt`, `scripts/hdl_comment_only.py` |
| scope of the round | 6 paths: `CHANGELOG.md`, 4 `docs/` pages, `milan_datapath.sv`. All modes 100644. No gitlink change | same receipt |
| docs and source gates | all rc 0: `docs_check` (0 findings, scrub 23/23); `check_em_dash --base 50e78097` (0 over 261 added lines, arms 57/57); `check_doc_style`; `gen_toc --check`; `gen_toc --verify-anchors` (150 links); `check_doc_paths`; `gen_module_matrix --check`; `check_rtl_source_lists`; `check_feature_status`; `git diff --check` | `receipts/02-docs-gates.txt` |
| `make crflic` at head | 85 checks, 0 failures | `receipts/03-crflic.log` |
| BDD suite at head | 317 scenarios passed, 0 failed | `receipts/04-behave.log` |
| `make crflic-mutants` at head | 4 checks: 4 PASS (the clean control plus all 3 plants caught on their named checks), 167 s | `receipts/05-crflic-mutants.log` |
| F1 chain | every link present as described | `receipts/06-0x82c-lobs-trace.txt`, `scripts/trace_0x82c_lobs.py` |
| processor and parent excerpts | quoted with line numbers | `receipts/07-processor-claims.txt`, `scripts/processor_claims.sh` |
| clone restored | HEAD and tree exact; index == HEAD tree; 874 tracked files byte- and mode-exact; no hide flags; no modified, untracked or ignored paths. `protocol-processor 09f9bf38`, `gptp-processor c1b61743` and `third_party/verilog-axis 48ff7a7e` are at their gitlinks and clean. `external` (`efeb541a`) is recorded and not initialised in this clone | `receipts/08-restore-verification.txt`, `scripts/verify_restore.py` |
| exact-head hosted state (read only, 06:53Z) | 0 check runs recorded against `e65dccfe`; combined status `pending` with 0 statuses; PR open, not draft | `receipts/09-hosted-state.txt` |
| the round's diff | as reviewed | `receipts/10-diff-446e79b9-to-head.patch` |

## Lens results (R284-3, exact head `e65dccfe`)

```text
[R284] PASS Conformance - receipts/01 (logic byte-identical to c593cbef after comment stripping), receipts/03-crflic.log (85/0: [A] no emission before Listener Ready, [C] item 1 bound through LeaveAll cycles, [F] item 3 FRAMES_TX), milan_datapath.sv:1913-1916,2017-2027,5280-5307,6632 against KL_srp_talker_fsm.sv:800-803 and Milan v1.2 5.3.7.3 / 5.3.7.7 Table 5.4; FR_NFR.md:207-220 now quotes FR-SRP-03 as worded and discloses the refused-branch licence (#551, manager split); [A237] silicon PASS on c593cbef (identical logic) per issue #530 and archive 1b3fa460 - #530 acceptance items 1 to 3 met; the PR Closes #530
[R284] UNCLEAN RTL - F1 open - milan_datapath.sv:6575-6650 comment block read against KL_srp_top.sv:445,746,772-779,855-858, KL_srp_admission.sv:152-155,187-214, KL_srp_talker_fsm.sv:438-441,540-541,636-639,684-710,800-803, KL_talker_diag_ctx.sv:255-278, KL_crf_tx.sv:497-510, KL_aaf_packetizer.sv:314-316,732-738, milan_csr.sv:2912-2921, milan_datapath.sv:1861-1886,2483,2502-2508,5280-5319,6638-6647,6690-6695 - every other statement in the block is correct; logic unchanged (receipt 01)
[R284] PASS Robustness - receipts/01 (no logic, harness or step change since c593cbef), receipts/03-crflic.log phases [B2] [D] [E] [INV] at head, the refused optimistic-window path re-derived from the processor source (bounded to three rounds of N_SOURCES cycles, at most one PDU per source, ACTIVE still needs a registered Ready/ReadyFailed) - benign and disclosed at every site; the design question is #551
[R284] PASS Tests - tb/verilator/milan_dp/sim_crf_licence.cpp, crflic_mutants.py, Makefile, tests/features/milan_streaming_licence.feature, tests/steps/milan_streaming_licence_steps.py untouched since c593cbef (receipt 01 scope); receipts/03 (85/0), 05 (control plus 3/3 caught), 04 (behave 317/0) at this exact head
[R284] UNCLEAN Docs - F1 open (milan_datapath.sv:6613-6614) - also checked and correct at head: CHANGELOG.md:38-51, EGRESS_QUEUE_MAP.md:76-101, FR_NFR.md:207-220, REGISTER_MAP.md:1109-1133,1167-1168, ieee8021q.md:53-68,98-99, the PR body Known limitations and disposition table; receipts/02 gates green; S1 and S2 optional
```

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gate and licence RTL (logic byte-identical to `c593cbef`, receipt 01); processor ACTIVE and window; FR_NFR FR-SRP-03 note; `crflic` 85/0 at head; [A237] silicon PASS on `c593cbef` | R284-3 | `e65dccfe586bea9455cf1e10397d275c220c740a` |
| RTL | UNCLEAN (F1) | the `milan_datapath.sv` SRP block and every status bit it names; processor window, admission and ACTIVE; diag edge counters; CRF and AAF emitters; the `0x82C` pack; comment-only proof | R284-3 | `e65dccfe586bea9455cf1e10397d275c220c740a` |
| Robustness | CLEAN | closing, reopening and invariant phases at head; the refused-window path re-derived from source; escape terms `milan_datapath.sv:1913-1916,5305-5307` unchanged | R284-3 | `e65dccfe586bea9455cf1e10397d275c220c740a` |
| Tests | CLEAN | leg, mutant driver, Makefile, BDD feature and steps (untouched since `c593cbef`); `crflic` 85/0, mutants control plus 3/3, behave 317/0 at head | R284-3 | `e65dccfe586bea9455cf1e10397d275c220c740a` |
| Docs | UNCLEAN (F1) | CHANGELOG, EGRESS_QUEUE_MAP, FR_NFR, REGISTER_MAP, ieee8021q, the in-RTL comments, the PR body; docs gates | R284-3 | `e65dccfe586bea9455cf1e10397d275c220c740a` |

If a fix of F1 touches only comments, Markdown and the PR body:
- RTL and Docs must be re-covered at its head;
- Conformance, Robustness and Tests stay banked at `e65dccfe` only while the comment-free RTL, the leg, the mutants, the Makefile and the BDD step stay unchanged. A comment-only proof like receipt 01 shows that.

## Prior public findings: disposition at this head

I read these after my verdict, F1 and the draft ledger were written.

| prior item | disposition at `e65dccfe` | basis |
|---|---|---|
| R284-2 F1 = R285-2 F1, MINOR (RTL, Docs): the corner called status skew its whole or only effect, rested on a Listener Ready "registered at the declaration", said ACTIVE falls inside the window, and named `LWSRP_STATUS[8]` for the CRF output | **RESOLVED** at every named site: `milan_datapath.sv` OPENING EDGE and later-lane paragraphs, CHANGELOG, EGRESS_QUEUE_MAP, REGISTER_MAP (paragraph, `0x694[9]`, `0x698`), ieee8021q (second consequence, Q-9), the FR_NFR note and the PR body. The one new inaccuracy the fix introduced, the lobs clause taken from R285-2 F1's required outcome, is filed as **F1** above | the "Round-2 claims checked" table; `receipts/10` |
| R284-1 F1 = R285-1 F1, MINOR (RTL, Docs): a shaper that does not exist | **RESOLVED**, and still so. Round 2 adds only "no shaper reads either word" statements and no shaper claim | `receipts/10`; read at head |
| R284-1 F2 = R285-1 F2, MINOR (Docs): the raw verdict named as the gate | **RESOLVED**, and still so. Q-9 names `srp_active_o` (`ieee8021q.md:98`) | read at head |
| R284-2 S1 (Docs): `milan_datapath.sv:1588` "stop consulting the admission verdict" | retained as a SUGGESTION; unchanged | read at head |
| R284-2 S2 / R285-2 S1 (Docs): legacy "bw-gate" and "CBS slope MUX" terms | retained as SUGGESTIONS; unchanged, pre-existing | read at head |
| R285-2 observation: `sw/builder` slope-MUX and bw-gate remnants | out of scope; for triage | not changed |
| R284-1 S1 / R285-1 S3 (Tests, Docs): mutant time 139 s; absolute `CRFLIC_MDIR` | retained as SUGGESTIONS. I measured 167 s this round | `receipts/05` |
| R284-1 S2, R285-1 S1 (Tests): old-pin arm by hand only; t>0 AAF gates graded by source text only | retained as SUGGESTIONS; unchanged | read at head |
| R285-1 S2 (Docs) | resolved in round 1 (R284-2, R285-2); unchanged | read at head |
| R284-1 observation: no `~cfg_lwsrp_enable` escape for t>0 AAF gates | not a finding; unchanged and intentional | read at head |

## Real limits

- The refused branch, and F1's claim that `0x82C[2]` does not follow ACTIVE at index 0, are established by reading the cited RTL line by line. No simulation here stages a refused declaration inside the window. The leg and earlier probes do not reach the corner.
- Not run, outside this round's permission or scope:
  - the full parent, processor, gPTP, Yosys and builder banks;
  - the other `milan_dp` legs and `pp_shadow`;
  - the old-pin and gate-reverted arms;
  - `lint_rtl`, the `xvlog` ratchet, `check_sv_idiom` and `check_hygiene`;
  - act or Docker, and any hardware.
- **Manager banks.** The brief says the manager's source static/builder and native banks passed at this head. The public tree `9d1b176c` `review-evidence/530-r1` lists the author and correction-a236 packets (and review packets I did not open), and I found no manager bank receipt for `e65dccfe` there. I take the result as the manager's statement, and this verdict does not rely on it.
- **Hosted.** At 06:53Z no check run was recorded against `e65dccfe` (receipt 09). There is no exact-head `rtl-fast`, `verilator-suites` or `yosys-portability` evidence yet.
- **Spec text.** Milan v1.2 and 802.1Q readings rest on the repository and processor documents and the prior rounds. I did not re-read the standards this round.
- **Physical calibration NOT RUN.** Simulation and skipped field contexts are not hardware proof. The silicon PASS is the manager's [A237] run on `c593cbef`. I read it from the issue and the archive listing and did not replay it.
- **Clone hygiene.** The focused runs created build products (`obj_crflic`, `ltn_rom.hex`, `ucode.hex`) and Python caches, one of them inside the processor checkout, plus a `scripts/__pycache__` cache that was present before. All were removed before the restore check.

## Pending manager duties

- Route F1 (a one-line comment correction in `milan_datapath.sv`) to a docs-only fix, then have RTL and Docs re-covered at the new head.
- Hosted and act acceptance at the final head. None was recorded at `e65dccfe` when read.
- Candidate merge validation against live dev `f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f` (source base `50e78097`), with the full local bar, then post-merge containment.
- Optional: bring the PR body's Contents and DoD lines in line with "Closes #530" (S2); triage S1, the retained suggestions and the `KL_pp_shadow.sv:629` wording into Issues.

Publishable receipts and scripts are listed in `MANIFEST.sha256`. Disposable material lives only under `scratch/`.

R284-3 FINISHED
