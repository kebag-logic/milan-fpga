[R598] NEGATIVE - exact head 988ec7f653d0a21e0f7b40b03b8c74155d8962cf

# R598-1: internal cleared-context review of PR #722 (issue #640, Mark II lane M5 / plan L8)

- Head under review: `988ec7f653d0a21e0f7b40b03b8c74155d8962cf`, tree `8c80b6e209e642e4e345d0d7c0cda0b70702057d` (verified in the review clone; index tree equal; working tree and the three initialised submodules clean).
- Source base: dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (ancestor of the head). Measured product commit `1abe18eb`; `git diff 1abe18eb HEAD -- hdl syn sw configs` is empty, so the head's RTL is the routed RTL.
- Seven one-line commits, one parent each, no trailers.
- Authorities read: AGENTS.md, CONTRIBUTING.md (by reference), the issue body, the manager rulings D1/D3/D7/D8, the owner decisions, the M5 assignment (issue comment 6098404907), the TAKEN and REVIEW READY comments, REQUIREMENTS.md REQ-CSR-01..04, NFR-RES-01, `docs/design/MARK_II_AREA_PLAN.md` (L8, ledger), `docs/design/AREA_BUDGET.md` (gate policy), `syn/ooc/pp_resource_baseline.json` (route-1x1 record), the full diff `e8454e27..988ec7f6`, and the public evidence tree `review-evidence/640-m5-r1` at `648503cf` (HANDOFF.md and PR-BODY.md; both digests match its MANIFEST.json).
- Prior public review findings on PR #722: none exist. The only PR comment is the review-start notice (6105018560), and the PR has no reviews or review comments. Nothing is carried over.

**Verdict:** NEGATIVE, on one MINOR (Docs) only. The RTL change is correct and equivalent to the frozen block, and the tests are strong. Conformance, RTL, Robustness and Tests are covered clean at this head.

## Findings

### R598-1-F1: MINOR, lens Docs. The published attribution of the uncredited −690 double-counts nested scopes

- **Where:**
  - the live PR #722 body, line 55: "The routed whole image moved -690 LUT, but about -686 of that is in untouched blocks (`u_pp`, the processor wrapper) and is not credited.";
  - the published evidence `review-evidence/640-m5-r1/author/HANDOFF.md`, section 5 "Attribution" ("-344 in `u_pp` and -342 in the processor wrapper") and section 7 item 3 ("about -686 is in untouched blocks").
- **Authority and evidence:**
  - The gate's `wrapper` scope is the processor wrapper instance's *Total LUTs* row, and that total already includes `u_pp`:
    - `syn/ooc/pp_resource_gate.py:255-270` maps the root key to `wrapper`;
    - `syn/ooc/pp_baseline_rank.py:39-64` reads the "Total LUTs" hierarchy rows;
    - the record has `wrapper` 23,345 ⊇ `u_pp` 22,794 (`syn/ooc/pp_resource_baseline.json`).
  - So −344 (`u_pp`) and −342 (`wrapper`) are nested, and adding them to "−686" counts `u_pp` twice. The wrapper as a whole moved −342.
  - The same sentence also contradicts the PR body's own credited figure. "−686 of −690" leaves about −4 for `csr`, but the body credits `csr` with −121 (−121 − 686 = −807 ≠ −690).
- **Impact:**
  - The credited saving (121 routed, 127 post-synthesis, "about 125") is right.
  - The in-tree ledger sentence (`MARK_II_AREA_PLAN.md:1016`, "mostly the processor wrapper") is also right: −342 of the −569 outside `csr`.
  - But the evidence a cold reviewer or the week-4 re-measure reads for the uncredited movement states a figure that no route produced, and it cannot be reconciled with the credited figure.
  - This changes a figure, so it is not wording-only RESIDUE.
  - It is not attributed to Conformance: the acceptance item "report the measured saving honestly" is met by the ledger and by the credited figure.
- **Required outcome:** The PR body, and the HANDOFF if it is republished, state an attribution whose parts are disjoint and sum to −690. For example: `csr` −121; the processor wrapper −342 (`u_pp` −344 of it); all other scopes about −227. Alternatively, quote the per-scope routed deltas directly, with nested scopes marked as nested.
- **Verification:** The corrected text's disjoint parts sum to −690, and `wrapper` and `u_pp` are not added together.

### R598-1-S1: SUGGESTION, lens Docs. Say what the measured L8 figure does to the partial-central scenario

