[R810] POSITIVE - exact head 794f8442c3d9da158c99d358d825c7b277516bba

# R810-1: external independent review of processor issue #217 / PR #219

**Scope**
- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #219, issue #217 (parent kebag-logic/milan-fpga#858).
- Exact head `794f8442c3d9da158c99d358d825c7b277516bba`, tree `9b60c7bbf6b35e34c4c1c2aae306d7477d1eda5d`.
- Source base `044cb25f`. The current-dev merge candidate (live dev `123f57a922bf07476cd69f91867f3b6f07080804`) is the manager's to build. It was not built or inferred here.
- No manager source bank ran at this head, and none is claimed.

**Review clone**
- Detached at the head.
- After every run and probe, all 830 tracked blobs match the head in bytes and mode. The index tree is `9b60c7bb…`. `git status --ignored` is empty, because the ignored caches the runs created were removed (`receipts/restore/restore_check.txt`).
- This repository has 0 gitlinks, so there is no submodule pin to check.

**Reading order**
1. The repository has no AGENTS.md or CONTRIBUTING.md, so I started with README.md and docs/README.md.
2. Issue #217's body and its two comments. Parent #858's body and its one comment.
3. REQ-ADP-011, 04 §5 and 06 §6.1.
4. `git diff 044cb25f..794f844` and its 5 commits.
5. The published evidence at kebag-logic/milan-fpga `ea450d8d…/review-evidence/pp217-r1`, read from a sparse clone.

**Clause text** was read from the IEEE 1722.1-2021 and Milan v1.2 PDFs, with text extracted locally:
- 6.2.2.15
- 6.2.3.1.2
- 6.2.4 and 6.2.5
- Table 7-2
- 7.5.2
- Milan v1.2 5.6.3

**Order of my verdict and the prior review**
- My own verdict and ledger were written at 19:39:09 UTC, before I read any other reviewer's report (`receipts/verdict_before_prior_findings.md`, sha256 `08231f13…`).
- The prior review R809-1, posted during this round, and the manager's ruling on it were read only after that. Their findings are resolved or retained in the section on prior findings below.

**Tools**
- Simulator: Verilator 5.050 (`verilator_bin` sha256 `44898b22…`).
- Synthesis: Yosys 0.66 with sv2v v0.0.13 (`receipts/verilator_identity.txt`).

## Verdict basis

**The change is correct against the clauses.**
- At the head, READ_DESCRIPTOR(ENTITY) octets 36..39 carry the available_index of the last ENTITY_AVAILABLE handed to TX on the commanded interface:
  - 0 before any advertisement and after the first;
  - N-1 after N;
  - 0 after ENTITY_DEPARTING;
  - then 0 and 1 after re-enable.
- Every other octet is the image's.
- The AEM image, `hdl/srp`, ADP's wire logic, and the top's ports and parameters are unchanged.
- The new path is single-clock.

**The tests.**
- Every acceptance arm and both re-anchored arms are KILLED on behaviour, and I re-ran each one at the head.
- The base reproduction gives exactly the 4 failures the PR claims.

**The prior review's findings.**
- R809's MAJOR finding F-1 does not hold: the evidence commit is complete, 541 of 541 manifest files with matching sha256.
- Its MINOR finding F-2 is fixed in the live PR body.
- What remains is two RESIDUE wording items and two SUGGESTIONs. None of them leaves a lens unclean.

## 1. The served value per interface (Conformance, RTL)

**Clause.**
- IEEE 1722.1-2021 Table 7-2 puts available_index at ENTITY offset 36, 4 octets: "This is the same as the available_index field in ATDECC Discovery Protocol. See 6.2.2.15."
- 6.2.2.15: "incremented after transmitting an ENTITY_AVAILABLE message and is reset to zero (0) when transmitting an ENTITY_DEPARTING or after a power cycle."
- Milan v1.2 5.6.3: "an independent instance of the Advertise state machine … for each AVB Interface". IEEE 6.2.3.1.2/6.2.5.2.1 keep one entity-wide `entityInfo`. The design's per-interface counter (`aidx_r[N_IF_P]`) predates this PR and follows Milan, which prevails (Milan §5.5.2.1).
- Serving the commanded interface's value is a reasoned choice, documented in 04 §5 and 06 §6.1. At one interface, the shipping shape, the two readings coincide.

