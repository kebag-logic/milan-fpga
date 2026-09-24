[R284] NEGATIVE - exact head 446e79b977640d13fa1e5dc0f9896d6c5a70391d

Round R284-2: internal, cleared-context, independent re-review of issue #530 / PR #549.

- Head: `446e79b977640d13fa1e5dc0f9896d6c5a70391d`, tree `9f1c9511ca70d889ea2eb2b0a9a3f06d3b29f7fb`.
- Source base: `50e78097564244c124e1ec30dd8821f83951ab06`. The round-1 head is `c593cbeffaffa647cda70fb1a233455bf9c80d55`, and this round adds five one-line commits (docs-only correction round 1).

**Summary.** The correction does what it set out to do:
- The `hdl/` change is comments only. I proved this independently, so the image built from `c593cbef` stays valid.
- No text now claims that a shaper budgets or reads the raw verdict or the slope.
- No page still names `sr_admitted` as the stream gate in the current tense.
- Both round-1 MINORs (F1, F2) are fixed as round 1 specified them.

The verdict is still NEGATIVE, because of one new MINOR (F1 below). The corrected corner text says, on five pages and in the PR body, that status skew is the corner's *whole* or *only* effect. That statement is wrong for the sub-case the same text describes: a round that refuses the stream. In that case the processor's ACTIVE rises and then falls. ACTIVE is both the emission licence and the Milan Table 5.4 streaming level. So a STREAM_START/STREAM_STOP pair is counted, and a PDU whose slot falls in the window can leave.

The text also names `LWSRP_STATUS[8]` as the place the lead shows. That bit is source 0's gate only, so it never shows the CRF output's corner.

This wording came from the required outcome of my own R284-1 F1, which R285-1 repeated. The author implemented what the reviewers asked for. The defect is in that prescription, and this round corrects it.

## Reconstruction (public state only)

