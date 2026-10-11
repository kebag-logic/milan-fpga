[R604] POSITIVE - exact head 02063dc1b593d422406991bf0bc60e5cc47828ff

# R604-2 internal independent review: processor PR #175 (issue #151)

- PR #175 on `Mister-M-alt/protocol-processor-control-plane-avb-milan`. Exact head `02063dc1b593d422406991bf0bc60e5cc47828ff`, tree `2fd23c4ce9d7f23f73d6b4440b494e62d88a2682`.
- Five commits on source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`: three from round 1 (`9385799`, `eb7e596`, `ef86ea8`) and two from round 2 (`71da740`, `02063dc`).
- Review start: PR #175 comment 6106548217. Cleared context, isolated detached clone, no GitHub writes.
- Reconstruction order:
  1. Repository rules: `README.md`, `docs/README.md`, `hdl/README.md`, `docs/guides/hdl-engineer.md`, `docs/architecture/09_verification.md`. This repository has no `AGENTS.md` or `CONTRIBUTING.md`, so I also read the reviewer procedure (§6) of the parent's `AGENTS.md` at dev `ac2c5e77`.
  2. The issue body (frozen acceptance) and the manager's comments: lane scope 6098621173, round 2 6105580039, TAKEN, REVIEW READY.
  3. Interface authorities: the integrator guide §2 and diagram 21, and the parent's Rule 12 (`docs/development/CODE_QUALITY.md` and `scripts/check_py_idiom.py`, at dev `ac2c5e77`).
  4. `git diff 2cbed0a9..02063dc1` and its history, then `ef86ea84..02063dc1` for round 2. Round 2 touches no `hdl/` file.
  5. Public evidence: `kebag-logic/milan-fpga@bda25e67/review-evidence/pp151-r1`, the hosted check runs at the exact head, and the PR body.
- **Order of reading.** I wrote my verdict draft and ledger before reading the prior review round. Only after that did I read the R604-1 and R605-1 findings, which are resolved below.

## Verdict

**POSITIVE.** At the exact head, I checked every acceptance criterion of issue #151, every lane-scope proof item, and round-2 items 1 to 6, except two I could not reach: the Vivado legs and the parent disposition patch (see Real limits). Everything I checked is met. I found no BLOCKER, MAJOR, MINOR or RESIDUE. The four MINORs and one RESIDUE of the prior round are resolved; one prior SUGGESTION is retained. The five open SUGGESTIONs below do not affect the verdict.

What holds, and the receipt for each:

- **Inventory.** All 31 elaboration guards under `hdl/` (13 files) are module-scope `if (...) begin : <label> $fatal(1, ...); end`. No other elaboration-severity construct exists.
- **No condition changed.**
  - The diff changes only the task token on 29 guards.
  - The listener guard moves from `initial begin : parameter_checks` to `begin : g_strm_tmo_check` with a byte-identical condition and message.
  - The remaining guard, `KL_pp_nvm_port.g_maxp_check`, was already `$fatal` at base.
  - At default shapes, the netlists of the 13 guard-carrying tops are identical at base and head under both sv2v versions. A negative control shows the comparison can fail.
- **Every violating case is refused at its own guard.** Under Verilator 5.050 lint, sv2v 0.0.12 + Yosys 0.66, and sv2v 0.0.13 + Yosys 0.66, each refusal is a `$fatal`, in the front end's own words, at the guard's line. Every nearest passing case elaborates. The hosted portability job re-ran the Yosys leg at this head with its own Yosys 0.33: 93/93.
- **Mutation campaign.** The author's 160-arm campaign kills 160/160 under each sv2v. Every `$error`, `$warning`, `initial`, tightened and loosened arm is killed by name, and every boundary arm is killed in both the Verilator and Yosys legs. Seven reviewer-owned mutants met their predictions.
- **Recorded rule.** The rule (HDL engineer guide §2 and §2.1, `hdl/README.md` rule 6) matches my re-measurement of the three non-vendor columns cell for cell.

## Findings at this head

### S1 - SUGGESTION - Tests: only one boundary of each multi-term guard is graded

- **Where:** `tb/elab_guards/guards.py:90-179` (`GUARDS`) and `tb/elab_guards/mutants.py:106-165` (`BOUNDARIES`). Each grades one selected comparison per guard.
- **Untested comparisons**, other terms of the same guard:
  - `KL_pp_originator.sv:148`, `INFLIGHT_P < 32'd1`;
  - `KL_aecp_desc_store.sv:269`, `NAME_ENTRIES_P == 0`;
  - `KL_aecp_desc_store.sv:266`, `IDX_ENTRIES_P * 2 > 511`;
  - `KL_aecp_ucpu.sv:295`, `RESP_D8_CAP_BYTES_P < RESP_CAP_C`;
  - `KL_aecp_notify.sv:366`, the power-of-two term;
  - `protocol_processor_top.sv:875`, `N_AVB_IF_P < 1`;
  - eight of the nine `gen_g_tmr_overlap` comparisons and nine of the eleven `gen_g_owner_overlap` comparisons;
  - most terms of `KL_aecp_nvm_writer.g_shape_check`.
  - Two of these lower bounds are graded elsewhere: `N_AVB_IF_P=0` in `tb/pp_top if-guards`, and `MEM_TIMEOUT_CYC_P` 2^31 - 1 / 2^31 in `tb/nvm_port/elab_bounds.sh`.
