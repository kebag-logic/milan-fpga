[R735] POSITIVE - exact head f99405af0b2caad46e84f50f8251ffbffaa80836

# Internal cleared-context review of PR #813 (#806), round R735-1

- Head: `f99405af0b2caad46e84f50f8251ffbffaa80836`, tree `6547cf95cce6a564f9c1822cbc3551301aece764`; base `dev` `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
- Scope: the whole PR, nine commits `f911adec`..`f99405af`, 28 files.
- Packet: author-r1 (`[A701]`), public evidence at `review-evidence/806-r1` of `83d9cd72`.
- Reading order: AGENTS.md and CONTRIBUTING.md (sections 1, 3, 5, 6), docs/README, the #806 body, REQUIREMENTS.md (REQ-PTP-05/07, the soak's asCapable rule), the clause text, the donor PR #95 body and its pin, then `git diff 1e80128f..f99405af` with its history, then the public receipts.
- PR data came only from `gh pr view --json title,body,headRefOid,baseRefName,baseRefOid,files,commits` (`receipts/pr813.json`). The issue came only from `gh issue view --json title,body,state,labels` (`receipts/issue806.json`).
- I listed no PR or issue comment, and read no other reviewer's report, before this verdict and ledger were on disk.
- No manager source bank runs at this head, and I infer none. Source-head execution evidence here is the author's published receipts plus my own focused runs below.

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR is open. All five lenses were applied and are clean at this head. The five SUGGESTIONs (S1 to S5) are optional and leave coverage unchanged.

The area gate's route-1x1 refusal is not a finding against this change. The refusal is on WNS alone: +0.032 ns against the record's +0.440 ns, tolerance 0.25 ns. The worst setup path is `FSM_onehot_socbushandler0_axilite2wishbone_state_reg[3]` to `milansoc_spiflash_phy_cnt_reg[8]`: 18 levels, SoC clock, outside every module this PR touches (`receipts/vivado/route-1x1-worst-setup-path.txt` of the evidence tree). I found nothing showing the change's logic causes it. Merged with the open #806 acceptance "the area gate passes", it stays a merge-bar item for the manager (Pending manager duties).

## What I checked, by the brief's items

### (1) The gitlink and the companion

- **Gitlink.** The `gptp-processor` gitlink is `135afd043309369a87ddbc8d6550aff8ec52a157` at head and at every commit from `f911adec` on. The public FPGA-gPTP `main` is `135afd04` (GitHub API, `commits/main`), tree `b552de22`, parents `f97c1803` and `409c3075`. PR #95 is merged, `merge_commit_sha` `135afd04`, head `409c3075`. `409c3075^{tree}` = `135afd04^{tree}` = `b552de2244475b15bfc430b683f8a4fe9c6a7db3`. Issue #94 is closed.
- **Companion.** For all eight companion files, `a20f458e^` equals dev `1e80128f` blob for blob. `a20f458e`'s post-images equal the blobs the published apply receipt lists (`receipts/companion/apply-evidence.txt`). `a20f458e` changes no gitlink: `ls-tree` on it and on its parent both give `135afd04`.
- **Companion content.** It matches what PR #95's "milan-fpga companion" section describes: the shadow port, `eff_link_w` driving it, three wrappers tied high, three leg checks. Four later commits change two of those files: `sim_gptp.cpp` (`e67ae2f1`, `cf3ef596`) and `GPTP_PLANE.md` (`12a7948f`). Each change is reviewed below.
- **Limit.** The companion patch bytes (sha256 `aeeab9c8...`) are not published, so I could not hash them myself. The correspondence rests on the blob equalities above and the donor PR text.

### (2) portEnabled against 802.1AS-2011 10.2.4.11, Figure 11-8, and Milan v1.2 4.2.6.2.4/4.2.6.2.5

- **Clause text.** I read it from the standards on this host. 10.2.4.11 defines portEnabled TRUE iff MAC_Operational and the administrative port state is Enabled (802.1X does not apply). Milan v1.2 4.2.6.2.5 ends the cease on a link-state toggle, a portEnabled toggle, a pttPortEnabled toggle, or after 5 minutes. 4.2.6.2.4 reports asCapable after 2 to 5 good exchanges.
- **Wiring.** `hdl/milan/milan_datapath.sv:8903` drives `.port_enabled_i (eff_link_w)`. `eff_link_w` at `hdl/milan/milan_datapath.sv:3194-3195` is `i_link_up & cfg_sw_link & (cfg_linkg_dis | linkg_est_w)`: the MultiReg-synchronised PHY link (`sw/litex/milan_soc.py:1921`), `LINK_CTRL[0]`, and the guard's estimate unless the guard is disabled.
- **Mapping to the clause.** That is MAC_Operational (PHY link and the guard's receive-clock liveness) AND the product's only administrative qualifier (`LINK_CTRL[0]`, the firmware link qualification, reset value 1 per `docs/reference/REGISTER_MAP.md:752`).
- **Pass-through.** `KL_gptp_shadow.sv:199` adds the input and `:711` passes it straight to the engine.
- **Engine side.** The engine at the pin (`gptp-processor/hdl/top/KL_gptp_engine.sv:1117-1132`) registers the level once and takes the first sample after reset as the reference. Each later edge raises the slot-6 NOT_ENABLED leg, and a rise also queues the request beat (INITIAL_SEND_PDELAY_REQ).
- **Domain.** The three terms and the engine are all `axis_clk` (`milan_datapath.sv:8851`), so no CDC primitive is needed. That meets CONTRIBUTING section 1.
- **Planted kills.** Each loss check is killed by its planted wiring mutant, measured here (`receipts/probe-table.md`):
  - PHY alone (W2): LINK_CTRL[0] and guard checks fail.
  - No guard term (W3): guard check fails.
  - No LINK_CTRL[0] (W4): LINK_CTRL[0] check fails.
  - No PHY term (W5, a probe the author's table does not list): link-loss and toggle-exit checks fail.
  - Tied high in the datapath (W1) or in the shadow (W7): all four loss and toggle checks fail.
  - Tied low (W6): the three preconditions fail.

### (3) The new checks are behavioural, not tautological

- **asCapable falls at a loss.** Each fall check reads `CLKV_STAT[16]` (`0x77C`) over the AXI path, 2 ms after the loss. That bit is the bit GET_AVB_INFO serves (`REGISTER_MAP.md:793`). Before #94 asCapable fell only at the fifth lost response, about 4 s later.
- **Preconditions.** Each fall check is preceded by a graded precondition that asCapable is TRUE.
- **Toggle exit.** With the toggle removed (T1), the leg fails the toggle-exit check. So that check depends on the toggle, and the cease is really in force when the link drops.
- **Measured values (D0).**
  - The first Pdelay_Req follows the return by 316 fabric cycles (158 us at 2 MHz). The bound is one interval, 2,000,000 cycles. Without the fix it would come about 2.2 s after the return.
  - The countdown exit comes 9,999,990 cycles after the last request, inside 10,000,000 +/- 2,000.
- **Countdown.** It is killed by "the countdown loads one beat less" (E3) and by "a portEnabled edge keeps the cease" (E1).
- **Shipping default.** The 5-minute default is unchanged at the pin (`CEASE_MS_C = 300_000` at both `f97c1803` and `135afd04`). The leg runs its 3 s image (`--cease-ms 3000`, `tb/verilator/milan_dp/Makefile`).

### (4) Pin-derived records

- **ROM ledger.** I regenerated `gptp_ucode.hex` with the pin's generator at its defaults. The sha256 `99266fa9197a17a75812ea11dfa0fb9e9e1bd403df1a6a06381857c94ecaed32` equals the new `syn/yosys/rom_digests.tsv` row and the donor's tracked `syn/ooc/work` image (`receipts/rom_regen.log`).
- **Diagrams.** `submodule_boundaries.gen.py --check` and `timesync_chain.gen.py --check` are rc 0.
- **Doc and port gates.** `check_submodule_docs.py`, `check_gptp_docs.py --with-submodule` and `check_port_contracts.py` are rc 0. The last one covers the `port_docs.budget` header.
- **Old pin.** No document outside the dated #803 history and the ledger names `f97c1803` as current.

### (5) Other gPTP consumers

- **Run here at head, rc 0** (`receipts/consumers/`):
  - `milan_dp gptp` and `gptp-lat`: 210 / 210 each.
  - `gptp_shadow run`: 325 / 325.
  - `gptp_plane run`: 29 / 29.
  - `gptp_txts run`: 85 checks, 0 failures.
  - `milan_dp gmstep`: 196 checks, 0 failures. The suite's 202 is this leg plus its control lines.
- **Not run here:**
  - `tsn_fuzz ptp`: this host has no tsn-gen, so it would only SKIP. The author's receipt reads 675 pass.
  - The physical `milan_dp_gptp` leg (205 checks, about 5,650 s): the author's receipt at `cf3ef596`, whose inputs equal this head's.

## Findings

My own pass found no BLOCKER, MAJOR, MINOR or RESIDUE. One prior RESIDUE, R736-1-R1, is retained at this head (Prior public review findings below).

**S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/sim_gptp.cpp:1770-1772` - the toggle check bounds the return's request at one interval.**
- Evidence: the donor text "a rise sends no request at once" (E5) survives the parent leg, 210 / 210. The bound is the issue's frozen acceptance ("within one interval"), and the donor suite grades "at once". `GPTP_PLANE.md` states "The link's return sends one Pdelay_Req at once".
- Impact: none on the acceptance. The parent leg alone does not tell INITIAL_SEND_PDELAY_REQ from the next cadence beat.
- Optional outcome: a tighter bound (the measured value is 316 cycles), or a note that the parent bound is the acceptance's.
- Verification: E5 then fails the toggle check.

