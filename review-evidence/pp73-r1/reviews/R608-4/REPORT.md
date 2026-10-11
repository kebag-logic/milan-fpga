[R608] POSITIVE - exact head 4029dc5de2a0a540d6a015c747319fbee7abba2e

# R608-4: internal independent delta review of issue #73 / PR #174

- **Head:** exact head `4029dc5de2a0a540d6a015c747319fbee7abba2e`, tree `33ec74ea7812208d7648475763816bc14a80bc8a`.
- **Base and delta:** source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`. The round-4 delta is `15981b51..4029dc5d`: one commit, 11 files.
- **Scope was reconstructed from:**
  - the issue's acceptance items 1-4;
  - the lane scope (6100509798) and the Mark II re-scope (6009640063);
  - rounds 2 and 3 (6104932386, 6105354276, 6107323038);
  - the round-4 ruling (6112358948): option (a), hold `echo_entries` by construction;
  - `docs/README.md`;
  - 09 §7/§8.10, the REQ-VER-002 row and GAP-11 in 00, and the suite README.
- **Missing files:** the repository has no AGENTS.md and no CONTRIBUTING.md.
- **How this report was written:**
  - The verdict, findings and ledger come from an independent pass over the delta and my own probes. They were written to this file before any prior review was opened.
  - The public R608-3 and R609-3 findings were read only after that. They are resolved in their own section below.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR is open. All five lenses are CLEAN.

Three items are open, and none of them changes the verdict:

- **Two RESIDUEs** (R1, R2). Both are wording only.
- **One new SUGGESTION** (S1).
- **Three retained SUGGESTIONs** from earlier rounds.

Every round-4 ruling item is met at this head:

| Ruling item | At this head | Evidence |
|---|---|---|
| **Membership.** Each `echo_entries` member is either a shared program that no served command owns as its first entry, or listed in `shared_entries`. Anything else is refused by name. | **Met.** `scripts/aecp_gate/table.py:169-179` refuses a member that is not in `shared_entries` when it is a first entry, or is used by fewer than two commands. Each refusal line names the member. A non-list or non-string member is refused as well. The check runs inside `check_schema` (`table.py:206`), so the gate, `--write`, the suite verdict and the record step all refuse. `BADARG` and `NSUPPE`, which are also first entries, are now listed in `shared_entries` (`aecp_commands.json:44-45`). | Probes F2, F3 (GCLKS), F5 (RDESCENT), F6 (key removed), F7 (string) and F8 (NSUPPE unlisted) are each refused by name. F4 (TIZ4NS, shared and unowned) is accepted, as clause 1 allows (`receipts/probe-echo-head.log`). |
| **Exemption scope.** The echo exemption covers non-SUCCESS answers only. A SUCCESS answer must have the table's response size. | **Met in both consumers.** The ROM walk uses `echo_ok = (s != 0 and e in echo_shared) or echo` (`rom.py:336`). The observed answers use the same rule (`record.py:326`). Before this commit, both granted the exemption for every status. | At head: M1-M3 (E_BADARG, E_NSUPPE and E_NOTIMPL set to SUCCESS) fail with `rom: <CMD>: E_<prog> answers SUCCESS at cdl 12`. M4 and M5 (observed SUCCESS at the echo length from BADARG and NOTIMPL) fail with `decode: <CMD>: <prog> answered SUCCESS at the command's own length`. At `15981b51`, M4 and M5 give **0 findings**, and M1-M3 show only incidental status-set lines (`receipts/probe-echo-prev.log`). |
| **Self-test.** R608-3's `echo-hide` drift is planted, and the gate or the suite fails it by name. | **Met.** The `FILE_MUTANTS` entry (`selftest.py:44-61`) plants the exact file edit and expects `schema: echo_entries: EAVL … nor listed in shared_entries`. Nine further in-memory plants (`plants.py:136-154`) cover the membership refusals and the SUCCESS scope, for the ROM, observed and symbolic forms. | R608-3's own `probe_engine.sh echo-hide`, rerun at this head, returns `--write` rc 1, record rc 2, gate rc 1 and suite rc 2. Each step names `schema: echo_entries: EAVL`. At `15981b51` all four were rc 0. The `echo-control` variant still fails by name (`receipts/r608-3-engine/`). With EAVL also listed in `shared_entries`, so that membership passes, the suite names `decode: ENTITY_AVAILABLE: EAVL answered SUCCESS at cdl 12`. After `make record`, the gate still names both the `decode:` and the `rom:` line (`receipts/suite-echo-hide-*.log`). |
| **Registry.** The entry is *held*, and the generated references are regenerated. | **Met.** `aecp_fields.json:694-717` is *held*, with a consumer, a check and a probe. The registry has 62 fields: 30 held and 32 held to nothing. The field sweep plants `echo_entries` and reports `caught`. REQ-VER-002 Arch (`00:535`), the 09 §8.10 registry block (`09:654-657`) and the gate docstring (`check_aecp_commands.py:115-118`) are regenerated. The gate's reference check passes. | `aecpcmd` rc 0. `--pr-body` passes against the published PR body (rc 0, `receipts/head-prbody-check.*`). |
| **R609-3's POSITIVE scope is unchanged.** | **Met.** The delta touches only the echo rule, its plants, two `shared_entries` keys and the generated references. No production HDL changed. Both ROMs are byte-identical across base, `15981b51` and head. The suite still gives 176/176, and the 16 standing controls are unchanged. The self-test grows from 220 to 231 plants: nine plants, one file plant and one held field were added, and no prior plant was removed. | See below. |

