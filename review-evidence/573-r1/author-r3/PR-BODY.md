[A355]

Closes #573
Closes #574
Closes #575
Closes #576

## Status

Round 3 implementation is complete at
`8c956234699b5dec5e6c9aeada651be667974e9b` in three item-group commits.
Both full-builder modes and all required local gates returned zero.
The present mode records only the unavailable calibration report.
The absent mode also records the intentional compiler-instrument stand-down.
This body is prepared for publication; the head remains unpushed.
Independent re-review remains required across all five lenses.

## Description

Refuse reserved model identities, invalid listener buffer lengths,
oversized or mixed-family format lists, altered CRF words, and outputs
without an available INTERNAL clock source.
Refusals identify the affected declaration before artifact generation.

Literal, pinned and hash-derived model IDs reject zero and all ones.
Pins cannot hide invalid literals. Model evolution remains with #495.
Every listener buffer must lie within `2126000..0xFFFFFFFF` nanoseconds.
The final format list, including derived listener entries, permits 46 entries.
Both CRF directions require the Milan format word.
CRF may remain selected when INTERNAL is available.
Input-only clock loading retains CRF-only support.

All five tracked configurations remain accepted, including the three Arty
configurations. Their 85 generated artifacts match the baseline sizes
and SHA-256 hashes at `e0920d77162284d8da52ffaf13a973e451e44f90`.
The independent CLI inventory also matches 80/80 files.

## Round 2

The [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/573#issuecomment-5854262940)
corrected the 2021 format maximum and listener field width.
The 46-entry boundary packs into 506 octets, below the 508-octet maximum.
Listener buffers at the u32 maximum pack unchanged at every index.
The reserved-ID citations identify Milan 5.3.3.1 and 5.6.2.
Empty clock-source lists receive a named L6 refusal.
The CRF-output source requirement has a direct discriminating control.

## Round 3

The [round-3 decision](https://github.com/kebag-logic/milan-fpga/issues/573#issuecomment-5854630094)
addresses both reviewers' scalar and probe-label findings, plus strict u32 packing:

- Hexadecimal identity, destination and format values require YAML strings.
  Quote `entity_id`, `entity_model_id`, `model_id_pin`, `srp.stream_dmac_base`,
  AAF format entries and both CRF format words.
  Hex text accepts an optional `0x` prefix and underscores.
  YAML numbers and other non-strings receive a field-named `ConfigError`
  telling the user to quote the value.
  A declared null pin also refuses. Internal hash-derived IDs retain
  their reserved-value check.
- The parent audit names 46 entries/506 octets as the legal boundary.
  It labels 47 entries/514 octets as exceeding the 2021 cap.
  The processor packer's acceptance remains measured and attributed
  to processor issue 60 as defence-in-depth debt.
- Every AEM u32 packs through the unsigned encoding without masking.
  Negative and overflowing values now raise instead of truncating.
  Zero and `0xFFFFFFFF` retain their exact wire bytes.

Declaration controls exercise eight scalar paths with actual YAML text.
Both identity keys accept quoted prefixed and digit-only hexadecimal values.
All paths reject the assigned unquoted hexadecimal, decimal-looking and
octal-looking numeric spellings with the quote instruction.
Quoted parser controls preserve their digits before MAC-width or format-family
validation; complete-loader controls use valid values for those fields.

All five current mutations are killed, including restored integer acceptance
and u32 masking. Both unchanged round-2 probe scripts return zero.
The round-2 mutation banks kill 14/14 and 10/10 applicable required cases;
changed old patterns are reported as not applied and receive current replacements.
The existing optional null-clock-source test-coverage probe still survives.
The historical banks kill 30/30 and 12/12 applicable cases.
Every restored control passes and sources are restored byte-identically.

The unchanged historical format-length script prints the accepted 46-entry
boundary, then exits 1 on the required 47-entry `ConfigError`.
A separate evidence check verifies that exact expected refusal and exits zero.
Its raw nonzero exit remains explicit in the evidence.

## How to reproduce

Run `python3 sw/builder/test_declarations.py` from the repository root.
Controls start from tracked configurations and change assigned declarations.
They grade named refusals and exact packed bytes at accepted boundaries.

## How to validate

Run `python3 sw/builder/test_builder.py --require-rv32`.
Run the complete builder again through the evidence packet's `builder_absent.py`.
That wrapper hides only the three RV32 compiler candidates in process.
The absent mode records its intentional compiler-instrument stand-down.
Unavailable utilization calibration remains an explicit builder skip.

Run the declaration suite, descriptor audit and AEM store self-test.
Run RTL lint, Python idiom and naming checks.
Run documentation checks with Git and with `GIT_DIR=/dev/null`,
the em-dash gate against `e0920d77`, style, contents, anchors and paths.
Run `git diff --check` on the worktree and branch delta.
The Markdown gates use the repository's pinned dependency versions.

Fetch `573-review-evidence` and extract the reviewers' scripts with `git show`.
Run them unchanged against committed archive exports under disposable scratch.
Compare both five-configuration inventories against `e0920d77`.
The handoff records exact commands, exit statuses, mutation outcomes,
script hashes and full artifact hash tables.

## Definition of done

The assigned changes have positive, negative and boundary controls,
mutation evidence and updated authoritative documentation.
All five tracked configurations and their generated bytes are preserved.
Independent reviewers must re-cover all five lenses at the final head.
Publication, exact-head workflow evidence and candidate-merge validation
remain with the maintainer.
Processor semantic refusal remains with issue 60;
model evolution remains with #495 and processor issue 38.
