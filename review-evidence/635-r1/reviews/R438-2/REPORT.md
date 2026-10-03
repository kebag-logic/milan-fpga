[R438] POSITIVE - exact head 420b778a52e4f4bcc8040c13bbc4bef9bc94ada0

# R438-2: milan-fpga issue #635 / PR #636, internal cleared-context round-2 review

- **Head under review:** `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0`, tree `845371799bcdb235cfe12ad4db2aeaf5fcafb61d`. That is five one-line commits on the round-1 head `3370c6cb`. Source base and live `dev` are both `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- **Scope reconstructed from public material only:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #635 body (frozen acceptance 1 to 5);
  - on #635: the round-1 assignment (5958619779), the round-2 assignment (5962734738), TAKEN (5962752104) and REVIEW READY (5963295768);
  - the PR #636 body's "Round 2" section, which is byte-equal to the author-r2 packet `PR-BODY.md` at `635-review-evidence` `37ccf808` apart from a trailing newline;
  - processor PR #140 and the processor sources at both pins.
- **The delta changes four files** (`receipts/delta_raw.txt`): `CHANGELOG.md`, `docs/reference/REGISTER_MAP.md`, `docs/reference/SUBMODULES.md`, and `hdl/milan/KL_pp_shadow.sv` (one comment line). All four gitlinks are unchanged (`receipts/gitlinks_head.txt`). Nothing outside the assignment changed.
- **Why POSITIVE:**
  - Every round-1 finding is closed at this head, under its original severity.
  - Each new factual claim in the delta matches the processor at `631eeb34`. Two of them were also confirmed by planting the processor's own reviewed mutation arms (`receipts/arm_*`).
  - The only new item is one SUGGESTION.

## Findings

### S1 - SUGGESTION - Conformance, Docs - `docs/reference/SUBMODULES.md:115` - the citation names only Milan's MVU table for every non-AEM type

- **Evidence.**
  - The row covers "a non-AEM command" and cites Milan v1.2 Section 5.4.3.3, Table 5.19. That table is the MVU status table.
  - For the other non-AEM types (ADDRESS_ACCESS, AV/C, HDCP APM, EXTENDED), the processor bases the same answer on IEEE 1722.1-2021 Table 9-2. See `KL_aecp_engine.sv:1743-1749` at `631eeb34` (`receipts/processor_source_checks.txt`) and PR #140 round 2, item 3.
- **Why this is not a defect.**
  - Nothing stated is false. Table 5.19 is the clause behind the row's named example, GET_MILAN_INFO.
  - The processor's operator guide (`docs/guides/operator.md:326`), which R438-1 F1 named as the text to match, cites the same table.
  - The linked PR carries the full clause set.
  - `CHANGELOG.md:49` ("Processor PR #140 cites Milan Table 5.19 for this") is literally true.
- **Optional fix.** Append "; IEEE 1722.1-2021 Table 9-2 for the other non-AEM types" to the row's citation.
- **Verification.** `check_submodule_docs.py` and the docs gates stay rc 0.

No BLOCKER, MAJOR, MINOR or RESIDUE is open.

## Prior public findings, judged at this head

Read only after this round's own pass over the diff (above, and "What was checked") was complete.

| Finding | Original severity | Status at `420b778a` | Evidence |
|---|---|---|---|
| R438-1 F1 = R439-1 F1: C5a's NOT_IMPLEMENTED echo, for a non-AEM command whose response memory fails, is not recorded | MINOR (Docs, Conformance) | **CLOSED** | See item 1 below. `CHANGELOG.md:46-49` and `SUBMODULES.md:115` now record it. The claims match the RTL at both pins and processor `operator.md:55` and `:326`. DL8 grades the behaviour, and the arm that restores the old answer fails DL8 4 times |
| R438-1 S1: bare `#80` at `KL_pp_shadow.sv:1099` | SUGGESTION | **CLOSED** | The line reads "manager ruling on protocol-processor #80". Processor #80 is the identify ruling (GAP-06); milan-fpga #80 is unrelated (`receipts/issue80_check.txt`) |
| R439-1 F2: the deadline-answer summary is too broad | RESIDUE | **CLOSED** | `CHANGELOG.md:44-45` carries the reviewers' words as two bullets. The split is forced: rejoined, the sentence fails `check_doc_style.py` rc 1, "sentence has 20 words; maximum is 10" (`receipts/probe_style_joined_sentence.*`). The text matches `KL_aecp_engine.sv:1723-1740` |
| R439-1 F3: bare `#80` | RESIDUE | **CLOSED** | The reviewers' exact text. The edit is comment-only: the comment-stripped diff `3370c6cb..420b778a` is empty (`receipts/kl_pp_shadow_comment_stripped.*`) |
| R439-1 F4: kill tie-offs on the hazard row | RESIDUE | **CLOSED** | The reviewers' exact text on both rows (`SUBMODULES.md:114`, `:116`). At `b2db3a97` the top tied `kill_valid_i`, `kill_id_i` and `kill_resp_queued_i` to 0 (`:983-985`). At `631eeb34` the deadline block drives them (`:1022-1024`) |
| R439-1 S1: the `ADP_IDX0[15:0]` meaning predates C3 | SUGGESTION | **CLOSED** | See item 3 below. The added ", and again after a D3 roll-back" is true. AD6 grades it, and arm `cfg-valid-hard-reset` fails AD6 |
| R438-1 F1's optional pointer from the REGISTER_MAP memory-bridge section (`REGISTER_MAP.md:2358`) | optional | Not taken, as disclosed | Both F1s called it optional. The section's trigger ("the entity answers ENTITY_MISBEHAVING") is still true for AEM commands at this pin. It stays optional |