**ADP.**
- `hdl/adp/KL_adp_engine.sv:977-987` loads `last_aidx_r[if]` from `bld_aidx_r` on `bld_done_avail_w`, which is `B_REQ`, the cycle the frame goes to `txreq_valid_o`.
- `bld_aidx_r` is the value the builder wrote at wire bytes 50..53 (`:914`, `:953-955`).
- The single builder is the only writer of `aidx_r` between B_SAMPLE and B_REQ, so the sample is the wire value.
- The register clears on `bld_done_dep_w` and on reset.
- `aidx_r`, the next frame's index, is untouched (`:717-730`).

**Top.**
- `hdl/top/protocol_processor_top.sv:4154-4160` selects `adp_last_aidx_w[32*aecp_cmd_if_r +: 32]`.
- `aecp_cmd_if_r` latches on `aecp_txn_valid_w && aecp_sb_grant_w && aecp_eng_ready_w` (`:4139-4146`). That is the handshake that loads the engine's `cmd_r`, so the latch holds for the whole program.
- With one interface, or an index past the last, interface 0's value is served. `N_AVB_IF_P` is guarded to 1..2 (`:913`).

**Executed at the head** (`receipts/proc/pp_top_ai_if.log`):
- pp_top section AI: 16 checks, 0 failures.
  - Reads before any ADPDU, after each of 4 byte-exact ENTITY_AVAILABLE on ADP's own cadence, after the ENTITY_DEPARTING (which carries 4), and after re-enable (0 then 1).
  - Every response is compared whole.
- pp_top IF, two interfaces: 8 checks, 0 failures. IF4 runs interface 1's index ahead and reads once on each interface.

**Base reproduction.**
- Base `hdl/` (blob-identical to 044cb25f) with the head's benches gives "AI: 16 checks, 4 failures": AI2 at 1, 2, 3 and AI4 at 1, all reading 0 (`receipts/repro-base/ai_at_base.log`).
- In every failing response the only differing wire byte is 81, which is descriptor octet 39 (`receipts/repro-base/base_dump_diff.txt`).

## 2. Other octets, the AEM image, ADP timing (Conformance, RTL)

- `git diff 044cb25f HEAD -- hdl/aecp/desc hdl/srp` is empty.
- Because AI's comparisons are whole-frame, a correct AI pass, together with the base diff confined to octets 36..39, shows that every other octet is the image's.
- The other ENTITY-read checks still compare whole frames: A1, A10, N5b, M7, B4, B4b, B7, B11, K7, U7 and G8. Each takes octet 36 from the bench's wire capture (`tb/pp_top/sim_main.cpp:1744-1745`, `H::served_entity`), never from the processor.
- **E_RDESCENT** (`hdl/aecp/ucode/gen_ucode.py:798-830`):
  - Both `current_configuration` paths reach the new `GATHER_EXT`. The dynamic path's `BRANCH` targets +17, and an assert holds that target (`:830`).
  - The noncanonical-length fallback to `E_RDESC` is kept.
  - `E_RDESC` and `E_RDSTUB` contain no gather, so a set `rdent_r` cannot misroute one.
  - `TAIL` copies 270 of the 310 bytes from offset 40.
- **ADP timing is unchanged by construction.** `KL_adp_engine.sv` is +31/-0, and the new register's only reader is `last_avail_index_o` (`:1120-1123`). In the top, its only consumer is the AECP gather mux, and AECP does not feed ADP.
- tb/adp_engine's existing cadence and byte-exact checks pass with unchanged expectations: 1,354 + 11 checks (`receipts/proc/adp_engine_suite.log`).
- The author's twin (section 6) shows the fabric's 195 frames identical in time and bytes, except the one READ_DESCRIPTOR(ENTITY) response at wire byte 81.

## 3. Arms: planted, killed, behavioural (Tests)

Run at the head, each campaign with its controls:

