[R335] NEGATIVE - exact head a9b7874d415d935949becd7ccfd58799927efb08

# R335-1 external independent review: processor issue #120 / PR #121

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `a9b7874d415d935949becd7ccfd58799927efb08`, tree `14040d6f4646d648748540d73c1c2e38de4f2b2e`
- Source base: `0922e43408f891fc0b84a84691df86b4fd0f1c0d`. Commits reviewed: `691f1d2b` (round 1) and `a9b7874d` (round 2)
- Round: R335-1, the first external review of this PR. The session started from a cleared context in an isolated detached clone.

## Verdict

**NEGATIVE.** The one open finding is **F1 (MINOR, Tests)**.

The PR adds one new C++ compiler warning to the `tb/pp_top` suite build, whose base transcript compiles with zero warnings under the bench's own `-Wall -Wextra`. The fix is one line and needs no change to stimulus or assertions.

Everything else checks out:

- The RTL change is correct and minimal.
- The export is structurally the descriptor store's live name-RAM write enable.
- No other port, width or behaviour of `protocol_processor_top` changes.
- The documentation is accurate.
- The area delta is trivial, with no new state.
- The tests kill every reviewer-built mutant that is observable at the processor top.
- The executor's receipts show the parent consumer bar passing.

## Reconstruction (order followed)

1. **Repository conventions.** This repository has no `AGENTS.md` or `CONTRIBUTING.md` at any path. I read `README.md`, `docs/README.md` (conventions, single-source rules), `docs/guides/hdl-engineer.md` (gates table) and `hdl/README.md` in their place.
2. **Issue #120.**
   - The issue body: decision and acceptance 1 to 3.
   - Maintainer comments: 5845129313 (assignment), 5845319119 (round-1 ready) and 5845334300 (correction to acceptance 3). The correction means the parent consumer bar runs with an explicit open `.aecp_name_wr_o()` because strict parent lint makes PINMISSING fatal.
   - 5845451831: round-2 parent-gate findings 1 to 4.
   - 5845608406: round-2 ready.
3. **PR #121.** The body, the review-start comments and the review/inline-comment API. That API holds no formal reviews and no inline comments.
4. **Authorities.**
   - Store acceptance: `hdl/aecp/KL_aecp_desc_store.sv` (`st_ready_o`, `take_wr_w`, `name_ram`, `ram_ports`, the `core` FSM).
   - The engine's state-port routing: `hdl/aecp/KL_aecp_engine.sv:1433-1650`.
   - The µCPU state port: `hdl/aecp/KL_aecp_ucpu.sv:285-357`.
   - The SET_NAME µprogram: `hdl/aecp/ucode/gen_ucode.py:2068-2096`.
   - Integration contracts: `docs/architecture/02_interfaces.md` §8.1 and `docs/guides/integrator.md`.
5. **Diff and history.** The full diff `0922e434..a9b7874d` (11 files, +344/-14) and both commits.
6. **Public evidence.**
   - kebag-logic/milan-fpga `27f87160…/review-evidence/pp120-r1`. At that commit it holds `MANIFEST.json`, `author/` and `author-r2/`; I found no separate manager-bank directory there (see Limits).
   - Hosted runs at the exact head.

## Focus verification

### (1) Pulse source and count

**Source.**
- `KL_aecp_desc_store.sv:457` defines `assign name_wr_o = take_wr_w && st_name_i;`.
- `take_wr_w = st_req_i && st_we_i && st_ready_o` (`:454`).
- The live branch of the name-RAM mux uses that same wire as its enable: `name_we_w = name_wr_o` (`:545`).
- The boot-load branch (`S_NAM_RSP && beat_w`, `:539`) is excluded by construction, because `st_ready_o` is 0 in every boot-walk state (`:447`).

So the export *is* the live RAM write enable. It is not reconstructed from command decode, and it adds no new state. The engine forwards it unchanged (`KL_aecp_engine.sv:1629`), and so does the top (`protocol_processor_top.sv:3470`).

**Per-lane semantics.** The SET_NAME µprogram issues one `NAME_WR` per changed 8-byte lane and skips unchanged lanes (`gen_ucode.py:2077-2086`). A multi-beat name therefore pulses once per written lane. That matches the issue's "each accepted live name write into the descriptor store" and its pointer to the name-RAM write enable.

