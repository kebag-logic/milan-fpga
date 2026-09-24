[R290] POSITIVE - exact head 2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f

# R290-3: independent internal review of issue #94 / PR #110, round 2

| | |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| PR / issue | #110 / #94 |
| Exact head | `2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f`, tree `b83ba761298a353d80c2f48bc178764615525e1d` (verified in the clone) |
| Source base | `008edbbf486598ae237414273d75e385cf0e1a56` |
| Previous reviewed head | `cc077a6ffe20585d20b116f008e07189ba1bb7f8` (R290-2 and R291-2, both NEGATIVE on the same MINOR) |
| Round scope | [A252] (issue comment 5812432287): fix R290-2 F1 = R291-2 F1; take R291-2 S1-S4 if cheap; nothing else |
| Verdict | **POSITIVE**. There is no open BLOCKER, MAJOR or MINOR finding, and all five lenses are CLEAN. One non-blocking SUGGESTION is raised (S1). |

## 1. How the scope was reconstructed

1. **Contributor rules.** The repository has no `AGENTS.md` or `CONTRIBUTING.md`. The contributor rules are in `README.md` ("Building and checking"; "Every diagram is drawn against the landed RTL"), `docs/README.md` §3/§6 (figure rules, `make check` before commit) and `docs/diagrams/README.md`. That last file requires every change to the five hand-authored SVGs to be rendered to PNG and looked at.
2. **Issue #94.** The body contains the T9 contract, the proposed seam and the acceptance criteria. The manager's scope decision (5810666541) narrows it to the standalone guard:
   - late-beat isolation, with a hold-deleted mutant;
   - bounded stuck memory;
   - hard-reset-only debt;
   - the store suites stay green;
   - out-of-context area against 5 LUT / 1 FF.

   D3 roll-back is deferred, and `debt_o` is the documented interface for it.
3. **PR #110.** The manager's port decision (5811722803) is that `debt_o` stays on the guard's own port and the product top's ports stay unchanged. The [A252] round-2 assignment is on the issue (5812432287), and the author's round-2 PR body is at the exact head.
4. **Code.** I read `git diff 008edbbf..2e1675d2`, 22 files, then `git diff cc077a6f..2e1675d2`, 8 files. I read the whole diff independently before opening any prior review text.
5. **Public evidence.** `kebag-logic/milan-fpga@c23839d5:review-evidence/pp94-r1`: the `author-r2` receipts (CI gates, parent consumer gates, diagram verification, parent index restoration). I read the `reviews/R290-2` and `reviews/R291-2` entries only in the PR comments, after my own pass. The exact-head hosted check runs were also read.

## 2. Findings

No MINOR, MAJOR or BLOCKER finding.

### R290-3-S1: SUGGESTION. Lenses: Docs, Tests. No gate keeps the committed PNG renders fresh

- **Where.** `Makefile` target `stale` (checks `docs/diagrams/src/*.drawio` against `*.svg` only) and `docs/diagrams/README.md` ("Inventory (hand-authored SVG)"). The committed PNGs `docs/diagrams/2[0-4]-*.png` are covered by no gate.
- **Authority and evidence.**
  - The previous round's F1 (stale PNGs of figures 20 and 22) passed every repository gate, `make check` included, at `cc077a6f`.
  - At this head, all five committed PNGs are byte-identical to fresh `rsvg-convert` renders of their SVGs at their committed widths (`receipts/png-render-compare.txt`). A mechanical check is therefore cheap and deterministic with the documented renderer version.
- **Impact.** A future SVG edit can again leave a stale PNG for a renderer-less reader, and only review would catch it. There is no defect at this head.
- **Suggested outcome.** A follow-up outside this PR, because [A252] says "No other change". Either extend `make stale` or `make check` with a PNG-versus-SVG freshness check (render-hash comparison, or a commit-time ordering like the draw.io rule), or state in `docs/diagrams/README.md` that the PNG must be re-rendered in the same commit as its SVG.
- **Verification.** Edit a hand-authored SVG without re-rendering its PNG. The new gate should fail. With the PNG re-rendered, it should pass.

