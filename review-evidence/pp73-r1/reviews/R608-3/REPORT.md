[R608] NEGATIVE - exact head 15981b511370a8cfb58ec023fae27f8a800c058c

# R608-3: internal independent delta review of issue #73 / PR #174

- **Head:** exact head `15981b511370a8cfb58ec023fae27f8a800c058c`, tree `e4dacda27467378e175562d5001b8dbadea9d4bd`.
- **Base and delta:** source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`. The round-3 delta is `9975764..15981b5`: four commits, 20 files.
- **Scope was reconstructed from:**
  - the issue's acceptance items 1-4;
  - the lane scope (6100509798);
  - round 2 (6104932386) and its addendum (6105354276);
  - the round-3 assignment (6107323038);
  - `docs/README.md`;
  - 06 §6/§8, 09 §7/§8.10, and the REQ-VER-002 row and GAP-11 in 00.
- **Missing files:** the repository has no AGENTS.md and no CONTRIBUTING.md.
- **How this report was written:**
  - The verdict, findings and ledger come from an independent pass over the diff and my own probes.
  - The public R608-2 and R609-2 findings were read only after that pass. They are resolved in their own section below.

## Verdict

**NEGATIVE.** One MINOR is open (F1). It leaves the Robustness, Tests and Docs lenses unclean.

Every item the round-3 assignment rules by construction is met at this head:

- **Registry.** The field registry is exhaustive in both directions. Every *held* field has a standing named drift. The docstring, 09 §8.10 and REQ-VER-002 Arch are generated and checked, and the published PR field reference matches the registry.
- **Record steps.** Echo-row `per` is held exactly by the accepted-offset gcd, including after re-recording. Zero, null, negative, bool and float steps are refused.
- **Half-record observation.** A count-1 half-record trial is observed. Both 4-byte and 16-byte engine step controls fail by name.
- **Held-to-nothing declarations.** `common_status`, `engine_status` and `oversize` are declared held to nothing.
- **`documented[]`.** Its semantic fields are separated from its identity and rendering fields.
- **Generator refusals.** All eight generator refusals, and five more, print named lines, both normally and under `-O`.
- **ROMs.** Both ROM images are byte-identical across base, round 2 and head. No production HDL source changed.

What remains is the same class the assignment ruled for statuses, now on response sizes:

- **The trusted exemption.** `echo_entries` is declared held to nothing.
- **The unconditional claims.** The *held* claim on `commands[].response.cdl`, the REQ-VER-002 Arch cell and 09 §8.10's size claims are not conditioned on it.
- **The probe.** A one-element `echo_entries` edit hides a real ENTITY_AVAILABLE response-size drift. With it, the gate, the re-recorded sweep and the suite are all green, and F06.14 still says cdl 32.

## Executed at the exact head

Receipts are under `receipts/`. Every run used a disposable extraction under `scratch/`. The review clone was never written.

| Check | Result | Receipt |
|---|---|---|
| Simulator identity | Verilator 5.050 rev v5.050; wrapper sha256 `905795b9…` | `toolchain.txt` |
| `aecpcmd --selftest` | rc 0. **220 planted defects, 220 caught by name**. The field sweep reports 29 of 29 held fields `caught` | `head-runs/selftest.log`, `.rc` |
| `aecpcmd` gate | rc 0: 31 commands, 84 entries, 41 F06.14 rows | `head-runs/gate.log` |
| `tb/aecp_cmds` suite | rc 0. 585760 trials, 0 timeouts, 176/176 PASS | `head-runs/suite.log` |
| Standing controls (`make -C tb/aecp_cmds mutants`, 4 jobs) | rc 0. **16 of 16** fail by their named line, including `mappings-four-byte-record` (gcd 4) and `mappings-sixteen-byte-record` (gcd 0). Golden and restored PASS | `mutants/results.json`, `mutants/*-run.log`, `head-runs/mutants.log` |
| `make` links, matrix, modmatrix, params; ids, figures, lint (scratch git clone); stale (clone, read-only) | all rc 0. ids 571 files; links 1188; lint 41 Mermaid and 18 WaveDrom blocks | `make_check_subset.txt`, `head-runs/make-*.log` |
| ROM identity | `ucode.hex` `518b900c…` and `ltn_rom.hex` `23cc67ee…` are identical at base, `9975764` and head. The `ucode.hex` digest equals the one `decode.json` records | `rom_digests.txt` |
| Production HDL | Base to head, the only `.sv` change is the bench wrapper `tb/aecp_cmds/aecp_cmds_wrap.sv`. Under `hdl/`, only `aecp_commands.json`, `aecp_fields.json` and `gen_ucode.py` change | `production_hdl_diff.txt` |
| 26 table and registry probes (F06.14 regenerated where semantic) | all as expected. Per drifts (8→4 on both rows, 8→16, 8→2) fail naming the command and the gcd. Zero, null, negative, bool and float `per` are refused by schema. A documented-GDI opcode drift fails semantically. Unregistered fields, stale registry entries, a held field without a probe, and a reason or status edited without `--write` all fail by name. The four declared limits pass, as declared. **The published PR body's field reference matches the registry** (`--pr-body`, rc 0) | `probe_table.json`, `.txt`, `pr174-body-at-review.md` |
| Generator alone, 13 defects × {normal, `-O`} | 26 of 26 exit 1 with a named last line and no traceback. Unmodified: rc 0, 2048 words, 89 programs | `probe_generator.json`, `.txt` |
| Engine and ROM probes (build, sweep, record, gate, suite) | `step-12`: fails by name (gcd 0) on both mapping commands, before and after re-recording. `echo-control`: fails by name. **`echo-hide`: everything green (F1)**. `count1-overlength`: only the input digest fails (S1) | `engine/summary.txt`, `engine/*.log`, `engine/echo-hide.*` |
| Parent Rule 12 approximation over the 16 changed Python files | One hit: `gen_ucode.py` module length (2507 lines; 2433 at base). It predates this lane, and the author's consumer receipts show the parent budgets unchanged | `py_rules_head.txt` |
| Clone integrity | Exact HEAD, tree and index. Detached. No untracked or ignored files. 610 entries with no byte or mode mismatch. No gitlinks and no `.gitmodules` | `clone_integrity.txt` |
| Hosted run 38162911571 (push, exact head; inspected, not owned) | docs-gates **success**: its `make check` step includes the AECP command model. portability **success**. suites **in progress**, with the simulator build step *skipped* on a cache hit, so that is not an executed build. No pull_request run at this head was listed when read | `hosted_jobs.txt`, `hosted_runs_at_head.tsv` |

**Author's exact-head receipts (not reviewer reruns).** These are published at milan-fpga `7ee91b25` under `review-evidence/pp73-r1/author-r3/receipts/r3/`:

- `final-head.sha` = `15981b51…`;
- `head-final-check.log` rc 0, with the field sweep;
- original suite records byte-identical;
- nine campaign pairs unchanged;
- `generator-final.txt`;
- the parent at `e8454e27` with the gitlink at this head.

No manager source bank ran at this head, and none is claimed.

## Findings

### F1 - MINOR - response sizes are held only as far as the untrusted `echo_entries`; the claims are not conditioned on it

- **Lenses:** Robustness, Tests, Docs.
- **Where:**
  - **The exemption in code.** `scripts/aecp_gate/rom.py:320,336` with `fits` at `rom.py:293`: a header-only send from any `echo_entries` program fits every rule. `scripts/aecp_gate/record.py:314,318,332,335`: an `echo_entries` program may answer at the command's own length, or at any cdl it was sent at. No check holds membership: `echo_entries` need not be a subset of `shared_entries`, and may name a served command's own program.
  - **Registry entries.** `hdl/aecp/ucode/aecp_fields.json:694` declares `echo_entries` *held to nothing*. But `:404` (`commands[].response.cdl`, *held*) and `:428` (`response.echo`, *held*) carry no condition on it. Contrast `:563` (`commands[].status`), which says "conditional on the trusted common_status and engine_status exemptions".
  - **REQ-VER-002 Arch.** `docs/00_MILAN_COMPLIANCE_REVIEW.md:535`, generated by `scripts/aecp_gate/field_docs.py:27-44`, says: "Explicitly held to nothing: commands[].engine_status, commands[].oversize, common_status. Status-path claims trust these status exemptions … decode/dispatch and sizes are observed or gated". The list is hard-coded to three paths (`field_docs.py:30-31`), and no size-path trust is stated.
  - **09 §8.10.** `docs/architecture/09_verification.md:481` (decode row: "every response the bench saw fits the response rule") and `:488` (µcode row: "Every response and unsolicited body has the table's size") are unconditional. Their status clauses were conditioned this round. The "Still hand-written and held to no table" list (`:504-509`) names the three status/oversize fields and omits `echo_entries`.
- **Authority:**
  - Round-3 assignment item 1: one class remains, "the docs say a table field is held … when it is not". The REQ-VER-002 Arch, 09 §8.10 and the docstring must come from, or be checked against, the registry.
  - Item 2 resolved the same trust for statuses by declaring it and conditioning the status claims.
  - The lane scope requires that a drift in any consumer fail by name.
- **Evidence:** `receipts/engine/`, scripts `scripts/probe_engine.sh echo-hide|echo-control`.
  - **The plant.** `E_EAVL` (ENTITY_AVAILABLE) drops its three `BUILD_FLD` words (flags and the acquired and locked controller IDs), replaced by NOPs at the same addresses. It then answers SUCCESS at cdl 12 instead of the table's 32.
  - **Control (`echo-control`), no table edit.** After `make record`, the gate (rc 1) and the suite (rc 2) name `decode: ENTITY_AVAILABLE: EAVL answered SUCCESS at cdl 12, the table's response is 32`, and the gate also names `rom: ENTITY_AVAILABLE: E_EAVL answers SUCCESS at cdl 12`.
  - **Hidden (`echo-hide`).** The same ROM edit plus `echo_entries += "EAVL"`, then `--write` and `make record`. The record step rc 0 (176/176), the `aecpcmd` gate rc 0, and the suite rc 0 (176/176).
  - **What the record and docs then show.** `echo-hide.decode-vs-head.diff` shows the re-recorded `decode.json` has EAVL answering `"0": "12"` and a new ROM digest. F06.14 still renders ENTITY_AVAILABLE as `44 B (cdl 32)` (`echo-hide.F06.14-row.txt`).
  - **Self-test.** No self-test plant or field-sweep entry exercises `echo_entries`. Being held to nothing, it has none.
- **Impact:**
  - A protocol-visible response-size defect can pass every gate and suite of this lane. It needs only a one-word edit to a field the registry calls trusted.
  - Meanwhile the generated REQ-VER-002 Arch, the registry's `response.cdl` claim and 09 §8.10 tell a reader that sizes are held unconditionally, and that only the status paths rest on trusted exemptions.
  - This is the R608-2-F2 class, with sizes in place of statuses. R608-2 noted `echo-entries-add-gctrs` as "only widens a check". This probe shows the widened check hides a real drift.
- **Required outcome:** choose one.
  - **(a) Hold `echo_entries` by construction.** For example:
    - require each member to be a shared program that no served command owns as its first entry, or one listed in `shared_entries`;
    - and/or restrict the echo exemption to non-SUCCESS answers, since the three current members answer failures only.

    Then plant an `echo_entries` drift in the self-test, and make the registry entry *held*.
  - **(b) Declare the trust everywhere the size claims are stated.** That means:
    - `commands[].response.cdl` and `response.echo` reasons, conditioned on `echo_entries` the way `commands[].status` is conditioned on its exemptions;
    - `arch()` in `field_docs.py`, so the Arch names `echo_entries` with the other explicit limits and says the size paths trust it;
    - 09 §8.10's decode and µcode rows and its "held to no table" list;
    - the PR field reference, regenerated.
- **Verification:**
  - Under (a): `scripts/probe_engine.sh <tree> <scratch> <out> <verilator> echo-hide` fails by name at the gate or the suite.
  - Under (b): the regenerated references carry the condition, `make aecpcmd` passes, and `scripts/probe_table.py` (`declared-echo-entries-extra`) still passes, as declared.

### R1 - RESIDUE - stale "not pushed" wording in the PR body (wording only)

- **Lenses:** Docs.
- **Where:** PR #174 body as published at review time (`receipts/pr174-body-at-review.md:34` and `:83`):
  - "The round-3 measurements below are local; its new commits have not been pushed."
  - "… merge-candidate or hosted acceptance. The new commits have not been pushed."
- **Why:** `15981b51` is the published head of the PR, and hosted run 38162911571 ran on it.
- **Exact fix:**
  - Replace line 34 with "The round-3 measurements below were taken locally before the head was pushed."
  - Delete the sentence "The new commits have not been pushed." from the last Validation paragraph.
- **Effect:** none on the verdict or on any lens. Carried to the manager's residue checklist.

### Suggestions (verdict-neutral)

- **S1 - keep an over-length count-1 mapping trial.** Round 3 changed the count-1 trial from cdl {28, 36} to {24, 28} (`tb/aecp_cmds/sim_main.cpp:306`), so no count ≥ 1 trial is longer than its records any more.
  - `count1-overlength` makes the engine accept count 1 at any cdl ≥ 28. It changes nothing the sweep observes: the only failure is the engine-input digest, so a re-record would be green.
  - The gate does not claim count-exact lengths; the gcd and floor claims still hold.
  - Recommendation: use `{24, 28, 36}` for count 1. The gcd is unchanged and the over-length refusal goes back into the record.
- **S2 (= R608-2-S1, not taken):** MVU protocol-id bytes @22 and @24 are never made wrong (`sim_main.cpp:397`).
- **S3 (= R608-2-S3, not taken):** a held lock, a deadline kill and a nonzero descriptor_index are never driven. Naming them in 09 §8.10's limits would make "outcomes no stimulus reaches" concrete.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Table vs Table 7-141 (schema map; `status_codes.*.code` field drift); F06.14 regenerated byte-equal by the gate; REQ-VER-002 and GAP-11 vs acceptance 1-4 and the lane scope; the parent export named (`aecp_commands.json` plus sibling `aecp_fields.json`) | R608-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |
| RTL | CLEAN | No production `.sv` change; both ROMs byte-identical across base, prev and head; the bench wrapper builds and sweeps clean with the pinned simulator; engine probes step-12 and count1-overlength | R608-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |
| Robustness | UNCLEAN (F1) | `fields.py`, `field_docs.py`, `field_plants.py`, `table.py` step refusals, `record.py` gcd, `rom.py` and `record.py` echo exemption; `gen_ucode.py` `_command_rows` and MVU regex; 26 table and registry probes; 26 generator probes; 4 engine and ROM probes | R608-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |
| Tests | UNCLEAN (F1) | Self-test (220 plants, 29-field sweep), `field_plants.py`, `plants.py` additions, 16 standing controls, `sim_main.cpp` count templates, `decode.json` digests, `mutants.py` doc copies, CI wiring (`hdl.yml`, `Makefile`) | R608-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |
| Docs | UNCLEAN (F1); RESIDUE R1 | Gate docstring, 09 §7/§8.10, REQ-VER-002 Arch, 06 §6 sentence, `tb/aecp_cmds/README.md`, the registry-generated references, the PR body (field reference checked via `--pr-body`) | R608-3 | 15981b511370a8cfb58ec023fae27f8a800c058c |

## Acceptance (issue #73) at this head

| # | Item | At this head |
|---|---|---|
| 1 | One machine-readable command table | Met: `aecp_commands.json` (31 rows) plus the registry `aecp_fields.json` (62 paths, 29 held) |
| 2 | Dispatch data and F06.14 generated or gated | Met in form. The size holding has the F1 condition gap |
| 3 | Gate in CI | Met. `aecpcmd` (including the field sweep) ran in hosted docs-gates at this head. Standing controls are in the suites job, which was still running |
| 4 | REQ-VER-002 and 09 §8 record generated vs hand-written | Met except F1: the size claims omit the `echo_entries` trust |
| Lane | ROMs and engine identical; planted drifts fail by name | Met. The parent consumer gates are the manager's |

## Prior public findings at this head

These were read after the sections above were written.

| Prior finding | Status | Evidence |
|---|---|---|
| R608-2-F1 (echo `per` held one way) | **RESOLVED** | `record.py:297-300` gcd check. Table probes per 8→4 (ADD, REMOVE), 8→16 and 8→2 fail naming the command. Standing controls `mappings-four-byte-record` and `mappings-sixteen-byte-record` fail by name. `step-12` fails before and after re-recording |
| R608-2-F2 (`common_status`, `engine_status`, `oversize` undeclared) | **RESOLVED by declaration** | Registry entries are *held to nothing*. The references are generated and checked. The status claims are conditioned. The four probes pass, as declared. The analogous size-side gap is the new F1 |
| R608-2-F3 (generator refusals) | **RESOLVED** | 26 of 26 generator probes are named, with no traceback, under normal and `-O` |
| R608-2-R1 / R609-2-R1 (stale push wording) | **RESOLVED for the quoted sentence**; recurs as R1 | The quoted sentence is gone and the exact texts appear in the body. New "not pushed" sentences remain (R1) |
| R608-2-S1 (MVU pid bytes) | Not taken | Retained as S2 |
| R608-2-S2 (undigested inputs) | **TAKEN** | `model_lint.py`, `model_rules.py` and `verilator_harness.hpp` are in `SWEPT_RAW` and `decode.json` |
| R608-2-S3 (unswept stimuli named) | Not taken | Retained as S3 |
| R609-2-F1 (`documented[]` called prose-only) | **RESOLVED** | The registry separates semantic `documented[].opcode`, `rtl` and `gdi` (held, each with a field drift caught) from `name` (identity) and `section`/`cells` (rendering). 09 §8.10 and the PR reference agree. The `documented-gdi-opcode` probe fails semantically |
| Earlier rounds (R608-1, R609-1) | Resolved at round 2 (per R608-2 and R609-2); nothing regressed | Standing q1 and q2 controls pass. Size and floor drifts are in the field sweep |

## Real limits

- **Not run here:**
  - the full processor suite bank (`run_suites.sh`) and the nine existing campaigns;
  - `syn/yosys/run.sh`;
  - `lint_hdl.sh`;
  - WaveDrom re-render (`wavedrom-check` needs a networked venv bootstrap; hosted docs-gates ran it, and the delta changes no WaveDrom block);
  - every parent, consumer, builder or native bank.

  For these, the evidence is the author's published exact-head receipts listed above, the unchanged RTL and the identical ROMs.
- **Hosted run 38162911571:** suites had not finished when read, and no pull_request run had been listed. The pull_request run tests the merge with processor main `6d536868` (#173, #151), which this head does not contain. The manager owns hosted and act acceptance.
- **Bounded sweep:** opcodes above 0x007F, cdl above 100 and undriven outcomes are declared limits, not proof.
- **Rule 12:** my Python rule check is an approximation, not the parent's `check_py_idiom.py`.
- **Hardware:** physical calibration NOT RUN, no hardware was used, and field skips are not hardware proof.

## Pending manager duties

- **Merge-turn validation.** The current-dev merge candidate: source base `2cbed0a9`, live dev `6bfeeb13`. It needs the builder and native banks, with receipts linked on the PR. It must also include processor main `6d536868`.
- **Parent consumer bank at this head.** With the `parent-name-evidence` and `parent-aecp-cmds-evidence` patches:
  - `check_py_idiom.py` budgets;
  - the evidence-reader disposition for `tb/aecp_cmds/mutants.py`;
  - the moved-pin docs at adoption.
- **Hosted acceptance.** The suites job, including the "AECP command decode standing controls" step, and the pull_request merge run.
- **Residue checklist.** R1.
- **Follow-up lane.** The parent gate over the exported table and registry.

R608-3 FINISHED
