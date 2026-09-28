[R388] NEGATIVE - exact head 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8

# R388-1: internal independent review of PR #614 / issue #595

- Head under review: `44d3ae3b15a0d058abb837c655ad24bd9b64c6e8`, tree `47a89d188ea29c1b02da4919a448423c04acb2eb`.
- Source base: `1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a`.
- Role: internal reviewer, cleared context, own detached clone. Round R388-1.
- Authorities read: AGENTS.md, issue #595 body (acceptance 1-5, not-in-scope), assignment comment 5867362523 (manager decisions), executor TAKEN / REVIEW READY comments, PR #614 body, the PR #585 quoted-hex rule in `sw/builder/README-parameters.md` (Entity identity section), `scripts/pp_srcs.py`, and the public evidence tree `review-evidence/595-r1` at `a3c8a9a1`.
- Prior public review findings on PR #614 before this round: none. The PR carries only the review-start comment. It has no review objects and no inline comments. Nothing to resolve or retain.

## Verdict

NEGATIVE. The product change is correct. It meets issue acceptance 1-5 and every manager decision, as shown below. However, the head fails a repository gate that is part of the required `rtl-fast` workflow. The new declaration test names a protocol-processor source path literally, and `scripts/pp_srcs.py --check` refuses this. The failure reproduces locally at this head, and the base commit is clean (finding F1). Under AGENTS.md section 7, the current PR head must have a successful `rtl-fast` verdict, and existing regressions must stay green.

## Findings

### F1: MAJOR. Lenses: Tests, RTL

- **Location:** `sw/builder/test_declarations.py:231`, which reads `source = (ROOT / "protocol-processor/hdl/adp/pp_adp_pkg.sv").read_text()`.
- **Authority and evidence:**
  - `scripts/pp_srcs.py` (`PROSE_OK`, `check()`) forbids any tracked non-Markdown file outside the submodule from naming a submodule source literally unless its `PROSE_OK` entry lists that exact literal. The rule prevents stale source copies after a submodule bump.
  - `PROSE_OK["sw/builder/test_declarations.py"]` permits three literals. `protocol-processor/hdl/adp/pp_adp_pkg.sv` is not one of them. It is permitted only for `sw/builder/test_builder.py`.
  - Hosted `rtl-fast`, job `verilator-lint` (run 36408739329, job 108883709381, head_sha `44d3ae3b…`), was executed, not skipped. Step 7 "Prove protocol-processor source lists are derived" (`python3 scripts/pp_srcs.py --check --selftest`) failed with exit code 1 and this message: `sw/builder/test_declarations.py: names submodule source(s) literally that are not permitted prose: protocol-processor/hdl/adp/pp_adp_pkg.sv`.
  - The failure reproduces in the exact-head clone (rc=1, `receipts/pp_srcs_check.txt`). I also ran the same `check()` over the git blobs of each commit. The base `1fa2357f` has 0 findings and the head has 1 (`receipts/pp_srcs_base_vs_head.txt`, `scripts/pp_srcs_at_commit.py`).
  - This PR introduced the regression. The executor's 19-gate list (`review-evidence/595-r1/author/gates.jsonl`) does not include this check. The manager's builder, Markdown and native banks do not exercise it either.
- **Lens attribution:** Tests, because an existing repository regression is no longer green. RTL, because the violated contract is the repository's derived-submodule-source contract with the pinned protocol-processor, and it is enforced in the RTL lint job. That is an existing module/interface contract.
- **Impact:** the required `rtl-fast` context is red at this head, so the completion bar in AGENTS.md section 7 cannot be met. If the rule were simply bypassed, a future move of `pp_adp_pkg.sv` in the submodule would break this suite, which is the silent staleness the gate exists to name.
- **Required outcome:** `python3 scripts/pp_srcs.py --check --selftest` returns 0 at the corrected head. Either the literal gets its own `PROSE_OK` entry with a stated reason, following the precedent for `test_builder.py`, or the test obtains the constant without naming the path. This must not weaken the independent read of `ADP_ENTITY_CAPS_C` that the capabilities round-trip relies on. No product behaviour should change.
- **Verification:** at the new head, `pp_srcs.py --check --selftest` returns rc 0, `test_declarations.py` returns rc 0, and hosted `rtl-fast` `verilator-lint` succeeds on the exact head.

