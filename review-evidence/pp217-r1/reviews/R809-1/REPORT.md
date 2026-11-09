[R809] NEGATIVE - exact head 794f8442c3d9da158c99d358d825c7b277516bba

# R809-1: independent review of processor issue #217 / PR #219

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #219 (base `main`), issue #217 (parent kebag-logic/milan-fpga#858).
- Exact head `794f8442c3d9da158c99d358d825c7b277516bba`, tree `9b60c7bbf6b35e34c4c1c2aae306d7477d1eda5d`. Source base `044cb25f`. Live dev for the merge candidate `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36` (not built here).
- Review clone: detached at the head. After every probe its tracked bytes, modes and index match the head: `git diff HEAD` and `git diff --cached HEAD` are empty, and the `git ls-files -s | sha256sum` fingerprint `d1a02687…28ee93` is the same at start and end. The processor tree has 0 gitlinks. The only stray file was an ignored `tb/common/__pycache__` left by a `--help` call; it was removed, and `git status --ignored` is now empty.
- Inputs, in this order: the repository has no AGENTS.md or CONTRIBUTING.md (checked), so docs/README.md; the issue body and its 2 comments; the PR body and its 1 comment; REQ-ADP-011 and 04 §5 / 06 §6.1; `git diff 044cb25f..794f844` and its 5 commits; then the published evidence at kebag-logic/milan-fpga `ea450d8d…` `review-evidence/pp217-r1`. Prior public review findings were read only after this reviewer's own pass: there are none (PR #219 has 0 reviews, 0 review comments, and only the review-start comment; issue #217 has only the TAKEN and REVIEW READY comments). Nothing is carried forward to resolve or retain.
- All of this reviewer's execution happened at the exact head. The simulator is Verilator 5.050 (`verilator_bin` sha256 `44898b22…`, matching CI's pinned `v5.050`). Copies were exported with `git archive` into the packet's scratch directory. Receipts are in `receipts/`, scripts in `scripts/`.

## Verdict basis in one paragraph

The change is correct. At the head, READ_DESCRIPTOR(ENTITY) carries the available_index of the last ENTITY_AVAILABLE sent on the commanded interface: 0 before any advertisement and after the first, N-1 after N, 0 after ENTITY_DEPARTING, then 0 and 1 after re-enable. Every other octet is the image's. ADP's wire logic, the AEM image, `hdl/srp` and the top's ports and parameters are unchanged. Every acceptance arm and the two re-anchored arms are KILLED on behaviour. The 36 suites pass with 1,032,052 checks.

The verdict is NEGATIVE for one reason. The published executable evidence at the named commit is missing 248 of the 541 files its own manifest lists: every exact-head processor gate receipt, the whole twin run, the base reproduction, and half of the parent consumer gates. So issue acceptance bullet 4 and the twin claim cannot be checked from public evidence (F-1, MAJOR). A misstated suite count in the PR body is F-2 (MINOR).

## What was checked, against the clauses

The clause text is the text quoted in the repository, the issue and the author's STANDARDS.txt receipt. IEEE 1722.1-2021 Table 7-2 says available_index is "the same as the available_index field in ATDECC Discovery Protocol". Per 6.2.2.15 (the repository's citation) that field is incremented after an ENTITY_AVAILABLE is transmitted and reset to zero when an ENTITY_DEPARTING is transmitted. Milan v1.2 5.6.3 runs one advertise machine per interface. The IEEE and Milan PDFs themselves were not available to this reviewer (see Limits).

### 1. The served value per interface: CLEAN

**ADP side.** `hdl/adp/KL_adp_engine.sv:977-987` adds a new register, `last_aidx_r[if]`:
- It loads `bld_aidx_r`, the builder's own sample that it writes to wire bytes 50..53 (`:914`, `:953-955`), on the cycle an ENTITY_AVAILABLE is handed to TX (`bld_done_avail_w`, `:964`).
- It clears on the cycle an ENTITY_DEPARTING is handed to TX (`:965`).
- It is 0 at reset.
- `aidx_r`, the next frame's value, is untouched (`:717-730`).

