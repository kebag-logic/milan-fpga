[R319] POSITIVE - exact head 490e4309749c83f92d794a8ff10d3043e0f5f080

# R319-2: external independent delta review of processor PR #118 / issue #77 (round 2)

- **Repository:** Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #118, branch `510-mvu-waiver`. The PR closes #55, #56 and #77 and is the processor side of milan-fpga #510.
- **Exact head:** `490e4309749c83f92d794a8ff10d3043e0f5f080`, tree `84028b430d19317b6bfae8931ebd15cee68388d6`.
- **History:**
  - Parent `b51bc389` is the round-1 head, which merged main `990f9652` into author commit `05fd9e1b`.
  - The source base is `265d6762a58d9d9e545624d6d3f1a34e7006d171`.
  - Main is still `990f9652` at review time, so the PR is current with main.
- **Reviewer role:** external, cleared context, isolated detached clone.
  - Round-2 executor [A293]; assignment in issue #77 comment 5824629677.
  - No source edits, commits, pushes or GitHub writes were made.
  - My own verdict and ledger were fixed (`receipts/own-verdict-before-prior-findings.txt`) before I read the other reviewer's prior public findings.

## Verdict

**POSITIVE.** No finding at MINOR or above is open, so all five lenses are CLEAN at this head.

Round 2 closes my round-1 MINOR, R319-1-F1:
- The waiver's mutation section now names the commit its counts were measured at, `b51bc389`.
- It says the counts must be re-measured before they are quoted for any later head.
- Every count it quotes matches my own round-1 measurements at that commit.

All three suggestions I made in round 1 were taken, and each checks out:
- **Whole Milan note plus a revision trigger:** the quote matches Milan v1.2 word for word, apart from two misspellings the text itself marks as normalized. A second trigger was added for a future Milan revision that makes support mandatory.
- **Phantom P-ID:** the last one in 06 §11 was removed.
- **No-lock-check claim:** the new M4L test pins it. A microcode fault that adds a lock check to the unsupported-command path fails exactly M4L's two refusal checks and nothing else.

There is no RTL change. All round-1 probes were re-run and give the same results; the counts are larger only because the head now includes M4L.

One optional SUGGESTION is below.

## Scope reconstructed (public sources, in order)

1. **Repository conventions.** This repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read both from the parent at `kebag-logic/milan-fpga@6d48f9cf`: section 6 for the reviewer procedure and five lenses, section 7 for coverage being banked per commit. I also read `README.md` and `docs/README.md`: F01.5 is the only home for parameter values, and 01 §7 is the P-ID registry.
2. **Issue #77.** Body and all four comments:
   - the processor assignment (5823862684);
   - round-1 REVIEW READY (5824183596);
   - the round-2 assignment (5824629677), items 1–3;
   - round-2 REVIEW READY (5824839988).
3. **Authority.** Milan v1.2 Consolidated (Final Approved 2023-11-30). The local PDF's sha256 is `6bb902be…3bba8`, the same fingerprint as in round 1. I checked 5.4.3.3 (Table 5.19), 5.4.4.1–5.4.4.5, Table 5.20 and 7.6 (`receipts/spec-check.txt`).
4. **PR #118.** The body, and all six issue comments on the PR: four review-start notices and two round-1 reports. There are no PR reviews and no inline comments.
5. **Diff and history.**
   - `git diff 265d676..490e430`, and the round-2 delta `b51bc38..490e430`.
   - The delta touches four files: `docs/00_MILAN_COMPLIANCE_REVIEW.md`, `docs/architecture/06_aecp_engine.md`, `tb/pp_top/README.md` and `tb/pp_top/sim_main.cpp`.
   - The PR's own diff against main `990f965` changes no path under `hdl/`, `syn/`, `scripts/`, `.github/` or `Makefile` (`receipts/scope-and-history.txt`).
6. **Public evidence.**
   - `kebag-logic/milan-fpga@6d48f9cf/review-evidence/pp510-r1`, whose `author-r2/` packet records processor head `490e430` and parent pin `d1d1fbba`, which pins `490e430`.
   - The hosted runs at the exact head (`receipts/hosted-ci.txt`).

## Round-2 assignment items, verified at this head