### S1: SUGGESTION. Lens: Robustness (pre-existing, out of scope)

- **Location:** `sw/builder/endstation_builder.py:3188-3190` (`_mac48`) and `:3669` (`_declared_uint`).
- **Evidence:** quoted strings are still parsed leniently. `"-2"`, `"0:2"` and `"2"` resolve to MAC `00:00:00:00:00:02`, because `-` is stripped as a separator. `" 020000000002 "` is accepted with its whitespace, and `vendor_oui: "+1BC5"` is accepted.
- **Scope:** base behaves identically (`receipts/edge_probe_base.txt` against `receipts/edge_probe_head.txt`). The acceptance asks that quoted spellings keep their current meaning, so this is not a defect of this PR.
- **Recommendation:** optionally, a separate issue could consider requiring a six-octet MAC shape and rejecting signs and whitespace.

### S2: SUGGESTION. Lens: Docs

- **Location:** `docs/ENDSTATION_BUILDER.md:883` ("require quoted YAML strings") and `sw/builder/README-parameters.md:70` ("quoted EUI-48").
- **Evidence:** the loader sees only resolved types. A plain scalar that YAML 1.1 resolves to a string is accepted, which is consistent with the PR #585 rule. Examples are unquoted `02:00:00:00:00:02`, `001BC5`, `0000C588` and list entry `[0205022000806000]` (`receipts/edge_probe_head.txt`, `receipts/yaml_resolution_local.txt`).
- **Impact:** the "quote it" instruction is safe guidance, and the README Entity-identity text states the rule precisely ("require YAML strings", "non-strings receive a named quote instruction"). The only gap is the word "quoted" in the summary lines. Not blocking.

## Assignment judgements (1)-(6)

(1) The string rule is met for the MAC and every `_declared_uint` field.
- **Call sites:** I searched the whole tree for `_mac48` and `_declared_uint`.
  - `_mac48` has two callers: `load_platform` (`endstation_builder.py:3309`, raw YAML value) and the gPTP microcode step (`:5701`, re-parsing the normalized `aa:bb:…` string, always a `str`).
  - `_declared_uint` has two callers: `_vendor_oui` (`:3685`) and `_verify_entity_capabilities` (`:3704`).
  - No caller remains on the old path. No other module parses raw `platform.mac_address`, `entity.vendor_oui` or `entity.entity_capabilities`. `avdecc/gen_aemi_image.py:166`, `sw/litex/boot_policy.py:41` and `endstation_builder.py:4913` read the normalized overlay or config string.
- **Guards:** both functions refuse every non-string with `"<field>: quote the hexadecimal value as a YAML string"`, which is PR #585's `_eui64` text. The `int(str(v), 16)` reread and integer acceptance are gone.
- **Explicit null:** presence tests changed from `is None` to `not in`, so an explicit null now receives the quote instruction instead of "required" (MAC) or a silent default (OUI and capabilities). The docs state this.
- **YAML 1.1 resolution:** checked myself against the local PyYAML 6.0.3, the same version as the pinned Markdown venv; CI installs unpinned `pyyaml` (`receipts/yaml_resolution_local.txt`).
  - `020000000002` resolves to int 2147483650 (octal), and `10:20:30:40:50:02` to int 8041827002 (base-60).
  - `yes`, `on` and `off` resolve to bool, `2026-09-28` to date, `1:30.5` to float, and `0x…` to int.
  - `02:00:00:00:00:02`, `001BC5` and `0205022000806000` resolve to str.