| Arm | Campaign | Required check | Result |
|---|---|---|---|
| `ai-entity-image-copy` | aecp_dispatch `--only` | AI2 … carries available_index 1 | KILLED, 4 failures |
| `ai-gather-constant` | aecp_dispatch `--only` | the same | KILLED, 4 |
| `rdc-base-no-overlay` (re-anchored) | aecp_dispatch `--only` | RDC1 … byte-exact | KILLED, 8 (README records 8) |
| `last-index-is-next` | adp_engine, full | P2 last … available_index | KILLED, 5 |
| `last-index-is-next-top` | adp_engine, full | AI2 … carries available_index 0 | KILLED, 6 |
| `last-index-kept-after-departing` | adp_engine, full | P7 … 0 after DEPARTING | KILLED, 1 |
| `last-index-kept-after-departing-top` | adp_engine, full | AI3 … after ENTITY_DEPARTING | KILLED, 1 |
| `if-top-aidx-interface-0` | adp_engine, full | IF4 … on each interface | KILLED, 1 |
| `store-link-detector-resets-up` (re-anchored) | ctr `--only` | K9 … byte-exact | KILLED, 11 (README records 11) |

**Campaign totals.**
- tb/adp_engine: 6 controls PASS and 62 of 62 arms KILLED ("68 checks: 68 PASS") (`receipts/proc/adp_mutants.log`).
- The README's changed counts match exactly: `gate-enable-dropped` 31, `walk-departing-keeps-index` 7, `if-top-count-collapsed` 4, `if-top-ingress-collapsed` 5, `if-top-ingress-live` 4.
- Dispatch: the controls `aecp-dispatch` and `avail-index` PASS (`receipts/proc/aecp_dispatch_focus.log`).
- ctr: the control `counters` PASSes (`receipts/proc/ctr_focus.log`).

**Re-anchoring.**
- I applied the base and head `rdc-base-no-overlay` patches to their own engines. The effective edit is the same at both: the READ_DESCRIPTOR(CONTROL) re-dispatch block is removed and the ENTITY block is kept, at the head including `rdent_r`.
- `store-link-detector-resets-up` removes and inserts the same lines as at base. Only its context moved, past the new `adp_last_aidx` reset line.

**The arms test behaviour, not a constant.**
- The expectations come from the clause offsets and the captured wire frames (`own_avail(k)`, `last_index_on(ifx)`).
- The constant arms fail only where the expected index is nonzero. The next-index arms fail at every read. The departing arm fails only at AI3.

**Reviewer probes** (`probes/`, `receipts/probes/`):

| Probe | Plants | Result |
|---|---|---|
| `aidx-byteswap` | the gather serves the index byte-reversed | KILLED, AI 4 failures (reads 16777216 for 1) |
| `rdent-sticky` | `rdent_r` not cleared at command load | KILLED by the default build: 32 failures, K1 to K4b and following; GET_COUNTERS then reads ADP's index |
| `gather-low-byte` | the gather serves only the index's low byte | survives AI, 16/16, because no bench index exceeds 4 (S-1) |

## 4. Clock domains and the top's interface (RTL, Robustness)

- `u_adp` and `u_aecp` both take the top's single `clk_i`/`rst_n` (`protocol_processor_top.sv:2059-2061`, `:3937-3939`). The top has one clock input (`:254`).
- The new path runs from ADP flops, through a combinational select, into AECP's registered gather answer `gxr_data_r` (`KL_aecp_engine.sv:2459-2484`). It is one domain, so there is no CDC.
- The gather answers at once, because `rdent_r` is in `gx_alt_w` (`:2265-2266`), so `ctr_req_o` is not raised. No new hold term was added.
- The `module protocol_processor_top … );` header, 756 lines with every parameter and port, is byte-identical between base and head (sha256 `7c29c974…` both). All four hunks in the top sit after it.
- Every instantiation of the two engines is updated: the top, `tb/aecp_cmds/aecp_cmds_wrap.sv` (tied 0), and `tb/adp_engine/tb_adp_top.sv`.
- `scripts/lint_hdl.sh` (zero tolerance) is rc 0 (`receipts/proc/docs_lint.log`). The `if-guards` lint at `N_AVB_IF_P` 1 and 2 passes inside the full pp_top run.

## 5. Area (Conformance of claims, Docs)

**Engines alone**, sv2v plus `synth_xilinx -family xc7 -flatten` re-run here at base and head (`scripts/engine_area.sh`, `receipts/area/`). The results equal the author's receipts exactly:

| Run | FF | LUT1-6 | MUXF7/8 |
|---|---|---|---|
| KL_adp_engine | 513 → 545 (+32) | 1470 → 1619 (+149) | 396 → 412 |
| KL_aecp_engine | 4662 → 4663 (+1) | 10019 → 10256 (+237) | 2598 → 2693 |

- The ucode inputs hash `49a993be…` at base and `264fbb03…` at head. These equal `tb/aecp_cmds/decode.json`'s recorded digests and the author's area inputs.
- The +33 FF at the top, the 32-bit last index at one interface plus `rdent_r`, is stated and attributed correctly.
- The top runs at 2x2 and 8x8 (LUT -74/+442, MUXF7/8 +53/+291, RAM and CARRY4 unchanged) are the author's receipts. A full top synthesis was not re-run here.
- The LUT and MUXF movement is stated but not attributed (R-2, residue).

## 6. Parent consumer gates and the twin (Tests)

These are the author's published receipts at `ea450d8d`. My census found every MANIFEST entry present with its published sha256 (`receipts/evidence_census.txt`).
- **Pin.** The scratch parent is milan-fpga dev `ac0a01e3` plus local, unpushed pin and ROM-digest commits, with gitlink `794f8442…`. `rom_digests` reports "recorded ROM content digests for protocol-processor pin 794f8442c3d9…".
- **Gates, all rc 0:**
  - `milan_dp`, plus the five benches that build the processor inside the datapath: `pp_shadow` (317 checks), `nvm_cosim` (465, with 39 of 39 mutants), `milan_dp_mclk` (34), `capture_coherence` (42), `milan_dp_render` (5).
  - Firmware `test_ctrl_firmware` shards 0 to 3, each with `--self-test` (shard 1: "mutants: 523 of 523 caught").
  - `fw_ctrl_nvm`, `fw_boundary`, `fw_verilator`, `fw_coverage`, `lint_rtl`, `behave` (508 scenarios), `publication_census`, `yosys_elaborate`, and the CI-scope gates.
  - Every one started after the head commit's time (07:07 UTC).
- **The twin.**
  - Base: 3 findings, all from the all-fabric MVRP.
  - Head: the same 3, plus "[DIFF] owed row entity-available-index: the difference has gone", with rc 2 at both.
  - At base, the `entity-available-index` row is an `[OWED]` note. At head it is gone from the notes.
  - `capture_diff.txt`: the fabric's 195 frames are identical except frame 59, wire byte 81 (octets 36..39, 0 → 1). The split's 260 frames are unchanged.
- **The author's explanation of rc 2 holds.** By the twin's design a vanished owed row is a finding, so that the lane taking the pin deletes the row. The only new finding is that vanished row.
- The twin samples the descriptor once, after an index of 1. DEPARTING and re-enable are covered by the processor's section AI.
- I did not run parent or twin gates (not allowed). This is author evidence. Issue acceptance bullet 4 rests on it, and the manager validates the merge candidate.

**Author's process notes.** None of these is a defect of the change, and none is RESIDUE, because none is a wording error in the PR text:
- **Memory excursion.** Anonymous memory reached 14.4 GB for about 3 minutes: no OOM, no process killed, gates rc 0.
- **Serial sweep.** The processor has no shard runner, so the sweep ran serially.
- **Piped gates.** Two gates first run through a pipe were re-run unpiped (`run_suites` at 16:52 to 17:24 UTC, then `check_req_tags_exec`), with the piped records kept apart. This is the correct handling.

## 7. Docs match the code (Docs)

**04 §5** (`docs/architecture/04_adp_engine.md:135-144`) states:
- the 32-bit last index;
- "the wire field of each ENTITY_AVAILABLE on the cycle it is handed to TX";
- 0 from reset and from DEPARTING;
- per-interface publication, with the top serving the command's interface.

All of this matches `KL_adp_engine.sv:964-987` and `protocol_processor_top.sv:4154-4160`.

**06 §6.1** (`06_aecp_engine.md:318-330`, `:602-605`) states selector 0xE0, routing by `rdent_r`, octets 0..35 / 36 / 40..309, and the AI/IF4 coverage. All of this matches `gen_ucode.py:798-830` and `KL_aecp_engine.sv:2265-2266`, `:2481`. The one inaccurate phrase is the comparison with 0xD0 (R-1).