## Executed at the exact head

Every run used a disposable `git archive` export under `scratch/`. The review clone was never written; read-only `check-ids.py` and `check-figures.py` were run in it with bytecode writing disabled. Independent campaigns ran concurrently, each with its own log and rc file.

| Check | Result | Receipt |
|---|---|---|
| Simulator identity | Pinned simulator 5.050, rev v5.050, wrapper sha256 `905795b9…` | `receipts/toolchain.txt` |
| `aecpcmd --selftest` | rc 0. **231 planted defects, 231 caught by name.** It reports the same under `-O` | `receipts/head-selftest.*`, `head-selftest-O.*` |
| `aecpcmd` gate | rc 0: 31 commands, 84 entries, 41 F06.14 rows | `receipts/head-gate.*`, `head-make-aecpcmd.*` |
| `tb/aecp_cmds` suite | rc 0. 585760 trials, 0 timeouts, 176/176 PASS | `receipts/head-aecp_cmds-run.*` |
| Standing controls (`mutants.py --jobs 6`) | rc 0. **16 of 16** fail with their named lines. Golden and restored PASS | `receipts/head-aecp_cmds-mutants.*` |
| `make` links, matrix, modmatrix, params (export); ids, figures (clone, read-only) | All rc 0. Links 1188, 115 REQ rows, 94 matrix rows with 0 untested, 571 ID files, figures OK. The export-only ids/figures attempt failed with rc 2 because the export has no git index. That is a setup limit, and the clone rerun passes | `receipts/head-make-*`, `head-clone-*` |
| ROM identity | `ucode.hex` `518b900c…` is identical at base, `15981b51` and head. `ltn_rom.hex` `23cc67ee…` is identical at base and head. The `ucode.hex` digest equals the one recorded in `decode.json` | `receipts/ucode-digests.txt` |
| Production HDL | Under `hdl/`, only `aecp_commands.json`, `aecp_fields.json` and `gen_ucode.py` change from base to head. The only `.sv` change is the bench wrapper | `receipts/hdl-diffstat.txt` |
| Delta probes at head and at `15981b51` (16 each) | All as tabulated above | `receipts/probe-echo-{head,prev}.log`, `scripts/probe_echo.py` |
| Suite-level echo-hide (plain, shared, shared after re-record) | All fail by name (plain rc 2, shared rc 2, re-recorded gate rc 1) | `receipts/suite-echo-hide-*`, `scripts/suite_echo_hide.sh` |
| R608-3 `probe_engine.sh` echo-hide and echo-control | Every step fails by name. One adaptation: a `rm -rf` of the fresh target directory was dropped | `receipts/r608-3-engine/`, `receipts/r608-3-probe_engine-adaptation.diff`, `scripts/r608-3/` |
| Parent Python rules | I ran the parent's own `check_py_idiom.scan` (public, at `ac2c5e77`) over the 16 changed Python files at `15981b51` and at head. The only hit is the pre-existing `gen_ucode.py` long-module count: 1 at prev, 1 at head. The new functions are short, annotated and documented | `receipts/py-rules-delta.txt`, `parent-style-checker-identity.txt`, `scripts/py_rules_delta.py` |
| Clone integrity | Exact HEAD, tree and index; detached. No untracked or ignored files. 610 entries with no byte or mode mismatch. Zero gitlinks and no `.gitmodules` | `receipts/clone-integrity.txt` |
| Hosted push run 38178399598 (exact head; inspected, not owned) | **Executed:** docs-gates **success** (its `make check` step includes `aecpcmd`) and portability **success**. **Not finished:** suites was in progress when read. Its simulator build step was *skipped* on a cache hit, and the standing-controls step was pending. **No pull_request run** was listed at this head | `receipts/hosted-jobs.txt`, `hosted-*.json` |

