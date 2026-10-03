[R443] POSITIVE - exact head 81edaaa74f688081ad34c1e2f392612f46eb558c

# R443-2: external independent review of processor PR #147 (lane C7, counters), round 2

- **Head:** exact head `81edaaa74f688081ad34c1e2f392612f46eb558c`, tree `39b33c89e8305384affb5d49ca73ff1ab6d92670`. Verified in the review clone; receipt `receipts/clone-integrity.txt`.
- **Round delta:** `e2c7d97d..81edaaa`, nine commits, 23 files, no merges (`receipts/round2-commits.txt`, `receipts/round2-changed-files.txt`). The diff against the source base `c74711d45a8bbc0d6b38cb49211b26a4a6413e88` was read as well.
- **Authorities:**
  - Issue #79's acceptance list and the owner decision of 2026-09-19 (#79 comment 5740180166).
  - The lane assignment (5962255629), the GPTP_GM_CHANGED ruling (5963704232), the round-2 assignment (5963890173) and its addendum (5963896239).
  - IEEE 1722.1-2021 §7.4.42.2.2 to §7.4.42.2.4 (Tables 7-152 to 7-157) and Milan v1.2 §5.3.6.3, §5.3.11.2 and §5.4.2.25 (Tables 5.1, 5.4, 5.6, 5.7, 5.13 to 5.17). This round read the printed standards. The values used are in `receipts/spec-crosscheck.txt`; no standard text is reproduced.
  - The public parent at milan-fpga dev `1269cdafb4bb964c757baae0f0c5a932d43f540b` (`hdl/milan/milan_datapath.sv`), read only.
- **Order of work:** the diff was reviewed independently before the round-1 findings were read. Every round-1 finding is resolved below.

## Verdict

**POSITIVE.** All five lenses are clean.

- Every round-1 finding is closed at this head under its original severity, and every SUGGESTION and RESIDUE item that was taken landed as specified:
  - R443-1: F1 (MINOR), F2 to F4 (SUGGESTION), F5 and F6 (RESIDUE).
  - R442-1: F1 and F2 (MINOR), S1 and S2 (SUGGESTION).
  - The addendum's `.gitattributes` item.