**Top side.** `hdl/top/protocol_processor_top.sv:4154-4160` serves `adp_last_aidx_w[32*aecp_cmd_if_r +: 32]`. `aecp_cmd_if_r` is the interface latched on the handshake that loads the command (`:4139-4146`), the same latch the registry port uses. An out-of-range index, or a build with one interface, gets interface 0's value.

**Executed at the head:**
- pp_top section AI (`make avail-index`, inside the dispatch campaign's control): 16 checks, 0 failures. It reads before any ADPDU, after each of four ENTITY_AVAILABLE frames (each byte-exact, on ADP's own cadence), after the ENTITY_DEPARTING (which carries 4), and after re-enable (0, then 1).
- pp_top IF4 (two interfaces): interface 1's last index is run ahead of interface 0's, then each interface's read carries its own index (IF control PASS).
- This reviewer's mirror probe `top-serves-if1` (both interfaces served interface 1's index) is KILLED by IF4: "2 on interface 0 and 3 on interface 1 … (got 3 and 3)". So the per-interface selection is pinned in both directions, not just one.

**Base reproduction.** This reviewer's own probe `base-rtl` runs the head's benches with the base's four RTL and microcode files. Section AI gives "16 checks, 4 failures": AI2 at 1, 2 and 3, and AI4 at 1, all "available_index 0". That matches the PR's reproduction.

### 2. Every other octet, the AEM image and ADP wire timing are unchanged: CLEAN

- `git diff --quiet 044cb25f HEAD -- hdl/aecp/desc hdl/srp` rc 0 (`receipts/static.log`).
- Every AI and IF4 response is compared whole, frame by frame, against the image's ENTITY descriptor with only octet 36..39 replaced. The other ENTITY-read checks (A1, A10, N5b, M7, B4, B4b, B7, B11, K7, U7, G8) still compare whole frames. Their octet-36 value comes from the bench's wire capture (`tb/pp_top/sim_main.cpp:1744-1745`), not from the processor.
- Layout probes, all KILLED by AI's whole-frame compare:
  - `aidx-offset-32`: index built at octet 32; 8 failures, 350-byte response.
  - `tail-one-lane-late`: tail copy starts at 48; 8 failures, 346-byte response.
- ADP wire timing:
  - `KL_adp_engine.sv` has +31 / -0 lines. The new register is read only by `last_avail_index_o` (`:1120-1123`). No existing statement changed, so ADP's frames and timing are unchanged by construction.
  - tb/adp_engine's cadence, arm and byte-exact checks pass at the head (1,365 checks), as do pp_top's AD sections.
- `KL_aecp_engine.sv` changes only: the new input; `rdent_r`, set only at the ENTITY re-dispatch (`:3354-3360`) and cleared at reset, at each command load and at each unsolicited load (`:2819`, `:2914`, `:3015`); `gx_alt_w`; and one arm of the gather mux (`:2481`).
- `E_RDESCENT` (`hdl/aecp/ucode/gen_ucode.py:798-830`) keeps the noncanonical-length fallback and the `current_configuration` overlay. Its `+17` branch target is held by an assert (`:830`).
- The UPC map gate and the M9 opcode gate pass (`receipts/suites.log`).

### 3. Arms are planted, killed, and test behaviour: CLEAN