In order, I read:
1. `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
2. The issue #530 body and every issue comment:
   - the A205 DECISION and BLOCKED;
   - the manager decisions of 2026-09-23;
   - the processor issue 106 note;
   - the A229 assignment and REVIEW READY;
   - the A236 correction assignment (04:31Z) and the A236 REVIEW READY (05:19Z);
   - the manager's silicon-rerun note (05:08Z; the silicon runs `c593cbef`).
3. The PR #549 body at this head.
4. `REQUIREMENTS.md` section 5, `FR_NFR.md` 2.5 and its scope note, `EGRESS_QUEUE_MAP.md`, `REGISTER_MAP.md` 0x680 to 0x698, and `ieee8021q.md`.
5. The processor sources at the pin `09f9bf38`:
   - `KL_srp_top.sv:415-445,760-781,848-862` (the optimistic window);
   - `KL_srp_admission.sv:91-215` (the round walk, and `sr_admitted_o = grant_r & req`);
   - `KL_srp_talker_fsm.sv:434-441,532-545,793-803` (ACTIVE and the Failed swap).
6. `git diff 50e78097..446e79b9` and `c593cbef..446e79b9`, with the history.
7. The public evidence tree `9d1b176c` `review-evidence/530-r1` (author packet, correction-a236 packet, round-1 review packets).

I read the prior public review findings (R284-1, R285-1) only after my own pass and a draft verdict and ledger were written (`receipts/00-draft-before-prior-findings.md`).

Scope as frozen by the A236 assignment: a docs-only correction of R284-1 F1/F2 = R285-1 F1/F2, with no RTL change. The RTL logic, the `obj_crflic` leg, the mutants, the Makefile and the BDD step are outside it.

## Findings

### F1 - MINOR - lenses: Docs, RTL - the corrected corner overstates itself: the refused sub-case is a licence pulse, not only status skew, and `LWSRP_STATUS[8]` does not show the CRF output

**Where** (all at this head):
- `hdl/milan/milan_datapath.sv:6580-6594`, the OPENING EDGE paragraph:
  - `:6588-6590`: "the gates and LWSRP_STATUS[8] rise up to three rounds before LWSRP_STATUS[9] and 0x698 include the stream";
  - `:6590-6591`: "If the round then refuses it, ACTIVE falls inside the window";
  - `:6592`: "That status skew is the corner's whole effect here."
- `CHANGELOG.md:42`: "That status skew is the corner's only effect."
- `docs/reference/EGRESS_QUEUE_MAP.md:81-83`: "In the shipping datapath the only effect is status skew: `LWSRP_STATUS[8]` can lead ...".
- `docs/reference/REGISTER_MAP.md:1115-1116`: "The only effect is that `LWSRP_STATUS[8]` can lead `LWSRP_STATUS[9]` and `LWSRP_SLOPE`".
- `docs/traceability/ieee8021q.md:58`: "The only effect here is that those status words can trail `LWSRP_STATUS[8]`".
- The PR body, Known limitations: "so this status skew is the corner's only effect".
- Related: `docs/reference/FR_NFR.md:210-213` says the surviving obligation, "no transmit without a grant", is met because ACTIVE "needs ... the grant". Inside the window ACTIVE needs `opt_r | admitted`, not the grant.

**Authority and evidence** (processor pin `09f9bf38`, parent at head):
1. A fresh declaration sets `opt_r` with `opt_cnt_r = 2` (`KL_srp_top.sv:855-858`).
   - `opt_r` clears only on the third `round_done` (`:772-779`).
   - The talker FSMs receive `sr_adm_fsm_w = opt_r | adm_admitted_w` (`:445`, `:501`).
2. The first admission round that sees the request can refuse it. `sr_admitted_o = grant_r & req` then stays 0 and `over_limit_o` rises (`KL_srp_admission.sv:152-154,181-187,207-213`). ACTIVE stays high regardless, because it takes the windowed term:
   - `active_o = declaring & !fail_r & {Ready, ReadyFailed} & sr_admitted_i` (`KL_srp_talker_fsm.sv:800-803`);
   - `fail_r` only follows `sr_admitted_i` (`:440-441,541`).
   - So ACTIVE falls at the window's end, the third round, not "inside" it.
3. In the parent, ACTIVE is used directly:
   - it is the gate: `lwsrp_stream_gate = pp_cd_srp_active_w` (`milan_datapath.sv:6606`);
   - it is the CRF licence: `crft_emit_en_w` (`:5280-5307`), which feeds `KL_crf_tx.enable_i` (`:5631`);
   - it is the Table 5.4 streaming level: `tkd_streaming_w = {crft_emit_en_w, aaf_stream_en_w}` (`:3057`).
4. `KL_talker_diag_ctx.sv:258-277` counts every rising and falling edge of that level:
   - STREAM_START +1 and STREAM_STOP +1;
   - MEDIA_RESET, TIMESTAMP_UNCERTAIN and FRAMES_TX are zeroed;
   - `dirty_p_o` pulses.
   
   `KL_crf_tx.sv:497-509` latches a PDU on any media event that falls while `enable_i` is high.
5. So in the refused sub-case, which the text itself says occurs, the effect goes beyond status skew:
   - a controller-visible START/STOP pair and a counter reset, deterministically;
   - an emission licence of up to three rounds, for a declaration that the ceiling has already refused and that ends Talker Failed. At most one PDU per source can leave, if its media event falls in the window.
6. `LWSRP_STATUS[8]` is `lwsrp_stream_gate[0]` (`milan_datapath.sv:2502-2508`, bit 8 by position), which `REGISTER_MAP.md` itself calls "source 0's licence". On the flashed AX7101 1x1 shape the CRF output is source uid 1. Its lead shows on `CRFT_CTRL[6]`/`[7]` and `LWSRP_STATUS[6]` (`|ACTIVE`, `:6621`), never on `[8]`.

Scope of this evidence:
- This is RTL reading, cited line by line. I did not stage the refused re-declaration in simulation.
- R284-1's early-Ready probe could not trigger the corner at all.
- The finding does not depend on how reachable the corner is. The text asserts the refused sub-case, and in the same paragraph it calls status skew its whole effect.

**Judgement on the behaviour** (not a finding):
- The window is the processor's documented design (the `KL_srp_top.sv:31-35` banner). It lasts tens of cycles.
- ACTIVE always requires a registered Ready or Ready Failed, so #530's "no emission before Listener Ready" holds.
- FR-SRP-03's own words, "on failure the stream MUST NOT transmit", hold, because ACTIVE drops the cycle the failure is published.
- I retain no Conformance or Robustness finding. What is wrong is the description, on the pages that are there to tell a later lane what the corner does.

**Impact.**
- These texts are the lane's record of its one known corner. They tell a later shaping lane, and anyone reasoning about FR-SRP-03, that the corner has no wire or counter consequence.
- A refused re-declaration can in fact:
  - produce a spurious STREAM_START/STREAM_STOP pair that a controller reads;
  - reset the interval counters;
  - rarely, emit one frame for a stream the endpoint's own admission refused.
- A reader who watches `LWSRP_STATUS[8]` for the CRF output will never see the corner.

**Required outcome.**
- The five sites and the PR body describe both sub-cases:
  - Admitted: the gates and ACTIVE lead the raw-verdict status (`[9]`) and `0x698` by up to three rounds.
  - Refused: ACTIVE, and so the emission licence and the Table 5.4 streaming level, is high for up to three rounds and falls at the window's end, giving a START/STOP pair and possibly one PDU per source.
- "Whole" and "only" are dropped or made true.
- The status bits named are the right ones per source: `[8]` is source 0 only, and for the CRF output they are `CRFT_CTRL[6]`/`[7]` and `LWSRP_STATUS[6]`.
- `FR_NFR.md:210-213` either states the window caveat or phrases the obligation as FR-SRP-03 does ("stops when the failure is published").
- No RTL change.

**Verification.** A reviewer reads the revised text against the cited processor and parent lines at the new head. The comment-only proof of `hdl/` (this round's `scripts/hdl_comment_only_check.py`) and the docs gates stay green.

### Suggestions (do not affect coverage)

- **S1 (Docs).** `hdl/milan/milan_datapath.sv:1588` still says that clearing `LWSRP_CTRL[0]` makes "the AAF/CRF gates stop consulting the admission verdict". The gates consult ACTIVE (`:6606`), and that line is unchanged since base. It is not strictly false, because the verdict is one of ACTIVE's terms, but it names the pre-#530 input. Optional: "stop consulting the processor's ACTIVE".
- **S2 (Docs), pre-existing legacy terms.** These predate this PR, and none names the raw verdict as the gate:
  - `hdl/milan/KL_pp_shadow.sv:143,1238` ("a/its CBS slope MUX" as the consumer rationale);
  - `hdl/common/csr/milan_csr.sv:790` (`CRFT_CTRL[6]` "bw-gate: declared + Listener Ready + admitted", which omits Ready Failed);
  - `hdl/milan/milan_datapath.sv:5295` ("rides the same bw-gate");
  - `docs/reference/REGISTER_MAP.md:1590,1629` ("per-stream lwSRP bw-gate").
  
  Optional, for a later lane or a new Issue.

## Prior public findings: disposition at this head

I read these after my verdict, F1 and the draft ledger were written.

| prior item | disposition at `446e79b9` | basis |
|---|---|---|
| R284-1 F1 = R285-1 F1, MINOR (Docs, RTL): text describes a shaper the datapath does not have | **RESOLVED.** No shaper claim remains. The consumers are named (`[9]` from `lwsrp_slope_en`, `0x698` from `lwsrp_idle_slope`, `milan_datapath.sv:2502-2509,6612-6613`), and the budgeting invariant is scoped to the uninstantiated chain (`:6557-6564`). The new F1 above is a different defect in the corner wording that F1's required outcome prescribed. | `receipts/03-claim-search-head.txt`; the diff `c593cbef..446e79b9` |
| R284-1 F2 = R285-1 F2, MINOR (Docs): Q-9 names `srp_sr_admitted_o` as the gate; the EGRESS_QUEUE_MAP ordering sentence | **RESOLVED.** Q-9 names `srp_active_o` (`ieee8021q.md:89`). The EGRESS_QUEUE_MAP section is scoped to the retained chain, with the caveat (`:66-85`). The FR_NFR, REGISTER_MAP and ieee8021q recurrences were corrected too. | claim search; my reading of each page |
| R284-1 S1 (Docs): mutant campaign 139 s against 169 s | Retained as a suggestion. The PR body now gives "about 140 to 170 s"; `Makefile:372` still says 139 s. Tests scope untouched. | read at head |
| R284-1 S2 (Tests): the old-pin arm is by hand only | Retained as a suggestion; unchanged. | read at head |
| R285-1 S1 (Tests): the t>0 AAF gates are graded only by source text | Retained as a suggestion; unchanged. | read at head |
| R285-1 S2 (Docs): the t>0 "bandwidth gate" term, `ieee8021q.md:35`, processor PRs unnamed | **RESOLVED.** `milan_datapath.sv:1995` reads "the processor's per-stream ACTIVE (#530)"; `ieee8021q.md:35-36` reads back the slope as status; the PR body's `e8c273ff` row names the processor PRs. | read at head |
| R285-1 S3 (Tests): an absolute `CRFLIC_MDIR` breaks `make crflic` | Retained as a suggestion; unchanged. | read at head |
| R284-1 observation: t>0 AAF gates have no `~cfg_lwsrp_enable` escape | Not a finding; unchanged and intentional (`milan_datapath.sv:1991-2007`). | read at head |

## What was independently verified at this head

The simulator was the scoped 5.050: the wrapper sha256 is `905795b9...`, `--version` prints "Verilator 5.050 2026-07-01 rev v5.050", and compiles used 8 jobs. The include root in the build log is redacted to `<SIM_ROOT>`.

| claim | my result | receipt |
|---|---|---|
| `hdl/` change `c593cbef..446e79b9` is comments only | 83 changed lines, 0 non-comment. `milan_datapath.sv`, stripped of `//` and `/* */` outside strings and of whitespace, is identical at both commits (sha256 `a6f57d09...`). No changed line carries a tool metacomment (`verilator`, `synthesis`, `pragma`, `translate`, `lint_`, backtick). | `receipts/01-hdl-comment-only.txt`, `scripts/hdl_comment_only_check.py` |
| the checker can fail | on `50e78097..c593cbef` (a real gate change) it reports the non-comment lines and exits 1 | `receipts/02-hdl-check-canary-base-to-c593.txt` |
| scope | 6 files: CHANGELOG, 5 docs pages, `milan_datapath.sv`. All modes 100644. Gitlinks unchanged (`protocol-processor 09f9bf38`, `gptp-processor c1b61743`, `external efeb541a`). | `git diff --raw` read at head |
| `make crflic` at head | 85 checks, 0 failures | `receipts/07-crflic-head.log` |
| `crflic-mutants` at head | clean leg passes; all 3 plants caught on their named checks. Anchors occur exactly once at both heads. | `receipts/08-crflic-mutants-head.log`, `receipts/04-mutant-anchor-counts.txt` |
| BDD suite | 317 scenarios passed, 0 failed (the steps strip comments before reading the gate source) | `receipts/05-behave.log` |
| docs and source gates | `docs_check`, `check_em_dash --base 50e78097` and `--base c593cbef`, `check_doc_style`, `gen_toc --check` and `--verify-anchors`, `check_doc_paths`, `check_feature_status`, `check_hygiene --check`, `check_sv_idiom`, `check_rtl_source_lists`, `git diff --check`: all rc 0 | `receipts/06-docs-gates.txt` |
| residual-claim search | every hit read. Remaining raw-verdict mentions are historical ("until #530") or status-only. Remaining shaper mentions are the retained chain, the no-shaper statements, or the dated bench warning. S1/S2 list the legacy terms. | `receipts/03-claim-search-head.txt`, `scripts/claim_search.sh` |
| exact-head hosted runs (read only, 06:00Z) | every executed check run completed success, including `rtl-fast`, `verilator-suites`, `yosys-portability`, Verilator shards 0-4/5, Yosys shards 0-3/4, `bdd-conformance`, `docs-check` and `full-ci-gate`. "Physical gPTP (nightly and manual)" was **skipped**, which is not execution evidence. The combined commit status is `pending` with 0 statuses. | `receipts/09-hosted-check-runs.tsv` |
| clone restored | HEAD, index == HEAD tree (878 entries), 874 tracked files byte- and mode-exact, no hide flags, no untracked or ignored paths. Gitlinks: `protocol-processor`, `gptp-processor` and `third_party/verilog-axis` equal and clean; `external` is not initialised in this clone (empty) and none of the checks run needs it. | `receipts/10-restore-verification.txt`, `scripts/verify_restore.py` |