## 3. Prior public findings on this PR, resolved or retained at this head

I read these only after my own pass over the diff. The sources are R290-2 (PR comment 5812425622), R291-2 (5812328379) and the round-1 manager gate failures (5811722803).

| Prior finding | State at `2e1675d2` | Reviewer evidence |
|---|---|---|
| R290-2 F1 = R291-2 F1 (MINOR, Docs): PNGs of figures 20 and 22 stale against their edited SVGs | **Resolved** | The PNG blobs changed since `cc077a6f`: 20 is now `c3e54052…`, 22 is now `8ad3ecf8…` (at `cc077a6f` they were byte-identical to base). Fresh renders of the head SVGs at 2040 px (2040×1380) and 1950 px (1950×1440) are **byte-identical** to the committed PNGs (`receipts/png-render-compare.txt`; reviewer renders `receipts/render-2*-*.head-svg.png`; old PNGs `receipts/committed-2*-at-cc077a6f.png`). Visual check in §4 Docs. `make stale` rc 0, links/matrix/modmatrix rc 0. |
| R291-2 S1 (SUGGESTION): stray blank line in the top's port block | **Resolved** | `hdl/top/protocol_processor_top.sv` lines 170-700 are byte-identical to the base. The port list is 205 ports, same names and order as the base, with no `desc_mem_debt_o` (`receipts/top-port-list.txt`). The base..head diff of the top now touches only the guard insertion (≈3209-3310). |
| R291-2 S2 (SUGGESTION): acceptance-over-clear priority unpinned | **Resolved** | New check at `tb/desc_mem_guard/sim_main.cpp:327-333`. Its preconditions discriminate: no debt, `mem_req_ready_i=1`, `mem_rsp_valid_i=1` held from line 311, `unit_rsp_ready_i=1`, `last=1`. I ran the swapped priority mutant (`receipts/guard-prio-mutant.diff`): make rc 2, **77 PASS / 1 FAIL**, the only FAIL being `request acceptance must win over a coincident stray terminal beat` (`receipts/guard-prio-mutant.log`). The head passes 78/78. |
| R291-2 S3 (SUGGESTION): guard placement in the figures | **Resolved** | Figure 20: the guard is a solid module box between the AECP engine and "integrator main memory", with a `desc_mem_*` arrow down to memory. The response-buffer master bypasses it on its own line (`20-rtl-dataflow.svg:123-138`). The subtitle now says main memory is external. Figure 22: the guard sits between step 4 and the "descriptor image" box, and it also feeds the header/index-map box (`22-aecp-descriptor-fetch.svg:63-83`). |
| R291-2 S4 (SUGGESTION): reset instruction addressed to an unreachable wire | **Resolved** | `docs/guides/integrator.md:136-139` now tells the integrator to drive `protocol_processor_top.rst_n` only from a hard reset that flushes the descriptor-memory path, including CDC queues, and never from an entity disable, a store-only reset or a rollback reset. This matches the RTL: the top has a single `rst_n` (`:179`), and it reaches both `u_desc_mem_guard` (`:3220`) and `KL_aecp_engine` (`:3253`). The guard-internal rule stays in the RTL banner. It is consistent with the `rst_n` rows at integrator.md:29 and hdl-engineer.md:61. |
| Round-1 gate failures (Rule 11 C++ idiom, Rule 12 Python idiom, parent `PINMISSING`) | **Remain resolved** | Round 2 adds 8 C++ lines: plain member assignments, one `tick()` and one `CHECK`. They contain no cast and no declaration. `mutate.py` is unchanged. The top port list is identical to the base (above). The parent gates at this head are author receipts (`author-r2/parent-results.json`: cpp-idiom, py-idiom, xvlog, rtl-source-lists and pp-shadow all rc 0; `parent-state.json` records `index_restored: true`). The manager's receipts are pending (§7). |

## 4. Lens evidence

### Conformance: CLEAN