## What was checked, per item

1. **C5a response-memory arm** (`ce948861`; `receipts/processor_source_checks.txt`, `pp_base_deadline.*`, `arm_mvu_fault_status_10.*`).
   - **At `631eeb34`:**
     - `st_echo_w` is true for every message type but AEM_COMMAND (`KL_aecp_engine.sv:1751-1753`).
     - On `rsp_fail_w`, both fault rebuilds set `ST_NOT_IMPLEMENTED_C`, `echo_r` and the command's payload length when `st_echo_w` holds: A_ALLOC at `:3756-3781` and A_WR at `:3783-3808`.
     - An AEM command still gets `ST_ENTITY_MISBEHAVING_C`, header only.
   - **At `b2db3a97`:** the same two states set `ST_ENTITY_MISBEHAVING_C` for every type, and `st_echo_w` does not exist (0 occurrences). So "at `b2db3a97` it answered ENTITY_MISBEHAVING" is exact.
   - **Clause citation:** PR #140 round 2, item 2, heads with "Milan v1.2 §5.4.3.3 Table 5.19 (MVU statuses SUCCESS and NOT_IMPLEMENTED; 2 to 31 reserved)". That supports both records' citation (see S1).
   - **Executed, on a `git archive` of `631eeb34`:**
     - `tb/pp_top` deadline build, section DL: rc 0, 64 checks, 0 failures.
     - Planting the processor's reviewed arm `mvu-fault-status-10`, which restores status 10 on the fault path: rc 2, DL 64 checks, 4 failures. All four are DL8 lines of the form "GET_MILAN_INFO answers MVU NOT_IMPLEMENTED with the command echoed, byte-exact (status 10, 60 bytes)". They cover a read error, a write error, a tied-off memory, and a command padded to 540 payload bytes.
     - So the recorded behaviour is graded, and the old pin's answer is what the arm reproduces.
   - **No top port or parameter:** the declaration diff of `protocol_processor_top.sv` between the pins adds only `EN_IDENTIFY_NOTIF_P` and `identify_button_i`, both from C6.
2. **Wording items.**
   - The deadline text was checked against `KL_aecp_engine.sv:1723-1740`. A SUCCESS not yet built becomes ENTITY_MISBEHAVING. A program that has produced an effect ends with its own answer.
   - The `#80` and tie-off items were checked as in the table.
