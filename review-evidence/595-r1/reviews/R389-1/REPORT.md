[R389] NEGATIVE - exact head 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8

# R389-1: external independent review of PR #614 for issue #595

- Role: external independent reviewer [R389], round R389-1, cleared context.
- Exact head: `44d3ae3b15a0d058abb837c655ad24bd9b64c6e8`. Tree: `47a89d188ea29c1b02da4919a448423c04acb2eb`.
- Source base: `1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a`. Diff: 5 files, +198/-27, all mode 100644. There are no gitlink or configuration changes.
- Scope reconstructed from AGENTS.md, CONTRIBUTING.md, the issue #595 body (acceptance 1-5 and "Not in scope"), and the assignment comment 5867362523 with its manager decisions. I also read `sw/builder/README-parameters.md` (the PR #585 quoted-hex rule), the diff, the history, and the public evidence tree `review-evidence/595-r1` at `a3c8a9a1`.
- Prior public findings on PR #614: none. At the time of review the PR had only the two review-start notices. It had no review objects and no inline comments. So nothing needed to be resolved or retained.

## Verdict summary

The behaviour change is correct and well tested. All six judged points hold (details below):

- the string rule for `platform.mac_address` and both `_declared_uint` callers;
- the list rule for `formats`;
- the mutant kills;
- byte-identical artifacts for all five tracked configurations;
- the docs;
- no configuration value changed.

However, the PR adds a new literal submodule source path to `sw/builder/test_declarations.py`. That breaks the repository's derived-source-list contract. The required hosted `rtl-fast / verilator-lint` job fails on it at this exact head, and so does the same command run locally. At the base commit it passes. Finding F1 is open, so `Tests` and `RTL` are unclean and the verdict is NEGATIVE.

## Findings

### F1 - MAJOR - Tests, RTL - `sw/builder/test_declarations.py:231` - the new test names a protocol-processor source literally, and the required `pp_srcs.py --check` gate refuses it

- **Authority.**
  - CONTRIBUTING.md (lines ~503-515) says: "A build input never lists the protocol-processor sources, it derives them ... `--check` fails if any tracked file outside the script's `PROSE_OK` table names a submodule" source.
  - `scripts/pp_srcs.py:80-116`: `PROSE_OK` permits exact literals per file. For `sw/builder/test_declarations.py` it lists only `protocol_processor_top.sv`, `KL_srp_top.sv` and `KL_pp_prng.sv`.
  - AGENTS.md section 7 requires a successful `rtl-fast` verdict on the current PR head.
- **Evidence.**
  - Line 231 reads `(ROOT / "protocol-processor/hdl/adp/pp_adp_pkg.sv")`. That literal is new in this PR: count 0 at base, 1 at head.
  - `receipts/pp_srcs_base_vs_head.txt` runs `python3 scripts/pp_srcs.py --check --selftest` in disposable shared clones with the same processor pin `16be6768`. Base `1fa2357f` gives rc=0. Head `44d3ae3b` gives rc=1 with `sw/builder/test_declarations.py: names submodule source(s) literally that are not permitted prose: protocol-processor/hdl/adp/pp_adp_pkg.sv`.
  - Hosted: `rtl-fast / verilator-lint` at this head is `failure`. Step 7, "Prove protocol-processor source lists are derived" (`.github/workflows/rtl-fast.yml:108-109`, exactly this command), failed after step 6 (the whole-tree lint) succeeded. See `receipts/hosted_checks.txt` and `receipts/hosted_lint_job_steps.txt`. At base and at live dev `7a7582f0` this job was skipped, not run (`receipts/hosted_lint_base_dev.txt`). So the local base/head pair is the attribution evidence.
- **Why it was missed.** The assigned gate set was the builder banks and the Markdown gates, and it does not include `pp_srcs.py --check`. The public author evidence (`gates.jsonl`) lists no such run.
- **Impact.**
  - The PR head cannot hold a successful `rtl-fast` verdict, which is a section 7 completion bullet.
  - The contract exists so that a submodule bump cannot leave stale hand-written source paths behind. This literal is exactly that kind of path, and it is unregistered.