| Item | Result | Evidence |
|---|---|---|
| 1. Counts re-measured at the merged head, and the head named or the counts phrased so they cannot go stale | **Met.** `tb/pp_top/README.md:505-511` names merged head `b51bc3893b06…`, "before the M4L lock regression was added". It says the numbers "are measurements of that commit, not live suite totals; re-run the suite and both mutations before quoting counts for any later head". The quoted 7,660 / 7,640 / 197 / 3 match my own round-1 receipts at `b51bc38`. No `1,966` or `1,946` remains anywhere in the tree. The PR body's counts for this head (7,666 = 7,646 + 20; 199 of 7,646 including both M4L checks; 3 of 7,646; bank of 33 suites and 1,014,637 checks) match my reruns and the hosted run. The reproduction recipe at `:513-517` (disposable ROM copy, `ltn_rom.hex` next to it, an `obj_dir` for the tally, run the built binary from that directory) is exactly what my probes do, and it works. | `receipts/readme-b51bc38-counts-crosscheck.txt`, `receipts/pp_top-run-490e430.log`, `receipts/r1probes-at-490e430/rom-*.log`, `receipts/hosted-ci.txt`, `receipts/scope-and-history.txt` |
| 2a. Whole Milan note quoted, with a revision trigger | **Met.** `06_aecp_engine.md:624-626` and `00_MILAN_COMPLIANCE_REVIEW.md:118-120` quote both sentences of the note. It appears identically at 5.4.4.2, .3, .4, .5 and 7.6 (extraction lines 3331, 3384, 3397, 3499, 6026). The only differences are "recomendation" and "specificaiton", which are corrected and flagged "(Spelling normalized.)". Printed pages 58/59/59/61/115 are confirmed. The trigger "or a targeted Milan revision makes it mandatory" appears at `06:632`, `00:123` and REQ-MVU-003/004 (`00:384-385`), which is every place the P4 revisit is stated. | `receipts/spec-check.txt` |
| 2b. Last phantom P-ID in 06 §11 removed | **Met.** `06:1241-1250` lists only P-IDs that have F01.5 rows (`01_overview.md:149-175`). `MILAN_FEATURES_FLAGS.TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING` is named as the F01.5 microcode constant (`01:174`, §8.1 `06:1096`). `P-EN-TALKER-DYN` has no occurrence in the tree. | `receipts/scope-and-history.txt` |
| 2c. No-lock-check behaviour pinned by a response-level check | **Met.** `06:615-616` now cites M4L. M4L (`sim_main.cpp:2527-2574`) runs these steps, all checked byte-exact:<br>1. controller 1 takes LOCK_ENTITY;<br>2. a second controller, from another MAC, sends the complete nonzero SET_SYSTEM_UNIQUE_ID and SET_MEDIA_CLOCK_REFERENCE_INFO, and each gets the NOT_IMPLEMENTED echo;<br>3. no AECP frame follows during 20 ms;<br>4. controller 1 unlocks.<br>A microcode fault that adds `CHECK_LOCK` to `E_NOTIMPL` makes the refusal ENTITY_LOCKED. It fails **exactly** the two M4L refusal checks (2 of 7,646, and nothing else red), so the check detects the defect it claims to. | `receipts/r2probes-at-490e430/ucode-lockcheck.log` |
| 3. No RTL change; gates | **Met.** No path under `hdl/`, `syn/`, `scripts/`, `.github/` or `Makefile` changed in `b51bc38..490e430` or in `990f965..490e430`. The following pass at this head: lint, UPC map, `make check`, the matrix check, fixture guards, pp_top 7,666/0 and the hosted docs-gates, suites and portability jobs. | `receipts/lint-upc-490e430.log`, `receipts/docs-gates-490e430.log`, `receipts/pp_top-*.log`, `receipts/hosted-ci.txt` |

## Prior public review findings: resolution at this head

| Finding | Status at `490e430` | Basis |
|---|---|---|
| R319-1-F1 MINOR (Tests, Docs): waiver mutation section quoted pre-merge counts | **RESOLVED** | Item 1 above. The counts are commit-qualified to `b51bc38`, carry an explicit re-measure rule, and every quoted number reproduces. |
| R319-1-S1 SUGGESTION: whole note plus revision trigger | **TAKEN** | Item 2a. |
| R319-1-S2 SUGGESTION: phantom P-ID in 06 §11 | **TAKEN** | Item 2b. |
| R319-1-S3 SUGGESTION: grade the no-lock-check claim | **TAKEN** | Item 2c, including a mutation proof that M4L can fail. |
| R318-1-F1 MINOR (Tests, Docs): the same stale-count defect | **RESOLVED** | Same basis as R319-1-F1. Its own verification step (`grep '1,966\|1,946'` returns nothing or only commit-qualified text) returns nothing. |
| R318-1-S1 SUGGESTION: quote the whole note | **TAKEN** | Item 2a. |
| R318-1-S2 SUGGESTION: pin the no-lock-check claim | **TAKEN** | Item 2c. |
| Round-1 pending duty: correct the PR body's 1,966 count | **DONE** | The PR body now names `490e430` and quotes 7,666 checks and 872 links, both verified. |