**Refused paths.** Lock refusal, a bad descriptor or config, and a bad name_index all branch before any `NAME_WR` (`CHECK_LOCK` and the `BR_STATUS` arms at `:2071-2075`).

**Shipped tests.** I ran the focused suite in my own build: `make -C tb/pp_top name-writes` gives 85 checks and 0 failures (`receipts/10-head-name-writes.log`).

I also reran the shipped decode mutant (`tb/pp_top/name_wr_mutant.py`). Golden and restored pass, and the decode mutant builds, completes and fails `NW EIGHT`, `NW LOCKED` and `NW ABORT` (`receipts/21-shipped-mutant/`).

**Reviewer-built mutants** (`scripts/r335_name_wr_mutants.py`, `receipts/20-mutants/results.json`). Every store-side mutant keeps the RAM on its original enable, so only the exported wire changes.

| Mutant | Verdict | Killing checks (examples) |
|---|---|---|
| golden | PASS (85/0) | — |
| decode_dispatch (SET_NAME dispatch decode, one pulse per command) | KILLED | `NW EIGHT` count 1 want 8, `NW UNCHANGED` 1 want 0, `NW LOCKED` 1 want 0 |
| level_sticky (level after first write) | KILLED | `NW ONE` count 607 want 1, one-clock-wide |
| stretch2 (two-cycle pulse) | KILLED | `NW ONE` count 2 want 1, one-clock-wide |
| delayed1 (registered, one cycle late) | KILLED | output vs live RAM-enable tap, every phase |
| drop_lane3 (missing middle beat) | KILLED | `NW EIGHT` and `NW RELEASE` count 7 want 8 |
| drop_lane7 (missing last beat) | KILLED | `NW ONE` 0 want 1, `NW EIGHT` 7 want 8 |
| first_lane_only | KILLED | `NW EIGHT` and `NW RELEASE` 1 want 8 |
| with_boot (boot name loading included) | KILLED | `NW BOOT` |
| with_name_reads | KILLED | `NW ONE` 17 want 1 |
| from_nvm_mark7 (the later completion mark) | KILLED | `NW EIGHT` 1 want 8, precedes-mark |
| top_tied0 | KILLED | every count |
| decode_request (request without `st_ready_o`) | SURVIVED, equivalent at the top | see below |
| any_store_write (non-name store writes too) | SURVIVED, equivalent at the top | see below |

**The two survivors are equivalent at the processor boundary.**
- The store leaves `S_READY`/`S_BAD` only in response to a request. Every SET_NAME lane performs a `NAME_RD`, which waits for its answer, immediately before its `NAME_WR`, so a `NAME_WR` is never presented to a busy store.
- Every engine-dispatched `WRITE_ST` targets `RGN_DYN`/`RGN_STRQ`, which are routed away from the store. The only non-name store writers are the exemplar programs at µPC 288, 320 and 512, and none of them is among the 56 engine `UPC_*_C` dispatch constants.
- A display-only probe over the entire top suite (7731 default-build checks) confirms this. It recorded 0 held-not-ready writes, 0 non-name store writes, 31 export pulses and 1080 boot name loads (`receipts/50-probe-pp_top-summary.txt`).
- Both conditions *do* occur in the store's own unit suite, which never observes `name_wr_o` (`receipts/51-probe-desc_store-summary.txt`). See S1.

**Result:** Clean against the frozen acceptance.

### (2) No other port, timing or behaviour change

**Ports.** I compared the elaborated port lists with the scoped 5.050 elaborator's JSON output (`scripts/r335_json_ports.py`, `receipts/40-port-diff.txt`):

| Module | Base | Head | Change |
|---|---|---|---|
| `protocol_processor_top` | 205 | 206 | only `aecp_name_wr_o` (1-bit output) added |
| engine | 151 | 152 | only `name_wr_o` added |
| store | 27 | 28 | only `name_wr_o` added |

In every case the common ports keep identical names, directions, widths and order.

**RTL.** The only functional change is the new `assign`, the three port connections and the `name_we_w` alias, which is the same expression. `aecp_nvm_stb_o`/`aecp_nvm_mark_o` are untouched.

**Donor suites.** Run at head and base with the scoped Verilator 5.050 (`receipts/30-donor/`):