- **Required outcome.** At a new head, no tracked file names `protocol-processor/hdl/adp/pp_adp_pkg.sv` outside `PROSE_OK`. There are two ways to get there; the executor chooses:
  - derive the capabilities value through an existing authority reader;
  - or register the exact literal in `PROSE_OK` with its reason. That route touches `scripts/pp_srcs.py`, whose `--selftest` must then stay green.

  Either way, the declaration suite must still pin the capabilities value, and the three rule mutants must stay killed.
- **Verification.**
  - `python3 scripts/pp_srcs.py --check --selftest` gives rc=0 at the new head.
  - `python3 sw/builder/test_declarations.py` gives rc=0.
  - `scripts/mutants.py` shows all 12 mutants KILLED.
  - Hosted `rtl-fast / verilator-lint` is green at the new exact head.
  - `Tests` and `RTL` need re-review at that head.

### S1 - SUGGESTION - Robustness - `sw/builder/endstation_builder.py:3181-3195` (`_mac48`) - separators are deleted, not parsed as octet boundaries

- **Evidence.** `receipts/mac_unpadded_probe.txt`, identical at base and head:
  - quoted `"2:0:0:0:0:2"` resolves to `00:00:00:20:00:02`, not `02:00:00:00:00:02`;
  - `"02:00:00:00:02"` (five groups) is accepted as `00:02:00:00:00:02`;
  - `"-2"` is accepted as `00:00:00:00:00:02`.
- **Why this is not a finding.** This behaviour predates the PR. The manager decision explicitly preserves the current meaning of quoted colon and dash spellings. It is out of this lane's scope and does not affect the verdict.
- **Suggested outcome.** A new Issue could require six two-digit octets whenever a separator is present. That would refuse unpadded or short separated spellings rather than silently shifting them.

## Judged points (assignment focus 1-6)

### (1) String rule: MAC and every `_declared_uint` field

I searched the whole tree for callers myself (`git grep` / content search over `sw/`, `avdecc/`, `scripts/`, `tests/`).

**`_mac48` callers:**
- `load_platform` at `endstation_builder.py:3307-3309`. This reads raw YAML. The presence test is now `"mac_address" not in raw`, so an explicit null gets the quote instruction rather than "is required".
- `endstation_builder.py:5701`. This reads the normalised `aa:bb:..` string that `load_platform` produced, so it is not a raw path.

**`_declared_uint` callers:**
- `_vendor_oui` (`:3683-3685`) and `_verify_entity_capabilities` (`:3702-3704`). Both switched from `.get() is None` to `in`, so explicit nulls refuse.
- `:4394` already used `"vendor_oui" in ent`, which stays consistent.

**Remaining `int(str(...), 16)` sites.** `:1183`, `:1242`, `:2875`, `:2998`, `:3011`, `:3013`, `:3033` and `:3042` all read formats or CRF words after normalisation. So does `_fmt64` via `_eui64`. Neither of them is on the old path.

**Readers outside the builder.** `avdecc/gen_aemi_image.py:166`, `sw/litex/boot_policy.py:41` and `sw/builder/test_clock_contract.py:86` read only normalised overlay or cfg values.

**Messages.** Both parsers raise `<field>: quote the hexadecimal value as a YAML string`. This is byte-equal to PR #585's `_eui64` message (`:3333-3335`).

**YAML 1.1 resolution.** I checked it myself with the installed PyYAML 6.0.3 through `yaml.safe_load`, the same call `load_config` uses at `:3584` (`receipts/yaml_resolution.txt`):
- `020000000002` resolves to int 2147483650 (octal);
- `10:20:30:40:50:02` resolves to int 8041827002 (base-60);
- `1:30.5` resolves to float 90.5;
- `0b101` resolves to 5;
- `0x..` resolves to a hex int;
- `yes`, `no`, `on`, `off`, `true` and `false` resolve to bool;
- `~`, `null` and the empty value resolve to None;
- `2002-12-14` resolves to a date;
- `02:00:00:00:00:02` stays a str (the base-60 form needs a leading 1-9), and so do `08` and `001BC5`.