No prior finding is retained open.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### R319-2-S1: SUGGESTION (Tests, Docs). Record M4L's own mutation evidence in the tree

- **Location:** the M4L bullet at `tb/pp_top/README.md:199-203`, and the waiver mutation section at `:503-525`.
- **Issue:** the in-tree mutation table is scoped to `b51bc38`, before M4L existed. The only record that M4L can fail lives in the PR body, which is not a repository artifact: the SUCCESS mutant turns both M4L checks red at `490e430`. Nothing in the tree records a fault that targets the lock claim itself.
- **Suggestion:** add a head-qualified row for a "`CHECK_LOCK` prepended to `E_NOTIMPL`" fault. At `490e430` it fails exactly the two M4L refusal checks, 2 of 7,646 (`receipts/r2probes-at-490e430/ucode-lockcheck.log`). Optional, and it does not affect the verdict.

## Five-lens evidence at this head

### Conformance: CLEAN

**Changed text checked against the clauses.**
- The added note sentence and the revision trigger match Milan v1.2 5.4.4.2–5.4.4.5 and 7.6 (`receipts/spec-check.txt`).
- The M4L comment (`sim_main.cpp:2527-2529`) and `06:615-616` rely on Table 5.19, where 0 is SUCCESS, 1 is NOT_IMPLEMENTED and 2–31 are reserved. That makes the NOT_IMPLEMENTED echo, and not an AEM ENTITY_LOCKED, the right refusal under a foreign lock.

**Behaviour graded at this head.** The following hold byte-exact:
- the M4 refusal of 0x0001–0x0005, with cdl 28/20/92/20/20;
- the M4L refusal under lock;
- M1/M2 features_flags 0.

The pp_top run at this head is 7,666/0.

**Unchanged since round 1.** Everything else in the waiver record, which was examined in round 1, is unchanged since `b51bc38`:
- 06 §6.9/F06.14;
- 00 GAP-03/F00.2/§8;
- F01.5;
- 02, 03, 07.

### RTL: CLEAN

- **No RTL, microcode, synthesis, script or CI change.** The PR is RTL-free against both main and the round-1 head (`receipts/scope-and-history.txt`).
- **Engine behaviour re-read at this head:**
  - `E_NOTIMPL` (`hdl/aecp/ucode/gen_ucode.py:567-572`) is `SET_STATUS NIMPL; BUILD_HDR; SEND_RESP; END` with no `CHECK_LOCK`. That matches `06:615`.
  - `OP_CHECK_LOCK` (`hdl/aecp/KL_aecp_ucpu.sv:309, 631-632`) is the only way ENTITY_LOCKED gets written.
  - The engine latches `sent_r` and emits at most one response per command (`hdl/aecp/KL_aecp_engine.sv:3279-3323`). That is why a ROM fault cannot produce a duplicate response; see the limits section.
- **Gates run with the pinned Verilator 5.050:** `scripts/lint_hdl.sh` exit 0, and `scripts/check_upc_map.py` PASS (56 constants, 80 entry points), both in `receipts/lint-upc-490e430.log`. The hosted `portability` job succeeded at the exact head.

### Robustness: CLEAN

All round-1 probes were re-run unchanged at this head, with `HEAD_SHA` as the only edit (`scripts/probes.sh`; `receipts/r1probes-at-490e430/`).