| Arm (author's) | Campaign, run here | Required check | Result at head |
|---|---|---|---|
| `ai-entity-image-copy` | aecp_dispatch `--only` | AI2 … carries available_index 1 | KILLED, 4 failures |
| `ai-gather-constant` | aecp_dispatch `--only` | the same | KILLED, 4 failures |
| `rdc-base-no-overlay` (re-anchored) | aecp_dispatch `--only` | RDC1 … READ_DESCRIPTOR byte-exact | KILLED, 8 failures |
| `last-index-is-next` | adp_engine, full | P2 last … available_index | KILLED, 5 |
| `last-index-is-next-top` | adp_engine, full | AI2 … carries available_index 0 | KILLED, 6 |
| `last-index-kept-after-departing` | adp_engine, full | P7 … 0 after DEPARTING | KILLED, 1 |
| `last-index-kept-after-departing-top` | adp_engine, full | AI3 … after ENTITY_DEPARTING | KILLED, 1 |
| `if-top-aidx-interface-0` | adp_engine, full | IF4 … on each interface | KILLED, 1 |
| `store-link-detector-resets-up` (re-anchored) | ctr, `--only` and full | K9 … byte-exact | KILLED, 11 failures |

Campaign totals:
- tb/adp_engine: 6 controls PASS, 62 of 62 arms KILLED ("68 checks: 68 PASS").
- tb/pp_top `ctr_mutants.py`, full: 1 control PASS, 17 of 17 arms KILLED ("18 checks: 18 PASS"). This includes `ctr-index-from-type`, which also patches the gather mux.
- tb/aecp_cmds `make mutants`: "17 of 17 detected; golden and restored PASS". The engine digest in `decode.json` was re-recorded, and the generated `ucode.hex` digest `264fbb03…` equals the head's ROM digest in the author's area inputs.

**The re-anchored arms plant the same fault as before.**
- At base, `rdc-base-no-overlay` deleted `echo_r <= 0; end` plus the CONTROL block up to `upc_r <= UPC_RDESCCT_C`, keeping the CONTROL block's trailing `echo_r <= 0; end`. Net effect: the CONTROL re-dispatch block is removed. At head it removes exactly that block below the new `rdent_r` line. The effect is identical.
- `store-link-detector-resets-up` inserts the same `itf.link_q = true;` line, in context the new `adp_last_aidx` reset line moved.
- All 507 tracked patches apply at the head (`receipts/patch_census.txt`).
- None of the 7 pp_top campaigns names one of the edited ENTITY-read checks as an arm's required check. So the `served_entity` edits cannot have weakened a named kill.

**The arms grade behaviour, not a constant.** The constant arms fail only where the expected index is nonzero. The "next index" arms fail at every read. The DEPARTING arm fails only at AI3. Each expectation is built from the clause offsets and from the captured wire frames.

**Reviewer probes** (`scripts/probe.py`, `receipts/probe-*.log`):

| Probe | What it plants | Result |
|---|---|---|
| `last-from-live-next` | last index taken from `aidx_r + 1` | KILLED, AI 6 failures |
| `rdent-sticky` | `rdent_r` never cleared at command load | survives the `counters` and `aecp-dispatch` targets |
| `rdent-sticky-full` | the same fault, every section of the default build | KILLED, 32 failures (K1 to K4c, DL); GET_COUNTERS then reads ADP's index as its mask |
| `departing-clears-all` | one DEPARTING clears every interface's last index | survives adp_engine `interfaces`; see S-1 |

### 4. Clock domains and the top's interface: CLEAN

- `u_adp` and `u_aecp` both run on the top's single `clk_i` and `rst_n` (`protocol_processor_top.sv:2059-2061`, `:3937-3939`). The new path is a combinational mux from ADP's flops into AECP's registered gather (`gxr_data_r`), all in one domain, so no CDC.
- The `module protocol_processor_top … );` header, lines 98..853 with every parameter and port, is byte-identical between base and head (`receipts/static.log`, `top_ports rc=0`).
- `N_AVB_IF_P` is guarded to 1..2 (`:913`), so the 2-bit latch covers the range.
- `scripts/lint_hdl.sh` (zero tolerance) rc 0. The `if-guards` lint at `N_AVB_IF_P` 1 and 2 passes inside the pp_top suite.

### 5. Area: stated; FFs attributed, LUTs not (R-2)

These are the author's receipts, `area/base` and `area/head`, both rc 0, sv2v plus Yosys `synth_xilinx -flatten`. Yosys was not re-run here (Limits).

| Run | FF | LUT |
|---|---|---|
| top 2x2 | 20820 → 20853 (+33) | 42028 → 41954 (-74) |
| top 8x8 | 29891 → 29924 (+33) | 65192 → 65634 (+442) |
| KL_adp_engine | 513 → 545 (+32) | +149 |
| KL_aecp_engine | 4662 → 4663 (+1) | +237 |

- The FF attribution in the PR (32-bit last index at one interface, plus `rdent_r`) matches the per-engine deltas exactly.
- The ROM inputs hash to the `decode.json` digests (`49a993…` base, `264fbb03…` head).
- The PR states the LUT and MUXF7/8 deltas but does not attribute them (R-2).

### 6. Parent consumer gates and the twin: NOT VERIFIABLE from the publication (F-1)

**Present in the published tree**, each rc 0, all started after the head commit's time (07:07 UTC): `milan_dp`, `milan_dp_mclk`, `capture_coherence`, firmware shards 0 to 3 (AECP/ADP/SRP campaigns), `fw_ctrl_nvm`, `fw_boundary`, `fw_verilator`, `fw_coverage`, `lint_rtl`, `behave`, and the CI-scope gates. The scratch parent's diff from dev is `protocol-processor` and `syn/yosys/rom_digests.tsv`. The 43149fb→794f844 step touches only the two tb mutation patches, which the parent never builds.

**Named by the published INDEX/MANIFEST but absent:**
- `pp_shadow`, `nvm_cosim`, `milan_dp_render` (three of the five benches).
- `publication_census` and `yosys_elaborate` (rtl-fast jobs).
- The `rom_digests` record at 794f844.
- `ooc_*`, `pp_srcs`, `superseded-piped/`.
- The entire `twin/` directory.

**The twin's explanation.** It matches the twin's documented design. In the public `tb/verilator/milan_dp/twin_compare.py` at `a88772f1`, lines 21-24 say "a row whose difference has gone is a finding too, so the lane that fixes it deletes the row". Lines 89 and 484-491 hold the `entity-available-index` owed row and its "has gone" words. Lines 35-36 say the compare exits 1 on any finding (make reports 2). So a nonzero twin exit, with only this row newly vanished, is the expected result of this fix. But the receipt showing that this was the only new finding, and that the other three MVRP findings are unchanged at base, is not published.

### 7. Docs match the code: CLEAN except R-1, F-2

- 04 §5 (`docs/architecture/04_adp_engine.md:135-144`), 06 §6.1 (`06_aecp_engine.md:318-330`, and `:602-605`), REQ-ADP-011 (`00:399`), and both suite READMEs describe the RTL and benches as executed.
- The arm table in the tb/adp_engine README matches every count measured here. Examples: `gate-enable-dropped` 31, `walk-departing-keeps-index` 7, the IF arms 4/5/4, and the five new arms 5/6/1/1/1.
- 09 §8.1's dynamic-overlay table covers only controller-settable fields, so `available_index` correctly has no row.
- `make check` passes: lint, wavedrom, links, matrix, req-tags plus its selftest, modmatrix, params, aecpcmd, ids, figures, stale (`receipts/static.log`).
- The executed half of the req-tags gate, re-run here on the author's published `suites.txt` and `req-tags.txt`, reports "270 evidence lines, 14 suites, OK". The author's per-suite tallies are identical, line by line, to this reviewer's sweep.

**Comment rule.** The delta's source comments state behaviour and reason with issue and requirement IDs. "lane" occurs only in the 8-byte memory-lane sense (`gen_ucode.py:383`, `:794-797`). No lane labels, lane names, review rounds, reviewer IDs or comment IDs are added in source.

**Author's process notes.**
- The memory excursion and the serial sweep are run-environment events.
- The interrupted `fw_shard0` (`parent/interrupted-1034/`) was re-run to rc 0.
- Replacing piped gates with unpiped re-runs is the right outcome.

None is a defect of the change or needs a residue entry. The `superseded-piped/` receipts are among the missing files, so which re-runs replaced them can only be confirmed once F-1 is fixed.

## Findings

### F-1 MAJOR (Tests, Docs): the published executable evidence is incomplete against its own manifest and indices

- **Artifact:** kebag-logic/milan-fpga `ea450d8d30779e24e9dc8588957623e57dbccf48` (head of `pp217-review-evidence`), `review-evidence/pp217-r1/`.
  - `MANIFEST.json` lists 541 files; the tree holds 293 blobs. The 248 absent: `author/receipts/proc/` 142, `author/receipts/parent/` 54, `author/receipts/twin/` 30, `author/receipts/repro-base/` 6, `author/tools/` 16.
  - The INDEX.md files name 52 entries the tree lacks: the directories `receipts/proc/`, `receipts/twin/`, `receipts/repro-base/`, `receipts/parent/superseded-piped/`, and 48 files under `receipts/parent/`.
  - The git tree API reports `truncated: false`.
- **Authority:** issue #217 acceptance bullet 4 ("The parent's gates that read AECP and ADP pass on a scratch parent with this head pinned"), and the review brief's rule that source-head execution evidence is the author's published gate receipts. The PR body's "Measured at the head", consumer-gate and twin paragraphs cite results whose receipts are among the absent files.
- **Impact:** at this head, the public record holds no receipt for:
  - the processor gates as run by the author (only those at the parent commit 43149fb are published);
  - three of the five datapath benches;
  - two rtl-fast jobs;
  - the ROM digest record;
  - the base reproduction;
  - the twin run, whose result the PR uses to retire the parent's owed row.

  This reviewer re-ran the processor gates (below), but the parent and twin gates are outside a reviewer's allowed scope, so acceptance bullet 4 stays unproven in public.
- **Required outcome:** republish the complete packet at a pinned commit, so every MANIFEST entry and every INDEX row is present. Or, if any file was withheld on purpose, correct the manifest, the indices and the PR body to the receipts actually published, and say why each was withheld.
- **Verification:** against the new tree, `scripts/evidence_census.py LISTING DLROOT review-evidence/pp217-r1` exits 0 with 0 missing, and a manifest-to-tree comparison reports 0 absent. Then a reviewer reads the rc and log tails of `pp_shadow`, `nvm_cosim`, `milan_dp_render`, `publication_census`, `yosys_elaborate`, `rom_digests` and `twin/head` against `twin/base`. Receipt of this run: `receipts/evidence_census.txt` (52 missing).

### F-2 MINOR (Docs): the PR body misstates the suite count

- **Artifact:** PR #219 body, "Measured at the head" table: "`scripts/run_suites.sh` | 1,032,052 checks, 0 failing (39 suites)".
- **Evidence:** the sweep runs every `tb/*/` with a Makefile, which is 36 suites. Both the author's own `at-43149fb/proc/run_suites.log` and this reviewer's `receipts/suites.log` print 36 `PASS <suite>` lines and "suites: 1032052 checks total, 0 failing". The other 3 output lines are the UPC-map and M9 pre-sweep gates.
- **Impact:** a stated figure is wrong. The check total and the verdict are right.
- **Required outcome:** "1,032,052 checks, 0 failing (36 suites)".
- **Verification:** `grep -c '^PASS ' receipts/suites.log` = 36.

### R-1 RESIDUE (Docs): the comparison with START/STOP's 0xD0 routing is inaccurate

- **Artifact:** `hdl/aecp/ucode/gen_ucode.py:387-388` ("so the selector names the face for the reader alone, as 0xD names the started bit's") and `docs/architecture/06_aecp_engine.md:322-323` ("routed by the engine's `rdent_r` the way the started bit's 0xD0 is routed by START/STOP").
- **Evidence:** `KL_aecp_engine.sv:2261` routes START/STOP's gather by the command flag and the selector's high nibble (`gx_sel_w[7:4] == 4'hD`). `rdent_r` alone routes the 0xE0 gather (`:2266`, `:2481`). So 0xD is decoded; it does not only name the face. The comment does not feed any digest or generated artifact: `decode.json` does not hash `gen_ucode.py`, and the ROM is unchanged by comment text.
- **Exact fix:**
  - gen_ucode.py: "The engine routes the gather by command alone (its rdent_r), so the selector 0xE0 names the face for the reader only; START/STOP's 0xD is also decoded by the engine (strm_state_w)."
  - 06: "(`GATHER_EXT`, selector 0xE0, routed by the engine's `rdent_r` alone, where START/STOP's started bit 0xD0 is routed by the command flag and the selector's high nibble)".

### R-2 RESIDUE (Docs): the area paragraph attributes the flip-flops but not the LUT and MUXF deltas

- **Artifact:** PR #219 body, the area table and the sentence after it.
- **Evidence:** the author's `area/{base,head}/out/SUMMARY.md` give LUT -74 at 2x2 and +442 at 8x8, and MUXF7/8 +53 and +291, with +149 LUT in KL_adp_engine and +237 LUT in KL_aecp_engine alone. Only the 33 FFs are explained.
- **Exact fix:** append "The engines alone grow by 149 LUTs (KL_adp_engine) and 237 LUTs (KL_aecp_engine); the flattened top re-optimizes across them, so its net LUT change is -74 at 2x2 and +442 at 8x8, and MUXF7/8 +53 and +291."

### S-1 SUGGESTION (Tests): pin the per-interface clear on DEPARTING

- **Evidence:** the probe `departing-clears-all` (any DEPARTING clears every interface's last index) passes tb/adp_engine `interfaces` (11 checks, 0 failures). Every ENTITY_DEPARTING in this design leaves on all interfaces together (`entity_enable_i` is global; LINK_DOWN sends none). So the fault is visible only in the few clocks between the two DEPARTINGs and is not a reachable behaviour difference.
- **Suggestion:** an IF9 sample of `last_avail_index_o` between the two DEPARTINGs would pin it. This is not required.

## Processor gates run by this reviewer at the exact head

| Gate | Result (receipt) |
|---|---|
| `scripts/run_suites.sh` (36 suites) | rc 0, "suites: 1032052 checks total, 0 failing"; pp_top 11,082, adp_engine 1,365, aecp_cmds 181 (`suites.log`, 1 h 01 m) |
| `make check` | rc 0, all eleven sub-gates OK (`static.log`) |
| `scripts/lint_hdl.sh`, `gen_matrix.py --check`, `git diff --check 044cb25f HEAD`, `check-req-tags.py` static, `check_aecp_commands.py` | rc 0 each (`static.log`) |
| `check-req-tags.py --suites --evidence` on the author's published sweep files | rc 0, 270 evidence lines, 14 suites (`req_tags_exec_on_author_files.txt`) |
| AEM image, `hdl/srp` untouched; top ports and parameters byte-identical | rc 0, rc 0 (`static.log`) |
| `tb/adp_engine/mutants.py --jobs 3` | rc 0, 68 of 68 (`adpmut.log`) |
| `tb/pp_top/aecp_dispatch_mutants.py --only` the 2 AI arms and `rdc-base-no-overlay` | rc 0, 5 of 5 including 2 controls (`dispmut.log`) |
| `tb/pp_top/ctr_mutants.py --jobs 2`, full | rc 0, 18 of 18 (`ctrfull.log`; `ctrmut.log` for the re-anchored arm alone) |
| `tb/aecp_cmds` `make mutants` | rc 0, 17 of 17, golden and restored PASS (`cmdmut.log`) |
| every tracked mutation patch applies | 507 of 507 (`patch_census.txt`) |
| reviewer probes | 8 runs. `base-rtl` reproduces the defect (AI 4 failures). Of the 7 fault runs, 5 are KILLED (`top-serves-if1`, `aidx-offset-32`, `tail-one-lane-late`, `last-from-live-next`, `rdent-sticky-full`). `rdent-sticky` survives only its two focused targets, and the same fault is KILLED by the full default run. `departing-clears-all` survives (S-1). (`probe-*.log`, `probes/`) |

Exact-head hosted runs, read only: `hdl` workflow runs 42665288037 (pull_request) and 42665248413 (push). `docs-gates` and `portability` completed with success in both. `suites` was still `in_progress` when last read. Skipped contexts were not counted as executed.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Table 7-2 / 6.2.2.15 / Milan 5.6.3 semantics against `KL_adp_engine.sv:964-987`, `protocol_processor_top.sv:4139-4160`, `gen_ucode.py:798-830`; AI and IF4 executed; base reproduction 4 failures; issue acceptance bullets 1 to 3 | R809-1 | 794f8442c3d9da158c99d358d825c7b277516bba |
| RTL | CLEAN | the full `hdl/` delta (4 files, +103/-9); single clock and reset; port and parameter header identical; lint rc 0; `rdent_r` set and clear sites; ROM `+17` assert; UPC-map and M9 gates | R809-1 | 794f8442c3d9da158c99d358d825c7b277516bba |
| Robustness | CLEAN | sticky-flag, offset, tail, live-next, mirror-interface and clear-all probes; noncanonical-length fallback kept; out-of-range interface guard; `N_AVB_IF_P` 1..2 guard | R809-1 | 794f8442c3d9da158c99d358d825c7b277516bba |
| Tests | UNCLEAN (F-1) | sections AI and IF4, ADP P2/P3/P7/IF4/IF9, 9 arm rows, 4 campaigns, 36 suites, 507 patches; published evidence census (F-1) | R809-1 | 794f8442c3d9da158c99d358d825c7b277516bba |
| Docs | UNCLEAN (F-1, F-2) | 04 §5, 06 §6.1, REQ-ADP-011, both suite READMEs, 09 §8.1, PR body, published INDEX/MANIFEST; comment-rule scan of the source delta; R-1 and R-2 residue | R809-1 | 794f8442c3d9da158c99d358d825c7b277516bba |

## Real limits

- The IEEE 1722.1-2021 and Milan v1.2 texts were not available to this reviewer. Clause conformance was judged against the text quoted in the repository, the issue and the author's STANDARDS.txt. The repository cites 6.2.2.15 and Table 7-2; the review brief also names 6.2.1.18 and 7.5.2.1, and this reviewer could not reconcile those clause numbers against the standard. The behaviour satisfies the quoted text either way.
- Not run here, by scope or wall-time choice:
  - Yosys synthesis and area, and `tb/elab_guards/guards.py --frontend yosys`. The author's area receipts are present and consistent; the exact-head yosys receipts are among F-1's missing files.
  - The full AECP dispatch campaign (108 units). Only its 3 related arms were run here; the other arms' patches all apply, and none of their required checks was edited.
  - `aecp-mutants` (67).
  - The ACMP, D3, GSI, notification and name-write campaigns.
  - The `tb/maap` and `tb/srp_top` campaigns. Their code is untouched by the delta.
- The executed req-tags half was not re-run on this reviewer's own sweep: the sweep ran without `REQ_TAG_LOG`. It was re-run on the author's published files instead.
- Parent consumer gates, the twin, builder or native banks, hosted/act and Docker: not run (not allowed). No manager source bank ran at this head, and none is claimed or inferred.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- Unit memory peaked at 11,450 MiB under the 12 GiB cap. No Vivado run took place.

## Pending manager duties

- F-1: republish the complete evidence packet, or correct the manifest, indices and PR body; then re-check acceptance bullet 4 and the twin result from the receipts.
- F-2: correct the PR body's suite count.
- R-1 and R-2 to the residue checklist.
- At the merge turn: build and validate the current-dev merge candidate (source base 044cb25f, live dev ac0a01e3), with the builder and native banks, and link those receipts on the PR. Take the hosted `suites` job's conclusion for this head.
- When the parent takes this pin: delete the twin's `entity-available-index` owed row, as its design requires.
- Merge still needs two independent positive reviews and the full completion bar.

R809-1 FINISHED
