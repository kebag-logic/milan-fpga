[R648] NEGATIVE - exact head 42eb9aef3642f6d98058fe634a70f6a9c749cd25

# R648-1 independent review: issue #181 / PR #187 (notify-queue to event-router cut)

- Reviewed: exact head `42eb9aef3642f6d98058fe634a70f6a9c749cd25`, tree `f7319d373b083043cf896a68712302f640212838`. This is the author head `16c89c53` on main `22c139a4` plus the manager's merge of main `77cf6fb4`.
- Reviewer: R648 (internal reviewer, cleared context, own detached clone). Round R648-1.
- Scope sources, in order: the repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `docs/README.md`; issue #181's body; the [A10] assignment (comment 6241709741); TAKEN and REVIEW READY; the [A10] ruling on acceptance item 1 (comment 6249065327), which replaces item 1 with "the cone no longer limits the shipping timing gate"; the PR #187 body; `git diff 77cf6fb4..42eb9aef` and its history; and the published evidence at `kebag-logic/milan-fpga@5131f4ad` `review-evidence/pp181-r1`.
- Prior public review findings on PR #187: **none**. At this head the PR has only the two START comments (R648-1, R649-1): no review, no review comment, no findings page. There is nothing to resolve or retain.
- No manager source bank ran at this head, and none is claimed or inferred here. Source-head execution evidence is the author's published receipts, plus my own focused runs listed below.

## Verdict summary

The RTL change is correct and does what the ruling asks of it:

- The cut is real at both module boundaries.
- The router is sequentially equivalent to base at 10 shapes.
- The notify occupancy flop provably equals `cmdq_count_r != 0` after reset at three shapes. Since the head differs from base only by that flop and its two readers, every notify port is unchanged.
- Notification order, content and loss behaviour are therefore unchanged: every notification is still sent, in order, to every registered controller (Milan v1.2 §5.4.5, IEEE 1722.1-2021 §7.5.2).
- No cycle of latency is added, so the documented service bounds stand.
- There is no port, parameter or register-map change.
- The merge reproduces the exact tree and keeps both sides byte for byte.

Two MINOR findings keep the verdict NEGATIVE:

- **F-1:** the timing figures and the behaviour proofs the PR rests on have no published receipts.
- **F-2:** the occupancy flop is new duplicated state. Every in-tree gate passes when its push/pop rules are broken, so only the author's unpublished, out-of-tree proof keeps it in sync.

## Findings

### F-1 - MINOR - Lenses: Tests, Docs - the OOC, routed and proof figures are not reproducible from published receipts