- **Guard seam.** `hdl/aecp/KL_aecp_desc_mem_guard.sv` implements the seam as the scope decision states it:
  - `owed_r` is set on `m_req_valid_o && m_req_ready_i`;
  - it is cleared on a consumed `last || err`;
  - both request arms are held while owed (`m_req_valid_o`, `s_req_ready_o`);
  - responses pass through unchanged;
  - it is reset by `rst_n` alone;
  - it is published as `debt_o`.
- **Top placement.** `protocol_processor_top.sv:3209-3231` inserts the guard between the engine's descriptor master and `desc_mem_*`. `debt_o` ends at `desc_mem_debt_nc_w`, as the port decision requires.
- **Acceptance evidence at this head** (reviewer-run, pinned simulator):
  - The late-beat case passes: third locate `0005000011223344 5566778899aabbcc`, held 1,895 cycles, 0 overlap accepts.
  - The unguarded baseline fails exactly `late_beats_never_served` with `00060000deadbeef cafef00d01234567`: rc 2, 17/1.
  - The committed hold-deleted controller detects the mutant (rc 0; mutant rc 2, 17/1, same wrong bytes).
  - The stuck-memory and hard/store-only reset cases pass inside the 78 checks.
  - Receipts: `receipts/guard-head.log`, `guard-baseline.log`, `guard-hold-mutant.{txt,log}`.
- **Round-2 scope.** `cc077a6f..2e1675d2` touches exactly the eight files [A252] allows (`receipts/stale-diffcheck.log`):
  - two SVGs and two PNGs (F1, S3);
  - `integrator.md` (S4);
  - one deleted blank line in the top (S1);
  - the guard test and its README line (S2).

  No RTL behaviour changed. The guard, the store and `syn/` are byte-identical to `cc077a6f`.