3. **`ADP_IDX0[15:0]` fallback** (`420b778a`).
   - **The mux:** at `631eeb34`, the ADPDU index is `aecp_cur_cfg_v_w ? aecp_cur_config_o : current_cfg_i` (`protocol_processor_top.sv:1862`). The comment at `:1852-1856` says the default applies "from reset, and after a D3 roll-back".
   - **The valid flag clears on a roll-back:** the flag `dyn_cfg_v_r` resets on `store_rst_n_w` (`KL_aecp_engine.sv:1918-1920`), and `store_rst_n_w = rst_n && !d3_rb_rst_w` (`:1610`). So a roll-back clears it, and the ADPDU falls back to `current_cfg_i`.
   - **Parent wiring:** `current_cfg_i` is `ADP_IDX0[15:0]` (`milan_csr.sv:752`, `:2831`; `milan_datapath.sv:7611`).
   - **Executed:**
     - `tb/pp_top` `adp-config`: rc 0, AD 55 checks, 0 failures.
     - Planting the reviewed arm `cfg-valid-hard-reset` (the flag resets on the hard reset only, not with the store): rc 2, AD 2 failures. Both are AD6: "the first ENTITY_AVAILABLE carries the image default 1, byte-exact (got 0)", and the flag split from the store's for 96,227 clocks.
4. **Cited line numbers.** Every line the PR body and REVIEW READY cite was opened at the head and holds the quoted text: `CHANGELOG.md:44-49`, `SUBMODULES.md:114-116`, `REGISTER_MAP.md:1016`, `KL_pp_shadow.sv:1099`, `KL_aecp_engine.sv:1610`, `:1912-1920`, and `protocol_processor_top.sv:1852-1856`.

## Gates run at the head (`receipts/*.log`, each with its `.rc`)

Verilator identity: `Verilator 5.050 2026-07-01 rev v5.050`, the scoped install (`receipts/tool_identity.txt`).

| Gate | Result |
|---|---|
| `docs_check.py` | rc 0, 0 findings over 185 md files |
| `check_em_dash.py --base cdf49d1a` / `--base 3370c6cb` (pinned renderer, scratch venv) | rc 0: 0 findings over 69 / 9 added lines, arms 339/339 |
| `check_doc_style.py`, `--selftest` | rc 0, 22 documents |
| `check_solution_docs.py`; `check_submodule_docs.py`, `--selftest`; `submodule_boundaries.gen.py --check`; `DOC_MAP.gen.py --check`; `gen_module_matrix.py --check` | all rc 0 |
| `lint_rtl.py --check` | rc 0, 90 <= 90 |
| `check_port_contracts.py` | rc 0, 59 without a rationale, all recorded |
| `check_rtl_source_lists.py` | rc 0, 107 files, 4/4 lists |
| `gen_hdl_reference.py --selftest` and a full build (pinned parser, scratch venv) | rc 0, 44/44 arms; the reference was written |
| `behave` (tests/, as `rtl-fast` runs it) | rc 0: 404 scenarios, 1,968 steps |
| processor `tb/pp_top` `adp-config` and `--deadline-only`, plus the two arms | as in items 1 and 3 |

The clone itself was never edited. Every probe ran in a copy under the packet's scratch directory. In those copies, the only edits were the planted patch and a cap of 5 build jobs in the copy's `tb/pp_top/Makefile`. Restore verification is in `receipts/restore_verification.txt`:

- HEAD is `420b778a`, and `HEAD^{tree}` and `git write-tree` are `84537179`;
- there is no worktree or cached diff, and porcelain status is empty;
- all 980 tracked regular files rehash to their index blobs with matching modes;
- the gitlinks are `631eeb34`, `5dce647a`, `48ff7a7e` (checked out and clean) and `efeb541a` (`external`, not checked out).

Build logs had the home-directory prefix of the compiler include path replaced by `$HOME`. Nothing else in them was changed.

## Hosted evidence at this head (`receipts/hosted_check_runs.tsv`, snapshot 2026-10-03T00:06Z)