**REQ-ADP-011** (`docs/00_MILAN_COMPLIANCE_REVIEW.md:399`) adds Table 7-2 and 06 §6.1.

**The suite READMEs.**
- tb/adp_engine's README: the arm table matches every count measured here.
- tb/pp_top's README, section AI and IF4: the base failure counts match my reproduction. AI runs after RBT in the default build (`sim_main.cpp:16317-16318`).

**Gates.** `make check` is rc 0, covering lint, wavedrom-check, links, matrix, reqtags with selftest, modmatrix, params, aecpcmd, ids, figures and stale. `gen_matrix.py --check` and `git diff --check 044cb25f HEAD` are rc 0 too.

**Comment rule.** I scanned every added source line under `hdl/` and `tb/`, excluding Markdown and JSON, for lane labels, lane names, review rounds, reviewer IDs and comment IDs. There are 0 hits. The comments state behaviour and reason, with issue #217 and clause IDs. Section and check IDs (AI1, IF4, P7) are suite check names. "lane" in `gen_ucode.py` means an 8-byte memory lane.

**Clause numbers in the review brief.** The brief also cites 6.2.1.18 and 7.5.2.1.
- In the 2021 text, 6.2.1 is an Overview with no subclause 18, and there is no 7.5.2.1. 7.5.2, Unsolicited Notifications, lists only commands, so no notification is owed when available_index advances.
- In the 2013 text, 6.2.1.18 is gptp_domain_number.
- So the governing clauses are 2021 6.2.2.15 and Table 7-2, and those are what the change and its docs cite.

## Findings

### R-1 RESIDUE (Docs): the comparison with START/STOP's 0xD0 routing is inaccurate
*Raised by R809-1 and confirmed independently here.*
- **Artifact:**
  - `hdl/aecp/ucode/gen_ucode.py:387-388`: "so the selector names the face for the reader alone, as 0xD names the started bit's".
  - `docs/architecture/06_aecp_engine.md:322-323`: "routed by the engine's `rdent_r` the way the started bit's 0xD0 is routed by START/STOP".
- **Evidence:** `KL_aecp_engine.sv:2261` routes START/STOP's gather by the command flag and the selector's high nibble (`gx_sel_w[7:4] == 4'hD`). The 0xE0 gather is routed by `rdent_r` alone (`:2265-2266`, `:2481`).
- **Impact:** wording only. No digest hashes `gen_ucode.py`, and the ROM is independent of comment text.
- **Exact fix:**
  - In gen_ucode.py: "The engine routes the gather by command alone (its rdent_r), so the selector 0xE0 names the face for the reader only; START/STOP's 0xD is also decoded by the engine (strm_state_w)."
  - In 06: "(`GATHER_EXT`, selector 0xE0, routed by the engine's `rdent_r` alone, where START/STOP's started bit 0xD0 is routed by the command flag and the selector's high nibble)".
- **Verification:** reading the two lines against `KL_aecp_engine.sv:2261`, `:2265`.

### R-2 RESIDUE (Docs, PR body only): the area paragraph attributes the flip-flops but not the LUT and MUXF deltas
*Raised by R809-1 and found independently here (my RES-1).*
- **Artifact:** the PR #219 body, the sentence after the area table.
- **Evidence:** the engine-only runs here (`receipts/area/*/SUMMARY.txt`) give +149 LUT (ADP) and +237 LUT (AECP). The author's top runs give -74 (2x2) and +442 (8x8) LUT, and MUXF7/8 +53/+291. Only the 33 FF are explained.
- **Exact fix:** append "The engines alone grow by 149 LUTs (KL_adp_engine) and 237 LUTs (KL_aecp_engine); the flattened top re-optimizes across them, so its net LUT change is -74 at 2x2 and +442 at 8x8, and MUXF7/8 +53 and +291."
- **Verification:** the PR body text.

