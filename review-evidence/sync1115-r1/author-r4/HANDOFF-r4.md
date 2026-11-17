# HANDOFF r4: [A787] sync dev 6b66f66d into dev-soft-core, round 4 (#665)

Status: round-4 implementation and required validation complete at local head `c10c549e`, clean tree. The single round-4 [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6936610025) is posted on #665; nothing pushed. Round 3: REVIEW READY #665 issuecomment-6932432594, head `6ceed753`,
PR #934 (base dev-soft-core). Round 4 answers the external review's one MAJOR (PR #934 issuecomment-6932841237): the
LeaveAll check bound a timer's expiry to whichever participant's LeaveAll came first after it, so with two participants'
timers overlapping, MSRP's LeaveAll could skip its first transmit opportunity unseen behind MVRP's. The internal review
(R853-1, PR #934 issuecomment-6932499735) has only its start notice in the latest public check; no internal findings have been published.

## 1. The change, `c10c549e`

One commit on `6ceed753`: the harness's testbench and grading, its self-test and documentation. No firmware, RTL or
bound moves; no firmware hook is needed, since the owner is read from the CPU's register file.

- **The owner, recorded at the expiry** (`sim_main.cpp`, `note_owner` and `owner_of`; `observers.py`; `observe.vlt`):
  - the testbench reads VexiiRiscv's register file (`RegFileMem.asMem_ram`, made readable by `observe.vlt`) at
    function entries whose addresses `build.py` takes from the image's symbols (`observers.OWNER_HOOKS`);
  - lwSRP's three timers of a participant share one argument, its port's `timer_arg`. Inside `msrp_app_create` or
    `mvrp_app_create`, `shlan_timer_init` registers the LeaveAll timer (its callback `on_la_timer`, a1) with that
    argument (a2): the testbench holds it as that application's;
  - `srp_mbx.c`'s `create_participants` creates an interface's MSRP, then its MVRP, then publishes the interface's
    Domain, `mbx_pub_domain(index, false, ...)`. There the testbench binds the pair to interface `index`, printing
    `PARTICIPANT <cycle> <arg> if<n> MSRP|MVRP`. Anything but exactly one MSRP and one MVRP, or an index past the
    point's interfaces, is left unbound and printed `unbound`;
  - at each `on_la_timer`, `on_pt_timer` and `on_join_timer` entry, the testbench prints the owner of the callback's
    own argument (a0): `ENTRY <cycle> on_la_timer if0 MSRP`, or `unresolved <arg>`. Nothing is inferred from a later
    output.
- **The grading** (`grade.py`, `mrpdu_grade.py`, `join_grade.py`, `run.py`):
  - `grade.parse` keeps each timer entry's recorded owner (`Log.owners`) and each binding (`Log.participants`);
  - `mrpdu_grade.leave_alls` binds each LeaveAll expiry to its recorded owner (`owner`). From there everything is the
    owner's: its first transmit opportunity (`opportunity`, as round 3), its first MRPDU after the expiry, its
    LeaveAll. A LeaveAll of another participant answers nothing;
  - outcomes: `sent`, `skipped` (the owner committed an MRPDU without it first), `late` (past 49 ms after the
    owner's first opportunity), `absent` (no MRPDU of the owner's though the log runs past the bound), `unresolved`
    (the log ends first), and new, `unowned` (no owner recorded at the expiry, or recorded unresolved);
  - `skipped`, `late`, `absent` and `unowned` fail the run, each named by `run.leave_all_miss`; `unowned` reads
    "(LeaveAll owner unresolved)";
  - the LeaveAll's MRPDU row is timed on the owner's LeaveAll from the owner's first opportunity.
  - The 49 ms (`mrpdu_grade.LATE_MS`, from `ctrl_loop.h`) and the 20 ms row budget are unchanged.
- **The controls** (`selftest_leaveall.py`), synthetic held logs whose timer entries carry their owners:
  - **the reviewer's overlap**: MSRP's expiry at 1,050 ms, MVRP's at 1,190 ms; MSRP sends an MRPDU without the
    LeaveAll at 1,181 ms (its first opportunity, 1,180 ms) and the LeaveAll at 1,371 ms; MVRP's LeaveAll comes at
    1,221 ms, first after MSRP's expiry. It fails on MSRP, named at its 1,180 ms opportunity, 191 ms; MVRP's is sent;
  - **clean overlaps pass**: each owner's LeaveAll at its own first opportunity, in the expiries' order and reversed;
  - **both applications and both interfaces**: MVRP's skipped on interface 1, MSRP's late on interface 1, MVRP's
    absent on interface 0; interface 1's MSRP LeaveAll does not answer interface 0's MSRP expiry;
  - **unowned**: an expiry recorded `unresolved`, and one with no owner recorded, are named and fail the run;
  - round 3's single-participant controls, unchanged in substance: the opportunity timing (1 ms, where the run-out
    gives 131 ms), the idle join timer, skipped and late, another application's MRPDU, absent and unresolved, the
    parser on MSRP, its Listener and MVRP.