**Author's exact-head receipts (not reviewer reruns).** These are published at milan-fpga `0cc8f8f5` under `review-evidence/pp73-r1/author-r4/receipts/r4/`:

- `head.sha` = `4029dc5d…`, and `final-identity.json` places the scratch parent `e8454e27` with its gitlink at this head;
- `rom-identity.tsv` gives the same two ROM digests as mine;
- disabled-check controls: `membership-disabled.log`, `rom-success-disabled.log` and `record-success-disabled.log` show the new plants fail when their check is removed;
- the suite totals, campaigns and parent checks claimed in the PR body.

Some earlier attempts listed in `process-exit.txt` exit non-zero. Each is superseded by a final run that exits 0. I did not rerun the full suite bank, the campaigns, synthesis or the parent banks.

No manager source bank ran at this head, and none is claimed.

## Findings

### R1 - RESIDUE - two hand-written size claims omit the `echo_entries` exemption (wording only)

- **Lenses:** Docs.
- **Where:**
  - `tb/aecp_cmds/README.md:69-70`: "every response the bench saw fits its response rule and carries a status of its set, subject to the registry's trusted common_status and engine_status exemptions."
  - `docs/architecture/09_verification.md:488` (the µcode row): "Every response and unsolicited body has the table's size."
- **Why:** both statements are hand-written prose. A non-SUCCESS answer of an `echo_entries` program may carry the command's own length (`rom.py:336`, `record.py:326`). The adjacent 09 row (`:490`), the registry and the generated Arch cell state the exemption correctly. No measurement, test, code or generated artifact changes.
- **Exact fix:**
  - **README.** Append to the README sentence: "; a non-SUCCESS answer of an `echo_entries` program may instead carry the command's own length."
  - **09.** Replace the 09 sentence with: "Every response and unsolicited body has the table's size, except that a non-SUCCESS answer of an `echo_entries` program may echo the command (the `echo_entries` row)."
- **Effect:** none on the verdict or on any lens. Carried to the manager's residue checklist.

### R2 - RESIDUE - the PR body says no existing public text was edited, but its round-3 residue was applied (wording only)

- **Lenses:** Docs.
- **Where:** PR #174 body as published at review time, Round 4 section (`receipts/pr174-body-at-review.md:83`): "The publication-wording residue remains assigned to the merge manager under parent #495; no existing public text is edited."
- **Why:** the body was edited at 2026-10-11T21:56:21Z (`receipts/pr174-body-edits.json`). Line 34 now carries R609-3-R1's exact replacement text, and the "have not been pushed" sentences are gone.
- **Exact fix:** replace the quoted sentence with "The round-3 wording residue (R608-3-R1 / R609-3-R1) is applied in this body; its record goes to parent #495 at merge."
- **Effect:** none on the verdict or on any lens. Carried to the manager's residue checklist.