| Suite | Base | Head |
|---|---|---|
| `pp_top` | 7666/0 | 7751/0 |
| `desc_store` | — | 584/0 |
| `desc_mem_guard` | — | 78/0 |
| `ucpu` | — | 386/0 |

- **pp_top transcript:** After normalising line numbers, the only differences are the new `NW: 85 checks` line, the tallies, and one new compiler warning (F1) (`receipts/31-pp_top-transcript-diff.txt`).
- **Lint:** A scoped strict lint (repository flags, zero tolerance) is OK at both base and head for the top, the engine and the store.
- **Hosted:** At the exact head, the `hdl` workflow's `pull_request` and `push` runs both executed `docs-gates`, `portability` and `suites` with success. The PR run's suites job used Verilator 5.050 and reports `PASS pp_top (7751 checks)` and `suites: 1014722 checks total, 0 failing`.

### (3) Contracts and documentation

- **Top `//!` contract** (`protocol_processor_top.sv:648-655`): clk_i, one cycle per lane written, at the accepting edge, the exclusions, earlier writes surviving a later abort, no ready/ack, and the explicit open connection.
- **Relation to the NVM mark** (`:665-666`): the mark serves command completion, while `aecp_name_wr_o` and map edit phase 5 are the earlier live writes.
- **`02_interfaces.md:547` (§8.1 top table) and `integrator.md:318-319`** say the same, and add:
  - the clk_i domain,
  - that the consumer owns the crossing and must capture the pulse,
  - that the name write precedes the unchanged group-7 completion mark.
- **Other contracts:** The store, engine and harness ports carry `//!` contracts (`KL_aecp_desc_store.sv:185-188`, `KL_aecp_engine.sv:529-532`, `pp_top_wrap.sv:321-328`).
- **Document checks at head:** `check-links` 915 OK, `gen_matrix --check` OK, `check-integrator-params` 24/24/24 OK, `check-matrix` OK, `check_upc_map` PASS (`receipts/70-doc-checks.txt`).

**Result:** Clean. S2 is optional.

### (4) Area

**Scoped synthesis** (`synth_xilinx` xc7, flattened, `receipts/60-area/`):

| Block | Flip-flops | RAMB36 | DSP | LUTs | OBUF |
|---|---|---|---|---|---|
| store | 773 → 773 | 2 → 2 | 1 → 1 | 1311 → 1288 | +1 |
| engine | 4036 → 4036 | 6 → 6 | 1 → 1 | 6556 → 6583 (+0.4 %, mapping variation) | +1 |

**Whole processor.** The executor's whole-processor receipt (`author/area.json` in the public evidence) agrees: registers, RAM and DSP are identical, mapped LUTs go 66,461 → 66,439, and OBUF is +1.

**Result:** Zero new state and a trivial delta.

### (5) Parent consumer gates

I was not permitted to run parent banks. The public receipts at `author-r2/consumer/` cover parent `7eb3b0d4…` with the processor pin at `a9b7874d…` and the supplied patch, which touches `hdl/milan/KL_pp_shadow.sv` +2 and `scripts/measure_test_evidence.py` +3; its SHA-256 is recorded in `consumer-setup.log`. They show all 12 commands at rc 0:

- `pp_shadow`: 402 checks, 0 failures.
- Port-contract gate: protocol-processor undocumented 111 ≤ 111.
- Lint ratchet: 90 ≤ 90.
- `test_builder`: "ALL GATES PASS EXCEPT 1 NOT RUN". Gate 11 calibration did not run because the mf48 implementation report is absent. That is a registered not-run, not coverage.

**Whole-project view.** The pin bump from the parent's `990f9652` also carries processor PRs #118 and #119, which were merged and reviewed separately. The same consumer receipts cover them.

**Result:** No regression shown. The manager's own consumer-bank receipts at this head were not in the evidence tree I was pointed to (see pending duties).

## Findings

### F1: MINOR (Tests). New compiler warning in the `pp_top` suite build