- **Mutants** (`selftest_mutants.py`): four new, round 3's eight kept, each caught.
  - new: the expiry bound to the participant whose LeaveAll comes first (the earlier rule); an expiry with no owner,
    or unresolved, taken for interface 0's MSRP; the interfaces not told apart; an unowned LeaveAll not failing.
  - The self-test names the first check a mutant fails. `per_check.py` lists all of them
    (receipts/budget/probe/per-check-at-c10c549e.txt): the earlier rule fails the reviewer's overlap control itself,
    and five other checks.
- **The docs:** the harness README (the owner record, the outcomes, "What this proves" and what it does not, the
  mutant table's sixteen transmit and LeaveAll rows as the self-test names their checks) and FR_NFR.md 3.4.1.

## 2. Phase reruns and limits

Eleven phases at 8x8/1if (the product MAC and ten harness-only seeds), each running save-held and save-starved with the new owner record. Both valid-destinations shapes are recorded. The inherited optional save-second run was cancelled deliberately after the required product-MAC save-held and save-starved traces completed; it is not part of this round's acceptance and is not claimed as a pass. Its cancellation is recorded in `receipts/budget/optional-save-second-cancelled.txt`. The two required traces are separately regraded with build attestation.

The ten seed clones retain their experiment base `10b2fe21` and have the exact `c10c549e` harness copied in. A full tracked-file comparison finds only the experimental MAC, three documentation files and two unrelated benches different from `c10c549e`; the harness matches byte for byte. No product source differs. The clean product-MAC and valid-destinations clones are at `c10c549e`.

All thirteen rebuilt firmware ELFs equal their earlier measurement ELF byte for byte. See `receipts/budget/source-and-image-identity.json` for every SHA-256 and size. This proves unchanged firmware inputs for the repeated legs, not identity of the changed observer executable.

Phase results: complete, each with its own recorded rc. All eleven phases and their 22 required save-held/save-starved groups have 44 owned LeaveAlls sent: zero skipped, late, absent, unresolved or unowned expiries. Every probe row is within its unchanged bound. Worst MRPDU rows (20 ms bound):

| Row | Worst ms | Phase / group |
|---|---:|---|
| LeaveAll | 1.64360 | seed 12102 / save-starved |
| Periodic | 2.96879 | seed 13602 / save-starved |
| Join | 1.86217 | seed 10592 / save-held |

The required 1x1/1if valid-destinations leg is rc 0, with both LeaveAlls sent. The additional 8x8 valid-destinations leg has both LeaveAlls sent and no budget-row miss. All twelve 8x8 legs retain rc 1 on the already recorded #914 STATED costs: two polls-base statements per required phase leg, and nineteen build/slice statements in the extra valid-destinations leg. These are not whole-leg passes and are not treated as debt or waived.

All 26 group traces are identical to their earlier executions after removing only PARTICIPANT records and the owner suffix from timer ENTRY records. No timer owner is missing or unresolved. The aggregate checker exits 0 and verifies each row, owner, outcome, trace comparison and bound; it does not override any run's rc. See `receipts/budget/phases-at-c10c549e.md`, its JSON, `phase-audit-at-c10c549e.txt`, and each leg's log/rc and trace extract under `receipts/budget/legs/`.



## 3. Gates and evidence

| Check | Head / scope | Result | Receipt |
|---|---|---|---|
| Harness self-test and mutants | clean clone of `c10c549e` | rc 0, 876 PASS checks, 258 mutants caught, 0 failures; all eight round-3 mutants and four round-4 mutants caught | `receipts/budget/selftest-at-c10c549e.txt` |
| Supplemental full owner matrix | clean `c10c549e` | rc 0, 24 controls across both applications and both interfaces | `receipts/budget/probe/owner-matrix-at-c10c549e.txt` |
| Reviewer overlap, with recorded owners | `c10c549e` | rc 0: MSRP fails at its original 1,180 ms opportunity (191 ms); MVRP passes; clean overlap passes; single late control fails | `receipts/budget/probe/r854-probe-owned-at-c10c549e.txt` |
| Reviewer probe unchanged | `c10c549e` | expected rc 1: ownerless log is refused as two unowned expiries, so the old escape assertion no longer holds | `receipts/budget/probe/r854-probe-as-written-at-c10c549e.txt` |
| Docs workflow steps | fresh clean clone per job at `c10c549e` | 63 steps rc 0; 34 NOT RUN with explicit orchestration/environment reasons; no missing or bad steps | `receipts/workflows/verify-docs-at-c10c549e.md`, `receipts/workflows/logs/` |
| 1x1/1if valid destinations | clean `c10c549e` | rc 0; two groups, zero refusals or budget misses; both LeaveAlls sent | `receipts/budget/legs/v1/` |
| Eleven 8x8/1if phases | exact head harness; harness-only MAC seeds | 44 owned LeaveAlls sent; 0 probe-row misses; every leg retains rc 1 for #914 STATED costs | `receipts/budget/phases-at-c10c549e.md`, `receipts/budget/legs/` |
| Aggregate phase audit | clean `c10c549e` grader | rc 0; all 26 traces unchanged except owner records; 49 ms conformance bound unchanged | `receipts/budget/phase-audit-at-c10c549e.txt` |

The self-test's full raw log exceeds 200 KB: its digest, size and verdict are in the receipt; the receipt includes every mutant and the LeaveAll controls.
One docs log exceeds 200 KB: its summary records raw digest and size. Every other docs step log and rc file is copied.
The docs runner takes each workflow's actual step list at the recorded head, records every skip, and checks each executed step's head and rc.
Earlier image, route, workflow and sweep receipts cited by the PR body are copied under `receipts/carried/`, with their original source heads and limitations. This is source-head evidence, not hosted or manager acceptance. The final candidate, independent re-review and merge remain the manager's.

## 4. Changed artifacts at `c10c549e`

All paths below are relative to `tb/verilator/ctrl_service_budget/`, except FR_NFR.

| File:line | Reason |
|---|---|
| `sim_main.cpp:335`, `:422`, `:444` | Read the callback's argument at entry and bind it through participant creation to its interface and application; emit that owner at expiry. |
| `observe.vlt:43` | Make the CPU integer register file readable by the testbench. |
| `observers.py:18`, `:30`, `:35`, `:45` | Describe the observed modules and symbol hooks, derive the generated model's member paths, and emit register access and owner-hook constants. |
| `build.py:33`, `:674`, `:750` | Use those observers when generating the testbench configuration. |
| `grade.py:110`, `:166` | Retain owner-bearing ENTRY records and participant bindings. |
| `mrpdu_grade.py:243`, `:249`, `:281` | Associate each expiry with its recorded owner and use that owner for opportunity, first MRPDU, lateness/absence and row timing. |
| `join_grade.py:85`, `run.py:186` | Count and report unowned expiries and the owner's skipped/late/absent result; fail the run. |
| `selftest_leaveall.py:107`, `:151`, `:199` | Keep single-participant controls; add overlapping and reordered timers, both applications/interfaces, and missing/unresolved ownership. |
| `selftest_mutants.py:881` | Plant the old future-output association and three other owner defects. |
| `README.md:148`, `docs/reference/FR_NFR.md:388` | State the actual ownership evidence, first-opportunity guarantee and unresolved/commit-level limits. |

| New control | Planted defect caught | Failing words / required outcome |
|---|---|---|
| Overlapping MSRP/MVRP expiries | Bind expiry to the earliest future LeaveAll (old association) | `two participants' timers overlapping`; actual MSRP at 1,180 ms, `LeaveAll past its first transmit opportunity`, 191 ms. |
| Clean overlap, ordered and legitimately reordered | Collapse applications, or time from LeaveAll expiry | `overlapping timers whose owners each send their LeaveAll at their own first opportunity pass`; both clean results must be two sent. |
| Skipped, late and absent across applications/interfaces | Ignore skipped/late/absent outcomes, or collapse interface | `skipped, late and absent LeaveAlls are named for either application on either interface`; named actual owner. |
| Same application on another interface | Collapse interface, or restore future-output binding | `the owner is its interface's too`; the actual interface's skipped result remains. |
| Missing and unresolved ownership | Default absent owner to if0 MSRP, or suppress unowned failure | `a LeaveAll timer's run-out with its owner recorded unresolved, or with no owner recorded`; `LeaveAll owner unresolved`. |
| Run verdict with recorded findings enabled | Suppress unowned or skipped failure | `a skipped or unowned LeaveAll fails a run whatever findings it records`; rc 1. |

Exact full check names and every covering mutant are in `receipts/budget/probe/per-check-at-c10c549e.txt`.
That focused diagnostic applies only the LeaveAll checks: its three unrelated earlier transmit plants are marked ESCAPED by this subset, but all are caught by their own checks in the full 258-mutant self-test. No full-suite mutant escaped.
The supplemental 24-case matrix applies all six scenarios to all four interface/application combinations (`receipts/tools/owner_matrix.py`); it is evidence alongside the committed controls, not a product change.


## 5. Open items and scope

- R854-001 has an author fix; its independent re-review is pending. This handoff grants no clean lens or approval.
- R853-1 has only its public start notice at the final check; no internal finding has been published. Independent review remains pending.
- The extra 8x8/1if valid-destinations run exits 1 on the already scoped #914 STATED build/slice costs. Its two LeaveAlls are sent, with no new conformance failure. It is not called a whole-leg pass.
- #898 still owns the 305 us paced SET_CONFIGURATION and CTRL_LOOP_TX_MS 35; neither changes here. #914 owns the remaining 8x8 cost statements. Regrade the composition after their merges.
- #919 owns the split PHY/1000BASE-T advertisement gap. #929 and #916 retain the earlier twin and srptx findings.
- Routes and earlier full gates remain evidence at their recorded source heads; round 4 changes no firmware, product RTL, numeric bound, configuration or submodule pin. The timing floor remains +0.030 ns setup / 0 ns hold at every corner, best of three.
- No push, PR edit, merge or hardware access was made. The only issue write in this resumed session is the single round-4 REVIEW READY on #665, issuecomment-6936610025. The TAKEN and earlier-round comments were not repeated or edited.