### S1 - SUGGESTION - a `shared_entries` key can admit a single-use first entry to the non-SUCCESS echo exemption

- **Lenses:** Robustness, Tests.
- **Where:**
  - `table.py:174-179`: membership clause 2 accepts any key of `shared_entries`.
  - `aecp_fields.json:787-796`: `shared_entries` and `shared_entries.*` are *held to nothing*, and "added claims are not independently held".
- **Evidence** (`receipts/probe-shared-key-head.log`, `scripts/probe_shared_key.py`):
  - **The drift alone.** GET_CONFIGURATION's GCFG answers NO_SUCH_DESCRIPTOR at the echo length instead of cdl 16. On its own, it fails by name (S0).
  - **With two table edits.** Add `shared_entries.GCFG` and `echo_entries += GCFG`, and the same drift passes with 0 findings (S1). GCFG is the first entry of exactly one command.
  - **SUCCESS stays held.** The scope rule still stops a SUCCESS drift hidden this way, as F1 and the suite runs show.
- **Why this is not a finding:**
  - The ruling's clause 2 ("a program listed in `shared_entries`") permits this literally.
  - Both registry rows disclose the dependency.
  - The residual gap is limited to non-SUCCESS sizes and needs two deliberate edits to the table.
- **Recommendation:**
  - Refuse a `shared_entries` key that is the first entry of exactly one command and appears in no other command's `entries`. The `unserved` program and the non-entry programs (DLKILL, NOSEND, NAMEERR) are exempt.
  - Alternatively, state in the `shared_entries.*` reason that a key also admits its program to `echo_entries`' non-SUCCESS exemption, and plant S1 as a self-test case.

### Retained suggestions (verdict-neutral, not taken this round)

- **R608-3-S1:** add an over-length count-1 mapping trial at cdl 36 (`tb/aecp_cmds/sim_main.cpp`, unchanged this round).
- **R608-2-S1 = R608-3-S2:** the MVU protocol-id bytes @22 and @24 are never made wrong.
- **R608-2-S3 = R608-3-S3:** a held lock, a deadline kill and a nonzero descriptor_index are never driven.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling 6112358948 items 1-4 against `table.py` `_echo_entries`, `rom.py` `_entries`/`fits`, `record.py` `_answers` and `aecp_commands.json` (`echo_entries`, `shared_entries`); issue acceptance 1-4 and the lane scope; REQ-VER-002 and GAP-11; F06.14 regenerated byte-equal by the gate | R608-4 | 4029dc5de2a0a540d6a015c747319fbee7abba2e |
| RTL | CLEAN | No production HDL change; `ucode.hex` and `ltn_rom.hex` identical at base, prev and head, and equal to the `decode.json` digest; bench built and swept with the pinned simulator (176/176); 16/16 compiled controls; suite-level echo-hide builds | R608-4 | 4029dc5de2a0a540d6a015c747319fbee7abba2e |
| Robustness | CLEAN (S1 suggestion) | Membership edges F2-F8; SUCCESS-scope probes M1-M5 at head and at `15981b51`; the load-bearing check that each current member is needed (M0); the re-record escape; the `shared_entries` admission probe | R608-4 | 4029dc5de2a0a540d6a015c747319fbee7abba2e |
| Tests | CLEAN | Self-test 231/231 (normal and `-O`), including the R608-3 echo-hide file plant and nine new in-memory plants; the field sweep with `echo_entries` held; R608-3's `probe_engine.sh` echo-hide/echo-control; standing controls; CI wiring unchanged | R608-4 | 4029dc5de2a0a540d6a015c747319fbee7abba2e |
| Docs | CLEAN (RESIDUE R1, R2) | Registry entry; generated REQ-VER-002 Arch, 09 §8.10 block and gate docstring; the PR field reference (`--pr-body` rc 0); 09 §8.10 hand-written rows; `tb/aecp_cmds/README.md`; the PR body's round-4 text and its edit history | R608-4 | 4029dc5de2a0a540d6a015c747319fbee7abba2e |