## Lens results (R284-2, exact head `446e79b9`)

```text
[R284] PASS Conformance - hdl/milan/milan_datapath.sv:6606,5280-5307,3057 (logic byte-identical to c593cbef, receipts/01); protocol-processor KL_srp_talker_fsm.sv:800-803; receipts/07-crflic-head.log [A]-[F],[INV] - no logic changed since the round-1 coverage. At this head every gate still reads ACTIVE, which always requires a registered Ready/ReadyFailed (#530 "no emission before Listener Ready", Milan v1.2 5.3.7.3). Item 1 [C] and item 3 [F] pass. The optimistic-window refused sub-case meets FR-SRP-03's own wording (stop when the failure is published); F1 is about its description, not its conformance
[R284] UNCLEAN RTL - F1 open - hdl/milan/milan_datapath.sv:6535-6614,2502-2509,6621,3057,5280-5307,5631; KL_srp_top.sv:445,772-779,855-858; KL_srp_admission.sv:152-213; KL_srp_talker_fsm.sv:440-441,541,800-803; KL_talker_diag_ctx.sv:258-277; KL_crf_tx.sv:497-509 - the logic is correct and unchanged (comment-only proof, receipts/01-02). The in-RTL account of the gate's timing effect omits the refused sub-case's licence pulse and names a status bit that does not carry the CRF source
[R284] PASS Robustness - receipts/07-crflic-head.log phases [B2] [D] [E] [INV]; the refused optimistic-window path read in the processor sources above - logic unchanged since round 1. Closing edges, Asking Failed and unbind pass at this head. The refused-window pulse is bounded (three rounds of N_SOURCES cycles, ACTIVE falls at the window end, Failed swap follows), and I judge it benign
[R284] PASS Tests - tb/verilator/milan_dp/sim_crf_licence.cpp, crflic_mutants.py:52-64,111-119, tests/steps/milan_streaming_licence_steps.py:56-66,167-183; receipts/04,05,07,08 - no test artifact changed since c593cbef. The mutant anchors still match exactly once after the comment edits. The leg is 85/0, the campaign 3/3 caught plus the clean control, and behave 317/0 at this head
[R284] UNCLEAN Docs - F1 open - CHANGELOG.md:32-45; EGRESS_QUEUE_MAP.md:1-12,63-85; FR_NFR.md:144,147,207-213; REGISTER_MAP.md:1085-1125,1146,1151-1152; ieee8021q.md:30-60,89-90; milan_datapath.sv SRP block; PR body - R284-1/R285-1 F1 and F2 are resolved. F1 (new) is open; S1 and S2 are optional
```

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | gate and licence RTL (logic byte-identical to `c593cbef`), processor ACTIVE and window, `crflic` phases at head | R284-2 | `446e79b977640d13fa1e5dc0f9896d6c5a70391d` |
| RTL | UNCLEAN (F1) | the `milan_datapath.sv` SRP block and its gate and status consumers; processor admission, window and ACTIVE; diag edge counters; CRF emitter enable; comment-only proof | R284-2 | `446e79b977640d13fa1e5dc0f9896d6c5a70391d` |
| Robustness | CLEAN | closing, reopening and invariant phases at head; the refused-window path read in source | R284-2 | `446e79b977640d13fa1e5dc0f9896d6c5a70391d` |
| Tests | CLEAN | leg, mutant driver and anchors, BDD steps; `crflic` 85/0, mutants 3/3 plus control, behave 317/0 at head | R284-2 | `446e79b977640d13fa1e5dc0f9896d6c5a70391d` |
| Docs | UNCLEAN (F1) | CHANGELOG, EGRESS_QUEUE_MAP, FR_NFR, REGISTER_MAP, ieee8021q, in-RTL comments, PR body; docs gates | R284-2 | `446e79b977640d13fa1e5dc0f9896d6c5a70391d` |