- **Where:** `docs/design/MARK_II_AREA_PLAN.md:1025` ("The cumulative tables keep the planning figure until the week-4 re-measure") against `:949-953`, `:969` and `:974`.
- **Evidence:**
  - The partial-central total `50,267 - 3,910 - 4,600 - 3,800 = 37,957` (+83 to 38,040) carries M5 at its 600 planning figure.
  - At the measured 121, that row becomes about 38,436, which is −396 to 38,040. "Partial central clears 38,040" then no longer holds.
- **Why this is not a defect:**
  - The ledger discloses that the tables carry planning figures.
  - D8 assigns the re-measure to week 4.
  - The REVIEW READY flags this as a manager decision.
- **Optional:** add one sentence beside the M5 measurement naming that consequence.

### Observations (not findings)

- **Stage-1 window gate.** The gate `(strm_hit || rd_in_window) ? live_mux : 0` (`milan_csr.sv:2656`) changes no value in today's map.
  - The reviewer equivalence probe `E-stage1-gate-dropped` (gate removed) survives the lockstep.
  - It is guarded instead by `milan_dp_mclk` mutant 13, which this review ran and saw caught.
  - The lane already discloses this (HANDOFF section 7 item 7).
- **Em dashes in the reference copy.** `tb/verilator/csr/milan_csr_ref.sv` adds 22 em dashes, all verbatim from the base block. Byte identity is enforced by `gen_lockstep.py`'s SHA-256 check (base blob sha256 `c3106a14…` reproduced here). The em-dash gate's scope is tracked `*.md`, and no added Markdown line carries U+2014.

## Lens results (each with its examined artifact at this head)

```text
[R598] PASS Conformance — issue #640 comment 6098404907 (M5 assignment) vs hdl/common/csr/milan_csr.sv:1078,1462-1469,2289-2664,2923-3053; docs/design/MARK_II_AREA_PLAN.md:538,992-1027; REQUIREMENTS.md REQ-CSR-01/02; receipts/csr_suite.log, receipts/lock_variant_{a,b,c}.log — scope is the read path only; port list, addresses, widths, reset values, access semantics and snapshot coherence are unchanged; AXI-Lite read latency is unchanged; no register-map change; the measured saving is reported below the 400-1,000 range with only the scope credited
[R598] PASS RTL — hdl/common/csr/milan_csr.sv:1106-1107,1116-1161,2300-2505,2526-2600,2609-2664,2923-3053 vs base e8454e27; receipts/lint_{head,base}_n{1,8}.log, receipts/lint_rtl_check.log — the old four-way select order is preserved; at most one stage-2 operand is nonzero; kinds are written in the word's cycle and branch; the N_LISTENERS_P>1 arm is unreachable at N=1; no CDC; lint warning sets are identical, base vs head
[R598] PASS Robustness — tb/verilator/csr/sim_lock.cpp:435-457,603-631,646-676; receipts/lock_variant_{a,b,c}.log, receipts/csr_suite.log — reset with a read in flight, periodic resets under random traffic, out-of-range/talker/listener SNAP ordering, unaligned and >=0x1000 addresses, random RREADY/BREADY backpressure, and feature-disabled parameter sets (gPTP off, CHMAP_RDBK_P 0, PPS on, N_L != N_T) all lockstep-equivalent
[R598] PASS Tests — tb/verilator/csr/{gen_lockstep.py,sim_lock.cpp,lock_mutants.py,Makefile:68-163}; receipts/csr_suite.log (lane 8/8), receipts/r598_mutants.log (reviewer 10/10 killed by named checks, plus 1 disclosed equivalence probe) — the oracle is SHA-pinned to base, the top is generated from the port list, every output is compared every cycle, and every defect class can fail its named check
```

Docs: UNCLEAN under R598-1-F1. These parts were also examined and found correct:
- `hdl/common/csr/doc/milan_csr.md:147-170`: the signals and processes match the RTL; "three cycles after the AR handshake" matches `:1116-1161`;
- `tb/verilator/csr/README.md:34-35,84-96`;
- the `tb/verilator/csr/Makefile` header;
- `scripts/measure_test_evidence_readers.py:174-178`;
- `docs/design/MARK_II_AREA_PLAN.md:538,992-1027`: every figure checked against the HANDOFF tables, and the WNS-fall arithmetic against `AREA_BUDGET.md:396-405`;
- `docs/reference/REGISTER_MAP.md`: unchanged, and its `rd_in_window` carve-out text still holds.