## Prior public findings at this head

These were read after the sections above were written.

| Prior finding | Status | Evidence |
|---|---|---|
| R608-3-F1 (MINOR: `echo_entries` held to nothing; echo-hide all green) | **RESOLVED by option (a)** | Membership is held by construction and the exemption is non-SUCCESS only, in both consumers. R608-3's own echo-hide probe now fails at every step by name, and so do the shared-key and re-recorded variants. The registry entry is *held*, with a field-sweep plant. The references are regenerated. R608-3's alternative (b) items (conditioning the `response.cdl` text) were not required under (a). The leftover prose is R1 |
| R608-3-R1 / R609-3-R1 (PR body "not pushed" wording) | **RESOLVED in the body** | The exact R609-3-R1 replacement is at body line 34, and both "not pushed" sentences are gone (edit at 21:56:21Z). The ruling routes its record to #495 at merge. The new mis-statement about it is R2 |
| R608-3-S1 (count-1 over-length trial) | Not taken | Retained |
| R608-3-S2 = R608-2-S1 (MVU protocol-id bytes) | Not taken | Retained |
| R608-3-S3 = R608-2-S3 (unswept outcomes) | Not taken | Retained |
| R609-3 (POSITIVE; R609-3-R1 and two suggestions) | Scope unchanged | R609-3-R1 is resolved as above. Its retained suggestions are the two listed. Every R609-3 dispositions row (registry, per gcd, step refusals, status/oversize declarations, `documented[]`, generator refusals, decode/dispatch, sizes, prerequisites) is untouched by this delta. The 220 earlier plants and the 16 controls still pass |
| Earlier rounds (R608-1/2, R609-1/2) | Resolved at earlier rounds; nothing regressed | Standing q1, q2, floor and mapping controls fail by name. The prior plants are all inside the 231 |

## Real limits

- **Not run here:**
  - the full processor suite bank (`run_suites.sh`) and the nine existing campaigns;
  - `syn/yosys/run.sh`;
  - `lint_hdl.sh`;
  - Mermaid lint and the WaveDrom re-render (this delta changes no figure);
  - every parent, consumer, builder or native bank.

  For these, the evidence is the author's published exact-head receipts, the unchanged production HDL and the identical ROMs.
- **Parent Python rules:** my check runs the parent's scanner per file. It is not the parent's budgeted bank.
- **Hosted run 38178399598:** suites had not finished when read, and its simulator build was skipped on a cache hit. No pull_request run was listed. That run tests the merge with processor main `6d536868`, which this head does not contain. The manager owns hosted and act acceptance.
- **Bounded sweep:** opcodes above 0x007F, cdl above 100, unswept outcomes, GDI ceilings, the trusted status exemptions and `shared_entries` claims (S1) are declared limits, not proof.
- **Hardware:** physical calibration NOT RUN, no hardware was used, and field skips are not hardware proof.

## Pending manager duties

- **Merge-turn validation.** The current-dev merge candidate (source base `2cbed0a987c1e68402658d69459ab7e5aa571adc`, live dev `09c7231eca343607c97c0d66abebb2553688712c`) needs the builder and native banks, with receipts linked on the PR. It must include processor main `6d536868`.
- **Parent consumer bank at this head**, with the applicable evidence patches: the Python budgets and the `tb/aecp_cmds` evidence-reader disposition.
- **Hosted acceptance.** The suites job, including "AECP command decode standing controls", and the pull_request merge run.
- **Residue checklist:** R1 and R2, plus the round-4 ruling's carry of R1 to milan-fpga #495.
- **Follow-up lane:** the parent gate over the exported table and registry.

Packet: portable scripts and raw receipts are listed in `MANIFEST.sha256`. One redaction was applied to five build logs: the local simulator install prefix was replaced by `$SIMULATOR_PREFIX` (`receipts/redactions.tsv`). `scratch/` is disposable and not published. No source fix, commit, push, GitHub write, merge, author contact, sub-agent, container CI, shared install or hardware access occurred.

R608-4 FINISHED