- **Refusals:** the loader refuses every non-string I tried (octal, base-60, hex int, `0b`, bool `yes/on/off/true/false`, null `~`/`null`/empty, float, `.inf`, sexagesimal float, date, `!!binary`, list, mapping), each with the exact field-named message (`receipts/edge_probe_head.txt`). At base, an unquoted date was silently accepted as MAC `00:00:20:26:09:28` and `0b10` as `00:00:00:00:00:02` (`receipts/edge_probe_base.txt`).
- **Quoted MAC spellings:** colon, dash, underscore, `0x` and plain spellings keep their meaning.

(2) Non-list `formats` is met.
- `_streams` (`endstation_builder.py:1443-1446`) refuses any declared non-list with `"<stream>.formats: must be a list of quoted hexadecimal strings"` before defaulting or iterating.
- That covers a single quoted string, an int, bool, null, empty scalar, float, mapping, `!!set` and date. Omitted `formats` and `[]` keep the derived default.
- Entries still go through `_fmt64`, so a non-string entry gets the quote refusal.
- The emitters that read `formats` later (`:2997-3013`) receive the normalized config only.

(3) The suite pins the refusals and resolved values, and mutants are killed.
- `test_station_mac_string_contract`, `test_declared_hex_string_contract` and `test_formats_list_contract` pin exact refusal messages (string equality) for each non-string spelling. They also pin the resolved value of each quoted spelling through the loader: the normalized MAC, `entity_model_id >> 40` for the OUI, and the ENTITY descriptor bytes in the packed image for capabilities.
- The capabilities value is read independently from `pp_adp_pkg.sv`. That read is the literal behind F1.
- The suite passes at head (`receipts/test_declarations_head.log`, rc 0).
- I wrote and ran 14 mutants of my own (`scripts/mutants.py`, `receipts/mutants.txt`) on a disposable copy, with an unmutated control (rc 0) and a restored control (rc 0). All 14 are killed by named assertions. They include:
  - M1, the `int(str(v), 16)` MAC reread, killed at `_yaml_refused` "accepted 0x000000F42402".
  - M5, integer acceptance in `_declared_uint`, killed at "accepted 0x123456".
  - M6, a `_declared_uint` str reread, killed by exact-message mismatch.
  - M7, scalar `formats`, killed by exact-message mismatch against the family refusal.
  - M8 and M9, falsy-scalar defaulting and string wrapping.
  - M10 to M12, reverting null handling.
  - M13 and M14, call-site `str()` coercion.
  - M2 to M4, other `_mac48` regressions.
- The focused `test_builder.py` gates 25a and 25b, whose cases this PR re-spelled as strings, pass at head (`receipts/test_builder_schema12_head.log`).

(4) Artifacts are identical before and after. I re-derived them myself.
- I built the five tracked configurations from disposable base and head trees. They are identical except for the five PR files, and the configs, submodules, `hdl` and `avdecc` show no diff between the commits.
- Builder CLI output is 50 files: base and head sha256 lists are identical and `diff -r` is clean (`receipts/artifact_compare.txt`, `artifacts_{base,head}.sha256`).
- The paired descriptor image set (`aem_desc.bin/.json/.map`) and the normalized loaded config are 20 hashes, identical at base and head (`model_images_{base,head}.sha256`).
- The sweep fragments (`--write-fragment`) are 5 files, identical (`fragment_compare.txt`).
- All 70 artifact hashes the executor published, plus the 5 config-file hashes, match mine (`crosscheck_public_inventory.txt`, `fragment_compare.txt`).

(5) Docs are met.
- The `_mac48` docstring (`:3182-3185`) and the `_declared_uint` docstring (`:3665`) state the rule.
- `docs/ENDSTATION_BUILDER.md:883-891` and `sw/builder/README-parameters.md` (lines 70, 127-130 and 159-167) state the string rule, including octal, base-60, booleans and nulls. They also cover the MAC separators, the list rule and the defaults.
- The pinned Markdown gates return rc 0 at head: doc style, em-dash, TOC `--check` and `--verify-anchors`, doc paths, and `docs_check` (`receipts/doc_gates_head.txt`).

(6) No tracked configuration value changed. `git diff 1fa2357f..44d3ae3b` touches only the five listed files; `configs/` is untouched and the five config-file sha256 values match the public inventory.