### Equivalence argument (RTL)

- **Live tree has no window overlap.** No live case arm or range in `read_mux` lies in 0x800-0x86F:
  - the first live address at or above the window is `A_LTAP_CTRL = 0x870` (`:922`);
  - the PP override is 0x920-0x930.
  - So the new `else if (strm_hit)` leaf (`:2487`) is reached exactly when the old `strm_hit_q` arm won, and it sets `live_hit`.
- **Zero where unclaimed.** `live_hit = 0` only in the final `else`, where `live_mux` keeps its default 0. Therefore `live_mux` is 0 wherever the old select would have chosen the shadow.
- **Shadow only where it served before.** `shadow_qq` is nonzero only when `rd_in_window && !live_hit` (`:2635-2641`). That is the old shadow arm, because `rd_in_window` is false throughout 0x800-0x86F (bit 11 set).
- **Out-of-window reads stay 0.** Stage 1 keeps the old "0 outside `rd_in_window`" order (`:2656`).
- **SNAP kinds.**
  - The kinds reproduce the old stored values on read:
    - an out-of-range SNAP gives ZERO;
    - listener idx0 gives RAW of the same `i_avtprx_cnt10` latch;
    - talker idx0 and extra talker contexts give POISON;
    - a listener burst gives RAW with the word.
  - Words not rewritten keep their previous kind exactly as they previously kept their previous value.
- **Burst arm reachability.** The `N_LISTENERS_P > 1` arm is unreachable otherwise, because `win_in_range_w` (`:1106`) restricts the listener index below `N_LISTENERS_P`, and idx 0 takes the flat branch.
- **Handshake unchanged.** `rd_fire`/`rd_pend`/`rd_pend2`/`r_valid` (`:1116-1161`) are untouched, so RVALID timing is the same. The lockstep compares RVALID and RDATA every cycle.

## Executed evidence (this review, at the exact head, in disposable copies)

All suites used the pinned Verilator 5.050 (wrapper sha256 `905795b9…`, `receipts/tool_identity.txt`).

| Run | Result | Receipt |
|---|---|---|
| CSR suite `make -j16 run`: 6 earlier legs, `lock1`, `lock8`, reset bits, `lock_mutants.py` | rc 0. lock1 5/5, 340,861 cycles, 28,167 random reads; lock8 5/5, 374,265 cycles, 22,750 random reads; 0 mismatching cycles. Mutants 8/8 (control + 7). These reproduce the author's figures exactly. | `receipts/csr_suite.log`, `.rc` |
| Reviewer mutants (`probes/r598_mutants.py`): 2 of the lane's classes re-applied in a different form (decode at PTP_TRHI; torn PDUS) and 8 new mutants in the lane's change | 10/10 KILLED by the expected named check. The equivalence probe (stage-1 gate dropped) SURVIVED, as predicted. | `receipts/r598_mutants.log`, `.rc` |
| Lockstep at non-shipping parameters (`probes/lock_variants.mk`): a = 1x1 at 125 MHz, gPTP off, CHMAP_RDBK 0, PPS on; b = 4x4 with gPTP and PPS on; c = N_L 4 / N_T 2, gPTP off | rc 0, 5/5 each, 0 mismatching cycles | `receipts/lock_variant_{a,b,c}.log`, `.rc` |
| `tcam_csr` | rc 0, 2/0 | `receipts/suite_tcam_csr.log` |
| `milan_dp` shipping AX 1x1 leg (`make ax1x1`) | rc 0, 233 checks / 0 failures (5 pre-existing shape guards) | `receipts/suite_milan_dp_ax1x1.log` |
| `milan_dp` 8x8 `obj_nxn8` leg (`probes/nxn8_leg.mk`, suite variables) | rc 0, 3,751 / 0 | `receipts/suite_milan_dp_nxn8.log` |
| `milan_dp_mclk` (`make run`: leg + campaign) | rc 0, 31/31, mutant 13 "read-window terms missing" caught | `receipts/suite_milan_dp_mclk.log` |
| Lint, `milan_csr` alone, `-Wall`, shipping 1x1 and 8x8, head vs base | 76 vs 76 warnings in each shape; identical sets | `receipts/lint_*` |
| `scripts/lint_rtl.py --check` | PASS, 90 ≤ ratchet 90 | `receipts/lint_rtl_check.log` |
| Repository gates in a scratch clone: feature status, entity shape and its self-test, test evidence, naming, sv/py/cpp idiom, port contracts, fail-fast, hygiene, RTL source lists, resource `check-baseline`, `git diff --check e8454e27 HEAD` | all rc 0 | `receipts/gate_*` |
| Docs gates: `docs_check`, doc style, doc paths, DOC_MAP, module matrix | rc 0 | `receipts/docgate_*` |
| Docs gates: em dash, TOC check, TOC anchors | rc 2: "cannot judge", because the pinned Markdown renderer is not installed here. Not a pass. These rest on hosted `docs-check` (success at the head) and the direct added-line check above. | `receipts/docgate_*` |