| Probe | Round-1 result at `b51bc38` | Result at `490e430` |
|---|---|---|
| `base` (default build) | 7,640 / 0 | 7,646 / 0 |
| `rom-notimpl-success` (word 560 → SUCCESS) | 197 of 7,640; M4 10 | 199 of 7,646; M4 10 plus M4L 2 |
| `rom-features-1`, `-2`, `-3` (word 741) | 3 of 7,640 each (M1, M2, M5b) | 3 of 7,646 each (M1, M2, M5b) |
| `rtl-mvu-range` (GET_MILAN_INFO served for 0x0000–0x0007) | 16, all M4 | 18: M4 16 plus M4L 2 |
| `rtl-mvu-0003` (only 0x0003 answered SUCCESS) | 4 M4 0x0003 | 5: the 4 M4 0x0003 checks plus M4L 0x0003 |
| `rtl-bench-short-sets` | 3 (length/cdl) | unchanged probe no longer compiles, because its text replace now also edits M4L's near-identical body. The M4-scoped variant `rtl-bench-short-sets-m4` gives the same 3 length/cdl failures |
| `rtl-lock-probe` (additive foreign-lock probe) | 4/4 pass, 7,644/0 | 4/4 pass, 7,650/0 |

Round-2 probes (`scripts/probes-r2.sh`; `receipts/r2probes-at-490e430/`):
- **`ucode-lockcheck`** (foreign lock → ENTITY_LOCKED): 2 of 7,646, exactly the two M4L refusal checks.
- **`ucode-dupresp`** (a second SEND_RESP under a foreign lock): 0 failures. This is an equivalent mutant, because the engine emits one frame per command whatever the number of SEND_RESPs (RTL section above). It is not evidence against M4L.

I read the silence check's harness side directly. Every AVTP subtype-0xFB frame on TX is captured into `q_aecp` (`sim_main.cpp:1219-1233`). `run_ms(20)` steps the model (`:1553`). `h.q_aecp.empty()` is therefore a true "no AECP frame" check.

The lock state is left clean: the unlock is graded byte-exact before M5 runs.

### Tests: CLEAN

- **M4L** (`sim_main.cpp:2391, 2527-2574`) sends complete, nonzero SET forms from a distinct controller entity ID and MAC. It compares the whole response frame (`got == want`). Both the SUCCESS fault and the lock-check fault prove it can fail. It adds 6 checks: lock, 2 refusals, 2 silence, unlock. That accounts for 7,640 → 7,646.
- **M4 and M1/M2** are unchanged from round 1 and still reject every waived SUCCESS or features fault.
- **Runs at this head:**
  - reviewer `make -C tb/pp_top`-equivalent run: 7,646 default plus 20 fixture = 7,666 PASS, 0 FAIL;
  - fixture guards 4/4 (`receipts/pp_top-run-490e430.log`, `receipts/pp_top-fixture-guards-490e430.log`);
  - hosted `suites`: `PASS pp_top (7666 checks: 7666 PASS, 0 FAIL)`, 33 suites, 1,014,637 checks, 0 failing (`receipts/hosted-ci.txt`).
- **R319-1-F1** is resolved (see above).

### Docs: CLEAN

- **Gates:** `make check` exit 0: 41 mermaid plus 18 wavedrom blocks, 18 wavedrom renders, 872 links, 115 REQ rows and 17 GAPs, 92 module rows with 0 untested. `gen_matrix.py --check` also passes. `make stale` passes in the clone, read-only (`receipts/docs-gates-490e430.log`). The hosted `docs-gates` job succeeded at the exact head.
- **Round-2 text is accurate against code and measurement:**
  - the waiver prose in 00 and 06;
  - the F06.9 M4L sentence;
  - the 06 §11 constant reference;
  - the README M4L bullet (`:199-203`) and the commit-qualified mutation section (`:503-525`).
