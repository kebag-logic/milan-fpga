[R468] POSITIVE - exact head f9b8f0ee6604a73b9fa82c62b91811e9f53b320a

# R468-3: internal independent review of PR #157 (issues #81 / GAP-07 and #84 / GAP-10)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #157 (`Closes #81`, `Closes #84`, `Relates to #71`).
- **Exact head:** `f9b8f0ee6604a73b9fa82c62b91811e9f53b320a`, tree `0e4e1c96a8bbd9fd7812dc0c1c84697a9adb6242`.
- **Lane base:** `83999eba1ef4756e9e769e4fba164f5095761604`. The head merges processor `main` `07b1469d` (PR #154) into `1d6c78f1`.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open, and all five lenses are CLEAN.
  - Two SUGGESTIONs: S1, how tight the TD window is; S2, the F00.2 residue cells.
  - One new RESIDUE: RES1, the PR body's stale head sentence.
  - One prior RESIDUE is retained: R469-1 R1.
  - The prior MINOR, R468-1 F1, is resolved at this head.
- **Order.** I wrote my independent verdict and ledger before reading any prior review of this PR (`receipts/verdict-before-prior.md`). Reading the prior findings afterwards changed no verdict.

## 1. Scope, reconstructed

**Authorities.**
- The repository has no AGENTS.md or CONTRIBUTING.md. `docs/README.md` holds the author conventions:
  - the single-source rules in §2;
  - the figure and citation rules in §3 and §4;
  - the editing workflow in §6, with `make check`.
- The #81 issue body and its acceptance items 1 to 4.
- The #84 issue body and its acceptance items 1 to 4.
- The closeout assignment, #81 comment 5977862493, with items 1 to 4 and its constraints.
- The manager rulings, #81 comment 5981958399:
  - T-IDENT-* is "implemented and graded";
  - T-CTR-OBSERVE is integrator-owned;
  - the area pair is base to head.
- PR #140 delivered #81 acceptance 1 to 3 and #84 acceptance 1 to 3. This lane owns only:
  - #81 acceptance 4: the F08.1 rows without RTL, and the 300 s / 60 s defaults pinned;
  - #84 acceptance 4: 02 §2 rule 5;
  - the assigned R419-2 F5 remainder: GET_DYNAMIC_INFO serialized against listener steps.

**What the diff contains.**
- `git diff 07b1469d..f9b8f0ee` is exactly the lane's 16 files: docs 02, 03, 06, 08 and 09; `hdl/top/protocol_processor_top.sv`; and `tb/pp_top` (Makefile, README, wrap, `sim_main.cpp`, `notify_phases.hpp`, `aecp_mutants.py` and four mutation patches).
- The rest of `83999eba..f9b8f0ee` is PR #153 and PR #154 as merged on `main`.
- The manager's merge is a clean three-way merge. `git merge-tree --write-tree 1d6c78f1 07b1469d` gives tree `0e4e1c96`, the published tree. The two sides share no file.
- `git diff --check` passes against both `83999eba` and `07b1469d`.

## 2. Findings

### S1: SUGGESTION (Tests). TD pins each default to a 21 ms band, not to the ms

- **Where:** `tb/pp_top/notify_phases.hpp:1624` (`SLACK_MS = 20`) and the TD1/TD2 windows at `:1684-1708`.
- **Evidence:** my probes plant both parameter defaults in one build and run `make timer-defaults`.

  | Probe | Defaults | TD measures | TD verdict |
  |---|---|---|---|
  | `scripts/qa-td-lower-slack.patch` | `LOCK_TIMEOUT_MS_P` 59,997, `REG_TL_TIMEOUT_MS_P` 299,998 | 60,000 / 300,000 ms | 3 of 3 PASS |
  | `scripts/qb-td-upper-slack.patch` | 60,017 and 300,018 | 60,020 / 300,020 ms | 3 of 3 PASS |

  Logs: `receipts/runs/probe-qa-td-lower-slack.log` and `receipts/runs/probe-qb-td-upper-slack.log`. The head itself measures 60,003 and 300,002 ms.
- **Impact.** No stated claim is false. 09 §8.3 and the README state the window exactly: "no sooner than the default ... and at most 20 ms later". Both committed ±1 s arms are killed. Acceptance 4 ("pinned by a check") is met for any realistic fault.
- **Suggested outcome.** Narrow `SLACK_MS` toward the measured +3 ms, or record the effective band in the TD paragraph. R468-1 S1 and R469-1 S1 make the same observation.

### S2: SUGGESTION (Docs). F00.2 still names #81 and #84 as open residue

- **Where:** `docs/00_MILAN_COMPLIANCE_REVIEW.md:549` (GAP-07) and `:552` (GAP-10), "Open residue" column.
- **Evidence.** Both cells link the issue this PR closes, with no remainder text.
- **Impact.** After the merge, the matrix points at closed issues as open residue. GAP-06's row (#80) keeps the same convention, so this is not a regression of this lane, and neither issue's acceptance asks for it.
- **Suggested outcome.** At merge, the manager may restate the two cells, as GAP-02 and GAP-05 do. GAP-07's remainder would be "ACMP's stamped deadline has no kill consumer (08 §4, ruled)". GAP-10's would be "none in this repository".

### RES1: RESIDUE (Docs, PR body). The opening paragraph names a superseded head

- **Where:** the PR #157 body, first paragraph: "Six commits: one per item, one README record, and the merge of `main` `c050d971` ... The head is `db2c4eb`."
- **Evidence.** The exact head is `f9b8f0ee`. Two commits follow `db2c4eb`: the manager's docs commit `1d6c78f1` and the merge of `07b1469d`. Only the closing "Manager commit" and "Manager merge" notes mention them.
- **Why it is RESIDUE.** It is wording only. No measurement, figure, verdict, test or code changes; the validation tables name their commits explicitly.
- **Exact fix.** Replace "The head is `db2c4eb`." with "The lane's commits end at `db2c4eb`; the manager's `1d6c78f1` and the merge of `main` `07b1469d` follow, and the exact head is `f9b8f0ee` (see the notes at the end)."

## 3. Prior public review findings on this PR (read after my own pass)

| Prior item | Severity | State at `f9b8f0ee` | Evidence |
|---|---|---|---|
| R468-1 F1: F06.14, F03.7 and the 03 §6 list call GDI RO_SNAPSHOT | MINOR | **RESOLVED** by `1d6c78f1` | F06.14 GDI cell: "MAP_CFG at admission, no-descriptor key (assigned by the top's classifier, 03 §6); records RO" (`docs/architecture/06_aecp_engine.md:269`). F03.7: RO_SNAPSHOT "all GETs but GET_DYNAMIC_INFO" and MAP_CFG lists GDI (`03_packet_engine.md:235,238`). The 03 §6 list names "GET_DYNAMIC_INFO `MAP_CFG` (below)" (`:252`). `grep "RO per record"` is empty. HZ1 wants MAP/NONE (`tb/pp_top/sim_main.cpp:13167`). `make check` rc 0. |
| R468-1 S1 / R469-1 S1: TD window | SUGGESTION | retained | my S1, re-measured at this head |
| R468-1 S2: HZ13 could also grade the batch answers and the talker side | SUGGESTION | retained, optional | unchanged at head. My probe q5 shows that HZ8, HZ13a and HZ13c already kill a GDI-as-STREAM_CFG classification. |
| R468-1 S3: "Relates to #71" | SUGGESTION | **applied** | the PR body carries "Relates to #71" |
| R469-1 S2: P-EN-PLAIN-IEEE-PROFILE has no RTL consumer and no F01.5 note | SUGGESTION | retained, a manager duty | `docs/architecture/01_overview.md:193` unchanged |
| R469-1 R1: 09 restates F08.1's values (`docs/README.md` §2 single-source rule) | RESIDUE | **retained** | `docs/architecture/09_verification.md:254` "60,000 and 300,000 ms" and `:272` "the real 300,000 ms" are unchanged. The exact fix is R469-1's: cite F08.1 / `T-NOTIF-TIMELIMITED` by ID. |
| R419-2 F5 (PR #140): GDI not serialized against listener steps | (assigned remainder) | **RESOLVED** | HZ13a passes at head. Arm `hz-gdi-key-none` reproduces the old admission ("refused 0 clocks"), killed with 7 failures. |

R468-2 and R469-2 were withdrawn unfinished and carry no findings.

## 4. Lenses

### Conformance: CLEAN

- **#81 acceptance 4, the F08.1 rows** (ruling 1):
  - `docs/architecture/08_timing.md:30-31` marks T-IDENT-BURST and T-IDENT-REARM **landed**, owned by `KL_aecp_notify` and gated by P-EN-IDENTIFY-NOTIFICATION. The cited grading exists:
    - `tb/aecp_notify/README.md:27-60`, FT1 to FT4 and their arms;
    - the `tb/pp_top` ID section, whose identify build ran 178/0 at this head.
  - `:32` marks T-CTR-OBSERVE **integrator-owned**, consistent with `docs/guides/integrator.md:470` and 06 §6.6.
  - 09's TIM row (`09_verification.md:53`) now claims only the rows with RTL here.
- **#81 acceptance 4, the defaults.**
  - TD1 grades T-LOCK-UNLOCK at the top's own 60,000 ms (IEEE 1722.1-2021 §7.4.2, Milan §5.4.2.2).
  - TD2 grades T-NOTIF-TIMELIMITED at the top's own 300,000 ms (IEEE §7.4.37.2).
  - Both use the real counts on the 1 ms = 100 clk prescaler, not the 400 ms override. The wrap drops the override only under `PP_TOP_TIM_DEFAULTS` (`tb/pp_top/pp_top_wrap.sv:549-557`).
  - Measured at head: 60,003 and 300,002 ms, with 6 monitor probes answered.
- **#84 acceptance 4.** 02 §2 rule 5 (`02_interfaces.md:115-124`) states one synchronous active-low `rst_n`. That matches the RTL:
  - all 164 `always_ff` in `hdl/` are `@(posedge clk_i)`;
  - nothing in `hdl/` matches `negedge` or `posedge rst`.
  
  The rule's boot-hold statement agrees with 07 §5.3's release table (`07_memory_maps.md:735-745`) and 05 (`:194-202`). No other asynchronous-reset wording remains in `docs/`. `docs/guides/hdl-engineer.md:63` and `integrator.md:175` already said "synchronous".
- **GET_DYNAMIC_INFO** (03 §6 F03.7, IEEE 1722.1-2021 §7.4.76.1, Milan §5.4.2.10):
  - A batch carrying a GET_STREAM_INFO record of STREAM_INPUT k now waits for, and holds back, sink k's listener step, as the stand-alone getter does (HZ6, HZ13a, HZ13c).
  - It still runs beside ACMP reads (HZ13b).
  - The over-serialization is the one the assignment accepted, and it is stated in 03 §6, F03.7, F06.14, 08 §4 (`:197-200`) and 09 §8.3.

### RTL: CLEAN

- **The change.** The only RTL change is one `unique case` item, `16'h004B: hz_class_w = 4'(PP_HZ_MAP_CFG);` (`hdl/top/protocol_processor_top.sv:1645-1646`), plus its comment (`:1542-1554`).
  - The key keeps the default `HZ_KEY_NONE_C = {6'h3F, 10'h000}`.
  - The item overlaps no other item.
  - It applies only under `hz_aem_cmd_w`, an AEM command for this entity.
- **What consumes the class.** `hazard_class` is read only at the scoreboard admission mux (`:3569-3576`). The normalizer only copies it (`KL_pp_normalizer.sv:136`). So no lock, deadline or dispatch path changes.
- **The scoreboard matrix** (`KL_pp_scoreboard.sv:119-157`):
  - **Rule 5.** It cross-locks `MAP_CFG` with any `STREAM_CFG`, so the batch is held as intended.
  - **Rule 2.** Against `RO_SNAPSHOT` it is same-key only. ACMP keys carry descriptor type 5 or 6, never 0x3F, so ACMP reads still run beside the batch.
  - **Rules 3 and 4.** `LOCK_OP`, `CFG_BARRIER` and a second `MAP_CFG` are presented only by the single-issue AECP engine, so they never meet the batch.
- **Probe q7** (`scripts/q7-sb-rule5-per-key.patch`) narrows rule 5 to same-key. It fails HZ7, HZ11d, HZ8 and HZ13a/c, 10 failures. The new checks therefore depend on the class-wide cross-lock, as the docs say.
- **Lint:** `scripts/lint_hdl.sh` rc 0, 41 modules (`receipts/runs/lint_hdl.log`).
- **Area.** The base-to-head pair (−30 LUT / −4 FF) is inside the ruling's 60/60 line, and the +67/+110 attribution was ruled by the manager. This round adds no RTL, and PR #154's SRP files are outside this lane's diff. I ran no Vivado (see limits).

### Robustness: CLEAN

- **The wait in each direction is bounded.**
  - An ACMP stream step that waits for a GDI is bounded by the AECP deadline. GDI is preempted past `T-BUDGET-AECP-WC`; DL4 passes in the head's full suite, DL 64/0. 08 §4 lists the hold (`08_timing.md:197-200`).
  - A GDI that waits for an ACMP step carries a deadline stamped at reception, and it is answered after its admission.
- **No circular dependency or starvation.**
  - While the batch waits it is not admitted, so the AECP engine is idle and the ACMP step cannot depend on it.
  - The round-robin's `sb_prefer_aecp_r` gives AECP the next pick after any ACMP grant (`protocol_processor_top.sv:3562-3564`).
- **TD cannot pass by accident.**
  - Its registration is kept alive only by answering the departing-controller monitor, so only the timer under test can end it.
  - Its expected frames are byte-exact apart from the echoed sequence_id.
  - The two committed arms fail it: 59,003 ms, and no DEREGISTER by 300,020 ms.
- **Probe q5** (`scripts/q5-gdi-as-stream-cfg.patch`), GDI as `STREAM_CFG`/NONE: killed by HZ1, HZ8, HZ13a and HZ13c, 7 failures. A plausible wrong class is therefore caught by more than HZ1.

### Tests: CLEAN

- **Head full suite.** `make -C tb/pp_top` in an exact-head export (tree `0e4e1c96`, verified): rc 0, **10,431 checks, 0 failures** over six builds.
  - Per build: default 9,943 (HZ 189/0, DL 64/0); fixture 20; identify 178; line 231; timebase 56; defaults 3 (TD 3/0).
  - Wall time 12 min 33 s; peak RSS 0.5 GB.
  - Logs: `receipts/runs/r1-pp_top-full.log` and `.rc`.
- **AECP campaign at head.** `tb/pp_top/aecp_mutants.py --jobs 3 --only` the lane's six arms plus the three arms whose counts changed:
  - rc 0: 2 controls PASS (`hazards`, `timer-defaults`), 9 of 9 KILLED;
  - `td-lock-default-59s` 1 (59,003 ms) and `td-tl-default-301s` 1 (got −1);
  - `hz-gdi-key-none`, `-held` and `-no-stream` 7 each;
  - `hz-gdi-as-barrier` 2;
  - `hz-stub-restored` 81 (HZ1 35 rows), `hz-acmp-reads-as-steps` 27, `hz-barrier-no-priority` 139.

  Every count equals `tb/pp_top/README.md`'s table and the PR body. Logs: `receipts/runs/r2-aecp-campaign.log`, per-arm logs in `receipts/aecp_selected/`.
- **The 12 new HZ checks** (HZ8's batch 3, HZ13a 3, HZ13b 2, HZ13c 4) take HZ from 177 to 189, as the PR body records.
- **Changing a default fails TD** at ±1 s (committed arms). Probes qa and qb above show the band at the window's edges. The band is a suggestion, not a defect.
- **CI wiring.** CI runs `run_suites.sh` (which runs `make -C tb/pp_top`, now six builds) and `make -C tb/pp_top aecp-mutants` (`.github/workflows/hdl.yml:54,70`), so both the TD build and its arms are in CI.

### Docs: CLEAN

- **Docs gates at head.** `make check` in an exact-head export: rc 0.
  - lint: 41 mermaid and 18 wavedrom blocks;
  - links: 1,133 OK (1,122 at `db2c4eb`, plus PR #154's);
  - matrix: 115 REQ rows and 17 GAP findings;
  - modmatrix: 94 rows, 0 untested;
  - params: 28/28/28.

  Log: `receipts/runs/docs-make-check.log`.
- **PR body citations** match the head's lines. I checked:
  - 08 `:30-32`, `:170-171`, `:197-200`; 09 `:53`, `:254`, `:270-272`; 02 `:115-124`; 03 `:264-278`;
  - `sim_main.cpp` `:13167`, `:13519-13520`, `:13703-13743`, `:13804-13808`;
  - `aecp_mutants.py` `:61-67`, `:176-189`; the wrap `:549-557`; the Makefile `:169-170`, `:185-196`;
  - `notify_phases.hpp` `:1608-1717`; the top `:1542-1554`, `:1645-1646`.
- **README records** match my reruns: the build tables, TD, HZ8 and HZ13, and the campaign table and note.
- **Open items:**
  - RES1 (PR body wording) is RESIDUE.
  - R469-1 R1 (09 values) is a retained RESIDUE.
  - S2 is a suggestion.

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #81/#84 acceptance, the assignment and rulings; F08.1, 09 TIM row and §8.3, 02 §2 rule 5, 03 §6 F03.7, F06.14, 08 §4; RTL reset sweep (164 `always_ff`); identify suites; TD1/TD2 against IEEE §7.4.2/§7.4.37.2 and Milan §5.4.2.2; HZ13 against IEEE §7.4.76.1 | R468-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |
| RTL | CLEAN | classifier item and comment; scoreboard matrix rules 1-6; `hazard_class` consumers; admission mux and round-robin; lint_hdl 41/41; probe q7 | R468-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |
| Robustness | CLEAN | 08 §4 hold bounds; deadline read at admission and DL4; deadlock and starvation analysis; TD keep-alive and byte-exact frames; probes q5 and q7 | R468-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |
| Tests | CLEAN | head `tb/pp_top` 10,431/0 (six builds); AECP campaign 2 controls + 9 arms with per-arm counts; TD band probes qa/qb; CI wiring | R468-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |
| Docs | CLEAN (RES1 and R469-1 R1 RESIDUE; S2 suggestion) | `make check`; PR body citations; `tb/pp_top` README records; 02/03/06/08/09 text; F00.2; the merge's tree identity | R468-3 | f9b8f0ee6604a73b9fa82c62b91811e9f53b320a |

## 6. Real limits

- **Not re-run by me.**
  - Full banks the brief reserves to the manager: `./scripts/run_suites.sh`, Yosys, the builder, and the parent consumer set at dev `fea346e7`.
  - AECP arms whose records this lane does not change, and the dispatch, ACMP, counters, GSI, NAME_WR, notify, D3, MAAP and ADP campaigns.
  - Vivado (no OOC run). Area rests on the manager's ruling and the published runs.
  - PR #154's SRP suites and campaigns. That PR shares no file with this lane. Its RTL (`KL_srp_*`) is built into `tb/pp_top`, and the head's full `tb/pp_top` passed.
- **Manager banks.** The manager's source static/builder and native banks are stated as passed at this head. Their receipts are not in the public evidence commit `5de7b6be`, which holds only the author's HANDOFF, PR body and parent patches, so I did not re-check them.
- **Hosted CI** at the exact head, snapshot 2026-10-04T17:34Z (`receipts/hosted_checks_snapshot.txt`):
  - `docs-gates` and `portability` succeeded for both workflow runs;
  - `suites` was still in progress for both.

  I accept nothing hosted; the manager owns hosted and act acceptance.
- **Not hardware proof.** Physical calibration was NOT RUN, and field skips are not hardware proof. This is source validation; the final current-dev candidate is the manager's, built at the merge turn.
- **Redaction.** One host path prefix is redacted in the logs: the simulator's install root, shown as `<pinned-simulator-root>`. Nothing else is altered.

## 7. Pending manager duties

- Build the final current-dev candidate at the merge turn: source base `83999eba`, live dev `fea346e7`. Run the parent consumer set with the lane's patches and PR #153's `parent-adoption-232-241f9184.patch`, which the pin bump owes for gate 9. Gate 16's T30 checks belong to milan-fpga #643 / PR #648.
- Accept hosted `suites` once it completes at `f9b8f0ee`.
- Carry RES1 (the PR body head sentence) and R469-1 R1 (09 `:254`/`:272`) to the residue checklist with their exact fixes.
- Decide on S1 (TD band), S2 (F00.2 residue cells), R468-1 S2 (HZ13 extra checks) and R469-1 S2 (the P-EN-PLAIN-IEEE-PROFILE note) before closing #84.

## 8. Receipts and clone state

`MANIFEST.sha256` lists every publishable receipt, with paths relative to the packet root.

**Scripts:**
- `scripts/env.sh`;
- `scripts/run_probe.sh` (export, `git apply --check`, run, log and rc);
- the probe patches `scripts/qa-td-lower-slack.patch`, `qb-td-upper-slack.patch`, `q5-gdi-as-stream-cfg.patch` and `q7-sb-rule5-per-key.patch`.

**Run logs and rc files** (`receipts/runs/`):
- the head full suite (`r1-*`);
- the AECP campaign (`r2-*`);
- the four probes;
- `make check`;
- `lint_hdl.sh`.

**Other receipts:**
- `receipts/aecp_selected/`: the per-arm and per-control campaign logs.
- `receipts/issue81*.json`, `issue84*.json` and `pr157*.json`: the public scope and comments as read.
- `receipts/evidence-*`: the public evidence files read.
- `receipts/verdict-before-prior.md`: the verdict recorded before reading prior reviews.
- `receipts/clone_integrity.txt`: the clone state below.

**Clone state.**
- **Simulator.** Every run used the pinned simulator, verified as `Verilator 5.050 2026-07-01 rev v5.050` through `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator` (wrapper sha256 `905795b9...`).
- **Isolation.** Every build and probe ran in a `git archive` export under `scratch/`. The review clone was never written.
- **Integrity after the runs:**
  - HEAD is `f9b8f0ee`, tree `0e4e1c96`;
  - `git status --porcelain --ignored` is empty;
  - the index equals HEAD (`write-tree` `0e4e1c96`);
  - all 558 worktree files equal their index blobs and modes: 543 at 100644, 15 at 100755.
- **Gitlinks.** This repository tracks no submodule gitlinks (0 entries at mode 160000), so there is none to verify.

R468-3 FINISHED