**Base vs head behaviour.** `receipts/behaviour_{base,head}.tsv` has 91 rows each: 31 spellings for the MAC and the OUI, 7 for capabilities, and 11 for each `formats` direction.
- At head, every non-string gets the exact quote refusal. That includes base-60, octal, binary, float, sexagesimal float, `.inf`, booleans in YAML 1.1 spellings, null, empty, list, map, `!!binary` and date.
- Every quoted spelling keeps its base value. That includes colon, dash, underscore and `0x`.
- The issue's cases are fixed: base accepted octal `020000000002` as `00:21:47:48:36:50` and base-60 as `00:80:41:82:70:02`, and head refuses both.
- Plain scalars that YAML already resolves to str (`08`, `001BC5`, `02:00:00:00:00:02`, `!!str ...`) resolve identically quoted or unquoted, so no value is reinterpreted.

### (2) Non-list `formats`

`_streams` (`:1443-1447`) is the only raw reader. It uses `s.get("formats", [])` and then `isinstance(list)`, and refuses with `<sctx>.formats: must be a list of quoted hexadecimal strings`. That message names the field and the expected list type.

- A single quoted string is refused before it can be iterated. Base iterated it and failed with the unrelated `'x' is not a hex EUI-64`.
- A scalar int or bool crashed with `TypeError` at base, and is now refused.
- Null, `0`, `{}` and `!!set` are refused. Base silently defaulted `~`, empty, `{}` and `0`.
- An omitted key or `[]` keeps the derived defaults, and list entries still go through the string rule.

The talker and listener rows are both in `receipts/behaviour_*.tsv`.

### (3) Declaration suite pins and mutants

Three new named tests exist (`test_declarations.py:189-306`) and are wired into `test_declaration_contracts` at `:512-514`: `test_station_mac_string_contract`, `test_declared_hex_string_contract` and `test_formats_list_contract`.

- They pin each refusal by exact message equality (`_yaml_refused`, `:178-186`). They assert that each probe spelling is a non-string under YAML (`:213`, `:263`).
- They pin the resolved value of each quoted spelling at the loader output, not only at the parser:
  - MAC: normalised `platform.mac_address`;
  - OUI: bits 63:40 of the hash-derived `entity_model_id`;
  - capabilities: ENTITY descriptor offset 20 of the packed `aem_desc.bin`, which matches the IEEE 1722.1-2021 ENTITY layout. The value is additionally forced by the divergence check.

`receipts/test_declarations_head.log`: rc=0.

Reviewer mutants (`scripts/mutants.py`, `receipts/mutants.tsv`) were each applied to a fresh copy of the head tree. All 12 were KILLED by named assertions:
- M1: the historical `str(v)` reread in `_mac48`;
- M2: face-value integer acceptance in `_mac48`;
- M3: an explicit null MAC treated as missing;
- M4: the dash separator dropped;
- M5: the historical `_declared_uint` integer acceptance;
- M6: a `_declared_uint` `str(v)` reread;
- M7 and M8: explicit nulls defaulted for the OUI and capabilities;
- M9: the historical scalar `formats` code;
- M10: only `str` refused for `formats`;
- M11: falsy non-lists defaulted;
- M12: any iterable accepted.

The three rules the assignment names are M1 (reread), M5 (integer acceptance) and M9 (scalar `formats`). All three were killed inside `test_station_mac_string_contract`, `test_declared_hex_string_contract` and `test_formats_list_contract` respectively.

The modified `test_builder.py` schema-1.2 fixtures now write quoted strings. I ran gates 25a and 25b in focused form: `test_schema_12_keys_reach_the_image` and `test_schema_12_refusals` both gave rc=0 (`receipts/test_builder_schema12_focused.log`).

### (4) Byte-identical artifacts for the five tracked configurations

I re-derived these myself (`scripts/artifacts.sh`, `scripts/aem_images.py`, `scripts/fragments.sh`). The base and head trees were built from `git archive` at one absolute path, with the same processor, gPTP and verilog-axis gitlink bytes.

| Artifact set | Result |
|---|---|
| Default CLI outputs | 50 files, sha256 table identical and `diff -r` raw bytes identical. Table digest `946c79c5...` for both base and head. |
| In-tree outputs | 11 identical: `adp_shape_defaults.svh` ×5, sweep fragments, `lwsrp_csr_defaults.svh`. |
| Packed `aem_desc.{bin,json,map}` | 15 identical. |
| `--write-fragment` sweep fragments | 5 identical. |
| Configuration files | 5 identical. |