If a fix touches only comments, Markdown and the PR body:
- it must be re-reviewed under RTL and Docs at the new head;
- Conformance, Robustness and Tests stay banked here only if the RTL logic, the leg, the mutants, the Makefile and the BDD step stay unchanged. A comment-only proof like `receipts/01` shows that.

## Real limits

- The refused optimistic-window sub-case is established by reading the cited RTL, not by simulation. I did not stage a refused re-declaration with a Listener Ready already registered, and round 1's early-Ready probe did not reach the corner at all.
- Not run, outside this round's permission or scope:
  - the full parent, processor, gPTP, Yosys and builder banks;
  - the other `milan_dp` legs and `pp_shadow`;
  - `lint_rtl` and the `xvlog` ratchet;
  - act/Docker, and any hardware.
- **Manager banks.** The manager's static/builder and native bank results at this head are cited in the brief. I did not find their receipts in the named evidence tree (`9d1b176c`, `review-evidence/530-r1` holds the author, correction and round-1 review packets) or in an issue or PR comment. I take them as the manager's statement, and this verdict does not rely on them.
- **Spec text.** Clause readings rest on the repository and processor documents. I did not consult the Milan v1.2 or 802.1Q text directly in this round.
- **Physical calibration NOT RUN.** Simulation at compressed time and the skipped physical context are not hardware proof.
- **Clone hygiene.** The focused runs created build products (`obj_crflic`, `ltn_rom.hex`, `ucode.hex`) and Python caches, one of them inside the processor checkout. All were removed before the restore check.

## Pending manager duties

- Route F1 to a docs-only correction, then have RTL and Docs re-covered at the new head.
- Hosted and act acceptance at the final head. At this head, every executed check run is success and the physical context was skipped.
- Candidate merge validation against live dev `f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f`, with the full local bar, then post-merge containment.
- The #530 silicon rerun on `c593cbef`, whose RTL equals this head's. The issue closes only after it.
- Optional: triage S1/S2 and the retained suggestions (R284-1 S1/S2, R285-1 S1/S3) into Issues.

Publishable receipts and scripts are listed in `MANIFEST.sha256`.

R284-2 FINISHED
