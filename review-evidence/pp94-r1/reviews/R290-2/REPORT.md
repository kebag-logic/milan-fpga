[R290] NEGATIVE - exact head cc077a6ffe20585d20b116f008e07189ba1bb7f8

# R290-2: independent internal review of issue #94 / PR #110

| | |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| PR / issue | #110 / #94 |
| Exact head | `cc077a6ffe20585d20b116f008e07189ba1bb7f8`, tree `caa8229363824fcafd939fbaecdbdf62fb9160a1` (verified locally) |
| Source base | `008edbbf486598ae237414273d75e385cf0e1a56` |
| Round | R290-2. R290-1 was voided before any verdict because its head was superseded |
| Lenses | Conformance, RTL, Robustness, Tests, Docs, each applied independently |

**Verdict: NEGATIVE, because of one open MINOR finding (Docs).** The RTL, the integration,
the robustness behaviour and the tests are clean at this head. I reproduced every acceptance
case myself. Eleven independent mutants were all killed. The only open defect is two
committed PNG renders that still show the pre-guard diagrams.

## 1. How the scope was reconstructed

1. **Repository conventions.** There is no `AGENTS.md` or `CONTRIBUTING.md` in this
   repository at the head. The governing conventions are in `README.md` (build and check
   gates, and the rule that the submodule pin moves only when all gates are green),
   `hdl/README.md` (Rules 1–5: vendor-neutral SystemVerilog, Verilator ≥ 5.050 plus Yosys
   portability, every RTL commit carries its `tb/` suite with an independent model, values
   kept single-source, spec citations in module banners), `docs/README.md` (single-source
   rules, figure rules, `make check`), `docs/diagrams/README.md` (the five hand-authored
   SVGs are rendered and looked at after every edit) and `.github/workflows/hdl.yml`.
2. **Frozen acceptance.** Taken from the issue #94 body plus the manager's scope decision
   (issue comment 5810666541):
   - the guard between the store's memory master and the memory face: `owed` is set on an
     accepted request and cleared by a terminal `last` or `err`, the next request is held
     while owed, and every beat passes through;
   - hard reset only, with `debt_o` published;
   - the late-beat case, including "deleting the hold reddens it" and a locate being served
     after the late burst;
   - the stuck-memory case, where requests stay held and every locate gets a bounded error;
   - the store suites stay green;
   - area measured out of context against the T9 estimate of 5 LUT / 1 FF.

   The D3 roll-back cases are deferred to the D3 lane.
3. **Manager port decision** (PR comment 5811722803). `debt_o` stays on the guard's own
   port. It is not routed to `protocol_processor_top` until the D3 lane. Round 1b also
   fixes the parent's Rule 11 (C++) and Rule 12 (Python) findings.
4. **Authorities.**
   - The T9 ticket and the proposed-seam text quoted in the issue.
   - `docs/architecture/07_memory_maps.md` §3.3.1 and `docs/guides/integrator.md` §4.1,
     which the PR adds to.
   - The `KL_aecp_desc_store` memory handshake: `mem_rsp_ready_o` is tied to 1, a beat is
     consumed only while `mem_busy_r` is set, and the watchdog is `MEM_TIMEOUT_CYC_P`
     (default 4096).
5. **Diff and history.** I read the full diff `008edbbf..cc077a6f` (20 files, +855/−43) and
   both commits, `4f525eb5` (round 1) and `cc077a6f` (round 1b).
6. **Public evidence.** `kebag-logic/milan-fpga@802e90eb:review-evidence/pp94-r1` (author
   and author-r1b packets, 77 manifest entries), the hosted checks at the exact head, and
   the manager comments on the issue and the PR.

## 2. Findings

### R290-2-F1: MINOR, Docs. The committed PNG renders of the two edited diagrams still show the pre-guard figures