- **PR body:** it names the head and states its counts are "snapshots and must be re-measured after a later change". Its round-2 numbers reproduce.
- **Optional:** S1.

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 5.4.3.3/Table 5.19, 5.4.4.1–5.4.4.5, Table 5.20, 7.6 (`receipts/spec-check.txt`); `06_aecp_engine.md:612-667, 1241-1250`; `00_MILAN_COMPLIANCE_REVIEW.md:106-130, 384-385`; `01_overview.md:141-179`; `sim_main.cpp:2527-2574` M4L; unchanged waiver record from R319-1 | R319-2 | 490e4309749c83f92d794a8ff10d3043e0f5f080 |
| RTL | CLEAN | path-scoped diffs `b51bc38..490e430` and `990f965..490e430` (no RTL/µcode/syn/scripts/CI change); `gen_ucode.py:567-572`; `KL_aecp_ucpu.sv:309, 631-632`; `KL_aecp_engine.sv:3279-3323`; lint; UPC map; hosted portability | R319-2 | 490e4309749c83f92d794a8ff10d3043e0f5f080 |
| Robustness | CLEAN | 10 round-1 probes re-run (1 as an M4-scoped variant) plus 2 round-2 µcode faults (`scripts/probes.sh`, `scripts/probes-r2.sh`, `receipts/r1probes-at-490e430/`, `receipts/r2probes-at-490e430/`) | R319-2 | 490e4309749c83f92d794a8ff10d3043e0f5f080 |
| Tests | CLEAN | `sim_main.cpp` M1/M2/M4/M4L and harness capture `:1219-1233`; reviewer pp_top 7,666/0 plus fixture guards; SUCCESS, features and lock-check faults; hosted suites log | R319-2 | 490e4309749c83f92d794a8ff10d3043e0f5f080 |
| Docs | CLEAN | `tb/pp_top/README.md:190-210, 500-525`; 00 and 06 round-2 text; `make check` subgates; `gen_matrix --check`; `make stale`; residue search; PR body | R319-2 | 490e4309749c83f92d794a8ff10d3043e0f5f080 |

**Clone integrity after probes** (`receipts/clone-integrity.txt`):
- HEAD, `HEAD^{tree}` and the index `write-tree` all equal `84028b43`;
- `status --porcelain --ignored` is empty;
- all 246 tracked blobs were re-hashed with 0 content or mode mismatches;
- there are 0 gitlinks and no `.gitmodules`, so no submodule pin applies at this head;
- every probe ran in `git archive` extracts under `scratch/`.

## Real limits

- **Banks not run.** I did not run the full processor suite bank, Yosys portability, the `nvm_port` figures or any parent gate, because they were not allowed. For those I rely on the hosted runs at the exact head:
  - push run 36079817702 and pull_request run 36079820839;
  - `docs-gates`, `suites` and `portability` all executed and succeeded, with no job skipped;
  - the only skipped step is "Build Verilator v5.050", which was skipped because a cached pinned build was used inside the executed `suites` job.
- **Manager banks not found.** The named public evidence tree (`pp510-r1`) holds `author/`, `author-r2/` and `reviews/R318-1/`. I found no manager static/builder or native bank receipts in it, so the statement that those banks passed at this head is the manager's, not something I verified.
- **Parent consumer not publicly verifiable.** Commit `d1d1fbba`, which pins `490e430`, is local and not present in the public repository. The public `508-pp-pin-adopt` branch has moved to `6a9828c1`. Public `dev` was `0755923d` when I checked, not the `c266432d` quoted in the assignment. I ran no parent checks.
- **Probe coverage.** Mutants used the default build only, and the ROM faults reused the head's default binary. The M4L silence checks could not be turned red by a microcode fault, because one frame per command is enforced by the RTL. Their soundness rests on reading the harness.
- **Probe execution incident.** A first batch of probe runs was moved to the background by a runner timeout. It kept running while I re-ran probes in the same scratch paths. For part of that time two compile jobs, each capped at 8, overlapped, so up to 16 compile jobs ran at once, above the 8-job limit. I discarded all receipts from that period and regenerated every one sequentially. The results were identical.
- **Spec reading.** The spec was read from a text extraction of a local PDF with a recorded fingerprint.
- **No hardware.** Physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof.

## Pending manager duties

1. At the merge turn, build and validate the final current-dev candidate: source base `265d6762…`, with live dev re-resolved at that time. Own hosted and act acceptance.
2. Re-run or publish the parent-consumer evidence on `508-pp-pin-adopt` at the head actually pinned. When the pin moves, retire or update the parent `SUBMODULES.md` known-conflict row for F01.5.
3. Keep #57 (REQ-MVU-005 timing) open. Track the parent `aecp_response_contract.feature` follow-up noted in milan-fpga #510 comment 5801832005.
4. Optionally take R319-2-S1.

## Receipts

Every publishable file is listed in `MANIFEST.sha256`.
- `scripts/probes.sh` is the round-1 probe script, with `HEAD_SHA` as the only change. Run it with `REPO`, `VERILATOR`, `SCRATCH` and `OUT` set.
- `scripts/probes-r2.sh` holds the round-2 faults. It also needs `BASE`, the `probes.sh` base extract.
- `scripts/vwrap-j8.sh` caps the suite's `-j 0` at 8 jobs.

Local absolute paths in the logs are replaced with `<packet>` and `<verilator-install>`.

R319-2 FINISHED
