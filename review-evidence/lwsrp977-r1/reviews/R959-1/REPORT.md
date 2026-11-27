[R959] NEGATIVE - exact head 73007b4807977517045e8aa485c61ebb8f5ee843

# R959-1: independent review of kebag-logic/lwSRP PR #22 (for kebag-logic/milan-fpga#977)

- Head: `73007b4807977517045e8aa485c61ebb8f5ee843` (tree `eeb3e733b50398a056f5b52325168959c280f45f`), branch `opt-exec-3`.
- Base: `main` `d1bb4f4e5954af6dabe7f210a6bf7adbb76bdd6b`. Delta: 20 commits, 20 files, +2439 / -63.
- Round: R959-1, a cleared-context internal review. It started at the public notice on PR #22 (issuecomment-7210516656).
- Scope reconstructed from: CONTRIBUTING.md and README.md (the repository has no AGENTS.md); doc/ guides; issue #977's body and maintainer/manager comments (the 2026-11-22 acceptance, the 2026-11-23 ruling, the round 2 to 7 STOPs and rulings); the PR body; the full diff and history; the author packet `review-evidence/lwsrp977-r1` at milan-fpga `94f4d347` (all 18 files match MANIFEST.json's sha256).
- Not read: private author material, lane scratch, management directories, other reviewers' reports.

## Verdict

NEGATIVE. The code is sound. With every option off, behaviour is main's: the traces are identical, and the objects are byte-identical at -O2, -Os and -fPIC. With each option on, I found no departure from IEEE 802.1Q-2018 clause 10 or 35.2, or from Milan v1.2 4.2.7, and I re-derived every Applicant and Registrar table cell the options rely on.

The verdict is NEGATIVE for six reasons:
- one MAJOR: a committed bytecode file carries a private host path;
- five MINORs: the one-port option's documented difference has no killing test; the reversal and planted-defect counts are wrong; the application-callback contract changes are not stated; and the "default objects are main's" claim needs qualifying.

## What I ran (exact head, clean clone; receipts listed in MANIFEST.sha256)