- **Area.** The out-of-context result (4 LUT / 1 FF against T9's 5 / 1) is prior author evidence on unchanged guard RTL. I did not re-run Vivado.

### RTL: CLEAN

- **Guard logic.**
  - `m_req_valid_o` depends only on `s_req_valid_i` and the registered `owed_r`, never on `m_req_ready_i`.
  - `s_req_ready_o` is a pass-through of ready gated by `owed_r`.
  - While owed, accept and clear cannot coincide, because `m_req_valid_o` is 0. When not owed, acceptance wins over a stray terminal beat. That is the safe choice, and it is now pinned.
  - There is no combinational loop and no new clock or reset.
- **Lint.** The guard lints clean under `-Wall` with the pinned Verilator 5.050 (`receipts/lint-guard.log`).
- **Top change this round.** One whitespace-only line deletion. The port block is byte-identical to the base.
- **Reset reach.** The engine and the guard share the top `rst_n`, and no store-only reset exists at the top.

### Robustness: CLEAN

- **Stray terminal beat.** The only new behavioural pin is this case, which R291-2 identified as what an unflushed path after hard reset would present. It keeps debt set, so no request is released early. The inverted-priority mutant is now detected.
- **Unchanged guard behaviour, re-run at this head:**
  - finite late burst (drains, byte-exact recovery);
  - never-ending burst (requests held, each locate answered an error within the 4,160-cycle bound);
  - debt survives a store-only reset;
  - hard reset clears debt;
  - `err` without `last` terminates the burst.
- **Integrated cases.** `tb/pp_top` A12/A13 are in the 1,454/1,454 run (`receipts/suite-pp_top.log`).

### Tests: CLEAN

- **Suites and gates run at the exact head** from a `git archive` copy (never the clone), with the pinned Verilator 5.050. The wrapper identity was verified (`receipts/guard-env.txt`):
  - `tb/desc_mem_guard` 78/78, rc 0;
  - `tb/desc_store` 584/584, rc 0;
  - `tb/pp_top` 1,454/1,454, rc 0;
  - baseline rc 2 (17/1, expected);
  - hold mutant detected;
  - priority mutant rc 2, 77/1, failing at the new assertion only;
  - `check-links` / `check-matrix` / `gen_matrix --check` rc 0;
  - `make stale` and `git diff --check` rc 0 in the clone.
- **The new check (S2).** It is placed after the transparent-response check and reuses the live `mem_rsp_valid_i=1`. Without that, the clear branch could not fire and the check would not discriminate. My mutant run shows it does. `tb/desc_mem_guard/README.md:25` describes it accurately.
- **Controller coverage.** The priority mutant is not part of the committed `mutate.py` controller, which covers the hold mutant only. [A252] asked for a test, not a controller, so this is not a finding.
- **Hosted.** At exact head (`receipts/hosted-check-runs.txt`), `docs-gates` and `portability` completed with success in both workflow runs. Both `suites` jobs were still **in progress** when I read them, so no hosted suites result is claimed here.

### Docs: CLEAN (S1 is a non-blocking suggestion)

- **Figure 20 PNG** (2040×1380), viewed:
  - The guard is a green solid module box, "KL_aecp_desc_mem_guard / at processor top · hard reset only / owed holds requests; responses pass through".
  - A purple arrow runs from the AECP engine's dashed interior to the guard, and a labelled `desc_mem_*` arrow runs down into "integrator main memory".
  - The memory box now lists `desc_mem_*: READ only, at DESC_BASE_P` and `resp_mem_*: READ + WRITE, at RESP_BASE_P`.
  - `KL_aecp_resp_buf` has its own line into memory, bypassing the guard.
  - No text overlaps or is clipped, and no line runs through a box. The only crossings are perpendicular crossings with the teal MRPDU route. The descriptor-arrow crossing already exists in the base. The new response-buffer line adds one more perpendicular crossing, which is acceptable under the diagrams README's rules.
- **Figure 22 PNG** (1950×1440), viewed:
  - The right column is titled "processor memory face / integrator main memory".
  - Step 4 → guard box (five lines of text, all inside the box) → "descriptor image" box. The guard also has an arrow up to "image header + index map".
  - The module list includes `KL_aecp_desc_mem_guard.sv`, and the suite list includes `tb/desc_mem_guard`.
  - The "desc_mem_* absent or wedged" panel carries the late-burst text.
  - No overlap or clipped text.
  - The step-3 → header arrow was removed. That is consistent with the header and index map being probed through the memory face, while LOCATE is served on chip.
  - The step-7 arrow starting in open space is unchanged from the base.
- **Other PNGs.** The PNGs of figures 21, 23 and 24 are unchanged and also byte-identical to their SVG renders.
- **Prose.**
  - `integrator.md` §4.1 (S4 wording) is consistent with 07 §3.3.1 and with the rest of the guide. The reciprocal `sec-desc-memory` anchors are present in both files, and the link gate passes.
  - `MODULE_MATRIX.md` (46 modules, 0 untested) matches `gen_matrix --check`.
  - `syn/ooc/README.md` and the suite READMEs are unchanged this round.

## 5. Reviewer probes and scripts

| Script | What it does | Receipts |
|---|---|---|
| `scripts/guard_probes.sh <clone> <packet> <verilator>` | `git archive` of the exact head into scratch. Runs the guard suite, the baseline, the committed hold-mutant controller, and the reviewer's inverted-priority mutant (Python text swap, refuses unless the block is found exactly once). | `guard-*.log/.rc/.txt`, `guard-prio-mutant.diff`, `KL_aecp_desc_mem_guard.prio.sv` |
| `scripts/focused_suites.sh <packet> <verilator>` | Runs `tb/desc_store`, `tb/pp_top`, the guard lint under `-Wall`, and the link, requirement-matrix and module-matrix gates on the archived copy. | `suite-*.log/.rc`, `lint-guard.*`, `docs-*` |
| `scripts/png_ports_integrity.sh <clone> <packet>` | Renders every hand-authored SVG at its committed PNG width and compares hashes. Also checks the top port list and port block against the base, `make stale`, `git diff --check`, the round-2 file list, and clone integrity. Read-only on the clone. | `png-render-compare.txt`, `top-port-list.txt`, `stale-diffcheck.log`, `clone-integrity.txt`, `render-*.png`, `committed-*-at-cc077a6f.png` |

Local absolute paths in the receipts are redacted to `$PACKET`, `$PINNED_BIN` and `$PINNED_VERILATOR_ROOT`.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #94 body/T9 seam; scope decision 5810666541; port decision 5811722803; [A252] 5812432287; guard and top RTL; round-2 file list against [A252]; late/baseline/hold-mutant/stuck/reset receipts | R290-3 | 2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f |
| RTL | CLEAN | `KL_aecp_desc_mem_guard.sv` (handshake, priority, reset); `protocol_processor_top.sv` guard insertion, `rst_n` reach, port block/list against base; guard `-Wall` lint | R290-3 | 2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f |
| Robustness | CLEAN | Stray-terminal-at-acceptance priority (new pin + mutant); late, stuck, store-only/hard reset and err-terminal paths in the guard suite; A12/A13 in `tb/pp_top` | R290-3 | 2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f |
| Tests | CLEAN | `tb/desc_mem_guard/sim_main.cpp:327-333` and README; guard 78/78, desc_store 584/584, pp_top 1,454/1,454; baseline; hold and priority mutants; doc gates; hosted check runs (suites in progress) | R290-3 | 2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f |
| Docs | CLEAN (S1 suggestion) | Figures 20 and 22 SVG and PNG (render identity + visual), figures 21/23/24 PNG identity, `integrator.md` §4.1, 07 §3.3.1 anchors, `MODULE_MATRIX.md`, `tb/desc_mem_guard/README.md`, `make stale`, link/matrix gates | R290-3 | 2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f |

## 7. Real limits and pending manager duties

Limits:

- **Not run, by instruction.**
  - the full processor bank (`run_suites.sh` over all 32 suites) and `lint_hdl.sh` over every module;
  - the NVM-figures gate and the repository Yosys portability bank;
  - Vivado out-of-context synthesis;
  - parent, gPTP and builder banks;
  - Docker/act and hardware.

  For these I rely on the author's round-2 receipts (`author-r2/ci-results.json`: all 12 gates rc 0) and on hosted jobs. Only `docs-gates` and `portability` had completed at exact head when I read them. `suites` was in progress.
- **Manager receipts.** The prompt says the manager's full source static/builder and native banks passed at this head. In the public evidence tree (`c23839d5`) and in the issue and PR comments I read, I found no manager-authored receipt at `2e1675d2`. The latest published manager validation is for `cc077a6f` (5812166128). The parent consumer results at this head in `author-r2/` were produced by the author at parent `5fd468a9`, with the gitlink staged temporarily and then restored.
- **Parent memory path.** Whether the parent's CDC FIFO and `pp_desc_bridge` honour the documented contract is not verified here. The contract is: `err` terminates a burst; the first response comes after acceptance; hard reset flushes the queue. It belongs to the parent/D3 lane.
- **Deferred D3 scope**, per the scope decision:
  - the owners are held while `debt_o` is set;
  - the deadline expiring ends in CLOSED;
  - the 5,000/16,000-cycle cases and the slot-shape cases;
  - the owner-release mutant;
  - `debt_o` is routed to the top and the parent.

  Nothing here claims them.
- **Physical calibration NOT RUN.** Field skips and post-synthesis area are not hardware proof.
- **Clone hygiene.** No probe ran in the clone. It is at the exact head with a clean status (ignored files included), index tree = head tree `b83ba761…`, and tracked bytes and modes equal to HEAD. The repository has no submodule gitlinks and no `.gitmodules` (`receipts/clone-integrity.txt`).

Pending manager duties:

- Publish the manager's own bank receipts at `2e1675d2`: donor bank, and parent consumer gates including `pp_srcs` and `test_builder`.
- Confirm that the exact-head hosted `suites` jobs completed successfully.
- Build and validate the final current-dev candidate at the merge turn (source base `008edbbf`, live dev `eaf0e6c4`). It is distinct from this source validation.
- Hosted/act acceptance.
- The second independent review. Merge requires two independent positive reviews and the full completion bar.
- Optionally, file S1 as a follow-up issue.

## 8. Receipts

Every published receipt and script is listed in `MANIFEST.sha256`, with paths relative to the packet root. `scratch/` is not published.

R290-3 FINISHED