- **Complete and successful:** `rtl-fast`, `changes`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0 to 3, and Verilator shard 3/5.
- **Skipped:** the physical gPTP job, which runs nightly and on manual dispatch only. A skipped job is not executed evidence.
- **Still in progress:** `docs-check`, `elaborate`, and Verilator shards 0, 1, 2 and 4. The combined status is `pending`, and no `verilator-suites` or `yosys-portability` aggregate was emitted yet.
- The manager owns hosted and act acceptance.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 is a SUGGESTION) | Acceptance 5 against `CHANGELOG.md:39-63` and `SUBMODULES.md:108-120`. Acceptance 1 to 3 unaffected (gitlinks and generated records unchanged; boundary and submodule checks rc 0). Processor `KL_aecp_engine.sv:1723-1753`, `:3756-3808` at `631eeb34` and `:3549-3590` at `b2db3a97`. `protocol_processor_top.sv` port diff and kill face. PR #140 round 2, items 2 and 3 (Milan v1.2 §5.4.3.3 Table 5.19; IEEE 1722.1-2021 Table 9-2). DL8 base and arm | R438-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |
| RTL | CLEAN | `hdl/milan/KL_pp_shadow.sv:1094-1100`: comment-stripped diff against `3370c6cb` is empty; lint 90 <= 90; port contracts; source lists; HDL reference build. Processor `protocol_processor_top.sv:1852-1862`, `:1022-1024`; `KL_aecp_engine.sv:1606-1610`, `:1902-1929`. Parent `milan_csr.sv:752`, `:2831`; `milan_datapath.sv:7611` | R438-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |
| Robustness | CLEAN | The failure paths the delta documents, run at the pin: response-memory read error, write error, tied-off master, and a 540-byte padded echo (DL8: base passes, arm fails 4); a D3 roll-back and the reset fallback (AD6: base passes, arm fails 2). `ADP_IDX0` at reset 0, the only valid value for the one-configuration image | R438-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |
| Tests | CLEAN | No test changed in the delta. Each new documented claim is backed by a processor check that was shown to fail under its arm (DL8, AD6). The style-gate probe proves the F2 split was forced. `behave` 404 scenarios. All docs gates above rc 0 | R438-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |
| Docs | CLEAN (S1 is a SUGGESTION) | `CHANGELOG.md:39-63`; `docs/reference/SUBMODULES.md:108-120`; `docs/reference/REGISTER_MAP.md:1016`, `:2356-2370`; PR #636 body "Round 2"; author-r2 `HANDOFF.md` / `PR-BODY.md` at `37ccf808`; docs, em-dash, style, submodule, solution and map gates | R438-2 | `420b778a52e4f4bcc8040c13bbc4bef9bc94ada0` |

## Real limits

- **Manager banks, not run here:**
  - `run_all_suites.sh`, `syn/yosys/run.sh`, `test_builder.py`, `milan_dp`, `milan_dp_render`, `nvm_cosim`, `pp_shadow` and `xvlog_gate.py` (no Vivado here);
  - the builder (48) and native (5) banks, and the candidate build.
  - The brief states that the source banks passed at this head. At review time, no public comment on #635 or #636 carried those results, so this round did not inspect them.
- **Processor suites:** only the `adp-config` and `deadline` sections of `tb/pp_top` and the two named arms were run. Neither the full processor bank nor its full mutation campaigns were run.
- **Not run:** act, Docker, hosted re-runs and hardware. Physical calibration NOT RUN, and field skips are not hardware proof.
- **The parent does not re-grade these behaviours:** no parent test grades the response-memory echo or the roll-back fallback. They are graded in the processor's simulation, which the parent pins.

## Pending manager duties

- Optionally carry S1 to the residue checklist (#495), together with the REGISTER_MAP memory-bridge pointer that both round-1 F1s left optional.
- Confirm that hosted `rtl-full` and `docs` complete at this head, with `verilator-suites` and `yosys-portability` emitted and successful.
- Publish the builder and native bank results for this head.
- At the merge turn: run act and the current-dev candidate build (live `dev` `cdf49d1a`), then the post-merge containment check.
- Obtain the second positive review, from the external round, before merge. An agent may merge only with explicit maintainer authorization.

R438-2 FINISHED