**S2 - SUGGESTION - Tests, Robustness - `tb/verilator/milan_dp/sim_gptp.cpp:1729-1757, 1760-1773` - the leg does not check that a disabled port transmits nothing.**
- Evidence: the donor text "a disabled port keeps its credit and starts its frames" (E6) survives the parent leg, 210 / 210. The donor grades the silence. The parent docs state it (`GPTP_PLANE.md` Port enable; `GM_LOSS_RECOVERY.md:40` "send nothing") but do not claim the leg grades it.
- Impact: none on the acceptance. The wiring that carries portEnabled is already proven by the loss checks.
- Optional outcome: count gPTP frames in `tx_frames` inside each down window.
- Verification: E6 then fails.

**S3 - SUGGESTION - Tests - `tb/verilator/gptp_shadow/gptp_shadow_wrap.sv`, `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:190-199` - the shadow-level withdrawal seam is exercised by no parent test.**
- Evidence: all three plane wrappers tie `port_enabled_i` high. The comment's claim, that a withdrawn frame leaves nothing because the gearbox and the ticket take accepted bytes only, holds on reading: `KL_gptp_shadow.sv:799` qualifies `tx_byte_w` on valid and ready, and `KL_gptp_txticket.sv:147` qualifies `beat_w` the same way. No parent harness drives a withdrawal under a stalled lane.
- Optional outcome: a `gptp_shadow` phase that drops `port_enabled_i` while the lane stalls a frame's first byte.