Cross-check against the public author table `artifacts-after.json`: all 75 of its entries are reproduced with equal sha256 (55 + 15 + 5), and there are no differing entries (`receipts/author_hash_crosscheck.txt`, `receipts/aem_images_compare.txt`).

The configuration sha256 values are `c9d907e6...` (arty_4x4), `3cdf5b05...` (arty_8ch), `95304ca8...` (arty_current), `d2c757e2...` (ax7101_1x1_tdm8) and `ede309aa...` (ax7101_8x8). The full values are in `receipts/configs_head.sha256`.

### (5) Docstrings and builder docs

- The `_mac48` docstring (`:3182-3185`) states: quoted hex, colon and dash spellings, and non-strings must be quoted. `_declared_uint` (`:3665`) states a quoted hex field.
- `sw/builder/README-parameters.md` states the rule:
  - `:70` (quoted EUI-48);
  - `:127-130` (the `formats` list rule, defaults and quoted entries);
  - `:159-167` (all three fields; octal, base-60, booleans and nulls refused; the MAC separator examples).
- `docs/ENDSTATION_BUILDER.md:883-891` states the same, with a working anchor to the parameter guide.
- A search for statements of the old rule found none.
- Pinned Markdown gates, all rc=0 (`receipts/docs_gates.log`): `docs_check.py` with and without Git, `check_em_dash.py --base 1fa2357f`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, and `check_doc_paths.py`.

### (6) No tracked configuration value changed

`git diff --raw 1fa2357f..44d3ae3b` touches only the five files above. `configs/` is untouched, and the configuration sha256 values are equal at base and head. No tracked configuration declares `vendor_oui` or `entity_capabilities` (only a comment mentions them), and every `mac_address` is already quoted.

## Lens results