- **Where:** `syn/ooc/README.md:241-285` (the new "notify-queue to event-router cone" record), and PR #187's "Behaviour", "Depth" and "Routed" sections. The published evidence `review-evidence/pp181-r1` holds exactly three files: `MANIFEST.json`, `author/HANDOFF.md` and `author/PR-BODY.md` (`receipts/published_evidence.txt`).
- **Authority / evidence:**
  - The review brief requires the OOC and routed measurements (route-1x1 with #760 at +0.144 ns versus base +0.016 ns) to be reproducible from the published receipts.
  - The ruling closes #181 on the routed figure ("+0.016 ns ... to +0.144 ns, and the worst path leaves this cone").
  - Every figure exists only as prose tables. No `report_timing` output for the four from/to pairs, no utilization or hierarchy report, no route-1x1 timing summary or resource-gate log, no scratch-parent composition record (parent dev sha, gitlink sha, #760 patch digest), no Yosys proof script or log, and no campaign log is published. HANDOFF says they are "under the lane's scratch root", which is not published.
  - The base figure in parent milan-fpga #760 comment 6241681577 is also prose only.
  - This host has no Vivado, so I could not re-derive any of these figures independently.
- **Impact:** nobody outside the author lane can check the timing claims behind the ruling: 22 vs 32 levels, WNS -5.416 / -11.482 / -6.045, +0.181 / +0.144 routed, and "no path". The same holds for the author's proof claims (91/205/286/505/859 cells, the N1-N3 / R1-R3 kill words). I reproduced the proofs independently (see the behaviour evidence below), but not the timing.
- **Required outcome:** publish raw receipts under the PR's evidence directory and link them from the PR:
  - the OOC `report_timing` text for each row of the `syn/ooc/README.md` table at 1x1 and 8x8, base and head, with the exact commands;
  - the three route-1x1 timing summaries and resource-gate logs, with the scratch parent's composition (dev `7d79ffb2`, gitlink sha, #760 head `22840662` patch sha256) and the Vivado build;
  - the equivalence and induction scripts and logs, and the planted-mutant logs.
- **Verification:** a reviewer re-derives every figure in `syn/ooc/README.md:258-271` and every row of the PR's routed table from the published files alone.

### F-2 - MINOR - Lenses: Robustness, Tests - the new duplicated occupancy state is guarded by no in-tree check

- **Where:**
  - `hdl/aecp/KL_aecp_notify.sv:429` declares `cmdq_nempty_r`.
  - Its writes are at `:1196` (reset), `:1299` (push) and `:1511` (pop without push).
  - Its readers are `:832` (the emission pick) and `:1165` (`amap_busy_o`).
  - The only unit bench, `tb/aecp_notify/sim_main.cpp:804-824`, pushes one command notification per round.
  - `docs/architecture/06_aecp_engine.md:1001-1004` documents that the queue holds "at most the pushes of the command that was running", and that a full queue would be dropped and counted in `cmdq_drop_r`, which no port reads.
- **Authority / evidence:**
  - Assignment item 2 ("suites stay unchanged and passing" as the evidence that no behaviour changes).
  - The review brief: the suites must cover notify ordering, back-to-back commands and queue full, and every new or changed check needs a planted mutant that fails it.
  - Base computed occupancy from the count, so it could not drift. Head adds a second state bit that every count update must keep equal to `count != 0`; the comment at `:426-428` states this invariant, but nothing in the tree enforces it.
  - My planted mutants (`receipts/mutant_matrix.txt`, diffs in `receipts/mutant_N*.diff`):
    - **N7** (pop clears the occupancy at once, so later queued entries are stranded) and **N4** (a pop beside a push clears it) pass `tb/aecp_notify` (67/67) and every section of `tb/pp_top`'s main build. Those sections are Suite with the arm queue, NP/ST/RN, gsi, name writes, d3, volatile, cuts, acmp, adp, aecp dispatch/response, deadlines, hazards, identify, spacing, domain notify, withdraw and counters: 0 FAIL lines. Only the out-of-tree occupancy induction kills them (`receipts/nfy_inv/N4_1x1.out`, `N7_1x1.out`).
    - **N5** (`amap_busy_o` drops the occupancy term) passes every suite and the induction too.
    - **N1, N2, N3 and N6** are killed by `tb/aecp_notify` (DR2/DR2b, TS/TW).
  - The two base equivalents also survive (**B5**: `amap_busy_o` without the count term; **B7**: a pop empties the count). So the multi-entry and push-beside-pop regime was untested at base as well. What is new is the drift risk.
- **Impact:** the behaviour is correct at this head; I proved it (see the behaviour evidence below). But a later edit can desynchronise the flop from the count with every in-tree gate green: a flush path, a new push site, or a pop-rule change. That would strand or reorder queued notifications, which are Milan v1.2 §5.4.5 / IEEE 1722.1-2021 §7.5.2 obligations. It would also break the `amap_busy_o` hold that the 06 text relies on for losslessness. The PR's acceptance evidence for "no behaviour change" on these rules is an out-of-tree proof that is not published (F-1).
- **Required outcome:** one of the following.
  - (a) Put the occupancy invariant and the router equivalence into the tree as a gate run by `make check` or CI. Each takes about a minute; `scripts/nfy_inv.sh` and `scripts/evr_equiv.sh` in this packet are a working model. Record N1-N4, N6 and N7 (and R1-R5) as planted mutants that fail it.
  - (b) Add a `tb/aecp_notify` section that queues several command notifications back to back, up to the `P-NOTIF-QUEUE-DEPTH` depth and one past it, with a push in the cycle of a pop. It should check that every entry is emitted in order to every registered controller and that `amap_busy_o` holds until the last claim. N4, N5 and N7 must be recorded as killed by it.
  - (c) A manager ruling that accepts the published out-of-tree proof for this PR and opens a tracking issue for the in-tree guard.
- **Verification:** apply `receipts/mutant_N4.diff`, `mutant_N5.diff` (for b) and `mutant_N7.diff` to a copy of the head. Each must fail the new gate or section, and the head must pass it.

### RES-1 - RESIDUE - Lens: Docs (PR text) - the PR body's closing statement is superseded by the ruling

- **Where:** the first paragraph of PR #187's body ("Refs #181. This PR does not close the issue, because acceptance item 1 is not met ...").
- **Evidence:** the [A10] ruling (issue comment 6249065327) replaces item 1 and says the PR may close #181 once both reviews are POSITIVE and the banks pass.
- **Exact fix:** replace the paragraph with: "Closes #181. Under the [A10] ruling on acceptance item 1 (issue comment 6249065327), item 1 is replaced by its purpose: the cone no longer limits the shipping timing gate. The depth target is not met (22 levels OOC, 24 routed); the measurements are below."
- This is wording only: no figure, test or code changes.

### S-1 - SUGGESTION - Lens: Docs (source comment) - `hdl/packet_engine/KL_pp_event_router.sv:104-105`

The pre-existing lines still say the scan works from "the REGISTERED pending set minus the event delivered this cycle; base = one past the delivered source". The scan is now keyed on the *presented* event; the new paragraph at `:110-117` qualifies this, but the first sentence alone reads as the old scan. Consider "minus the presented event (it leaves on its delivery); base = one past the presented source".

### S-2 - SUGGESTION - Lenses: Tests, Docs - idle select hold, and the "worst path" wording in the OOC table

- **R5** (when no grant is found, the select clears instead of holding) is killed only by the equivalence proof. `tb/event_router` and `tb/pp_top` pass it. `evt_src_o` and `evt_payload_o` while `evt_valid_o` is 0 are probably a don't-care. If they are part of the contract, a router check that pins them would close the gap.
- **Wording:** in `syn/ooc/README.md:261-262`, the row "Worst path from `cmdq_count_r`: 2 levels" sits above a 3-level `cmdq_count_r` to `cmdq_nempty_r` row. Saying "worst (least slack)" would remove the apparent contradiction.

## Behaviour evidence (reviewer-run, this packet)

Everything below ran on `git archive` exports of `42eb9aef` (head) and `77cf6fb4` (base) under scratch. Tool identities:

- Verilator 5.050 (`2026-07-01 rev v5.050`), the pinned wrapper, sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`;
- sv2v v0.0.12, sha256 `b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b`;
- host Yosys 0.66.

**Router equivalence** (`scripts/evr_equiv.sh`; `receipts/evr_equiv/`):

- Method: base against head. Every port and register is matched by name; the internal `*_w` wires, which differ by design, are hidden first. Then `equiv_simple -seq 2`, `equiv_induct -seq 2`, `equiv_status -assert`.
- Result: all cells proven, 0 unproven, at `N_SRC_P` 1, 2, 3, 4, 5, 7, 8, 16, 29 and 32 (89 / 115 / 144 / 170 / 199 / 251 / 277 / 488 / 829 / 907 cells).
- Mutants R1-R5 each fail it at N = 5, 8 and 16:
  - R1: the base is always `ptr_r`;
  - R2: the presented event is not removed;
  - R3: the load ignores the acknowledge;
  - R4: the select reloads outside the enable;
  - R5: no grant clears the select.
- R6, a semantically equivalent mix (removal keyed on `deliver_w`), passes as expected. This confirms the "a load only happens on delivery or from idle" argument.

**Notify occupancy invariant** (`scripts/nfy_inv.sh`; `receipts/nfy_inv/`):

- Property: `cmdq_nempty_r == (cmdq_count_r != 0)`, proven by 1-step temporal induction after the reset cycle, at three shapes: 1 in / 1 out; the default shape; and 1/1 with `N_IF_P=2, EN_IDENTIFY_NOTIF_P=1`.
- Mutants N1, N2, N3, N4, N6 and N7 fail it. N5, a reader mutant, is outside the property's reach (F-2).
- Structural diff (`git diff 77cf6fb4..42eb9aef -- hdl/aecp/KL_aecp_notify.sv`): the only edits are the flop, its three writes, and the two reads that replace `cmdq_count_r != 5'd0`. With the invariant, every notify port equals base in every cycle.

**The cut at RTL level** (`scripts/cone_check.sh`; `receipts/cone/`):

| | `cmdq_count_r` combinationally reaches notify outputs | `evt_ack_i` combinationally reaches the router scan |
|---|---|---|
| Base | `amap_busy_o` | `gnt_found_w`, `gnt_src_w`, `base_w`, `pend_after_w` |
| Head | none | none |

At head the acknowledge only feeds the existing load enable.

**Suites that build a changed file, head and base** (`receipts/suites/`): identical tallies, all rc 0.

| Suite | Head | Base |
|---|---|---|
| `tb/event_router` | 81/81 | 81/81 |
| `tb/aecp_notify` (5 runs) | 67/67 | 67/67 |
| `tb/pp_top` (all 7 builds) | 10505/10505 | 10505/10505 |

**Mutants against the suites:** listed in `receipts/mutant_matrix.txt` (logs in `receipts/mut_suites/`, `receipts/mut_pp_top/` and `receipts/base_mut/`).

**Gates** (`receipts/gates/`):

- `scripts/lint_hdl.sh` rc 0 at head and base, 41 `LINT OK` lines, logs identical.
- `make check` rc 0 at head and base in scratch clones, logs identical, worktree clean afterwards.

**Merge** (`receipts/merge/`):

- `git merge-tree --write-tree 77cf6fb4 16c89c53` gives `f7319d37...`, the head tree.
- The author side (`22c139a4..16c89c53`) equals `77cf6fb4..42eb9aef`, and the main side (`22c139a4..77cf6fb4`) equals `16c89c53..42eb9aef`, apart from index and hunk-header lines.
- The one overlapping file, `docs/architecture/06_aecp_engine.md`, merged in disjoint hunks.

**Interfaces:**

- No hunk touches a port list, parameter, `protocol_processor_top.sv`, `docs/architecture/07_memory_maps.md` or the side-port.
- The five changed files are the two RTL files, `03_packet_engine.md`, `06_aecp_engine.md` and `syn/ooc/README.md`.
- No #176, #177 or #178 decode path is touched.

**Comment rule:** the new source comments state behaviour and reason and cite issue #181. The delta has no bench lane label, lane name, review round, reviewer ID or issue-comment ID (the scan's only hits are "round-robin").

**Hosted** (`receipts/hosted/summary.txt`, snapshot 2026-10-18T12:13:23Z, exact head):

- `docs-gates` success and `portability` success in both workflow runs (39121683333, 39121667584).
- `suites` was still in progress in both. No hosted suites result is claimed.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Milan v1.2 §5.4.5 / IEEE 1722.1-2021 §7.5.2 notification order, content and loss, via router equivalence (10 shapes) and the notify invariant (3 shapes) plus the structural diff; no port, parameter or register-map change; #176/#177/#178 paths untouched; merge keeps both sides | R648-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |
| RTL | CLEAN | `KL_aecp_notify.sv` (flop, 3 writes, 2 reads), `KL_pp_event_router.sv` (scan keyed on `valid_r`, `sel_next_w`, enable unchanged); RTL cone check at base and head; `lint_hdl.sh` identical | R648-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |
| Robustness | UNCLEAN (F-2) | the drift risk of the duplicated occupancy state; N4/N5/N7 surviving all in-tree suites; base equivalents B5/B7 | R648-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |
| Tests | UNCLEAN (F-1, F-2) | `tb/event_router`, `tb/aecp_notify` and `tb/pp_top` at head and base; 13 head mutants and 2 base mutants against suites and proofs; published evidence directory contents | R648-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |
| Docs | UNCLEAN (F-1); RES-1 carried | `03_packet_engine.md:227-231`, `06_aecp_engine.md:998`, `syn/ooc/README.md:241-285`, the PR body, `make check` identical | R648-1 | 42eb9aef3642f6d98058fe634a70f6a9c749cd25 |

## Real limits

- I reproduced no OOC or routed timing figure. This host has no Vivado and no raw report is published (F-1). The ruling's +0.144 ns and the README's OOC tables stand on the author's prose alone.
- I did not run the full `scripts/run_suites.sh` sweep, the mutation campaigns (`notify_mutants.py`, `d3_mutants.py` and the others), `check-req-tags.py --suites --evidence`, `gen_matrix.py --check` on its own, `syn/yosys/run.sh`, the elaboration guards, or any parent consumer gate. The brief excludes full banks. The author's tables for these are unverified here.
- Mutants were run against `tb/pp_top`'s first (default) build only, not its six override builds (VID, identify, line, real timebase, timer defaults, two interfaces).
- The proofs use host Yosys 0.66, not the CI image's 0.33. The router proof's matched-register method differs from the author's: its cell counts are mine.
- The hosted `suites` job was in progress at the snapshot.
- Physical calibration NOT RUN. No hardware claim is made.

## Pending manager duties

- The current-dev merge-candidate builder and native banks at the merge turn (source base `77cf6fb4`, live dev `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`), with receipts linked on the PR.
- Hosted/act acceptance, including the in-progress `suites` jobs at `42eb9aef`.
- The parent consumer gates, and the re-measure of route-1x1 on the next pin adoption's image, as the ruling records.
- Disposition of F-1 and F-2, and RES-1 on the residue checklist.

## Packet

- `scripts/`: the portable probe scripts. Paths are arguments, and tool paths can be overridden by environment variables.
- `receipts/`: raw logs, rc files and the summaries cited above. The full Yosys induction logs (16-32 MB each) are kept as excerpts that name each full log's sha256.
- `MANIFEST.sha256` lists every published file except this report.
- After the probes, the review clone was verified: HEAD and tree exact, `git status` empty, worktree equals index equals HEAD in blob bytes and modes (632 files), and no gitlinks in the tree (`receipts/integrity/clone_integrity.txt`).

R648-1 FINISHED