**Hosted, exact head** (`receipts/hosted_check_runs.tsv`, polled 2026-10-11T04:04:38Z):
- Success: `rtl-fast`, `verilator-lint`, Verilator shards 0/5 and 3/5, `yosys-elaboration`, Yosys shards 0-3, `elaborate`, `firmware-unit`, `bdd-conformance`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `changes`, `full-ci-gate`.
- Still in progress at the poll: Verilator shards 1/5, 2/5 and 4/5.
- Skipped context, not executed: "Physical gPTP (nightly and manual)".
- The manager owns hosted and act acceptance.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | M5 assignment 6098404907; `milan_csr.sv` read path and SNAP FSM; REQ-CSR-01/02; plan L8 and ledger; lockstep receipts | R598-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |
| RTL | CLEAN | `milan_csr.sv:1078-1161,1462-1469,2289-2664,2923-3053` vs base; lint head/base; lint ratchet | R598-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |
| Robustness | CLEAN | `sim_lock.cpp` reset, freshness and random phases; 3 non-shipping parameter variants; mclk read-window control | R598-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |
| Tests | CLEAN | `gen_lockstep.py`, `sim_lock.cpp`, `lock_mutants.py`, Makefile; lane 8/8; reviewer 10/10 + 1 equivalence probe | R598-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |
| Docs | UNCLEAN (R598-1-F1 MINOR open) | `milan_csr.md`, csr `README.md`, Makefile header, `measure_test_evidence_readers.py`, `MARK_II_AREA_PLAN.md`, live PR body, published HANDOFF | R598-1 | `988ec7f653d0a21e0f7b40b03b8c74155d8962cf` |

## Real limits of this review

- No Vivado run. The route figures are the author's published receipts, not reproduced here:
  - route-1x1 49,577 LUT / WNS +0.097 against the record 50,267 / +0.299;
  - the WNS fall of 0.202 is within the 0.25 limit (`AREA_BUDGET.md:404`);
  - `csr` scope 3,037 → 2,916.
  - The gate record values and the policy were checked in the tree.
- No 8x8 integrated synthesis exists from anyone. The 8x8 shape rests on OOC figures (author) and on the `lock8` and `obj_nxn8` simulations (run here).
- The selected-split placement is not measured. Split parity rests on the author's elaboration identity. This review confirmed only that the `milan_csr` instance in `milan_datapath.sv:2445-2472` takes no placement parameter.
- Not run locally:
  - the full `milan_dp` suite (only its two shipping legs);
  - `milan_dp_render`, `capture_coherence`, `follow_ring`, `pp_shadow`, `milan_dp_gptp`;
  - firmware host tests and `behave` (hosted `firmware-unit` and `bdd-conformance` succeeded at the head; the diff touches no firmware or register-map file);
  - Yosys (a forbidden bank here; hosted Yosys contexts succeeded).
- Physical calibration was NOT RUN. Field and nightly skips are not hardware proof. No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Carry R598-1-F1 to the executor (PR body / HANDOFF attribution).
- Rule on R598-1-S1 at the week-4 re-measure.
- Accept or reject the hosted Verilator shards 1/5, 2/5 and 4/5 at the exact head; they were still running at this review's last poll.
- Build and validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with its builder and native banks, and link the receipts.
- Collect the external review (R599). Both positives are required.
- Post-merge: the plan's bench boot readback, and containment.

Packet: `REPORT.md`, `MANIFEST.sha256`, `probes/` (reviewer scripts) and `receipts/` (raw logs and rc files; home-directory paths redacted). `scratch/` is not published.

R598-1 FINISHED