```text
[R389] PASS Conformance - issue #595 acceptance 1-5 + assignment decisions vs endstation_builder.py:1443-1447,3181-3195,3307-3309,3664-3704 at 44d3ae3b; receipts/behaviour_{base,head}.tsv, yaml_resolution.txt, artifacts_compare.txt, author_hash_crosscheck.txt - every non-string MAC/OUI/capabilities value (incl. YAML 1.1 octal, base-60, bool, null) refused with the field-named quote instruction; quoted colon/dash/underscore/0x spellings keep base values; non-list formats refused with field + list type; five configs and 81 hashed artifacts byte-identical; no config value changed
[R389] MAJOR RTL - sw/builder/test_declarations.py:231 - F1 (derived protocol-processor source-list contract broken; hosted rtl-fast/verilator-lint step 7 fails at this head). Otherwise applied: no HDL, no gitlink change (git diff --raw); generated RTL-facing outputs adp_shape_defaults.svh, lwsrp_csr_defaults.svh, lwsrp_table.svh, aecp_aem_rom.svh and gptp_ucode.hex identical base vs head
[R389] PASS Robustness - endstation_builder.py:1443-1447,3181-3195,3307-3309,3664-3704 at 44d3ae3b; receipts/behaviour_head.tsv, mac_unpadded_probe.txt - malformed, boundary and type-confused inputs (floats, .inf, !!binary, dates, lists, maps, sets, explicit nulls, empty values, over-width, negative, I/G) give named ConfigErrors, no TypeError/crash; omitted/[] formats keep defaults; S1 is pre-existing and out of scope
[R389] MAJOR Tests - sw/builder/test_declarations.py:231 - F1 (the new test violates the repository's pp_srcs gate). Otherwise applied: test_declarations.py:166-306,512-514 and test_builder.py:25544-25810 at 44d3ae3b; receipts/mutants.tsv (12/12 killed), test_declarations_head.log rc=0, test_builder_schema12_focused.log rc=0
[R389] PASS Docs - sw/builder/README-parameters.md:70,127-130,159-167; docs/ENDSTATION_BUILDER.md:883-891; endstation_builder.py:3182-3185,3665 at 44d3ae3b; receipts/docs_gates.log (7 pinned Markdown gates rc=0) - the rule is stated for all three fields and for formats, the separator/0x/underscore claims match the code, and no stale statement of the old rule remains
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #595 acceptance and assignment; `endstation_builder.py` parsers and every caller; YAML resolution; base/head behaviour matrix; artifact identity for 5 configs (81 entries) | R389-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |
| RTL | UNCLEAN (F1) | `scripts/pp_srcs.py` contract with base/head runs; hosted `rtl-fast/verilator-lint` steps; `git diff --raw` (no HDL, no gitlink); generated `.svh` and `gptp_ucode.hex` identity | R389-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |
| Robustness | CLEAN (S1 is a suggestion only) | `_streams`, `_mac48`, `load_platform`, `_declared_uint`, `_vendor_oui`, `_verify_entity_capabilities`; 91-row behaviour matrix; unpadded-MAC probe | R389-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |
| Tests | UNCLEAN (F1) | `test_declarations.py:166-306`, `:512-514`; `test_builder.py` schema-1.2 fixtures; 12 mutants; suite and focused gate runs | R389-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |
| Docs | CLEAN | `README-parameters.md`, `ENDSTATION_BUILDER.md` section 3, docstrings; 7 pinned Markdown gates | R389-1 | 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 |

A fix for F1 touches `sw/builder/test_declarations.py`, and possibly `scripts/pp_srcs.py`. That falls inside the `Tests` and `RTL` scopes, which must be re-covered at the new head. Conformance, Robustness and Docs stay banked at `44d3ae3b` only if the fix commit changes nothing within their scope. The builder source, the docs and the parser behaviour would have to be untouched.

## Real limits

- I did not run the full builder bank (`test_builder.py --require-rv32 --require-elaboration`), the compiler controls, or any parent, PP, gPTP or Yosys bank; the assignment disallowed them. For the builder I ran only `test_declarations.py`, the two schema-1.2 gate functions, and the five-config builds. I relied on the public author and manager bank evidence for the rest.
- I did not use Verilator (the PR contains no HDL), so I did not verify the scoped binary's identity.
- I used no Docker or act.
- Hosted checks were inspected at one moment (`receipts/hosted_checks.txt`). At that moment 10 were success, 1 was failure (`verilator-lint`), 1 was skipped (Physical gPTP), and 7 were still in progress: `docs-check`, `elaborate`, Verilator shards 0, 1, 2 and 4, and `yosys-elaboration`. The failing job's full log was not retrievable. I took the step-level status from the jobs API and reproduced the failing command locally.
- YAML resolution was checked with the locally installed PyYAML 6.0.3 (libyaml present, pure-Python `SafeLoader` via `safe_load`). The CI workflows install an unpinned `pyyaml`, and I did not test other versions.
- Physical calibration was not run, and field skips are not hardware proof. The gate-11 calibration arm shown in the author evidence did not run.
- My default CLI build emits 50 files per the five configs. I obtained the author's other 20 entries through `_entity_model_image` and `--write-fragment`, which may not be byte-for-byte the author's invocation path. The hashes nonetheless match the published table.

## Pending manager duties

- Route F1 to the executor. Require re-review of `Tests` and `RTL` at the corrected exact head.
- Own the hosted and act acceptance at the corrected head. Distinguish executed jobs from skipped contexts. `verilator-lint` at base and dev was skipped, not passed.
- Build and validate the final current-dev candidate at the merge turn: source base `1fa2357f`, live dev `7a7582f0`. This includes the #577 / PR #612 builder collision noted in the assignment.
- Merge requires two independent POSITIVE reviews and explicit maintainer authorisation. Consider filing S1 as a new Issue.

## Packet contents

- `scripts/`: `yaml_resolution.py`, `mutants.py`, `artifacts.sh`, `aem_images.py`, `fragments.sh`, `behaviour_matrix.py`, `mac_unpadded_probe.py`, `pp_srcs_base_vs_head.sh`.
- `receipts/`: raw outputs, with local absolute paths redacted to `$PACKET`, `$CLONE` and `$DATA`.
- `MANIFEST.sha256` lists every publishable file.
- After the probes, the reviewed clone was verified at the exact head (`receipts/clone_integrity.txt`):
  - 943 tracked blobs re-hashed with 0 mismatches;
  - `git diff-index HEAD` is clean for content and mode;
  - the gitlinks are unchanged: protocol-processor `16be6768`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`, external `efeb541a` (uninitialised);
  - the 18 session-created bytecode files were removed.

R389-1 FINISHED