| Gate | Command (portable) | Result | Receipt |
| --- | --- | --- | --- |
| Default objects against main | `scripts/objects_identical.sh` over 8 sources and 6 flag sets, without debug info | 47 of 48 pairs byte-identical; `-O0` `core/mrp_mad.c` differs in `rx_on_attr` only | `receipts/objects-identical.txt` |
| Differential, generic | `python3 -I tests/check_differential.py --work-dir W --milan OFF --sanitize-memory clang` | rc 0; 22 builds; 36 of 36 planted defects killed, plus the sanitizer plant; end-station build clean under MemorySanitizer; per-build digests equal the author's receipt | `receipts/gates/diff-OFF.*` |
| Differential, Milan | same with `--milan ON` | rc 0; the same counts; digests equal the author's | `receipts/gates/diff-ON.*` |
| Unit suite | Debug CMake builds: default, `LWSRP_MILAN`, `LWSRP_SCALE`, both | rc 0; 27199 / 27187 / 27227 / 27215 passes (key suite 28 in the scale builds) | `receipts/gates/unit-*` |
| Unit suite, end-station set | the scale build plus the five end-station defines, both profiles | rc 1: 27225 passes and 2 failures (27213 / 2 with Milan), both in `registrar_recovery_stops_aging_without_duplicate_join_or_map` (policy calls 0, expected 1) | `receipts/unit-endstation-*.log` |
| Reversals | `tests/check_reversals.py` with `--milan OFF/ON` x `--scale OFF/ON` | rc 0 for all four; 110 KILLED with `--scale OFF` (4 SKIP), 4 KILLED with `--scale ON`; each run prints "Reversals: 114" | `receipts/gates/rev-*` |
| Reviewer probes on the differential | `scripts/probe_mutants.py`, both profiles, 200 seeds | 6 of 6 survive in each profile (see F2 and the lean-validation note) | `receipts/probes-*.log` |
| Reviewer probe under MemorySanitizer | `scripts/probe_msan.py` (the delivering pass's zeroing removed) | reported at seed 4 in both profiles | `receipts/probe-msan-*.log` |
| Embedded and freestanding | `check_embedded.py`; `check_freestanding.py` default, Milan, and the whole end-station set | pass | `receipts/embedded-freestanding.txt` |
| Guides | `doc/tools/check_sentences.py`, `check_references.py` (and `--self-test`), `check_links.py` | rc 0 each: 0 over the limit, 0 unlinked, 79 self-test cases, 0 failed links | `receipts/doc-checks.txt` |
| Hosted evidence at the head | GitHub API, read-only | 0 check runs, 0 statuses; the repository has no workflow directory, so nothing executed and nothing was skipped | `receipts/hosted.txt` |
| Checkout restored | git | HEAD and tree exact; worktree and index equal HEAD; 0 untracked entries; no gitlinks in this repository | `receipts/checkout-state.txt` |

I did not rerun `check_equivalence.py` or its controls. The author's receipts are the only evidence for those gates (see the limits).

## Per-option analysis

- **LWSRP_TIMER_SLOTS** (`src/ports/timer.c:53-226`). The wheel keeps the list walk's semantics:
  - a timer armed outside a tick fires n ticks later;
  - within one tick, timers fire latest registration first (`sort_due`);
  - a timer armed by a callback counts the current tick only if it registered before the running timer (`ahead`); that is exactly the timers the old walk had not yet reached.
  - Zero and unregistered arms, disarming a pending timer, and removal all match. The tick counter wraps safely (the 4-slot wrap build).
  - The only divergence is a timer removed from inside its own callback. On main that is undefined (the walk reads a cleared or freed link). lwSRP never does it (S1).
- **LWSRP_ATTR_KEY / LWSRP_ATTR_BUCKETS** (`src/core/mrp_mad.c:539-613, 627-670, 1225-1235, 1315-1331`).
  - Buckets are fed at the head and unlinked together with the list, so a bucket's first match is the list's.
  - The MSRP key is the StreamID's last octet. It is shared by Talker Advertise, Talker Failed and Listener, so `attr_replaces` pairs and the Listener-as-Talker lookup in `msrp_map_join` stay in one bucket.
  - The MVRP key is a VID octet that `mvrp_attr_cmp` compares. The struct layout depends on the define and the build passes it as a PUBLIC definition; the documentation says so.
- **LWSRP_TX_MERGE** (`src/core/mrp_mad.c:1598-1766`).
  - The run merge is stable and equals main's backward-swap insertion order. Ascending Messages are left in place, and only strictly descending ones are reversed.
  - The LeaveAll vector (NumberOfValues 0, 10.8.2.8) is written before `first` and never moved. A failed build leaves the same ordered prefix (the transmit buffer is digested after every opportunity).
- **LWSRP_ONE_PORT_MAP** (`src/core/mrp_mad.c:709-713, 864-867`). With one port, MSRP's policy returns `all_ports_except(src)`, which is 0, and MVRP and MMRP have no policy. Skipping the reservation, publication and replay is therefore exact, except for the documented refusal difference (F2). The `mrp.h` policy contract does not forbid naming the source port; the integrator guide states the new precondition.
- **LWSRP_LEAN_VALIDATE** (`src/core/mrp_pdu.c:204-212`; option block `:21-30`). The in-tree decoders write before they read (sanitizer clean). Removing the delivering pass's zeroing is reported by the sanitizer run (probe), so that path has a killing check even though no trace plant targets it. The precondition this puts on application decoders is not stated (F5).
- **LWSRP_RAPID_REPLACE** (`src/core/mrp_mad.c:1238-1245`). After rLv! has left MT, the LEAVETIMER cell is `{none, none, MT}` (`:495`) and every Applicant LEAVETIMER cell is `_X` (`:366-371`). The transmit-request switch already ran with the same Applicant state on the rLv! delivery. The skip is exact.
- **LWSRP_LEAN_COPY** (`src/core/mrp_mad.c:803-813, 1201-1209`; `src/modules/msrp.c:40-60`). The refresh writes only `attr_store_len` octets of the same instance, so restoring those octets is exact. The octet copies equal `memcpy`.
- **LWSRP_LEAN_TX** (`src/core/mrp_mad.c:1894-1901, 1775-1781`).
  - The Registrar's tx! row is all `_RX` (`:435`). The Applicant tx! cells skipped are VO, QA, AO, QO and QP, all `_X` (`:275-280`); none of them is in the transmit-request switch.
  - AN's special case has `tx` NEW, so it is still delivered. The word skip is right for `uint32_t open[8]`.

## Findings

### R959-1-F1 - MAJOR - Robustness, Tests, Docs

- **Artifact:** `tests/__pycache__/check_reversals.cpython-314.pyc` (added by `cce36b5`; blob sha256 `8bb74e5b...`).
- **Evidence:**
  - It is a generated CPython 3.14 bytecode file.
  - Its embedded `co_filename` is an absolute path of 9 components outside any checkout. It points into a private host data directory and names the author's lane worktree. `receipts/pyc-origin.txt` gives its sha256 without disclosing it.
  - The repository has no ignore file.
- **Authority:** CONTRIBUTING.md, "Do not include private infrastructure details or generated assets." The PR body itself says a stray output file "is removed".
- **Impact:** merging publishes private host-layout and lane details in main's tree and history. The stale bytecode also does not match the current `tests/check_reversals.py`.
- **Required outcome:**
  - Remove the file and add an ignore rule for `__pycache__/` and `*.pyc`.
  - Merge so that main's history does not carry the blob (squash, or a rebuilt branch). That choice is the manager's.
- **Verification:**
  - `git ls-files '*.pyc'` is empty at the new head.
  - After the merge, `git log --all --format=%H -- 'tests/__pycache__'` on main shows no commit adding it.

### R959-1-F2 - MINOR - Tests, Docs

- **Artifact:** `tests/check_differential.py:76-111` (`normalized`, `compared`); `doc/integrator.md:102-111`; `doc/tester.md:170-171`.
- **Evidence:** the two documented differences of LWSRP_ONE_PORT_MAP have no killing test.
  - The first difference is that the policy is not called at one port. The differential strips exactly those lines (`UNNAMED`) and the allocation counts.
  - The second is that a refused reservation no longer refuses the receive. The differential never compares any seed that refuses allocations at one port (23 of 200, "excused").
  - My probes survive 200 seeds in both profiles (`receipts/probes-*.log`):
    - `one-port-refusal-kept` keeps the policy skip but restores main's refusal, i.e. it reverses the documented difference; it survives in the end-station build and alone;
    - `one-port-inert` turns the option off;
    - `one-port-policy-called` calls the policy at one port.
  - No unit test references any end-station option, and no gate builds the unit suite with them. Built that way, the suite fails 2 assertions in `tests/unit/review_test.c:303` (`maps` 0, expected 1). That is the documented no-policy-call difference, but the tester guide does not say so.
  - The only planted defects for the option (`one-port-reserve`, `one-port-publish`) move its boundary to two ports.
- **Impact:** both product shapes of #993 ship this option. Under refusal, the behaviour its guide promises is unverified, and a regression to main's behaviour or worse would pass every gate.
- **Required outcome:**
  - Add directed tests built with LWSRP_ONE_PORT_MAP: a refused one-port allocation applies the event where the default build refuses it; no policy call is made at one port; two or more ports are unchanged.
  - Run them in an end-station unit build that the gates and `doc/tester.md` name, and make `registrar_recovery_stops_aging_without_duplicate_join_or_map` option-aware or document its expected difference.
  - Add a planted reversal such as `one-port-refusal-kept` that the new tests kill.
- **Verification:** the end-station unit build exits 0, and the probe `one-port-refusal-kept` is KILLED.

### R959-1-F3 - MINOR - Tests, Docs

- **Artifact:** `tests/check_reversals.py:405-409, 457`; the PR body's Reversals row.
- **Evidence:**
  - The summary prints `len(CASES)` (114) whatever ran.
  - With `--scale OFF`, 110 run and 4 print SKIP. With `--scale ON`, 4 run and 110 are skipped silently. My four runs all print "Reversals: 114" (`receipts/gates/rev-*.log`).
  - The PR body says "114 reversals each, 0 failures". `doc/tester.md:343` states it correctly.
- **Authority:** CONTRIBUTING.md, "Do not describe an empty suite as protocol coverage". Main ran every case, so its summary was true.
- **Impact:** a run that executes 4 cases reports 114 as coverage.
- **Required outcome:** the summary reports cases run and cases skipped, and the PR body states 110 run plus 4 skipped (`--scale OFF`) and 4 run (`--scale ON`).
- **Verification:** rerun both modes and read the summaries.

### R959-1-F4 - MINOR - Docs, Tests

- **Artifact:** `doc/tester.md:212` (written by `73007b4`, whose subject is this very count).
- **Evidence:**
  - The guide reads "ten in the timers, five in the buckets, eleven in the vector order, and twelve in the end-station switches". That sums to 38 against the "All 36" in the same sentence.
  - The next sentence lists 2 + 1 + 4 + 3 = 10 end-station plants, and `MUTANTS` holds 10 (`tests/check_differential.py:179-199`).
- **Impact:** a stated figure in the tester guide is wrong.
- **Required outcome:** "ten in the end-station switches".
- **Verification:** count the `MUTANTS` entries carrying `END_STATION`.

### R959-1-F5 - MINOR - Docs, Robustness

- **Artifact:** `doc/integrator.md:89, 97`; `src/include/shish_lan/mrp.h:195-208` (the `encode_attr` and `decode_attr` contracts).
- **Evidence:**
  - The guide says "Each option changes no output, callback, or callback order" and lists LWSRP_LEAN_VALIDATE's difference as "None". Yet application callbacks do change:
    - LWSRP_LEAN_VALIDATE passes `decode_attr` an unzeroed buffer in the validation pass. A decoder that reads its output before writing it (the shape of the sanitizer's own plant) then validates on indeterminate memory.
    - LWSRP_TX_MERGE calls `encode_attr` again for every vector it moves (`tx_order`, `src/core/mrp_mad.c:1686-1689`).
    - LWSRP_ATTR_KEY and the buckets call `attr_cmp` and `attr_replaces` less often. This one is stated.
  - `mrp.h` states none of these preconditions.
- **Impact:** a host application can rely on options that silently tighten its callback contract.
- **Required outcome:**
  - State in `mrp.h` and the integrator table that, under LWSRP_LEAN_VALIDATE, `decode_attr`'s result must depend on the wire octets only, never on `attr_val_out`'s prior content.
  - State that, under LWSRP_TX_MERGE, `encode_attr` must be a pure function of type and value and may be called more than once per value.
  - Narrow "callback" to indications, observations and the receive filter.
- **Verification:** read the revised text.

### R959-1-F6 - MINOR - Docs

- **Artifact:** the PR body, "the default build compiles every object `main` does" and "the default objects are `main`'s"; `src/core/mrp_mad.c:1205`.
- **Evidence:**
  - Without debug info, all 8 objects are byte-identical to main's at -O2, -Os, -O2 -DLWSRP_MILAN=1, -Os -DLWSRP_MILAN=1 and -O2 -fPIC.
  - At -O0, which is the README's Debug build type, `mrp_mad.o` differs: `rx_on_attr`'s new `kept` local changes its code (0x574 against 0x4fb bytes). Behaviour is unchanged; the default differential build is identical.
  - Objects are generated artifacts, so the claim is not wording only.
- **Required outcome:** qualify the claim ("byte-identical at -O2/-Os without debug info; behaviour-identical at every level"), or make the default branch use `sizeof(previous_value)` directly.
- **Verification:** `scripts/objects_identical.sh`.

### R959-1-R1 - RESIDUE - Docs

- **Artifact:** the new option comment blocks: `src/core/mrp_mad.c:22-99`, `src/core/mrp_pdu.c:21-30`, `src/include/shish_lan/mrp.h:27-39`, `src/ports/timer.h:13-18, 28-38`, `src/modules/msrp.c:40-60`.
- **Evidence:** they state behaviour and some clauses, but no issue ID. The owner rule of 2026-10-15 asks for behaviour and reason with issue and requirement IDs.
- **Exact fix:** add "kebag-logic/milan-fpga#977" to each option's comment, and "#872" to the bucket and wheel blocks.
- No lane labels, lane names, review rounds, reviewer IDs or comment IDs appear in the delta's added lines (scanned).

### Suggestions (not blocking)

- **S1:** neither the timer driver nor the timer contract covers removing a timer inside a tick, for example a host calling `mrp_reclaim` from an indication during a leave-timer expiry. Main is undefined there and the wheel is safe; state that it is unsupported, or add the case.
- **S2:** the `tx_reverse` fallback for a vector longer than its 52-octet buffer is unreachable for every in-tree application, and no test exercises it.
- **S3:** name the sanitizer guard of the delivering pass's zeroing as a planted defect in `MUTANTS`' documentation. My probe shows it is reported at seed 4.
- **S4:** the repository has no hosted workflow, so every gate is evidence the author ran.

## Prior findings

- No review finding had been posted on PR #22 before this round; it holds only the two review-start notices.
- The brief says this PR exists because R957-1-F2 (milan-fpga PR #993) found the lwSRP pin unpublished. At this round, `73007b48` is the published head of PR #22 (`receipts/hosted.txt`). I did not read that finding's text.

## Ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Option code against IEEE 802.1Q-2018 Tables 10-3 and 10-4, 10.3, 10.7 timers, 10.8.2.7 order, 10.8.2.8 LeaveAll vector, 35.2.6 replacement, Milan v1.2 4.2.7.2.2; differential traces, both profiles | R959-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |
| RTL (implementation source; the repository has no RTL) | CLEAN | `src/core/mrp_mad.c`, `src/core/mrp_pdu.c`, `src/ports/timer.[ch]`, `src/modules/msrp.c`, `src/modules/mvrp.c`, `src/include/shish_lan/mrp.h`, CMakeLists.txt; object identity at 6 flag sets; freestanding and embedded with the end-station set | R959-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |
| Robustness | UNCLEAN (F1, F5) | Committed artifacts, callback contracts, refusal and restore paths, timer removal in a tick, sanitizer run | R959-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |
| Tests | UNCLEAN (F1, F2, F3, F4) | `tests/check_differential.py`, `tests/differential/*.c`, `tests/unit/key_test.c`, `tests/check_reversals.py`; 4 unit builds plus the end-station build; 4 reversal runs; 2 differential runs; 7 probes in each profile | R959-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |
| Docs | UNCLEAN (F1, F2, F3, F4, F5, F6; R1 residue) | `doc/integrator.md`, `doc/tester.md`, `doc/developer.md`, `doc/manager.md`, `doc/architecture.md` (every changed line anchor checked), the PR body, the source comments; guide tools | R959-1 | 73007b4807977517045e8aa485c61ebb8f5ee843 |

## Limits

- No manager source bank ran at this head, and I claim none. Source-head execution evidence is the author's published receipts plus my runs above.
- Physical calibration was NOT RUN. No hardware or field result is implied.
- No hosted job exists for this repository, so none executed.
- I did not rerun `check_equivalence.py` or `check_equivalence_controls.py`, the Zephyr build, an RV32 target build, or any cycle measurement. The performance claims of #977 are outside this review.
- The unit framework was built in scratch from its upstream revision `25137a17` (recorded in `receipts/checkout-state.txt`); the author's version is not recorded.
- There is no CHANGELOG file in lwSRP at the base or the head, and no repository rule asks for one. The options are stated in the integrator, developer and tester guides and the PR body.
- milan-fpga PR #993 itself was not reviewed.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks; source base `d1bb4f4e`) at the merge turn, and own hosted and act acceptance.
- Decide F1's merge method, so that main's history does not carry the bytecode blob.
- Carry R959-1-R1 to the residue checklist.
- Re-review F1 to F6 at the next head.

R959-1 FINISHED