## Reviewer-owned lens ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #595 acceptance 1-5 and assignment decisions against `endstation_builder.py:1443-1446, 3181-3200, 3307-3309, 3664-3704, 5701`. YAML 1.1 resolution receipts, edge probes, artifact identity receipts, and `git diff 1fa2357f..44d3ae3b -- configs` (empty). | R388-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |
| RTL | UNCLEAN (F1) | No HDL in the diff, and `hdl/`, gitlinks and `avdecc/` are unchanged against base. Generated SV headers (`adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `lwsrp_*.svh`) are byte-identical. The derived-submodule-source contract (`scripts/pp_srcs.py`) is violated by `test_declarations.py:231`, and hosted `rtl-fast` `verilator-lint` step 7 fails. | R388-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |
| Robustness | CLEAN (S1 is a suggestion) | `receipts/edge_probe_{base,head}.txt`: 39 malformed, boundary or type-confusion spellings across four fields. Null and omitted handling at `:3307`, `:3683` and `:3702`, and nested and non-string list entries. Head refuses everything base mishandled, with no crashes. | R388-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |
| Tests | UNCLEAN (F1) | `sw/builder/test_declarations.py:163-306, 509-511` and `sw/builder/test_builder.py:25544-25811`. The suite passes (rc 0), 14/14 reviewer mutants are killed, and gates 25a/25b pass. The existing regression `scripts/pp_srcs.py --check --selftest` fails at head and passes at base. | R388-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |
| Docs | CLEAN (S2 is a suggestion) | `docs/ENDSTATION_BUILDER.md:883-891`, `sw/builder/README-parameters.md:70, 127-130, 159-167`, and the docstrings at `endstation_builder.py:3182-3185, 3665`. Pinned Markdown gates rc 0. The PR and issue evidence is sufficient for a cold reviewer. | R388-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |

## Real limits

- I did not run the full parent, protocol-processor, gPTP, Yosys or builder banks; the assignment forbids them. The full `test_builder.py` bank result is the manager's evidence, not mine.
- I did not use Verilator, because the diff contains no HDL, so I did not verify its identity. There were no Docker, `act` or host `act_ci` runs.
- PyYAML resolution was checked against 6.0.3 only. CI installs an unpinned `pyyaml`.
- Hosted snapshot at 2026-09-28T10:24:59Z (`receipts/hosted_checks_snapshot.txt`):
  - `verilator-lint` executed and failed.
  - `bdd-conformance`, `changes`, `wire-accountability`, `docs-check-no-git`, `full-ci-gate`, Yosys shards 0-3 and Verilator shard 3 had succeeded.
  - `docs-check`, `elaborate`, `yosys-elaboration` and Verilator shards 0, 1, 2 and 4 were still in progress.
  - "Physical gPTP" was skipped.
  - Skipped contexts are not evidence.
- Physical calibration was not run. Field skips are not hardware proof.
- This is a source-base review. The current-dev candidate merge (live dev `7a7582f0`, with the possible #577 / PR #612 builder collision) has not been validated by me.

## Clone integrity after probes

All probes ran on disposable copies under `scratch/`. The clone still has HEAD `44d3ae3b…` and tree `47a89d18…`, a clean status, and no index or worktree diff. The five changed files' blobs match `HEAD:` with mode 644. The gitlinks are unchanged: external `efeb541a`, gptp-processor `5dce647a`, protocol-processor `16be6768`, third_party/verilog-axis `48ff7a7e` (`receipts/clone_integrity.txt`).

## Pending manager duties

- Route F1 to the executor, then re-review the corrected head. F1 un-covers Tests and RTL. A fix touching `scripts/pp_srcs.py` or the test file also needs Tests re-covered at that head.
- Hosted and `act` acceptance on the exact head, including a green `rtl-fast` `verilator-lint`.
- The external review (R389).
- Validation of the current-dev candidate merge and any #612 integration.
- Post-merge containment.

R388-1 FINISHED
