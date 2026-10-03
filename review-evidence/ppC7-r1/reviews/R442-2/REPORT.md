[R442] NEGATIVE - exact head 81edaaa74f688081ad34c1e2f392612f46eb558c

# R442-2 internal independent review: issue #79 / PR #147 (lane C7, counters), round 2

- Exact head `81edaaa74f688081ad34c1e2f392612f46eb558c`, tree `39b33c89e8305384affb5d49ca73ff1ab6d92670`. Verified in the review clone before and after the probes (`receipts/clone_integrity.txt`).
- Round delta reviewed: `e2c7d97d..81edaaa`, nine commits (459f2fd, 9078094, 5599879, 52bf47b, d3f9e0f, e27c070, a34c505, 274b424, 81edaaa), 23 files. I also re-read the whole PR diff `c74711d45a8bbc0d6b38cb49211b26a4a6413e88..81edaaa` (45 files) for anything the round left inconsistent.
- Authorities used:
  - The acceptance lists of #79, #44 and #78.
  - The owner decision of 2026-09-19 (#79 comment 5740180166).
  - The lane assignment (#79 comment 5962255629) and the GPTP_GM_CHANGED ruling (5963704232).
  - The round-2 assignment (5963890173) and its addendum (5963896239).
  - The printed IEEE 1722.1-2021: §7.4.42.2, Tables 7-150 to 7-159, and Table 7-112 to check the citation correction.
  - The printed Milan v1.2: §5.3.6.3, §5.3.8.10, §5.3.11.2, §5.4.2.25, and Tables 5.1, 5.6, 5.7 and 5.13 to 5.17.
  - The reference parent's counter at milan-fpga dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`, read only.
- Public evidence read:
  - milan-fpga `c0212c4d`: the round-1 author archive.
  - milan-fpga `05cfbac1`: `review-evidence/ppC7-r1/author-r2`, the round-2 author packet. Its PR-BODY.md equals the live PR body (`receipts/public_evidence.txt`).
  - The hosted check runs at the exact head (`receipts/hosted_check_runs.txt`).

## Verdict

**NEGATIVE.** One MINOR stays open: R442-2-F1.

Everything else the round promised holds at this head, and I re-executed it:
- **GPTP_GM_CHANGED.** The rule is now the exact identity comparison. It agrees with IEEE Tables 7-152/7-153, Milan Table 5.1, K11, the harness store and the parent's counter.
- **Removed ops in text.** The five locations my round-1 F2 named are fixed. No removed adapter op or event name remains in any Markdown or Mermaid source.
- **RTL.** The two changed files are comment-only. Their preprocessed source is byte-identical to `e2c7d97d`.
- **GET_COUNTERS paragraph.** It matches `gen_ucode.py`: a 17-µop hit path, an 11-µop miss arm and a 2-µop `E_GCTRSNS`.
- **Mutation campaign.** `ctr_mutants.py --jobs 1` and `--jobs 8` gave byte-identical records (sha256 `0fd23cc6…`, the author's value). Both had control PASS and 17 of 17 arms KILLED, with per-arm counts equal to the README.
- **K17.** It grades the notify slot decode, and two extra reviewer probes were killed.
- **STREAM_INPUT quadlets 6 and 7.** They are correct.
- **Whitespace.** `git diff --check` against main gives rc 0.

The defect is in the draw.io figures of 01 and 03. The round-2 assignment (item 2) asked for those documents to be corrected "figures and tables included, so that nothing names a removed op or event". F01.2 and F03.1 still draw an in-processor counters block and the gPTP, AVTP and media-clock adapters. A figure is not wording, so this cannot be RESIDUE.

My round-1 searches covered Markdown and Mermaid sources, not the draw.io exports. I missed these figures in round 1, which is why my round-1 F2 did not list them.

## Findings

### R442-2-F1 - MINOR - Docs, Conformance - F01.2 and F03.1 (and F01.1) still draw an in-processor counter block and the removed gPTP/AVTP/media-clock adapters

- **Where:**
  - **F01.2**, "Processor top level". Embedded at `docs/architecture/01_overview.md:72-74`; source `docs/diagrams/src/01-top-level.drawio`, export `docs/diagrams/01-top-level.svg`.
    - `:63` draws a "Counters subsystem" block inside the core clock domain, fed by the AECP engine.
    - `:83`, `:86`, `:92` and `:95` draw an "External-engine adapters" group with "gPTP adapter", "AVTP adapter" and "Media-clock adapter" boxes feeding the event router.
  - **F03.1**, "Shared datapath & memory interconnect". Embedded at `docs/architecture/03_packet_engine.md:13-16`; source `docs/diagrams/src/03-shared-datapath.drawio`, export `docs/diagrams/03-shared-datapath.svg`.
    - `:65` draws "counter banks" in the state-RAM complex.
    - `:75` draws "adapter events: srp · maap · gptp · avtp · mclk" into the event router.
    - `:121` labels the router's output "to SMs / counters".
    - The note below it (`03:18-22`) excuses only the descriptor-image move, and says "the component table below is correct". That table now says the opposite: "registry (no counters …)" at `03:31`.
  - **F01.1**, "System context" (`01_overview.md:27-30`; `docs/diagrams/src/01-system-context.drawio:25`). It lists "counters" among the processor's own functions.
  - Renders: `receipts/F01.2_render.png` and `receipts/F03.1_render.png`. Labels: `receipts/stale_names.txt`, last section. None of these sources or exports changed after 2026-08-11.
- **Authority and evidence:**
  - The owner decision (2026-09-19) and #79 acceptance 3: the processor keeps no counter bank.
  - #78 and 02 §1 and §4.3 to §4.5 at this head: gPTP, AVTP and media clocking reach the processor as class-D levels and read faces, not class-B adapters.
  - The round-2 assignment item 2: "remove every removed adapter op and the in-processor counter block from 01, 05 and 06, figures and tables included".
  - The text next to these figures now denies what they draw:
    - `01_overview.md:42-46`: the external engines are reached through levels and read faces.
    - `01_overview.md:98`: "no event feeds a counter here (the counters are the integrator's)".
    - `01_overview.md:36`: "the counter banks GET_COUNTERS reports" are out of scope.
    - `03_packet_engine.md:31` and `:223-225`.
  - The PR body's Round 2 item 2 says there is "no removed op and no in-processor counter block in 01". At this head, F01.2 contradicts that.
  - The `make check` gate passes, because its `stale` step only compares the timestamps of a draw.io source and its export. No gate reads the labels.
- **Impact:** The overview's top-level figure, the first picture of the processor a reader meets, shows a counters subsystem and three adapters that do not exist. F03.1 shows counter banks in on-chip RAM. A reader of 01 and 03 is told both that the processor keeps counters behind adapters and that it keeps none. GAP-04 and GAP-05 were meant to settle exactly that.
- **Required outcome:**
  - In `01-top-level.drawio`:
    - remove the "Counters subsystem" block, or redraw it as the `ctr_*` read face to the integrator;
    - replace the gPTP/AVTP/Media-clock "adapter" boxes with the landed faces (class-D levels plus the `gsi_*`/`ctr_*` read faces), keeping SRP/MAAP as the class-B faces.
  - In `03-shared-datapath.drawio`:
    - remove the "counter banks" store;
    - relabel the "adapter events" source to the integrator's strobes and levels plus the internal engines' events;
    - relabel "to SMs / counters" to "to SMs / notifications".
  - In `01-system-context.drawio`, replace "counters" with "GET_COUNTERS reporting", as `01:9` and `01:36` now say.
  - Re-export the three SVGs.
  - If a redraw is not possible in this round, the minimum acceptable outcome is an explicit note under F01.1, F01.2 and F03.1, like F03.1's existing "predates" note. It must name the counters block and the gPTP/AVTP/media-clock adapters as superseded and point to 02 §4.3 to §4.6 and the integrator guide §7.1.
  - Then correct the PR body's Round 2 item 2.
- **Verification:**
  - `grep -o 'value="[^"]*"' docs/diagrams/src/{01-top-level,03-shared-datapath,01-system-context}.drawio | grep -iE 'counter|gptp.*adapter|avtp|media-clock.*adapter'` shows no in-processor counter block or removed adapter. Alternatively, each figure carries the superseded note.
  - `make check` rc 0, including `stale`.

### R442-2-S1 - SUGGESTION - Docs - F01.5's "Affects" cells still list "counters"

`01_overview.md:154-159`: P-N-AVB-INTERFACES ("keys registry/ADP/counters/records"), P-N-STREAM-IN, P-N-STREAM-OUT and P-N-CLOCK-DOMAINS each name "counters" as processor state that scales.

The processor scales only its GET_COUNTERS notification slots, one per stream index plus AVB_INTERFACE 0 and CLOCK_DOMAIN 0 (`KL_aecp_notify.sv:385-392`). The slots do not scale with P-N-CLOCK-DOMAINS. Suggested text: "counter-notification slots" in the stream rows, and drop "counters" from the CLOCK_DOMAIN row. This is not a round-2 regression.

## Prior findings at this head

| Finding | Original severity | Status at 81edaaa | Evidence |
|---|---|---|---|
| R442-1 F1: GPTP_GM_CHANGED rule | MINOR | **CLOSED** | See the R442-1 F1 notes below. |
| R442-1 F2: removed ops and an in-processor counter block in 01, 05 and 06 | MINOR | **All five named locations CLOSED. The finding's scope (01 and 03 figures) is RETAINED, narrowed to R442-2-F1, MINOR.** | See the R442-1 F2 notes below. |
| R442-1 S1: stale GET_COUNTERS paragraph | SUGGESTION | **CLOSED** | See the R442-1 S1 notes below. |
| R442-1 S2: `--jobs` for `ctr_mutants.py` | SUGGESTION | **CLOSED** | `tb/pp_top/ctr_mutants.py` imports `tb/common/mutant_pool.py` `add_jobs_argument`/`in_order`, and every unit runs in its own copy. `--jobs 1` and `--jobs 8` printed byte-identical records, sha256 `0fd23cc6151456beb54d51c9238ed820de4af232423cd4ec1789f6ee6c8cbdc5`, equal to the author's (`receipts/ctr_jobs1.log`, `ctr_jobs8.log`). |
| R443-1 F1: A8 `avtp.INPUT_DISABLE`, the 05 edge, the 01 node, the listener comment | MINOR | **CLOSED** for every location it named | See the R443-1 F1 notes below. |
| R443-1 F2: slot decode ungraded | SUGGESTION | **CLOSED** | See the R443-1 F2 notes below. |
| R443-1 F3: `--jobs` | SUGGESTION | **CLOSED** | Same as R442-1 S2. |
| R443-1 F4: STREAM_INPUT quadlets 6 and 7 | SUGGESTION | **CLOSED** | See the R443-1 F4 notes below. |
| R443-1 F5: watchdog parameter name | RESIDUE | **CLOSED** | `02:209-211` and `:435` both read "`DESC_MEM_TMO_CYC_P` (the engine's `MEM_TIMEOUT_CYC_P`, 06 §8.1)". |
| R443-1 F6: `LINK_UP/DOWN` consumers | RESIDUE | **CLOSED** | The `02:481` Consumers cell carries the exact text. Its relative link `11_maap_engine.md` resolves, and `make check` links pass. |

Notes on the rows above:

- **R442-1 F1.** `integrator.md:486-498` states one identity comparison:
  - count when `gm_id_i` differs from the identity in force at an update;
  - the first identity out of reset counts nothing;
  - neither strobe, nor their coincidence, identifies a GM change.

  It agrees with:
  - the table row `:466`, and F06.15 at `06:612`;
  - the harness, `sim_main.cpp:930-937`, where `gm_q` resets to GM0;
  - K11 (five changes give 5; a domain-only strobe gives nothing);
  - the parent's `pp_gm_id_edge_w`, `milan_datapath.sv:7267-7281` at `1269cdaf`, where a prior all-zero identity counts nothing;
  - Table 7-153 offset 20, "gPTP grandmaster change count", and Table 7-152 bit 26 (`0x20`). Table 7-112 is the 802.3 PON media-subtype table, so the citation correction is right (`receipts/spec_check.txt`);
  - Milan Table 5.1.

  Reviewer probe `rv-store-strobe-coincidence` makes the store count only when both strobes coincide, the rule round 1 objected to. K11 kills it with 8 failures (`receipts/probe1.summary.txt`).
- **R442-1 F2.** The five named locations are now:
  - `01:222-253` F01.3: no `ctrs` node; `faces -- "gsi / ctr read words" --> ucpu`;
  - `01:98`: the event router row;
  - `05:286-287` A8 and A9;
  - `05:106`: the edge;
  - `06:469`: the SET_CLOCK_SOURCE row ends on `aecp_clk_src_index_o`.

  The removed-op search over `docs`, `hdl`, `tb` and the root documents is clean except the honest `mc_locked` "no port" row (`receipts/stale_names.txt`).
- **R442-1 S1.** `06:1137-1154` describes the landed program. I counted the µops in `gen_ucode.py:823-863`:
  - hit path: 7 + 8 `READ_CTRS` + 2 = 17;
  - miss arm: 11;
  - `E_GCTRSNS`: 2;
  - ENTITY is refused NOT_SUPPORTED by the type gate (`KL_aecp_engine.sv:1164`, `:3340-3346`).

  `10_RESOURCE:404-407` and the top's face comment (`:366-368`) are corrected.
- **R443-1 F1.** A8 now issues only `WITHDRAW_LISTENER` and points at A9's withdrawal of the bound view. F05.1's edge goes to `srp face + acmp_bound levels`. F01.3's node names the landed faces. The listener comments at `:25`, `:184`, `:188` and `:1162` are fixed. The reviewer's own verification grep finds nothing (`receipts/stale_names.txt`). The "two figures" that finding named were the Mermaid ones; the draw.io exports are R442-2-F1.
- **R443-1 F2.**
  - K17 (`counters_phases.hpp:347-387`) strobes AVB_INTERFACE 1, CLOCK_DOMAIN 1, STREAM_INPUT 8 and STREAM_OUTPUT 8 alone. Each must stay silent for 1.5 s, measured by `any_pushes` over every object. Then a slotted strobe must still push, byte-exact.
  - The four new arms are KILLED, each by its own named K17 check and nothing else. `ctr-notify-avb-any-index` is the reviewer's earlier P3.
  - Reviewer probe `rv-notify-stri-off-by-one` (`<` becomes `<=` on the Stream Input range at `KL_aecp_notify.sv:492`) is KILLED by "K17: … STREAM_INPUT 8" (`receipts/probe2.summary.txt`).
- **R443-1 F4.** `integrator.md:456` names quadlet 6 TIMESTAMP_VALID and quadlet 7 TIMESTAMP_NOT_VALID, under `0x00000FFF` only and zero under `0x00000F3F`. The new row `:470` counts per received stream data AVTPDU with tv set or clear, as Table 7-157 defines it (offsets 24 and 28; Table 7-156 bits 25 and 24, bit values `0x40` and `0x80`). Resetting them with the input bank is the guide's own convention. Milan §5.3.8.10's reset rule covers only Table 5.6, which does not list them, so there is no spec conflict.

## Focus items

1. **GPTP_GM_CHANGED.** Closed (see the R442-1 F1 notes). The ADP comment `KL_adp_engine.sv:103-105` and the `tb/pp_top` README (`:1380`) say the same thing.
2. **No removed op or in-processor counter block remains.**
   - Markdown and Mermaid sources in 01, 03, 05, 06, `docs/guides/README.md` and `docs/README.md`: clean.
     - The remaining "adapter" hits are the real SRP/MAAP class-B faces (02 §4.1 calls `srp` an adapter).
     - The 05 `:449` hit is "the parent one-cycle block adapter" for MAAP.
   - draw.io figures: not clean. That is R442-2-F1.
   - RTL: the four listener lines and the one top line changed are comments only. The `-E -P` output of `KL_pp_acmp_listener.sv` (41,467 B, sha256 `5134a80a…`) and `protocol_processor_top.sv` (155,115 B, `dc511d2d…`) is byte-identical at `e2c7d97d` and at the head (`receipts/rtl_preprocessed_identity.txt`, script `pp_identity.sh`). These are the author's figures.
3. **GET_COUNTERS paragraph, `--jobs`, K17, quadlets 6 and 7.** Closed (see the notes above).
   - Arm-by-arm failure counts in both campaign runs: 9, 3, 18, 9, 1, 6, 8, 1, 3, 5, 8, 1, 1, 1, 1, 7, 11. They equal `tb/pp_top/README.md:1197-1213` and the PR body's table.
   - Every arm printed its named check.
   - The campaign's own tally is "18 checks: 18 PASS".
4. **Whitespace and the attributes entry.** `git diff --check c74711d4 81edaaa` gives rc 0 (`receipts/diff_check.txt`). `.gitattributes:7` carries `tb/pp_top/ctr_mutations/*.patch whitespace=-blank-at-eol,-blank-at-eof`, and `git check-attr` confirms it applies to the new patches.
5. **Nothing beyond the round changed.** Every file in `e2c7d97d..81edaaa` maps to one of the round's items:
   - the 00 GAP-05 "Verified by" cell and 09 §8.6 (K17 and fifteen arms);
   - the Makefile and `sim_main.cpp` comments (K9 to K17);
   - the 10_RESOURCE phrase (S1);
   - the README record.

   No port, parameter, register, `ctr_*` face or parent-visible signal changed.

## Commands run

All were run on disposable copies under the packet's scratch area. Each gate was launched concurrently with its own log and rc file, inside a memory-capped scope, and waited on in the foreground. The simulator was the pinned 5.050: wrapper sha256 `905795b9…`, binary `44898b22…` (`receipts/tool_identity.txt`).

| Run | Result | Receipt |
|---|---|---|
| `tb/pp_top/ctr_mutants.py --jobs 8` | rc 0: control PASS, 17 of 17 KILLED, 301 s | `receipts/ctr_jobs8.log`, `.rc` |
| `tb/pp_top/ctr_mutants.py --jobs 1` | rc 0: the same record, byte-identical, 588 s | `receipts/ctr_jobs1.log`, `.rc` |
| `make -C tb/pp_top run` (5 builds) | rc 0: **9,196** checks, 0 failing (default build 8,724, K-AVB 28) | `receipts/pp_top_suite.summary.txt`, `.rc` |
| `make check` | rc 0: 41 mermaid and 18 wavedrom blocks, 1,095 links, 115 REQ rows and 17 GAP findings, 94 module rows with 0 untested, 27 parameters | `receipts/docs_check.log`, `.rc` |
| Reviewer probe `rv-store-strobe-coincidence` (bench) | KILLED: K11 ×3 and 5 more (8 failures) | `probes/`, `receipts/probe1.summary.txt` |
| Reviewer probe `rv-notify-stri-off-by-one` (RTL) | KILLED: K17 STREAM_INPUT 8 (1 failure) | `probes/`, `receipts/probe2.summary.txt` |
| `git diff --check` against main | rc 0 | `receipts/diff_check.txt` |
| Preprocessed identity of the changed RTL | identical, 2 of 2 files | `receipts/rtl_preprocessed_identity.txt` |
| Removed-name and figure-label search | Markdown and Mermaid clean; draw.io labels as in F1 | `receipts/stale_names.txt`, `search_removed.sh` |
| Hosted check runs at the exact head (read only) | `portability` and `docs-gates` succeeded (two contexts each). `suites` was in progress when read. I claim no acceptance from them. | `receipts/hosted_check_runs.txt` |

After the probes, the clone was verified untouched at the exact head:
- HEAD and tree are exact, and `write-tree` gives `39b33c89…`.
- `git status --ignored` is empty.
- Worktree equals index, which equals HEAD.
- All 498 tracked blobs were rehashed: 0 differ and every mode is equal. The index and HEAD digests are equal.
- There are no gitlinks and no `.gitmodules`, so no submodule pins were needed.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R442-2-F1) | the integrator guide §7.1 (masks, quadlets, count, reset and the GM rule) against printed IEEE 1722.1-2021 Tables 7-152/7-153/7-156/7-157 (and 7-112) and Milan v1.2 Tables 5.1, 5.6, 5.13 and 5.16 and §5.3.8.10; the parent `milan_datapath.sv` GM edge and counter at `1269cdaf`; the GAP-04 and GAP-05 dispositions against the 01 and 03 figures | R442-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |
| RTL | CLEAN | the `KL_pp_acmp_listener.sv` and `protocol_processor_top.sv` comment diffs (preprocessed identity); the `KL_aecp_notify.sv` slot decode `:488-507`; `gen_ucode.py` E_GCTRS/E_GCTRSNS µop counts; the `KL_aecp_engine.sv` type gate | R442-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |
| Robustness | CLEAN | the unslotted-strobe rule (K17, four arms and a reviewer off-by-one probe); the identity-comparison rule against both-strobe coincidence (probe); the harness store's reset identity; the redundancy limit unchanged (one AVB_INTERFACE and one CLOCK_DOMAIN slot, recorded for #69) | R442-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |
| Tests | CLEAN | `counters_phases.hpp` K17 and `any_pushes`; the four new patches; `ctr_mutants.py` and `tb/common/mutant_pool.py`; the campaign at `--jobs 1` and `--jobs 8` (byte-identical, 17 of 17); the pp_top suite (9,196); the README record | R442-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |
| Docs | UNCLEAN (R442-2-F1) | the round's diffs of 00, 01, 02, 03, 05, 06, 09, 10_RESOURCE, `docs/README.md`, `docs/guides/README.md`, `integrator.md` and the `tb/pp_top` README; the draw.io sources and SVG exports embedded in 01 and 03; F01.5; the PR body Round 2 against the author packet; `make check` | R442-2 | 81edaaa74f688081ad34c1e2f392612f46eb558c |

## Real limits

- **Campaign timing.** I ran the two campaign runs concurrently with each other and with the pp_top suite, under one memory cap and on a host shared with other work. Their wall times (588 s and 301 s) are not comparable with the author's 940 s and 699 s; only the records are.
- **Figures.** I inspected the figures by rasterising the committed SVG exports. I did not re-export them from the draw.io sources.
- **Full sweep and lint.** I did not run the full processor sweep or `lint_hdl.sh`. The RTL is preprocessed-identical to round 1, where both were run, and the manager's banks are the source for them at this head.
- **Manager receipts.** The public evidence (`c0212c4d`, `05cfbac1`) holds the author packets and the round-1 review packets. I found no manager bank receipts for this head there or in the issue and PR comments, so I could not inspect the manager's static, builder or native results.
- **Parent.** I did not build or run the parent. Its counter was read at dev `1269cdaf` only.
- **First-identity rule.** "The first identity out of reset counts nothing" is the integrator's rule. The harness boots with `gm_q` equal to its reset identity and never strobes at boot, so no check grades a store that counts the first publish. That rule is outside what this repository's processor can hold.
- **Hosted runs.** The hosted `suites` jobs were still in progress when read.
- **Hardware.** Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Carry R442-2-F1 to the author:
  - redraw and re-export F01.2, F03.1 and F01.1, or add the superseded notes;
  - correct the PR body's Round 2 item 2;
  - optionally take S1.
- Run the donor bank (9) and the parent consumer set (16) at this head on milan-fpga dev `1269cdaf`, with `parent-adoption-c8`, and publish the receipts.
- Build the final current-dev candidate at the merge turn (source base `c74711d4`, live dev `1269cdaf`).
- Own hosted and act acceptance. `suites` was in progress at read time.

R442-2 FINISHED
