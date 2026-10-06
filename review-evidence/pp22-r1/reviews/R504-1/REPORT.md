[R504] POSITIVE - exact head 2139f3dc10161b456dfbd51d2f73a63f9164e041

# R504-1: internal independent review of PR #162 (Relates to #22)

| | |
|---|---|
| Repository | Mister-M-alt/protocol-processor-control-plane-avb-milan |
| PR / issue | #162 / #22 (assignment comment 6008772151) |
| Exact head / tree | `2139f3dc10161b456dfbd51d2f73a63f9164e041` / `b7d98916ed833c26c7f7d713964b16c10c36daa3` |
| Source base | `e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8` |
| Parent dev for the consumer patch | `28f9666feab2b2ba287643c63ed3a16b1e0bb863` (also checked: live dev `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`) |
| Round | R504-1, first review of this PR |
| Verdict | POSITIVE: no open BLOCKER, MAJOR or MINOR; two SUGGESTIONs; no RESIDUE |

All receipt paths below are relative to this packet and listed in `MANIFEST.sha256`.

## 1. Reconstructed scope

- **Repository rules.** The repository has no AGENTS.md or CONTRIBUTING.md. Read instead: `README.md`, `docs/README.md` and `hdl/README.md` (rules 1 to 5 and the consumption contract).
- **Frozen acceptance (issue #22 body).** (1) `xvlog -sv` analyses every module under `hdl/` with rc 0 and no `VRFC 10-3380`. (2) Vivado synthesis of `KL_pp_shadow` reports zero `Synth 8-6901`. (3) The suites stay green.
- **Public scope decisions:**
  - Comments 5974073699 and 5979513404: PRs #149 and #153 already fixed `protocol_processor_top.sv` and `KL_aecp_notify.sv`.
  - Comment 6008772151, the assignment: two sites remain, `KL_pp_originator.sv:194` `cancel_hit_w` and `KL_pp_rx_validator.sv:383` `vd_push_w`. The fix must be a pure declaration move (that is the STOP condition). It must come with a patch-context search, Yosys statistics identical at base and head, identical suite records, a per-file xvlog table, and `parent-adoption-22-28f9666f.patch` dropping budget lines 34-35.
  - PR body manager note: the `Synth 8-6901` count is measured at the next parent pin adoption, and #22 closes on it. The PR therefore says `Relates to #22`.
- **Prior public review findings on this PR.** None exist. The PR has only the two INDEPENDENT REVIEW STARTED comments (R504-1, R505-1), no reviews and no review comments, so there is nothing to resolve or retain.

## 2. The change

There is one commit (`2139f3dc`, a subject line with no body) touching two files, +5/-5 (`diff_base_head.patch`):

- `hdl/packet_engine/KL_pp_originator.sv`: `cancel_hit_w` and `cancel_ix_w` move from base 236-237 to head 188-189. That is module scope, after the `alloc_pick` block and before `cancel_pending_pick` (their first use, now at :197-198).
- `hdl/packet_engine/KL_pp_rx_validator.sv`: the two grouped statements `fifo_ne_w, fifo_full_w, vq_ne_w, vq_full_w` and `push_w, vd_push_w, vd_val_w, rd_fire_w, retire_w` move from base 621/623 to head 232-233. That is module scope, at the end of the combinational declaration list and before the first use at :385 (`vd_push_w && !vq_full_w`). `vq_head_w` stays at :623.
- The line multisets of both files are identical, and so are their line and byte counts (`receipts/line-multiset.txt`). The moved text is byte-identical. No port, parameter, register, initialiser or statement changed.

## 3. Executed evidence (this reviewer)

| # | Check | Result | Receipt |
|---|---|---|---|
| E1 | Derived source list (parent `scripts/pp_srcs.py --prefix hdl` with the head as the submodule), compared with an independent packages-first derivation at base and head | 46 files, identical order at both revisions | `receipts/xvlog/derived-list-head.txt`, `independent-list-*.txt` |
| E2 | `xvlog -sv --work work`, one invocation per file, packages first, fresh work dir per run; with `-d SYNTHESIS` (as the parent gate) and without | **Head:** 46/46 rc 0, 0 `VRFC 10-3380`, 0 `VRFC 10-8530`, no WARNING, all 42 modules analysed. **Base:** 2 rc 1 (`KL_pp_originator.sv:194` `cancel_hit_w`, `KL_pp_rx_validator.sv:383` `vd_push_w`), 2 `10-3380`, 2 `10-8530`. Both define variants agree | `receipts/xvlog/table-{base,head}-{syn,nodef}.tsv`, `summary-*`, `base-syn-errors.txt`, `analysed-*` |
| E3 | Published per-file analysis tables compared with E2 | identical (path order, rc, 3380, 8530) at base and head | `receipts/cross-check-published.txt` |
| E4 | sv2v (lowered as `syn/yosys/run.sh` does), then Yosys `hierarchy -check -top; proc; opt_clean; stat -json` for `KL_pp_originator`, `KL_pp_rx_validator`, `protocol_processor_top` | all three stat JSONs **byte-identical** at base and head, and byte-identical to the published JSONs (sha256 `102354aa…`, `b48ab825…`, `c19429cb…`) | `receipts/yosys/*.stat.json`, `compare.txt` |
| E5 | Stronger than E4: `write_verilog -noattr` of the elaborated design, with only the `all.v:<line>` source-line tokens in generated names normalised | identical at base and head for both modules and for the whole `protocol_processor_top` hierarchy | `receipts/yosys/compare.txt` |
| E6 | Every tracked `tb/**/*.patch`, checked with `git apply --check` | 277/277 at head and at base. Only `tb/maap/mutations/validator-maap-version-1-only.patch` touches an edited file | `receipts/planting/planting-{base,head}.json` |
| E7 | Every exact-text arm of every table with `MUTANTS` + `plant()`, planted by that table's own `plant()` into fresh copies | notify 56/56, acmp 33/33, d3 110/110 (199 arms) plant and change their file at head and at base. 8 arms edit an edited file: 4 originator (notify), 4 validator (acmp ×2, d3 ×2). The other drivers (adp_engine, maap, aecp, aecp_dispatch, ctr, srp_top) are patch-based or name-keyed, are covered by E6, and do not edit either file | same |
| E8 | Probe: each of the 7 distinct edit-sets of those 8 arms, plus the maap validator patch, planted at base and at head, then the mutated module's normalised netlist compared | every mutant's netlist is identical at base and head, and each differs from the unmutated module. Each mutant is the same design at both revisions, so no kill outcome can have changed | `receipts/planting/mutant-equivalence.json` |
| E9 | The suites that compile the edited files (`tb/originator`, `tb/rx_validator`, `tb/pp_top`, per the Makefile source lists), base and head, pinned Verilator 5.050 | originator 107/107, rx_validator 555/555, pp_top 10444/10444 (six builds: 9956, 20, 178, 231, 56, 3). Normalised full logs are identical at base and head (only the Verilator timing line differs, and it is normalised) | `receipts/suites/*.log` |
| E10 | Focused Verilator lint with `lint_hdl.sh` flags, tops `KL_pp_originator`, `KL_pp_rx_validator`, `protocol_processor_top` | rc 0, zero `%Warning`/`%Error` at both revisions | `receipts/lint-focused.txt` |
| E11 | `scripts/gen_matrix.py --check` on the base and head exports | `matrix: OK (94 rows, 0 untested)`, identical at both | `receipts/head-gen_matrix-check.log` |
| E12 | Scratch parent at `28f9666f` (submodules registered, processor gitlink staged at the head, gPTP at pin `5dce647a`): `148` patch then `22` patch | both apply. The diff touches only `scripts/xvlog.budget` and `tb/verilator/milan_dp/sim_nxn.cpp`. `git diff --check` is clean | `receipts/parent/apply.txt` |
| E13 | Patched budget compared with the parent's own `write_budget([])` | byte-identical (sha256 `f10b2bef…`). `read_budget` returns `{hdl: ∅, submodules: ∅}` | `receipts/parent/apply.txt` |
| E14 | Parent consumer 09: `python3 scripts/xvlog_gate.py --check` | `PASS (0 finding(s) == ratchet)`, rc 0, over 73 hdl/ + 52 pinned sources (processor at `2139f3dc`) | `receipts/parent/parent-xvlog_gate-check.log` |
| E15 | Fault probe: same patched parent, processor gitlink and checkout at **base** | gate rc 1, `REGRESSION` on exactly the two keys `cancel_hit_w` / `vd_push_w`. The ratchet patch is load-bearing and the gate can fail | `receipts/parent/parent-probe-xvlog_gate-check.log` |
| E16 | Parent consumer 04: `python3 scripts/pp_srcs.py --check --selftest` | rc 0 | `receipts/parent/pp_srcs-check-selftest.log` |
| E17 | Both patches against live dev `423ac5d9` (budget lines 34-35 still present there) | each passes `git apply --check`, and `22` applies after `148` | `receipts/parent/live-dev-apply-check.txt`, `patch-sha256.txt` |
| E18 | Line-number citations into the two edited files, or of the moved identifiers, in tracked processor and parent text (docs, tb READMEs, tables) | none in the processor. Parent prose cites block names only (`validator_seq`) | search recorded in section 4 (Docs) |
| E19 | Hosted checks at the exact head (read-only snapshot) | `docs-gates` success, `portability` success (push and PR). `suites` was **in progress** at snapshot time | `receipts/hosted-checks.txt` |

Tool identity: `receipts/tools.txt`. Verilator is 5.050 rev v5.050 through the pinned wrapper (binary sha256 recorded); xvlog is Vivado Simulator v2026.1; Yosys 0.66; sv2v v0.0.13. `scripts/verilator_jcap.sh` only rewrites the suite Makefiles' `--build -j 0` to a fixed job count, to keep within the 16-job budget.

## 4. Lenses

**Conformance.** No Milan or IEEE 1722.1 behaviour can change: E4/E5 show that the elaborated netlists of both modules and the whole top hierarchy are identical. The interface authority (`docs/architecture/02_interfaces.md`, `hdl/README` consumption contract) is untouched: the port lists, inside the identical netlists, are unchanged (`num_ports` 45/38/212, port bits 272/484/7161). Issue acceptance (1) is met by E2. Acceptance (2) is deferred by the public ruling to the next pin adoption, and the PR correctly says `Relates to #22`, not `Closes`. Acceptance (3): see Tests. CLEAN.

**RTL.**
- Both new sites are module scope, outside any generate, function or block.
- `IFL_AW_C` is declared earlier, so the sized declaration still resolves.
- Each declaration now precedes every use: originator :197/:198/:240-245/:362-363, validator :385/:625-679.
- Grouped statements are kept intact, so no identifier was split from its group.
- Nothing else is reordered.
- E2 shows no residual declare-before-use in either file. xvlog stops at the first error per module, and the head shows none.
- Lint is clean (E10).

The cosmetic consequence in the validator is recorded as S1. CLEAN.

**Robustness.** No behaviour, reset or timing path can differ (identical netlists, E5). The front-end portability defect itself is removed: both modules are now xsim-eligible under Vivado's analysis front end (E2). The parent ratchet goes to zero submodule findings and is proven able to fail (E15). It is the generator's exact output (E13), so a later normal gate run does not rewrite it. The patches also apply at live dev (E17). CLEAN.

**Tests.**
- Suite records for every suite that compiles the edited files are identical at base and head (E9). Suites that do not compile these files cannot be affected.
- The 33-suite figure in the PR body comes from the published evidence and the manager's bank.
- All 277 patches and 199 exact-text arms plant (E6, E7). Each arm that touches the edited files yields the same mutant design at both revisions (E8).
- No test or mutant file changed, and none needed to.
- `hdl/README` rule 3 (testbench with every RTL commit) is not triggered, because no behaviour changed. The assignment's STOP condition forbids any non-declaration edit.

CLEAN.

**Docs.**
- No documentation, README or traceability file cites a line number in either file or names a moved identifier (E18), so nothing went stale.
- `gen_matrix --check` is unchanged (E11). Hosted `docs-gates` succeeded at the exact head.
- Each PR body claim matches executed evidence: four declaration lines moved unchanged; 46-file analysis with zero 3380/8530 at head and the two at base; byte-identical statistics; 277 + 199 planting; the budget patch content and count; the builder arm not run; and the unmeasured synthesis item.
- The published HANDOFF tables agree with E2/E4.

The missing processor-side rule for this defect class is recorded as S2. CLEAN.

## 5. Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

**S1: SUGGESTION.** Lens: RTL (readability).
- **Where:** `hdl/packet_engine/KL_pp_rx_validator.sv:232-233`, compared with the V9 MRP route section at `:607-629`.
- **Observation:** The FIFO/verdict wires are now declared in the general combinational list, about 390 lines above the V9 section comment that describes them and above their assigns. They keep their original 7-space `logic` padding, while the neighbouring lines use 8. This follows from the assignment requiring byte-identical moved lines. It has no functional impact.
- **Optional outcome:** in a later cosmetic change, a one-line pointer comment, e.g. `// V9 MRP route FIFO/verdict wires, driven below` at :232, with matched padding. Doing so needs a fresh patch-context check.
- **Verification:** E6/E7 re-run.

**S2: SUGGESTION.** Lenses: Tests, Docs.
- **Where:** `hdl/README.md:46-48` (rule 2, tool floor: Verilator and Yosys via sv2v).
- **Observation:** Neither tool rejects use-before-declaration, and the only gate that does is the parent's `xvlog_gate.py`. With the submodule section now at zero, a new processor-side instance would first surface at pin adoption, as a ratchet REGRESSION. The issue body offered a processor-side xvlog check "if useful". It is outside this assignment.
- **Optional outcome:** a follow-up issue that either names declare-before-use in rule 2 or adds an analysis-only check.
- **Verification:** that issue's own acceptance.

## 6. Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #22 acceptance and comments 5974073699/5979513404/6008772151; PR body and manager note; `02_interfaces.md` contract via ports in identical netlists; E2, E4, E5 | R504-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |
| RTL | CLEAN | `KL_pp_originator.sv:174-248,362`; `KL_pp_rx_validator.sv:216-245,383-385,607-680`; `diff_base_head.patch`; E1, E2, E4, E5, E10; line multisets | R504-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |
| Robustness | CLEAN | E5 netlist identity; E2 xsim eligibility; parent budget, gate and writer (E12-E15, E17) | R504-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |
| Tests | CLEAN | `tb/originator`, `tb/rx_validator`, `tb/pp_top` runs (E9); 277 patches, 9 exact-text tables (E6, E7); mutant equivalence (E8); `pp_srcs --check --selftest`; xvlog gate pass and fault probe | R504-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |
| Docs | CLEAN | `README.md`, `docs/README.md`, `hdl/README.md`, tb READMEs, `MODULE_MATRIX.md` (E11), line-citation search (E18), PR body vs evidence, published HANDOFF/PR-BODY (manifest hashes verified), hosted docs-gates | R504-1 | `2139f3dc10161b456dfbd51d2f73a63f9164e041` |

## 7. Real limits

- **Not run here, by the bank rule:** the full 33-suite `scripts/run_suites.sh`, the full `scripts/lint_hdl.sh`, `syn/yosys/run.sh`, and `make check`. Covered here instead by E4/E5 (netlist identity), E9-E11, and the hosted portability and docs-gates successes at the exact head. The 1,021,651-check figure is the published author and manager evidence, not re-measured.
- **Parent consumers:** only 04 (`pp_srcs`) and 09 (`xvlog_gate`) were re-run. The other 15 of the 17 rest on the manager's published evidence. That includes the builder, whose calibration arm (gate 11) was reported as NOT RUN because the reference report is absent; that is not a pass.
- **Not measured, by ruling:** the Vivado `Synth 8-6901` count. No Vivado synthesis or implementation was run. xvlog was used for analysis only.
- **Mutants:** kill outcomes were not re-executed. E8 proves that each affected mutant is the same design at base and head, which is a sufficiency argument, not a kill run.
- **Hosted:** the `suites` jobs at the exact head were in progress at the snapshot. Hosted/act acceptance belongs to the manager.
- **Physical:** no hardware, bench or physical calibration (NOT RUN). Field skips are not hardware proof.
- **Clone hygiene:** two identity checks (`xvlog --version`) run with the clone as working directory each wrote an untracked 79-byte `xvlog.pb` at the clone root. Both were removed. The final verification shows HEAD, tree and index equal to the exact head, all 556 tracked blobs and modes re-hashed with 0 mismatches, and an empty status including ignored files. The repository has no submodule gitlinks (`receipts/clone-integrity.txt`).

## 8. Pending manager duties

1. Accept the hosted `suites` jobs at `2139f3dc` once they complete.
2. Build the merge-turn current-dev candidate (source base `e6a759de`, live dev `423ac5d9`). E17 shows both adoption patches apply there.
3. At the next pin adoption, apply `parent-adoption-148-6c22d3ca.patch`, then `parent-adoption-22-28f9666f.patch` (sha256 in `receipts/parent/patch-sha256.txt`). Record the `Synth 8-6901` count and close #22 on it.
4. Merge requires the second independent positive review (R505) and the full completion bar.
5. Optionally, open follow-up issues for S1 and S2.

R504-1 FINISHED