- **Evidence:** reviewer mutants `rm6` (originator floor dropped) and `rm7` (`NAME_ENTRIES_P == 0` dropped) survive the bench: `receipts/reviewer-mutants-sv2v013.log`, 35/35 PASS each, as predicted.
- **Why this is not a defect here:**
  - The issue's "No guard changes its condition" is met at this head by diff and netlist identity.
  - The bench's documents say "selected boundary" (`tb/elab_guards/README.md`, HDL engineer guide §2.1).
  - Round 2 asked for "the boundary" per guard, and each guard has one graded on both sides.
- **Suggestion:** grade each remaining comparison's two sides, or list the ungraded terms in the README's case table.

### S2 - SUGGESTION - Docs: the integrator's "stops the build" trap omits the `-Wno-fatal` simulation seam

- **Where:** `docs/guides/integrator.md:112-116`, trap 2.
- **Evidence:** `receipts/forms_wno_fatal_sim.log`. A violating module-scope `$fatal`, built with Verilator `--binary -Wno-fatal`, builds (rc 0, `%Warning-USERFATAL` only) and runs to completion (rc 0).
  - The HDL engineer guide §2.1 and `tb/elab_guards/README.md` "Seams" already record this.
  - The integrator guide does not. An integrator who simulates a too-large shape with `-Wno-fatal` gets no stop.
  - The guide's claim holds for the front ends the issue names: lint, sv2v + Yosys, Vivado.
- **Suggestion:** add one clause, for example "(a Verilator simulation built with `-Wno-fatal` carries it past; lint is the gate, HDL engineer guide §2.1)".

### S3 - SUGGESTION - Tests: a failed passing case under Yosys is reported as "no output"

- **Where:** `tb/elab_guards/guards.py:277`. The passing-case diagnostic filter matches only lines that start with `%Warning`, `%Error` or `ERROR`.
- **Why it misses:** Yosys prefixes its errors with `all.v:<n>:`.
- **Evidence:** every tightened arm's Yosys verdict reads `FAIL: ELAB  yosys ... rc 1: no output` (`receipts/mutants-v-y013.log`). The verdict itself is right, because the exit status fails it, but the front end's own words are dropped.
- **Suggestion:** also match `all\.v:\d+: ERROR`, so the failing line is quoted.

### S4 - SUGGESTION - Tests/Docs: the hosted portability job does not print the converter versions it grades with

- **Where:** `.github/workflows/hdl.yml:101-115`. The job installs the latest sv2v release and the distribution's Yosys, but never prints either version.
- **Evidence:** `receipts/hosted-portability-push-114413930410.log` shows `yosys (0.33-5build2)` only from the apt unpack line, and no sv2v version at all.
- **Suggestion:** add `sv2v --version; yosys -V` before the guard step, so each hosted receipt names the converter that graded the guards.