- The round changed nothing outside its items. The RTL changes are comment lines only: the preprocessed source of both files is byte-identical to `e2c7d97d`.
- Independent runs at this head:
  - The `tb/pp_top` suite: 9,196 checks, 0 failures.
  - The ctr campaign at `--jobs 8` and at `--jobs 1`: control PASS and 17 of 17 KILLED both times, with byte-identical records (sha256 `0fd23cc6…`, the same as the author's).
  - `make check`: rc 0.
  - `git diff --check` against main: rc 0. As a negative control, the same check with `e2c7d97d`'s attributes gives rc 2.
- Two new SUGGESTIONs are recorded. Neither affects the verdict.

## Round-1 findings resolved at this head

| Round-1 ID | Original severity | Status at 81edaaa | Evidence |
|---|---|---|---|
| R443-1-F1 (removed adapter ops in 05 A8, the 05 flowchart, the 01 node, the listener comment) | MINOR | **CLOSED** | My own verification grep `avtp\.[A-Z_]+\|srp \+ avtp adapters\|gptp · avtp · mclk adapters` over `docs` finds nothing (rc 1). Also checked: `05_acmp_engine.md:286` (A8, with no stream-datapath request), `:287` (A9 withdraws the bound view), `:106` (`srp face + acmp_bound levels`), `01_overview.md:240` (landed faces), and `KL_pp_acmp_listener.sv:25, :184, :188, :1162` (comments). A9's text matches the RTL: the `lstn_disc_disarm_w` clear at `protocol_processor_top.sv:1808-1819`, and the debounce at `:944-958` (falls only while the executor is idle). `receipts/static-checks.txt` §1 to §3 |
| R443-1-F2 (no check holds the slot rule; probe P3 survived) | SUGGESTION, taken | **CLOSED** | K17 is added (`counters_phases.hpp:347-387`). Four arms each remove one term of `KL_aecp_notify.sv:488-507`. `ctr-notify-avb-any-index` is the round-1 probe P3, and it is now KILLED by K17 "AVB_INTERFACE 1". Each new arm fails only its own K17 check (`receipts/ctr-campaign-jobs8.log`) |
| R443-1-F3 (`--jobs N` missing in `ctr_mutants.py`) | SUGGESTION, taken | **CLOSED** | The driver uses `tb/common/mutant_pool.py` `in_order` (one scratch copy per unit, results in declared order). The records at `--jobs 1` and `--jobs 8` are byte-identical (`receipts/ctr-campaign-jobs-compare.txt`) |
| R443-1-F4 (STREAM_INPUT quadlets 6 and 7 under `0x00000FFF`) | SUGGESTION, taken | **CLOSED** | `integrator.md:456` and `:470` are checked against Tables 7-156 and 7-157: TIMESTAMP_VALID is bit #25 (0x40, offset 24, quadlet 6) and TIMESTAMP_NOT_VALID is bit #24 (0x80, offset 28, quadlet 7). Each counts per received data AVTPDU with tv set or clear. `0xF3F` excludes them and `0xFFF` includes them |
| R443-1-F5 (`DESC_MEM_TMO_CYC_P`) | RESIDUE | **CLOSED** (exact text) | `02_interfaces.md:209-210` and `:435` |
| R443-1-F6 (the `link_up_i` consumers) | RESIDUE | **CLOSED** (exact text, relative link) | `02_interfaces.md:481`. Consumers confirmed: MAAP at top `:2328` and PRNG at `:976` / `KL_pp_prng.sv:68` |
| R442-1-F1 (GPTP_GM_CHANGED stated as a strobe coincidence) | MINOR | **CLOSED** | `integrator.md:486-498` now states one identity comparison: count when the published `gm_id_i` differs from the identity in force; the first identity out of reset counts nothing. It says neither strobe, nor their coincidence, identifies a GM change. The text agrees with:<br>• the table row `:466`, F06.15 `06_aecp_engine.md:612` and REQ-NET-004 (`00:483`);<br>• the harness store `sim_main.cpp:933-937` (`gm_q = GM0` at reset, `:1920`), which K11's domain-only check grades; the `store-counts-domain-strobes` arm is KILLED;<br>• Milan Table 5.1;<br>• IEEE Table 7-152 (bit #26, 0x20) and Table 7-153 (offset 20, "grandmaster change count").<br>The author's correction of the citation is right: in the printed IEEE 1722.1-2021, Table 7-112 is the EPON media-subtype table (§7.3.5.74), not a counters table. The parent's counter (`milan_datapath.sv:7267`, `:3514` at dev 1269cdaf) counts the identity edge only and never a domain-only write. It agrees except for a zero-identity corner the standards leave open (S1 below) |
| R442-1-F2 (removed ops and an in-processor counter block in 01, 05, 06) | MINOR | **CLOSED** | Checked in the tree:<br>• F01.3 no longer has the `ctrs` node or the `adapters --> ctrs` edge (`01:206-254`).<br>• The block-table row at `01:98` and the scope rows at `01:9, :36, :42-46` are corrected.<br>• §7 at `01:195-200` no longer lists a counter-mask ROM.<br>• 05 A8, A9, F05.1 and F05.6 are corrected.<br>• The F06.14 SET_CLOCK_SOURCE row at `06:469` ends on the `aecp_clk_src_index_o` level.<br>• Also fixed: the 03 state-RAM row (`03:31`), the guides index (`guides/README.md:34`) and the participants in `docs/README.md:141`.<br>My broader search (`receipts/static-checks.txt` §2 to §4) finds no removed op or counter block in 01, 03, 05, 06, `docs/README.md` or `docs/guides/README.md`. The remaining "adapter" hits are the `srp` class-B face, which exists |
| R442-1-S1 (the stale GET_COUNTERS paragraph) | SUGGESTION, taken | **CLOSED** | `06:1136-1154` is checked against `gen_ucode.py:823-863`:<br>• the hit path is 17 µops (locate, `BR_STATUS`, `SET_STATUS`, `GATHER_EXT`, `BUILD_HDR`, two `BUILD_FLD`, eight `READ_CTRS`, `SEND_RESP`, `END`);<br>• the miss arm is 11 µops at `E_GCTRS+17`;<br>• `E_GCTRSNS` is 2 µops and falls into the miss arm.<br>`10_RESOURCE_AND_EFFORT.md:404-407` and the top comment at `:368-369` are also corrected |
| R442-1-S2 (= R443-1-F3) | SUGGESTION, taken | **CLOSED** | As R443-1-F3 above |
| Addendum: `.gitattributes` for `tb/pp_top/ctr_mutations/*.patch` | assignment item | **CLOSED** | `.gitattributes:7`; `git check-attr` covers all 17 patches. `git diff --check c74711d4 81edaaa` gives rc 0. Negative control: in a scratch clone at `e2c7d97d` (its own attributes), `git diff --check c74711d4 e2c7d97d` gives rc 2 with the blank-context lines (`receipts/diff-check-negctl.rc`) |

## Findings of this round

| ID | Severity | Lenses | Where | Authority / evidence | Impact | Required outcome | Verification |
|---|---|---|---|---|---|---|---|
| R443-2-S1 | SUGGESTION | Conformance, Docs | `docs/guides/integrator.md:486-498` (the GPTP_GM_CHANGED rule) | The guide counts every published `gm_id_i` that differs from the identity in force. The reference parent at dev 1269cdaf counts only against a **nonzero** prior identity: `milan_datapath.sv:7267` `pp_gm_id_edge_w = (\|pp_gm_id_q_r) & (pp_gm_id_q_r != cfg_adp_gptp_gm)`. The two agree out of reset and on every GM-to-GM change. They disagree only if the published identity passes through 0 ("no grandmaster", which `:1487` also uses when the gPTP plane is absent): for A → 0 → B the guide counts 2 and the parent counts 1. Neither Milan Table 5.1 nor IEEE Table 7-153 defines this case, so neither reading is non-conformant. The PR body's "agrees with ... the reference parent" holds outside this corner | A reader may not know whether a lost-then-regained grandmaster counts once or twice. No check in either repository covers this case | Optional: say how a zero identity is treated (for example, "0 is no identity: the first nonzero identity after it counts nothing, as out of reset"), or note that the choice is the integrator's | Doc review |
| R443-2-S2 | SUGGESTION | Docs | `docs/architecture/09_verification.md:11` (F09.1 node "dispatch / response-size / transition / **mask ROMs**"); `docs/architecture/01_overview.md:153-159` (F01.5 "Affects" column names "counters" for P-N-AVB-INTERFACES, P-N-STREAM-IN/OUT and P-N-CLOCK-DOMAINS) | `07_memory_maps.md:532` says the processor stores no mask ROM, and no `mask*rom` exists in `hdl/` (`receipts/static-checks.txt` §5). In F01.5, the stream parameters do size the notification block's counter slots (`KL_aecp_notify.sv:491-497`), but P-N-CLOCK-DOMAINS does not: there is one CLOCK_DOMAIN 0 slot. Both texts predate this PR, lie outside the round's named documents (01's F01.5 aside), and do not name a removed op or event | Small residual ambiguity about an in-processor counter artifact | Optional: drop "mask" from F09.1, and qualify F01.5's "counters" as "the counter notification slots" or "the integrator's banks" | Doc review; `make check` rc 0 |

No BLOCKER, MAJOR, MINOR or RESIDUE finding is open.

## Five lenses

- **Conformance:**
  - The guide's AVB_INTERFACE, CLOCK_DOMAIN, STREAM_INPUT and STREAM_OUTPUT masks, quadlets and counting rules were re-checked against the printed Tables 7-152 to 7-157 and Milan Tables 5.1, 5.4, 5.6, 5.7 and 5.13 to 5.17, together with the round's new GPTP_GM_CHANGED rule and the quadlet 6/7 row.
  - The citation correction (7-112 → 7-152/7-153) is correct. The wrong number sits in the manager's assignment and ruling, not in the tree.
  - The parent comparison is recorded in S1.
  - Issue #79's acceptance items 1, 3 and 4 stay met. Item 2 does not apply (integrator option).
- **RTL:**
  - Of the two RTL files changed, every changed line is a comment (`receipts/static-checks.txt` §7).
  - Running the pinned simulator's preprocessor (`-E -P`) on `KL_pp_acmp_listener.sv` (41,467 B, `5134a80a…`) and `protocol_processor_top.sv` (155,115 B, `dc511d2d…`) gives byte-identical output at `e2c7d97d` and at the head (`receipts/preprocessed-identity.txt`). So no new out-of-context cost is possible.
  - No port, parameter or register changed.
  - The documented slot decode and µprogram match the RTL and the generator.
- **Robustness:**
  - K17 holds the unslotted-strobe rule for all four types at the first index past each slot range. Its 1.5 s waits exceed the 1 s window, so a strobe folded onto a slot that is still in its window would still be seen.
  - The final positive check ensures that silence is not a dead path.
  - `mutant_pool.in_order` clamps `--jobs` to at least 1, gives each unit its own scratch copy, and cancels pending units when the block exits.
  - The `.gitattributes` exemption is the narrow blank-at-eol/eof form already used by the other five campaigns.
  - Redundancy: the slot limit is now graded as it stands; #69 owns the seam.
- **Tests:**
  - `make -C tb/pp_top` (5 builds): rc 0, **9,196** checks, 0 failures; K-AVB has 28 checks (23 + K17's 5) (`receipts/pp_top-suite.log`).
  - The campaign at `--jobs 8` (134 s) and at `--jobs 1` (370 s): rc 0, control PASS, 17 of 17 KILLED. The per-arm failure counts equal the README table (`tb/pp_top/README.md:1197-1213`) and the PR body arm by arm: 9/3/18/9/1/6/8/1/3/5/8/1/1/1/1/7/11. K17 adds checks to exactly eight round-1 arms; the other counts are unchanged from round 1.
- **Docs:**
  - All round-2 doc edits in 00, 01, 02, 03, 05, 06, 09, 10, `docs/README.md`, `guides/README.md`, the integrator guide, the `tb/pp_top` README and the Makefile comment were read against code and tests.
  - `make check` (scratch clone at the head): rc 0 — 41 mermaid + 18 wavedrom, 1,095 links, 115 REQ / 17 GAP, 94 module rows with 0 untested, 27 parameters (`receipts/make-check.log`).
  - Only one heading changed ("K9 to K16" → "K9 to K17" in the `tb/pp_top` README), as the PR body states; no anchor was removed.
  - The live PR body equals the author-r2 `PR-BODY.md` (sha256 `6589c689…`, matching the evidence manifest).

## Executed evidence (all at the exact head, pinned simulator 5.050, wrapper sha256 `905795b9…`; `receipts/tool-identity.txt`)

| Run | Result | Receipt |
|---|---|---|
| `python3 tb/pp_top/ctr_mutants.py --jobs 8` (git-archive copy) | rc 0, 134 s, control PASS, 17/17 KILLED | `receipts/ctr-campaign-jobs8.log`, `.rc` |
| `python3 tb/pp_top/ctr_mutants.py --jobs 1` (separate copy) | rc 0, 370 s, control PASS, 17/17 KILLED; byte-identical to `--jobs 8`, sha256 `0fd23cc6151456be…` | `receipts/ctr-campaign-jobs1.log`, `.rc`, `receipts/ctr-campaign-jobs-compare.txt` |
| `make -C tb/pp_top` (separate copy, alongside `--jobs 1`) | rc 0, 410 s, 9,196 checks, 0 failures | `receipts/pp_top-suite.log`, `.rc` |
| `make check` (scratch clone at the head) | rc 0 | `receipts/make-check.log`, `.rc` |
| `git diff --check` main..head; e2c7d97d..head; negative control | rc 0; rc 0; rc 2 (attributes from `e2c7d97d`), and rc 0 in the same clone at the head | `receipts/diff-check-*.{log,rc}`, `receipts/check-attr-ctr-patches.txt` |
| Preprocessed identity of the two changed RTL files | identical | `receipts/preprocessed-identity.txt` |
| Static searches, µprogram listing, slot decode, anchors | as cited above | `receipts/static-checks.txt` (`scripts/static_checks.sh`) |
| Public evidence (milan-fpga `05cfbac1`, author-r2 archive) | the PR body and both adoption patches match the manifest's published sha256; the patches are unchanged from round 1 | `receipts/public-evidence-check.txt` |
| Clone integrity after the review | HEAD and tree exact; index tree = HEAD tree; 0 porcelain lines (ignored included); 498 tracked blobs rehashed, 0 differ; modes equal; 0 gitlinks (none required) | `receipts/clone-integrity.txt` |

The probes and builds ran in disposable copies under the packet's scratch area. No file in the review clone was edited. `scripts/run_dynamic.sh` reproduces the dynamic runs.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | integrator guide §7.1 (masks, quadlets, counting and reset rules, the new GPTP_GM_CHANGED rule and the quadlet 6/7 row) against printed IEEE 1722.1-2021 Tables 7-152 to 7-157 and Milan v1.2 Tables 5.1, 5.4, 5.6, 5.7, 5.13 to 5.17; the Table 7-112 citation check; F06.15; REQ-NET-004; the harness store; the parent counter at dev 1269cdaf (S1 recorded) | R443-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |
| RTL | CLEAN | the comment-only diffs of `KL_pp_acmp_listener.sv` and `protocol_processor_top.sv`, with preprocessed identity against e2c7d97d; `KL_aecp_notify.sv` slot decode; `gen_ucode.py` E_GCTRS/E_GCTRSNS against 06; bound-view RTL against 05 A8/A9 | R443-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |
| Robustness | CLEAN | K17 timing and positive control; `mutant_pool` (job clamp, private copies, cancellation, ordered results); the `.gitattributes` scope and its negative control; redundancy seam unchanged | R443-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |
| Tests | CLEAN | `counters_phases.hpp` K17; `ctr_mutants.py`; four new patches; `tb/pp_top` suite re-run (9,196/0); campaign at `--jobs 1` and `--jobs 8` (17/17, byte-identical, per-arm counts equal to the README) | R443-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |
| Docs | CLEAN | 00, 01, 02, 03, 05, 06, 09, 10, `docs/README.md`, `docs/guides/README.md`, integrator guide, `tb/pp_top` README/Makefile; `make check`; anchors; PR body Round 2 section against tree and runs; S2 recorded | R443-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |

## Real limits

- **Manager bank receipts not found in public evidence.** The assigned evidence commit `c0212c4d` holds round-1 author material only. The author-r2 archive `05cfbac1` adds the author's round-2 packet and the round-1 reviews. Neither carries the manager's static/builder or native bank receipts for `81edaaa`, and no manager evidence comment for this head was found on #79 or #147. This review therefore relies on its own focused runs and does not confirm the manager's bank results.
- **Not run here, per scope:**
  - the full processor sweep (`run_suites.sh`) and full `lint_hdl.sh`;
  - the other mutation campaigns;
  - out-of-context synthesis (not needed: the preprocessed source is identical);
  - the parent donor bank and consumer set;
  - the hosted/act jobs.
- **Resource note:** the `--jobs 8` campaign's eight concurrent builds briefly peaked near the 12 GB unit cap (no OOM event). It was therefore run alone, before the `--jobs 1` run and the suite.
- **The S1 zero-identity case is untested:** whether the parent's gPTP publisher ever drives a zero identity at runtime was not established.
- **No hardware claim:** physical calibration NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Run the donor bank (9) and the parent consumer set (16) at milan-fpga dev `1269cdaf` (which carries c4c6) with `parent-adoption-c8`, and publish the bank receipts for `81edaaa`.
- Build the final current-dev candidate at the merge turn (source base `c74711d4`, live dev `1269cdaf`), and own hosted/act acceptance.
- Correct the manager-side citation "Table 7-112" (assignment 5963890173 and ruling 5963704232) to IEEE 1722.1-2021 Tables 7-152/7-153 in any carried record. This is not a defect in the tree.
- S1 and S2 are optional and can be carried to #69 or a docs pass.

R443-2 FINISHED