- **Where**
  - `docs/diagrams/22-aecp-descriptor-fetch.png`: the blob `abe76f52…` is unchanged from the base.
  - `docs/diagrams/20-rtl-dataflow.png`: the blob `cd2525f5…` is unchanged from the base.
  - Their SVG sources were edited by this PR:
    - `22-aecp-descriptor-fetch.svg` +14/−7, edited in both `4f525eb5` and `cc077a6f`. It
      gains a "Guard at processor top, hard reset only" box, the guard in the module list,
      `tb/desc_mem_guard` in the suite list and new wedged-memory text.
    - `20-rtl-dataflow.svg`, edited in `4f525eb5`. Line 128 now reads
      "desc_mem_* via KL_aecp_desc_mem_guard (at processor top)".
- **Authority and evidence**
  - Commit `2ca216e` ("Keep the PNG renders beside the SVG sources so a wiki can show them
    without a renderer") introduced these PNGs as renders of the SVGs.
  - The base branch re-rendered a PNG when its SVG changed. `f8d30ec` ("Render the dataflow
    diagram's PNG again now that it shows…") did exactly that for diagram 20, on the base
    branch, on the morning this PR started.
  - `README.md`: "Every diagram is drawn against the landed RTL."
  - `docs/diagrams/README.md`: the hand-authored SVGs must be rendered and looked at after
    any change.
  - Receipt `receipts/11-diagram-png-staleness.txt` shows the base and head blob ids.
    `receipts/14-diagram22-head-svg-render.png` is the head SVG rendered by the reviewer.
    Next to the committed PNG, it shows that the PNG has no guard box, still lists four
    modules and three suites, and still has the old "req_ready tied 0" text.
- **Impact.** Anyone who reads the PNGs sees a READ_DESCRIPTOR path with no response-isolation
  guard. That contradicts the landed RTL and the SVG next to it. No gate catches it, because
  `make stale` only covers the draw.io sources.
- **Lenses.** Docs. Only Docs is affected; the other lenses are unaffected.
- **Required outcome.** Re-render both PNGs from the head SVGs and commit them. Use the
  sizes already committed: 22 at 1950 px wide, which gives 1950×1440, and 20 at 2040 px
  wide, for example `rsvg-convert -w 1950 -o docs/diagrams/22-aecp-descriptor-fetch.png
  docs/diagrams/22-aecp-descriptor-fetch.svg`. Then look at each result, as
  `docs/diagrams/README.md` requires. If the maintainers prefer, removing the PNGs is also
  acceptable, but that must be an explicit documented decision.
- **Verification.** Both PNG blob ids differ from the base. A visual check shows the guard
  box and the new module and suite lists in 22 and the new label in 20. `make check` stays
  at 0.

No other MINOR, MAJOR or BLOCKER finding. No SUGGESTION is raised.

## 3. Prior public findings on this PR, resolved at this head

The PR has no formal reviews and no inline review comments. R290-1 and R291-1 were voided
before any verdict. The only public findings against the PR are the three gate failures the
manager recorded against `4f525eb5` (PR comment 5811722803). I read that comment only after
my own pass over the diff.

| Prior finding | State at `cc077a6f` | Reviewer evidence |
|---|---|---|
| `check_cpp_idiom` (Rule 11): 10 C-style casts, 1 file-scope mutable, 6 multi-declarator declarations in `tb/desc_mem_guard/sim_main.cpp` | **Resolved at file level** | I ran the parent's own `scan()` from parent dev `9d328810` (`receipts/10-idiom-scan-changed-files.txt`, checker hashes in `10-parent-checker-sha256.txt`) on every changed C++ file. It finds 0 at the head. As a control, the same scanner on `4f525eb5` reproduces exactly 10/1/6. |
| `check_py_idiom` (Rule 12): `mutate.py` has an unannotated, undocumented public function | **Resolved at file level** | The same receipt shows 0 at the head, and the control on `4f525eb5` reproduces 1/1. `mutate.py:9` now reads `def main() -> int:` and has a docstring. |
| Parent `pp_shadow` stops with `PINMISSING` on `desc_mem_debt_o` | **Resolved** | The `protocol_processor_top` port list is identical to the base: 205 ports, same names, same order, no `desc_mem_debt_o` (`receipts/15-top-port-list.txt`). The guard's `debt_o` ends at `desc_mem_debt_nc_w` (`hdl/top/protocol_processor_top.sv:3218,3231`). The bench observes it hierarchically (`tb/pp_top/pp_top_wrap.sv`). |

The full parent gates with the ratchet, `xvlog_gate` and the parent build are the manager's
job. See §7.

## 4. Lens evidence

### Conformance (CLEAN)

| Acceptance item (issue #94 plus scope decision) | Evidence at the exact head |
|---|---|
| The guard sits between the store master and the memory face | `hdl/top/protocol_processor_top.sv:3220-3232`. Its `m_*` face is the top's `desc_mem_*`, and its `s_*` face is `KL_aecp_engine`'s `mem_*` |
| `owed` is set on acceptance and cleared on a consumed `last` or `err` | `hdl/aecp/KL_aecp_desc_mem_guard.sv:69-78` |
| The next request is held while owed, and beats pass through | `:58-59` holds both handshake arms. `:63-67` passes the response through unchanged |
| Hard reset only; `debt_o` published on the guard port only (manager decision) | `:32,70` for the reset, `:54,80` for `debt_o`. The top port list is unchanged (receipt 15) |
| Late-beat case: an error or the locate's own descriptor, never another burst's bytes; a locate is served after the late burst | Guard suite `late_case`: the third locate returns `0005000011223344 5566778899aabbcc`, and so does the locate after the drain. Product top A12 checks byte-exact wire responses (receipts 01, 05) |
| Deleting the hold reddens it | The author's control fails the exact completed byte assertion with the wrong bytes `00060000deadbeef cafef00d01234567`, 17 PASS / 1 FAIL, make rc 2 (receipts 03, 03-mutant-no-hold). My single-arm and top-level mutants G1, G2 and T1 are also killed (§5) |
| The unguarded reproduction fails | `make baseline` gives rc 2 with the same wrong bytes and `overlap-accepts=1` (receipt 02) |
| Stuck memory: requests held, every locate a bounded error | Guard `stuck_case`: 5 locates, max 4,102 cycles against a bound of 4,160, debt held, no new accepts. Product top A13: 3 wire commands answer `NO_SUCH_DESCRIPTOR` in under 6,000 cycles each |
| Store suites stay green | `desc_store` 584/584 (receipt 04). Hosted CI at the exact head: 32 suites, 15,894 checks, 0 failing (receipt 12) |
| Area against T9's 5 LUT / 1 FF | Author's Vivado OOC: 4 LUT / 1 FF (public `author-r1b/area/util_hier.rpt`). My single-module Yosys cross-check: 5 LUT / 1 FF (receipts 09). Both are within the estimate |
| D3 roll-back cases deferred | They are stated as deferred in the PR body, `07 §3.3.1`, the integrator guide §4.1 and the guard banner. Nothing in the PR claims them |

### RTL (CLEAN)

`KL_aecp_desc_mem_guard.sv`:

- It is 82 lines, with one flop and no comb loop. `m_req_valid_o` and `s_req_ready_o`
  depend only on the registered `owed_r` and on the inputs. The store's `mem_req_valid_o`
  is registered.
- The handshake stays consistent on both faces. The store's `accept_w`
  (`valid && s_req_ready_o`) is true exactly when the memory's `m_req_valid_o && m_req_ready_i`
  is true. So when a store watchdog fires in the same cycle that debt clears, the store and
  the memory still agree. The store's `S_FET_REQ` gives `accept_w` priority over `tmo_hit_w`.
- Setting `owed` takes priority over clearing it. This is only reachable when a stray
  terminal beat arrives with no debt, and the documented contract excludes that ("responses
  start after request acceptance").

Other RTL checks:

- **No zero-beat bursts.** Every request site in the store
  (`KL_aecp_desc_store.sv:642,699,748,944`) issues at least one beat: the header is a
  constant; the index needs `hdr_n_entries_r ≥ 1` (`hdr_ok_w`); names are requested only
  while lanes remain; a fetch needs `e_usable_w`, meaning length ≠ 0. So a conforming
  memory cannot be left owing a burst that has no terminal beat.
- **Store behaviour is unchanged.** The only store change is a 4-line banner comment.
- **Lint.** `lint_hdl.sh` passes with zero tolerance, including `KL_aecp_desc_mem_guard`
  and `protocol_processor_top` (receipt 06).
- **Portability.** Yosys portability now lists the guard as a top. The hosted `portability`
  job succeeded at the exact head.
- **Banner.** The banner cites IEEE 1722.1 §7.4.5 and 07 §3.3.1, as `hdl/README.md` Rule 5
  requires.

### Robustness (CLEAN)

- **Finite late burst.** It drains, and service recovers byte-exact, both in the guard suite
  and on the wire (A12).
- **Never-ending burst.**
  - Debt holds indefinitely.
  - The store watchdog still bounds every locate: 4,102 cycles at most, and under 6,000
    wire cycles in the product top.
  - Heal walks and fetches are held rather than issued into the stale queue.
  - This is the stated design ("nothing is served stale").
- **Store-only reset.** Debt survives it and drains while the store is held in reset
  (guard suite). Mutant W1, which couples the guard reset to the store reset, is killed.
- **Hard reset.** It clears debt. The integrator guide §4.1 makes flushing the memory path
  (CDC queues included) an integrator obligation. The guard banner states that `err` ends
  a burst.
- **Terminal `err` without `last`.** It clears debt, and the next fetch is served
  (`terminal_error_case`).
- **Backpressure.** A backpressured terminal beat does not clear debt. The request stays
  held through the terminal cycle (`handshake_case`).
- **Throughput.** No new latency: the store only issues after its own `mem_busy_r` clears,
  which happens in the same cycle as the guard's clear.

### Tests (CLEAN)

- **Suites I ran at the exact head** with the verified pinned Verilator 5.050 (receipts
  00–05):

  | Run | Result |
  |---|---|
  | Guard suite | 77/77 |
  | Unguarded baseline | expected fail, 17/1, rc 2 |
  | Author mutation controller | rc 0, detected |
  | `desc_store` | 584/584 |
  | `pp_top` | 1,454/1,454 |

  The other 28 suites do not compile any changed file. The only RTL edits are the new guard,
  a store comment, and the top instantiation, which only `pp_top` builds. Hosted CI ran the
  full bank at this head: the `suites` job executed and succeeded with 15,894 checks and
  0 failing, and `docs-gates` and `portability` also executed and succeeded, for both the
  push and pull_request events.
- **Independence.** The guard bench's memory is an in-order FIFO that accepts requests while
  a burst is owed. The expected results are image bytes and transaction counts, not copies
  of the guard's logic. The product-top model was changed to an always-ready in-order FIFO,
  and its `dram_overlap_accepts == 0` is asserted cumulatively.
- **Discrimination.** I ran 11 mutants of my own (§5). Every one was killed by a completed
  assertion, and none by a build failure.
- **Rule 11/12 at file level.** Zero findings, with a positive control (§3).
- **Other gates.** `make check` (lint, wavedrom, 838 links, matrix, modmatrix, stale) and
  `gen_matrix.py --check` both return 0 in a clone with full history (receipts 07, 08).

### Docs (UNCLEAN, R290-2-F1)

Checked and correct:

- **07 §3.3.1** (`07_memory_maps.md:146-174`) and **integrator §4.1**
  (`integrator.md:111-146`) state:
  - the owed/hold/pass-through contract;
  - hard reset only;
  - `debt_o` as the D3 interface, on the guard port, not a top port;
  - the D3 writer's obligations;
  - the terminal-`err` and first-response-after-acceptance obligations;
  - flushing on hard reset;
  - the unchanged watchdog.
- **Anchors and single-source.** The two sections link to each other through the
  `sec-desc-memory` anchors. No timing or parameter value is copied, as the single-source
  rules require.
- **Suite and matrix docs.** `tb/desc_mem_guard/README.md` and the `tb/pp_top/README.md`
  A12/A13 entries match what the suites do (5 later locates, bound 4,160, 3 wire commands).
  `MODULE_MATRIX.md` is regenerated (46 modules, 0 untested).
- **Area note.** The `syn/ooc/README.md` area note matches the public report and says it is
  post-synthesis only.
- **SVG render.** The rendered head SVG for diagram 22 was inspected and has no overlap or
  clipping.

Open: the PNG renders are stale (F1).

## 5. Reviewer mutation probes (`scripts/01_mutants.py`, `receipts/mutants/`)

| Mutant | Edit | Suite | Result (first completed failing assertion) |
|---|---|---|---|
| G1 | drop only the `m_req_valid_o` hold | guard | KILLED, 18 FAIL: "finite late burst should drain in time to serve the third locate" |
| G2 | drop only the `s_req_ready_o` hold | guard | KILLED, 4 FAIL: "third locate late_beats_never_served" |
| G3 | `err` does not terminate | guard | KILLED, 4 FAIL: "err without last did not clear debt" |
| G4 | clear ignores response ready | guard | KILLED, 4 FAIL: "backpressured last must pass but not clear debt" |
| G5 | clear ignores response valid | guard | KILLED, 3 FAIL: "last without valid cleared debt" |
| G6 | set ignores request ready | guard | KILLED, 1 FAIL: "request without ready must not create debt" |
| G7 | `debt_o` tied to 0 | guard | KILLED, 15 FAIL: "stuck burst premise…" |
| G8 | `owed` never set | guard | KILLED, 19 FAIL: "third locate late_beats_never_served" |
| W1 | guard reset follows the store-only reset | guard | KILLED, 9 FAIL: "store-only reset cleared memory debt" |
| T1 | both holds removed, product top | pp_top | KILLED, 5 FAIL: "A12: late STREAM_OUTPUT bytes reached STREAM_INPUT on the wire" |
| T2 | `debt_o` tied to 0, product top | pp_top | KILLED, 5 FAIL: "A12: timed-out burst no longer owed" |

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #94 body and scope decision 5810666541; PR port decision 5811722803; guard, top and store diff; suites and receipts 01–05, 09, 15 | R290-2 | `cc077a6ffe20585d20b116f008e07189ba1bb7f8` |
| RTL | CLEAN | `hdl/aecp/KL_aecp_desc_mem_guard.sv`, `hdl/top/protocol_processor_top.sv:3207-3311`, `KL_aecp_desc_store.sv` handshake, watchdog and burst sites; lint receipt 06; single-module Yosys receipt 09; hosted portability job | R290-2 | `cc077a6ffe20585d20b116f008e07189ba1bb7f8` |
| Robustness | CLEAN | late, stuck, store-reset, hard-reset, terminal-err and backpressure cases (receipts 01, 05); mutants G3–G6, W1; zero-beat reachability analysis | R290-2 | `cc077a6ffe20585d20b116f008e07189ba1bb7f8` |
| Tests | CLEAN | `tb/desc_mem_guard/*`, `tb/pp_top` diff, `mutate.py`; receipts 00–08, 10, 12; 11 mutants in `receipts/mutants/` | R290-2 | `cc077a6ffe20585d20b116f008e07189ba1bb7f8` |
| Docs | UNCLEAN (R290-2-F1) | `07_memory_maps.md`, `integrator.md`, both diagram SVGs and PNGs, suite READMEs, `MODULE_MATRIX.md`, `syn/ooc/README.md`; receipts 07, 11, 14 | R290-2 | `cc077a6ffe20585d20b116f008e07189ba1bb7f8` |

After all probes, the review clone was verified against the exact head (receipt 13):

- HEAD, tree and index-tree are all `caa82293…`.
- `status --porcelain --ignored` is empty.
- Every tracked file was re-hashed on disk and matches its index blob and mode: 0 mismatches.
- The repository has no submodule gitlinks and no `.gitmodules`, so no gitlink needed checking.

Every probe ran on copies under `scratch/`. No product source was edited, and nothing was
committed or pushed.

## 7. Real limits and pending manager duties

Limits:

- **Parent receipts at `9d328810` are not in the public tree.** The evidence tree I was
  given (`802e90eb`, `pp94-r1`) contains only the author and author-r1b packets. In them,
  the parent `check_cpp_idiom`, `check_py_idiom` and `xvlog_gate --check` return **rc 2
  (REFUSED, pin mismatch)** at parent `5b2415f4`. I found no public manager receipt for the
  parent consumer gates at parent dev `9d328810` with this head as the gitlink.
  - My file-level scans (§3) show the Rule 11/12 populations are zero.
  - The full ratcheted parent gates, `xvlog_gate`, `check_rtl_source_lists`, `pp_srcs` and
    the parent `pp_shadow` build at `9d328810` still need a published manager receipt.
  - Note that `9d328810` pins protocol-processor `424c688f`, which is 40 commits behind this
    PR's base `008edbbf`.
- **OOC area.** The Vivado 4 LUT / 1 FF figure is the author's receipt. I did not run Vivado.
  My cross-check is a generic Yosys `synth_xilinx` map (5 LUT / 1 FF). Neither is routed
  timing.
- **Parent memory path not verified here.** Whether the parent's `pp_desc_bridge` and CDC
  FIFO honour the documented contract is outside this repository and is not checked here:
  - `err` terminates a burst;
  - the first response comes after the acceptance cycle;
  - hard reset flushes the queue.
- **Physical calibration NOT RUN.** Field skips are not hardware proof. No hardware was used.
- **Deferred to the D3 lane**, per the scope decision: the D3 roll-back cases (owners held on
  `debt_o`, deadline to CLOSED, 5,000/16,000-cycle cases, the owner-release mutant), and
  routing `debt_o` to the top and the parent.
- **Suites not re-run by me.** I did not re-run the other 28 suites, the NVM-figures gate,
  or the repository Yosys bank. For those I relied on the hosted exact-head jobs (executed,
  success) and the author receipts.

Pending manager duties:

- Get F1 fixed and re-reviewed.
- Publish the parent consumer gate receipts at the merge-turn parent base.
- Build and validate the final current-dev candidate (source base `008edbbf`, live dev
  `9d328810`).
- Hosted and act acceptance.
- Obtain the second independent review.

## 8. Receipts (all listed in `MANIFEST.sha256`)

- `scripts/`: `00_extract_and_suites.sh`, `01_mutants.py`, `02_guard_area_yosys.sh`,
  `03_idiom_scan.py`, `04_verify_clone.sh`.
- `receipts/00-*`: return codes, tree id and simulator version.
- `receipts/01-05`: the guard suite, the baseline, the mutation controller and its log, the
  store suite and the product top.
- `receipts/06-08`: lint, `make check` and the matrix check.
- `receipts/09-*`: the Yosys area cross-check.
- `receipts/10-*`: the idiom scans and the checker hashes.
- `receipts/11`, `receipts/14`: the diagram staleness evidence.
- `receipts/12-*`: the hosted check runs and suite excerpt.
- `receipts/13`: clone integrity.
- `receipts/15`: the top port list.
- `receipts/mutants/`: a diff, a log and a summary for each mutant.

Local absolute paths in the receipts are redacted to `$PACKET`, `$CLONE`, `$HOME`,
`$PINNED_BIN` and `$VERILATOR_PREFIX`.

R290-2 FINISHED