### S5 - SUGGESTION - Robustness: the inventory reads `hdl/**/*.sv` only (R605-1-S2, retained)

- **Where:** `tb/elab_guards/guards.py:210`. The scan uses `rglob("*.sv")` and strips only `//` comments.
- **Risk:** a guard in a future `.svh`/`.vh` include would escape the inventory. Today `hdl/` has none (verified with `git ls-files hdl`).
- **Suggestion:** glob `*.sv*` and `*.vh` as well.

## Prior public review findings: resolution at this head

| Prior finding | Severity | State at `02063dc1` | Evidence |
|---|---|---|---|
| R604-1-F1: `gen_g_size` not graded at its nearest passing value; a tightened guard survived | MINOR | **RESOLVED** | `guards.py:142-144` grades 16/17. Author arm `KL_aecp_resp_buf.gen_g_size:tightened` is KILLED in both legs under both sv2v. Reviewer mutant `rm2` (`<= 23`, R604-1's own mutant) is KILLED: `FAIL: ELAB verilator ... RESP_BYTES_P=17` and `FAIL: ELAB yosys ... RESP_BYTES_P=17`. |
| R604-1-F2 = R605-1-F1: integrator guide and diagram 21 say `$error` | MINOR | **RESOLVED** | `integrator.md:114` reads "stops elaboration with `$fatal`", and `21-integration-faces.svg:53` reads "$fatal.". The SVG is well-formed, and a scratch render shows the text fits. Hosted `figures`/`params` OK. `git grep '\$error'` finds it only in the §2.1 measurement rows, the `tb/nvm_port` explanatory text and the bench. |
| R604-1-R1 = R605-1-F2: `$info` described as a Verilator warning | RESIDUE / MINOR | **RESOLVED** | `hdl-engineer.md:91-92`, `tb/elab_guards/README.md:5-6` and `guards.py:8-9` now say `$info` is an `-Info` note with exit status 0. Re-measured: `receipts/forms_probe.log` (`m_info_mod P=2 rc=0 :: -Info: ...`). |
| R604-1-S1: run the Yosys leg in the hosted job with sv2v and Yosys | SUGGESTION | **RESOLVED** | `hdl.yml:114-115`. Hosted portability, both runs at the exact head: `elab guards: 93 checks: 93 PASS, 0 FAIL`. |
| R605-1-S1: the deadline guards' `< 1` boundary not graded | SUGGESTION | **RESOLVED** | Passing value 1 is graded under a narrow `UNSIGNED` allowance (`guards.py:320-346`). Tightened arms (`< 2`) are KILLED in both legs. Reviewer mutant `rm1` is KILLED. The allowance's own arms, `bench:deadline_user` and `bench:deadline_other_warning`, are KILLED. |
| R605-1-S2: inventory reads `*.sv` only | SUGGESTION | **RETAINED** as S5 | `guards.py:210` is unchanged. |

The parent-side follow-ups both round-1 reviews raised, outside this PR, are carried under pending manager duties: the parent lint gate's processor-diagnostic hole, and the parent's own `$error` guard in `KL_nvm_backend.sv`.

## Evidence by lens

### Conformance (issue acceptance, lane scope, round 2)

1. **"Every elaboration-time parameter guard in `hdl/` stops elaboration in every front end the project uses."**
   - **Independent inventory.** I grepped every `$fatal|$error|$warning|$info|$display|$finish|$stop|assert|initial` under `hdl/`; `hdl/` holds no `.svh`/`.v`/`.vh` file.
   - **Result: 31 guards.**

     | Module | Guard line(s) |
     |---|---|
     | `KL_acmp_nvm_shadow` | :538, :545 |
     | `KL_pp_acmp_listener` | :347 |
     | `KL_aecp_desc_store` | :263, :267, :270, :273 |
     | `KL_aecp_engine` | :944, :949, :964, :968, :972 |
     | `KL_aecp_notify` | :367 |
     | `KL_aecp_nvm_writer` | :315, :318, :322, :326 |
     | `KL_aecp_resp_buf` | :194, :197, :201 |
     | `KL_aecp_ucpu` | :297 |
     | `KL_pp_nvm_port` | :189, :198 |
     | `KL_pp_originator` | :149 |
     | `KL_pp_release_merge` | :38 |
     | `KL_srp_encoder` | :148 |
     | `protocol_processor_top` | :876, :880, :884, :897, :911 |

     The other `initial` blocks are two `$readmemh` and one memory clear. The bench's inventory prints the same 31 sites (`receipts/head-guards-v-y013.log`).
   - **Verilator 5.050 lint** (`lint_hdl.sh` flags): 31/31 `%Warning-USERFATAL: <file>:<guard line>:<col>: <message with values>`.
   - **sv2v 0.0.12 + Yosys 0.66:** 31/31 `ERROR: FATAL: .` inside the guard's lowered block (`receipts/head-guards-y012.log`).
   - **sv2v 0.0.13 + Yosys 0.66:** 31/31 ``ERROR: System task `$finish' executed.`` (`receipts/head-guards-v-y013.log`).
   - **xvlog/Vivado:** not installed here. The HDL is byte-identical to round-1 head `ef86ea84` (`git diff --stat ef86ea84..02063dc1` touches no `hdl/` file). The public round-1 receipt `bench/head-xelab-synth.log` shows 31 `GUARD xsim` refusals as `[VRFC 10-8279] $fatal` and 31 `GUARD synth` refusals as `[Synth 8-6058]`, each at the guard's file and line (155/155). That covers the issue criterion. The round-2 Vivado boundary claims are a limit; see below.
   - **The design decision is recorded with its measurement:** HDL engineer guide §2 coding-rule row and §2.1 table, and `hdl/README.md` rule 6.
2. **"A bench grades each guard's severity, not only its message, and a `$error`/`$warning` mutant is killed."**
   - `tb/elab_guards/guards.py` grades the class (USERFATAL, FATAL/`$finish`, VRFC 10-8279, Synth 8-6058), the guard's line and the message words.
   - `mutants.py` with both legs:

     | Toolchain | Control | Arms killed | Wall time | Receipts |
     |---|---|---|---|---|
     | sv2v 0.0.13 | PASS | 160/160 | 15:57 | `receipts/mutants-v-y013.log`, `.tally.txt` |
     | sv2v 0.0.12 | PASS | 160/160 | 16:56 | `receipts/mutants-v-y012.log`, `.tally.txt` |

   - Kills by arm kind:
     - `error` and `warning`: 31 + 31, killed by Verilator and Yosys under both sv2v.
     - `initial`: 31, killed by both legs under 0.0.12 and by Verilator alone under 0.0.13, as the README records.
     - `tightened` and `loosened`: 31 + 31, killed in both legs under both sv2v.
     - The 5 bench arms: killed as listed in the README.
3. **"No guard changes its condition."**
   - The diff shows 29 guard lines that change only `$error(` to `$fatal(1, `, plus the listener's move with a byte-identical condition.
   - The sv2v-lowered trees at base and head differ only on guard task lines and the listener's `initial` to `generate` wrapper (`receipts/netlist-sv2v012.log`).
   - The head bench run on the base tree passes every passing case and fails only the 30 Verilator and 30 Yosys refusals plus 2 inventory checks (`receipts/headbench-on-base-v-y013.log`: 156 checks, 62 FAIL). Under sv2v 0.0.13, 29 of the 30 Yosys failures are `elaborated; the guard did not stop it`, which is the #151 defect itself, reproduced on base.
4. **Lane scope: "no passing elaboration changes; netlists and ROM digests identical."**
   - The 13 guard-carrying tops at defaults, base vs head, are IDENTICAL under both sv2v (`receipts/netlist-enum-canon-sv2v012.log`, `-sv2v013.log`).
   - Method: `read_verilog -defer; hierarchy -check -top; proc; opt_clean`, then location-bearing names hidden, `rename -enumerate`, `write_verilog -noattr`, and the remaining `$`-names numbered by first appearance.
   - A first pass without `rename -enumerate` differed only in Yosys's name-ordered auto numbering (`receipts/netlist-canon-sv2v01{2,3}.log`).
   - Negative control: `RESP_BYTES_P=1032` vs default DIFFERS (`receipts/netlist-canon-negative-control.log`).
   - ROM images are identical at base and head: `ucode.hex` `518b900c...`, `ltn_rom.hex` `23cc67ee...` (`receipts/netlist-sv2v012.log`).
5. **Round 2.**
   - Item 1: both sides of each selected boundary, plus tightened and loosened arms, in each front end run here. See S1 for the unselected comparisons.
   - Items 2 and 3: resolved; see the table above.
   - Item 4: the parent's Rule 12 per-module scan (`check_py_idiom.scan` at dev `ac2c5e77`) reports every refused and ratcheted count at zero for `tb/elab_guards/guards.py`, `mutants.py` and `tb/pp_top/{if,line}_guards.py` (`receipts/py_idiom_probe.log`).
   - Item 5: the parent disposition patch is at a non-public path, which is out of this reviewer's reach. It is a manager duty.
   - Item 6: done, and executed by the hosted job.

### RTL

- The 13 changed HDL files: task token only, messages and continuation lines unchanged, line counts unchanged.
- The listener guard is now a named module-scope generate block. Its new comment (`KL_pp_acmp_listener.sv:345`) and `KL_pp_nvm_port.sv:194-195` are accurate at this head.
- `scripts/lint_hdl.sh` with the pinned Verilator: rc 0, 41 `LINT OK`, logs byte-identical at base and head (`receipts/lint-{base,head}.log`).
- Netlist identity and ROM digests: see Conformance item 4.

### Robustness

- **Boundary pairs** pass at the head in both legs and both sv2v. Examples:
  - 16/17 bytes for `gen_g_size`;
  - 0/1 cycles for the three deadlines;
  - the fixture contexts for `gen_g_resp_cap_fit` (523/524), `gen_g_gamap_page_fit` (591/592), `gen_g_line_ceiling` (1025/1024) and the three timer-map plants.
- **The deadline allowance is narrow.**
  - At value 1, only `%Warning-UNSIGNED` at the recorded expressions is accepted: `KL_acmp_nvm_shadow.sv:566`, `KL_aecp_nvm_writer.sv:610` and `:630`.
  - Its two planted defects are killed: a USER warning on the passing side, and another warning class.
- **`tb/nvm_port/elab_bounds.sh`** passes under both sv2v (`receipts/head-nvm-elab-bounds-sv2v01{2,3}.log`).
  - Verilator refuses `MEM_TIMEOUT_CYC_P` at 0, 2^31 and 2^32 - 1, and `MAX_PAYLOAD_P` at 65,528, 65,535 and 2^32 - 1, each as `%Warning-USERFATAL`.
  - Yosys stops at 0 and 65,528 in its fatal words and builds 1 and 65,527.
- **The `-Wno-fatal` seam is as documented** (`receipts/forms_wno_fatal_sim.log`); see S2.
- **Seven reviewer-owned mutants**, planted with `sed` independently of `mutants.py` and graded by the head bench under sv2v 0.0.13 (`receipts/reviewer-mutants-sv2v013.log`). All seven met their predictions:

  | Mutant | Planted | Result |
  |---|---|---|
  | `rm1` | deadline tightened to `< 2` | KILLED |
  | `rm2` | `gen_g_size <= 23` | KILLED |
  | `rm3` | the listener's base `initial`-block form, label kept | KILLED by Verilator; inventory unchanged |
  | `rm4` | `g_rs_agg_check` as `$warning` | KILLED, both legs |
  | `rm5` | encoder as `$error` | KILLED, both legs, with Yosys `elaborated` |
  | `rm6` | originator floor dropped | SURVIVES, as predicted (S1) |
  | `rm7` | `NAME_ENTRIES_P == 0` dropped | SURVIVES, as predicted (S1) |

### Tests

- **The bench runs at the head:**
  - Verilator + Yosys (sv2v 0.0.13): `elab guards: 155 checks: 155 PASS, 0 FAIL`;
  - Yosys only (sv2v 0.0.12): `93 checks: 93 PASS, 0 FAIL`;
  - hosted Yosys 0.33: 93/93.
- **The tally line** is in the form `scripts/run_suites.sh` reads (`N checks: N PASS, M FAIL`).
- **Changed benches:**
  - `make -C tb/pp_top line-guards if-guards`: 6 cases and 4 checks, 0 failing, with refusals graded as `USERFATAL` (`receipts/head-pp_top-line-if-guards.log`).
  - The five mutation patches whose context this PR changed apply with `patch -p1 --dry-run` (`receipts/patch_apply_check.log`).
- **Matrix:** `scripts/gen_matrix.py --check` rc 0, 94 rows, 0 untested, at base and head.
- **Hosted, exact head, executed jobs:**
  - `docs-gates` succeeded twice. `make check` reports links 1191, ids 567 files, figures with 5 hand-authored, params 29/29/29, all OK (`receipts/hosted-docs-gates-push-114413930614.log`).
  - `portability` succeeded twice.
  - `suites` was **in progress** at the snapshot (`receipts/hosted_checks_snapshot.txt`) and is not counted here.

### Docs

- **The §2.1 table, re-measured** on a one-guard probe (`scripts/forms_probe.sh`, `receipts/forms_probe.log`): every Verilator, sv2v 0.0.12 + Yosys and sv2v 0.0.13 + Yosys cell reproduces.
  - Module-scope `$fatal` is refused everywhere.
  - `$error` elaborates only under sv2v 0.0.13.
  - `$warning` elaborates everywhere except Verilator.
  - `$info` elaborates everywhere.
  - An `initial` `$fatal` elaborates in Verilator, and is refused under sv2v 0.0.12 (`Can't resolve task name`) and 0.0.13 (`$finish`).
  - The Vivado columns agree with the public round-1 receipts (`[XSIM 43-4462]` for `$error` at base, `[VRFC 10-8279]` and `[Synth 8-6058]` at head).
- **"The versions the reference platform's CI pins"** is true: parent dev `ac2c5e77` pins sv2v `v0.0.12`, and its zip sha256 `ff8c9eea...` equals the release I downloaded. It pins Yosys `v0.66`.
- **These match the code and the measurements:** `hdl/README.md` rule 6, the HDL engineer guide §2 row and §2.1 prose, `tb/elab_guards/README.md` (case table, tally arithmetic 31 + 62 = 93 and + 62 = 155, mutation record), `tb/nvm_port/README.md`, the `elab_bounds.sh` header, `tb/pp_top/README.md`, and the `if_guards.py`/`line_guards.py` docstrings.
- **The PR body's round-2 claims** match this reviewer's runs where reproducible: 160/160 per converter, 93 hosted checks, production HDL unchanged in round 2. The Vivado claims are covered under Real limits.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #151 acceptance (3 items); lane scope 6098621173 and round-2 comment 6105580039 (items 1-6); independent 31-guard inventory; condition identity by diff and by the head bench on base; bench at head in Verilator, sv2v 0.0.12 + Yosys and sv2v 0.0.13 + Yosys; hosted Yosys 0.33 leg; round-1 Vivado receipts at byte-identical HDL; Rule 12 scan | R604-2 | `02063dc1b593d422406991bf0bc60e5cc47828ff` |
| RTL | CLEAN | 13 changed `hdl/` files; the listener's `initial` to generate move; `lint_hdl.sh` base and head; default-shape netlist identity for 13 tops under 2 sv2v versions, with a negative control; ROM digests | R604-2 | `02063dc1b593d422406991bf0bc60e5cc47828ff` |
| Robustness | CLEAN | boundary pairs and fixture contexts; deadline UNSIGNED allowance and its two arms; `elab_bounds.sh` under 2 sv2v; `-Wno-fatal` simulation probe; 7 reviewer mutants | R604-2 | `02063dc1b593d422406991bf0bc60e5cc47828ff` |
| Tests | CLEAN | `tb/elab_guards` (`guards.py`, `mutants.py`, Makefile, README); 160-arm campaign under 2 converters with per-kind tallies; `tb/pp_top` line and IF guards; 5 changed mutation patches; `gen_matrix --check` base and head; hosted docs-gates and portability logs (suites in progress) | R604-2 | `02063dc1b593d422406991bf0bc60e5cc47828ff` |
| Docs | CLEAN | `hdl/README.md` rule 6; HDL engineer guide §2 and §2.1 (re-measured); integrator guide §2; diagram 21 (rendered); `09_verification.md` §8; `tb/elab_guards`, `tb/nvm_port`, `tb/pp_top` READMEs and docstrings; PR body | R604-2 | `02063dc1b593d422406991bf0bc60e5cc47828ff` |

The five SUGGESTIONs (S1 to S5) leave every lens clean. No RESIDUE is recorded this round.

## Real limits

- **Vivado is not installed on this host.**
  - The issue's xvlog/Vivado criterion rests on the public round-1 receipts at byte-identical HDL.
  - The round-2 Vivado claims in the PR body have no public receipt at this head, because the author's round-2 packet is not yet published. Those claims are "all 31 boundary pairs in five toolchain combinations" (the new passing values `RESP_BYTES_P=17`, the deadline 1s and the fixture contexts) and "62 tightened and loosened arms in both vendor front ends". I did not verify them.
- **Focused gates only, by rule.** I did not run `scripts/run_suites.sh`, the whole `syn/yosys/run.sh`, `make check` locally, or the out-of-context Vivado netlists. For those I rely on the hosted jobs and the author's records. Hosted `suites` was still running at the snapshot.
- **Netlist identity covers default shapes only:** the 13 guard-carrying tops, with Yosys. Non-default shapes and parent shipping shapes were not compared.
- **No scratch parent was built.**
  - The parent disposition patch named in the REVIEW READY comment sits at a non-public path, outside this reviewer's reach.
  - The parent's whole-tree `check_py_idiom.py` ratchets and `measure_test_evidence.py --check` were not run. My Rule 12 check is the parent's per-module scan, applied to the four touched processor Python files.
- **Toolchain:** Yosys 0.66 is a distribution build (`86f2ddebc-dirty`). The hosted job uses apt Yosys 0.33 and an unprinted "latest" sv2v.
- **No manager source bank exists at this head, and none is claimed or inferred.** Physical calibration was NOT RUN. Field skips are not hardware proof. No hardware was used.

## Pending manager duties

- Merge-turn validation of the current-dev candidate (source base `2cbed0a9`, live dev `ac2c5e77`): builder and native banks, plus donor and consumer banks. The consumer bank runs with the pp170 parent-name-evidence patch and this lane's parent disposition patch. Confirm the parent's `check_py_idiom.py` and `measure_test_evidence.py --check` rc 0 there, and link the receipts on the PR.
- Accept or reject the hosted `suites` jobs at this head; they were in progress at the snapshot. Hosted and act acceptance is the manager's.
- Publish the author's round-2 packet, including the Vivado legs for the new boundary pairs and arms, if it is to be relied on.
- Parent follow-ups carried from round 1, outside this PR:
  - the parent lint gate drops processor-path Verilator diagnostics;
  - the parent's own `KL_nvm_backend.sv` guard is still a `$error`.
- Residue checklist: nothing new from this round.

## Integrity

- The review clone is unchanged after all probes (`receipts/clone_integrity.txt`):
  - HEAD is `02063dc1...` and `git write-tree` equals tree `2fd23c4c...`;
  - `status --porcelain --ignored` is empty;
  - the 592 index entries equal the pre-probe snapshot and the HEAD tree (modes and blobs);
  - 0 worktree blob mismatches;
  - the repository has no gitlinks and no `.gitmodules`.
- All edits and builds happened in copies under the packet's `scratch/`, which is not published.
- Tool identities are in `receipts/tool_identity.txt`. The pinned Verilator 5.050 was verified by version and sha256; sv2v 0.0.12 by release-zip sha256.
- The scripts are in `scripts/`. Every published file is listed in `MANIFEST.sha256`.

R604-2 FINISHED