### S-1 SUGGESTION (Tests): pin the index's upper octets
- **Evidence:** the probe `gather-low-byte` (`probes/probe-gather-low-byte.patch`) serves only bits 7..0 and passes AI 16/16 (`receipts/probes/probe-gather-low-byte.log`), because AI and IF4 never exceed index 4.
- **Impact:** the behaviour is correct by construction: a 32-bit register, a 32-bit gather lane and a 4-octet `BUILD_FLD FMT_D`. The byte order is pinned, because `aidx-byteswap` is KILLED.
- **Suggestion:** a check with an index of 256 or more would pin the upper octets. For example, drive `adp_avail_index_i` in `tb/aecp_cmds/aecp_cmds_wrap.sv` (now tied to 0) with a nonzero upper byte, or use an engine-level bench.

### S-2 SUGGESTION (Tests): pin the per-interface clear on DEPARTING
*Raised by R809-1 as S-1, and retained.*
- **Evidence:** R809's probe `departing-clears-all` survives tb/adp_engine `interfaces`.
- **Reachability:** DEPARTING comes only from the global disable, and goes to every non-DOWN interface in the same burst. So the fault is visible only where an interface was DOWN at disable and later serves a READ_DESCRIPTOR(ENTITY) before its next advertisement. That reachability is marginal.
- **Suggestion:** an IF9 sample of `last_avail_index_o` between the two DEPARTINGs, or with one interface DOWN at disable, would pin it.

No MINOR, MAJOR or BLOCKER finding is open.

## Prior public review findings on this PR, resolved or retained at this head

| ID | Severity | State at 794f844 | Basis |
|---|---|---|---|
| R809-1 F-1 | MAJOR | RESOLVED: refuted | The evidence commit `ea450d8d` holds 542 blobs under `review-evidence/pp217-r1` (`git ls-tree`). All 541 MANIFEST entries are present, with `published_sha256` matching, and 0 missing (`scripts/evidence_census.py`, `receipts/evidence_census.txt`). F-1's named files (`pp_shadow`, `nvm_cosim`, `milan_dp_render`, `publication_census`, `yosys_elaborate`, `rom_digests`, `twin/head` against `twin/base`) are present and were read in section 6, each rc 0, with the twin as described. This agrees with the manager's ruling (issuecomment-6749487294). |
| R809-1 F-2 | MINOR | RESOLVED | The live PR body now reads "1,032,052 checks, 0 failing (36 suites)". The author's `proc/run_suites.log` has 36 `PASS ` lines and "suites: 1032052 checks total, 0 failing". The head is unchanged (`794f844`). |
| R809-1 R-1 | RESIDUE | RETAINED as R-1 | Confirmed against `KL_aecp_engine.sv:2261`, `:2265`. |
| R809-1 R-2 | RESIDUE | RETAINED as R-2 | The same defect as my own RES-1. |
| R809-1 S-1 | SUGGESTION | RETAINED as S-2 | Reachability refined above. |

## Processor gates run by this reviewer at the exact head

Each gate ran in a `git archive` copy of the head or in the clone, with its own `.cmd/.start/.log/.rc/.end` receipts:

| Gate | Result | Receipt |
|---|---|---|
| `make check`, `scripts/lint_hdl.sh`, `scripts/gen_matrix.py --check`, `git diff --check 044cb25f HEAD` | rc 0 each | `proc/docs_lint.*` |
| `tb/pp_top` `make run`, all seven builds | rc 0, "11082 checks: 11082 PASS, 0 FAIL" | `proc/pp_top_full.*` |
| `tb/pp_top` `make avail-index`, `make interfaces` | rc 0. AI 16/0, IF 8/0 | `proc/pp_top_ai_if.*` |
| `tb/adp_engine` `make` | rc 0, 1365 PASS | `proc/adp_engine_suite.*` |
| `tb/aecp_cmds` `make` | rc 0, 181 PASS (617,956 trials) | `proc/aecp_cmds_suite.*` |
| `tb/adp_engine/mutants.py --jobs 4` | rc 0, 68 of 68 | `proc/adp_mutants.*` |
| `tb/pp_top/aecp_dispatch_mutants.py --only ai-entity-image-copy,ai-gather-constant,rdc-base-no-overlay` | rc 0, 5 of 5 | `proc/aecp_dispatch_focus.*` |
| `tb/pp_top/ctr_mutants.py --only store-link-detector-resets-up` | rc 0, 2 of 2 | `proc/ctr_focus.*` |
| Base reproduction: base `hdl/`, head benches, `make avail-index` | rc 2, AI 16 checks, 4 failures, as claimed | `repro-base/` |
| Engine-only area, base and head | rc 0, equal to the author's figures | `area/` |
| Reviewer probes, 3 | 2 KILLED, 1 survives (S-1) | `probes/` |