- **Where:** `tb/pp_top/sim_main.cpp:9744` (`static void run_name_writes(H& h)`), called only inside the `#else` branch of `#ifdef PP_TOP_SRP_DOM_DEF_VID` at `:9772-9784`.
- **Authority / evidence:**
  - The bench compiles with `-Wall -Wextra` (`tb/pp_top/Makefile:22`, and again for the fixture build at `:72`).
  - The base transcript of `make -C tb/pp_top` has 0 compiler warnings. The head transcript has exactly one, `warning: 'void run_name_writes(H&)' defined but not used [-Wunused-function]`, emitted by the second (fixture) build (`receipts/32-cxx-warning.txt`, `receipts/30-donor/{base,head}-pp_top.log`).
  - The other suites I ran (`desc_store`, `desc_mem_guard`, `ucpu`) and the focused build are also warning-free.
  - The neighbouring phase this PR mirrors (`InternalStreamInfoPhase`, a struct) does not warn.
  - The project applies zero-tolerance hygiene to its gates, and round 2 of this PR existed to satisfy code-idiom rules.
- **Impact:**
  - Every run of the canonical `pp_top` suite now prints a warning that was not there before. That erodes the warning-free baseline, so a future real warning is easier to miss.
  - Any move to `-Werror` would break this suite.
  - `run_suites.sh` discards passing logs, so the gates do not surface it.
  - No functional impact.
- **Required outcome:** The fixture build compiles without the new warning, and stimulus and assertions are unchanged. Any of these works:
  - define `run_name_writes` only under `#ifndef PP_TOP_SRP_DOM_DEF_VID`;
  - mark it `[[maybe_unused]]`;
  - fold it into a phase struct like `InternalStreamInfoPhase`.
- **Verification:** `make -C tb/pp_top` shows 0 compiler `warning:` lines in both builds, as at base, the tally is still 7751/0, and `name-writes` is still 85/0.

### S1: SUGGESTION (Tests). Pin the store-level contract in the store's unit suite

- **Where:** `tb/desc_store/sim_main.cpp` has 0 references to `name_wr_o`.
- **Issue:**
  - The store `//!` contract (`KL_aecp_desc_store.sv:185-187`) promises a pulse only on *accepted* name writes.
  - Two reviewer mutants (request instead of acceptance; any store write) are unobservable at the top, so only the structural identity at `:545` currently protects that promise.
  - The unit suite does exercise a non-name store write (probe: 1 occurrence) but never reads the output.
- **Suggestion:** Count `name_wr_o` in the unit suite for:
  - a name write,
  - a non-name write,
  - a write held during the boot walk.

### S2: SUGGESTION (Docs). State the output's combinational nature

- **Where:** `02_interfaces.md` §8.1.
- **Issue:** The rewrite dropped the sentence that these outputs are "combinational reads of clk_i-domain registers". `aecp_name_wr_o` is likewise a combinational function of clk_i registers only (µCPU E-stage and store `st_r`), with no top-input-to-output path.
- **Suggestion:** Saying so in the top `//!` or in §8.1 would tell CDC integrators to register it before capture.

## Prior public findings at this head

There are no formal PR reviews and no inline comments. The only prior public findings are the manager's four round-2 parent-gate items (issue comment 5845451831). I checked each against the head:

| Item | Status | Evidence |
|---|---|---|
| 1. Long C++ function | **Resolved** | Scenario split into `count`/`set`/`accepted_writes`/`refused_writes`/`stalled_and_aborted_writes` (`sim_main.cpp:9593-9763`); consumer `check_cpp_idiom.py` rc 0 |
| 2. Undocumented Python functions | **Resolved** | `run` and `main` have docstrings (`name_wr_mutant.py:15,24`); consumer `check_py_idiom.py` rc 0 |
| 3. Port contracts | **Resolved** | `//!` contracts on store, engine, top and harness ports; consumer `check_port_contracts.py` reports protocol-processor 111 ≤ 111 |
| 4. Wall-clock dependence | **Resolved** | `name_wr_mutant.py` uses no host time or deadline, and its verdicts come from completed simulation transcripts; `measure_test_evidence.py --check` rc 0 |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue decision and acceptance 1 to 3 with correction 5845334300; per-lane semantics against the SET_NAME µprogram; refusal and abort paths; NVM mark timing unchanged; parent consumer receipts | R335-1 | a9b7874d415d935949becd7ccfd58799927efb08 |
| RTL | CLEAN | `KL_aecp_desc_store.sv:185-188,447-457,536-549`; `KL_aecp_engine.sv:526-532,1613-1650`; `protocol_processor_top.sv:645-668,3467-3472`; `KL_aecp_ucpu.sv:285-357`; elaborated port diff; scoped strict lint; scoped area | R335-1 | a9b7874d415d935949becd7ccfd58799927efb08 |
| Robustness | CLEAN | boot-walk exclusion; busy-store and non-name write reachability (probe over the whole top suite); reset (synchronous `st_r` reset, output gated by `st_ready_o`); no input-to-output combinational path; watchdog-abort and stall scenarios; strict-lint consumer impact (explicit open connection) | R335-1 | a9b7874d415d935949becd7ccfd58799927efb08 |
| Tests | **UNCLEAN** (F1) | `tb/pp_top/sim_main.cpp` NW phase and sampling point (`:1159-1192`); `pp_top_wrap.sv` tap; `name_wr_mutant.py` rerun; 13 reviewer mutants; donor suites at head and base; compiler transcript | R335-1 | a9b7874d415d935949becd7ccfd58799927efb08 |
| Docs | CLEAN | top `//!`; `02_interfaces.md:539-557`; `integrator.md:315-320`; `tb/pp_top/README.md:25-48`; store, engine and harness `//!`; link, matrix, params and µPC checks | R335-1 | a9b7874d415d935949becd7ccfd58799927efb08 |

## Limits

- **Verilator path.** The assigned scoped Verilator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used a local shim that executes the same Verilator 5.050 (`rev v5.050`) installation the other manager pins reference, and recorded its identity and binary hashes in `receipts/00-tool-identity.txt`. The hosted run independently used 5.050.
- **Not run by me:** the full repository bank (`run_suites.sh`, full `lint_hdl.sh`, `make check` wavedrom/stale, `syn/yosys/run.sh`), any parent, gPTP or builder command, Docker/act, and hardware. Donor coverage here is the four affected suites, a scoped lint of three modules, and scoped synthesis of two modules.
- **Parent consumer evidence.** This is the executor's published receipts, not my own execution. The calibration arm (gate 11) did not run. Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Equivalence of the two surviving mutants.** This rests on source reading plus a probe over the existing top suite. It is not a formal proof.
- **Area.** My figures are scoped to the store and engine. The whole-processor figure is the executor's receipt.
- **Receipt paths.** In published receipts, home-directory prefixes are shortened to `~/`. Build logs are otherwise raw.
- **Clone integrity.** All probes ran on exported copies under the packet's `scratch/`. The review clone was never modified: `git status --ignored` is empty, the worktree and index equal HEAD, all 248 tracked blobs have identical bytes and modes, and this repository has no submodule gitlinks (`receipts/90-clone-integrity.txt`).

## Pending manager duties

- Publish or point to the manager's own consumer-bank receipts at this head. The public evidence at milan-fpga `27f87160` holds only the executor's `author/` and `author-r2/` receipts.
- Build the final current-dev candidate at the merge turn (source base `0922e434`, live dev `7eb3b0d4`).
- Accept the hosted and act results. Hosted `hdl` runs at the exact head show success for the push and pull_request events.
- Track removal of the parent's temporary open `.aecp_name_wr_o()` when kebag-logic/milan-fpga#502 adopts the pin.
- Schedule a follow-up round after F1 is addressed.

## Receipts (see MANIFEST.sha256)

| Receipts | Contents |
|---|---|
| `receipts/00-tool-identity.txt` | tool identity |
| `receipts/10-head-name-writes.log` | focused suite |
| `receipts/20-mutants/` | reviewer mutants: `results.json`, logs |
| `receipts/21-shipped-mutant/` | shipped mutant rerun |
| `receipts/30-donor/`, `31-pp_top-transcript-diff.txt`, `32-cxx-warning.txt` | donor suites, lint, transcript diff, F1 |
| `receipts/40-port-diff.txt` | elaborated port diff |
| `receipts/50-*`, `51-*` | reachability probes |
| `receipts/60-area/` | scoped synthesis |
| `receipts/70-doc-checks.txt` | documentation checks |
| `receipts/90-clone-integrity.txt` | clone integrity |
| `scripts/` | portable reproduction scripts |

R335-1 FINISHED
