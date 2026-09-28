[A417]

Closes #595

## Status

Implemented locally at `44d3ae3b15a0d058abb837c655ad24bd9b64c6e8`.
Assigned local gates return zero at this head.
Independent review and publication remain with the maintainer.

## Description

Unquoted YAML integers could silently change the station MAC or OUI.
Require hexadecimal strings for `platform.mac_address`, `entity.vendor_oui`
and `entity.entity_capabilities`. Every declared non-string receives a
field-named quote instruction, including booleans and explicit nulls.
Quoted MAC strings retain colon and dash spellings.

Require lists for declared AAF `formats` fields. Reject scalar strings
before iteration and other non-lists before defaulting. Omitted and empty
lists retain their existing derived defaults.

## How to reproduce

Run `python3 sw/builder/test_declarations.py` from the repository root.
For example, unquoted `020000000002` now receives the MAC quote refusal.
Quoted `"020000000002"` resolves to `02:00:00:00:00:02`.

## How to validate

Run `python3 sw/builder/test_builder.py --require-rv32 --require-elaboration`.
Run the declaration suite and compiler controls, including absent mode.
Run the documentation checks with the pinned Markdown environment.
The handoff records all 19 commands, results and log hashes.

## Definition of done

All 233 focused loader cases pass; three historical mutants are killed.
The five tracked configurations and 70 generated artifacts match baseline.
Configuration values and the processor pin remain unchanged.
The full builder bank reports one unrun calibration arm: its report is absent.
Compiler-absent controls record their intended instrument stand-downs.
Independent review, publication and merge remain pending.