**S4 - SUGGESTION - Robustness - `hdl/milan/milan_datapath.sv:3195` - the guard-disabled arm of `eff_link` is not graded for portEnabled.**
- Evidence: the leg writes `LINK_CTRL` only as `0` and `1` (`sim_gptp.cpp:1186, 1208, 1748, 1753`), so bit 2 (guard disabled) is never set. A mutant that drops `cfg_linkg_dis` would survive. I infer this from the writes and did not plant it.
- Impact: none on the acceptance. The expression predates this PR, and `GPTP_PLANE.md` states "A disabled guard drops that term".
- Optional outcome: one phase with `LINK_CTRL = 0x5` that kills the guard's receive clock and expects asCapable to hold.

**S5 - SUGGESTION - Docs - `docs/traceability/ieee8021as.md:44` - no traceability row for 10.2.4.11.**
- Evidence: AS-8 (peer delay and asCapable) lists "Donor; `tsn_fuzz`". The parent now owns the portEnabled source, which the `milan_dp` gptp leg grades, and no row names 10.2.4.11.
- Optional outcome: name `milan_dp` in AS-8's evidence, or add a 10.2.4.11 row owned by `milan_datapath` / `KL_gptp_shadow`.

## Lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 802.1AS-2011 10.2.4.11 and Milan v1.2 4.2.6.2.4/4.2.6.2.5 (clause text on this host) against `milan_datapath.sv:3194-3195, 8903`, `KL_gptp_shadow.sv:190-199, 711`, `KL_gptp_engine.sv:1117-1132` at `135afd04`; #806 scope and acceptance; the three #94 leg checks with measured values (D0) | R735-1 | `f99405af0b2caad46e84f50f8251ffbffaa80836` |
| RTL | CLEAN | `eff_link_w` terms and their domains (`milan_datapath.sv:3160-3195, 8851`, `milan_soc.py:1918-1921`); shadow port and pass-through; engine port block; gearbox and ticket acceptance (`KL_gptp_shadow.sv:784-833`, `KL_gptp_txticket.sv:143-196`); gitlink, tree and parent equality; `lint_rtl.py --check` PASS (89 <= 89) | R735-1 | `f99405af0b2caad46e84f50f8251ffbffaa80836` |
| Robustness | CLEAN (S2, S4 optional) | loss by each of the three terms (W2-W5), tie high and low (W1, W6, W7), the toggle inside the cease, the unchanged countdown, a first enable since reset (engine reference sample), a withdrawn unaccepted frame (structural); guard-disabled arm noted in S4 | R735-1 | `f99405af0b2caad46e84f50f8251ffbffaa80836` |
| Tests | CLEAN (S1-S3 optional) | `sim_gptp.cpp:533-607, 1655-1807, 2077, 2089-2093`; 17 probes rebuilt from scratch (`receipts/probe-table.md`): every new check fails under at least one planted defect, and the tautology probe T1 fails the toggle check; clean `gptp` and `gptp-lat` 210 / 210; consumers `gptp_shadow`, `gptp_plane`, `gptp_txts`, `gmstep` rc 0 | R735-1 | `f99405af0b2caad46e84f50f8251ffbffaa80836` |
| Docs | CLEAN (S5 optional) | `GPTP_PLANE.md` Port enable, `TIME_SYNC.md:89-91`, `GM_LOSS_RECOVERY.md:40, 52`, `AREA_BUDGET.md:143-144`, `SUBMODULES.md:24, 383-431, 564-567`, `CHANGELOG.md` entry, four guides, traceability, `milan_dp/README.md:91`, comments in the source delta (no lane, round or reviewer label); `docs_check.py`, `check_doc_style.py`, `check_cpp_idiom.py`, both diagram `--check`s, `check_gptp_docs.py --with-submodule`, `check_submodule_docs.py` rc 0 | R735-1 | `f99405af0b2caad46e84f50f8251ffbffaa80836` |