**Hosted, read only, exact head.** `docs-gates` and `portability` completed with success in both the push and the pull_request context. Both `suites` contexts were still `in_progress` when read. Those were not counted as executed evidence.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 1722.1-2021 6.2.2.15, 6.2.3.1.2, 6.2.4/6.2.5, Table 7-2, 7.5.2 and Milan v1.2 5.6.3 (PDF text) against `KL_adp_engine.sv:964-987`, `protocol_processor_top.sv:4139-4160`, `gen_ucode.py:798-830`; section AI and IF4 executed; base reproduction with failures confined to octets 36..39; issue acceptance bullets 1 to 3 | R810-1 | 794f8442c3d9da158c99d358d825c7b277516bba |
| RTL | CLEAN | the full `hdl/` delta (4 files, +103/-9); one clock and reset; top header byte-identical; every engine instantiation; `rdent_r` set and clear sites; gather timing; ROM +17 assert; lint rc 0; engine-only area re-synthesized | R810-1 | 794f8442c3d9da158c99d358d825c7b277516bba |
| Robustness | CLEAN | probes for a sticky flag (KILLED), byte order (KILLED) and low byte (S-1); noncanonical-length fallback; out-of-range interface guard; `N_AVB_IF_P` guard; re-enable and DEPARTING paths | R810-1 | 794f8442c3d9da158c99d358d825c7b277516bba |
| Tests | CLEAN | AI and IF4 benches; ADP P2/P3/P7/IF4/IF9; 9 arm rows re-run (4 campaigns with controls); re-anchored patches compared at base and head; full pp_top (11,082), adp_engine (1,365), aecp_cmds (181); evidence census 541/541; parent and twin receipts read; S-1, S-2 | R810-1 | 794f8442c3d9da158c99d358d825c7b277516bba |
| Docs | CLEAN | 04 §5, 06 §6.1/§6.4, REQ-ADP-011, both suite READMEs, the PR body (live), `make check`, comment-rule scan of the source delta; R-1 and R-2 RESIDUE | R810-1 | 794f8442c3d9da158c99d358d825c7b277516bba |

## Real limits

- **Not run here** (allowed scope or wall time), with the author's rc-0 receipts standing as the source-head evidence:
  - `scripts/run_suites.sh` as one sweep. The suites the delta touches were run individually: pp_top, adp_engine, aecp_cmds.
  - The executed half of `check-req-tags.py` on my own sweep. The static half ran in `make check`.
  - The full aecp_dispatch campaign: 3 of its 102 arms were re-run, plus its controls.
  - `aecp-mutants`; the ACMP, D3, GSI, notification and name-write campaigns; `tb/maap` and `tb/srp_top` mutants.
  - Top-level synthesis at 2x2 and 8x8, `syn/yosys/run.sh`, and `tb/elab_guards`.
- **My sv2v is v0.0.13, the author's v0.0.12.** The engine-only figures still matched exactly.
- **Not run, and not allowed:** parent consumer gates, the twin, builder or native banks, Docker/act, and host act_ci. No manager source bank ran at this head, and none is claimed or inferred.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. Parent #858's "grade it at the bench against the reference device" is outside this review.
- **Resources:** unit memory peaked at 9.89 GB, under the 12 GiB cap, and no Vivado run took place.
- **Path redaction:** host paths in published receipts are written as `$PACKET`, `$CLONE`, `$HOME`, `$VROOT` and `$PINNED_VERILATOR`. The full Yosys logs are not published; their sha256 and last 40 lines are.

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn (source base 044cb25f, live dev 123f57a9) with the builder and native banks, and link those receipts on the PR.
- Take the hosted `suites` conclusion for this head; it was in progress when read.
- Carry R-1 and R-2 to the residue checklist. S-1 and S-2 are optional.
- When milan-fpga takes this pin: delete the twin's `entity-available-index` owed row, as the twin's design requires, and re-record the ROM digests.
- Merge still needs two independent positive reviews and the full completion bar.

R810-1 FINISHED