## Real limits

- Physical calibration was NOT RUN, and no hardware was used. The bench link-toggle scenario that #806's second acceptance names is not run; no desk result stands in for it.
- **Gates not run here, author receipts only:**
  - the full parent sweep;
  - Yosys;
  - the builder and the docs workflow banks;
  - xvlog;
  - the Python and shell idiom gates;
  - the physical `milan_dp_gptp` leg;
  - `tsn_fuzz ptp` (this host has no tsn-gen);
  - the Vivado resource gate.
- `lint_rtl.py --check` ran with the host's default Verilator (5.052). The legs and every probe used the pinned 5.050.
- The companion patch bytes are not public, so I matched the companion by blob equality and the donor PR text (item 1).
- The #806 maintainer and manager comments were not read before this verdict. This brief's isolation rule forbids listing issue comments first, so the verdict's scope came from the issue body and the brief. I read them afterwards, and the verdict is unchanged.
- Raw logs carry host path prefixes, so the published copies replace them with placeholders (`receipts/redactions.json` holds each file's sha256 before and after). The originals stay under `scratch/`, unpublished.
- The host was heavily loaded (load average 57 to 69, from other work), so the wall times in the probe logs are not the leg's cost.

## Pending manager duties

- **Area.** Route-1x1 is refused on WNS. #806's "the area gate passes" is unmet. Per the manager's public disposition (read after the verdict), #814's logic cut comes first, with no floor or fall exception. Then this lane merges dev and re-routes, and a delta review covers that head.
- **Merge candidate.** Validate the current-dev merge candidate (builder and native banks), and accept the hosted and act results on the exact head.
- **Hosted window.** Watch the hosted window of `milan_dp` leg 0. The gptp case's local user time doubles (163.8 s to 351.1 s, author receipt). Refresh `PIECE_SECONDS` from the next complete hosted run, as `docs/testing/CI_WORKFLOWS.md:519` prescribes.
- **Bench.** The link-toggle gPTP scenario on an image built from this change, after merge, before #806 closes.

## Prior public review findings at this head

### What I read, and when

I read the PR and issue comment history only after the verdict and ledger above were written. At that time PR #813 had:

- two review-start comments;
- one review verdict, the external round R736-1 (`[R736] POSITIVE` at this same head);
- no submitted reviews and no inline comments.

On #806 I read the assignment, the TAKEN and REVIEW READY comments, and the manager's timing disposition (issuecomment-6514731297).

The assignment's wording, "port_enabled_i from eff_link (the link guard's link_est_o AND LINK_CTRL[0])", matches the head: the existing `eff_link_w` also carries the PHY term, and the assignment names `eff_link`. My verdict is unchanged.

### R736-1-R1, RESIDUE (Docs): RETAINED at this head

- **What it says.** The new sentences call the route-1x1 refusal an owner decision:
  - `CHANGELOG.md:76`: "That refusal needs an owner decision (#806)."
  - `docs/design/AREA_BUDGET.md:144`: "...#806 holds the owner decision that refusal needs."
  - `docs/reference/SUBMODULES.md:429`: "#806 holds the owner decision this refusal needs."
  - The PR body's Status, Known limitations and Definition of Done.
- **Why it is stale.** The manager's public disposition, posted after this head was published, says the refusal is not an owner decision. It is the #708 class of route miss, ruled a logic cut with no floor or fall exception, and #814 makes the cut. Once #814 merges, this lane merges dev and re-routes.
- **Why it is RESIDUE.** It is wording only: no figure, verdict, gate, test, code, generated artifact or clause claim changes. It leaves Docs clean.
- **Exact fix.** Replace each of those sentences with: "Timing recovery is assigned to #814; this change then merges dev and re-routes, with no floor or fall exception." Make the same replacement in the PR body for the "accept and re-record, or recover" choice and for "the area gate's open decision". Keep every measured figure, the refusal, and the open acceptance checkboxes.
- **My own report.** I did not raise this in my own pass, because the disposition was not among the sources I may read before the verdict. The area duty below is corrected to the disposition.

R735-1 FINISHED
