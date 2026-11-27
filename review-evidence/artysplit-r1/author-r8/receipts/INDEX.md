# Round 8 receipt index

Head `011aaa6f080321e0a89f915720ebb3ee14807a16`. The census, image and qualification are round 7's, at `74f942be516b84915f7d982fe1e3c65b497c227a`.
Round 8 changes only documentation, comments, the receipt regrader and a new extractor.
Prepared locally; nothing has been posted or pushed.

[FILES.manifest.json](FILES.manifest.json) and its numbered `FILES.tsv` parts list all 814 other files with bytes and SHA256.
Outside `census-extract/`, each receipt is redacted text; [MANIFEST.json](MANIFEST.json) gives each file's hash before and after redaction.

## Compact census extract

[census-extract/](census-extract/census.json): all 147 cases, 762 files, 1,434,762,896 bytes, largest file 13,999,999 bytes.
Each case directory holds `manifest.json`, `scenario.json`, `stimulus.txt`, `original-grade.json`, any `journal.hex.txt` and `observations.log` (numbered parts above 14 MB).
The scenario, stimulus, grade and journal are byte for byte round 7's.
The observations are round 7's extract less the SPAN and CALL lines of traced functions no grader reads; every other line is kept unchanged and in order.
The read set is `census_extract.READ_LABELS`, built from the graders' own constants.
Each case manifest names the full extract it came from (`full_extract`: bytes and SHA256).
[census-extract/FILES.json](census-extract/FILES.json) maps every extract file to the round-7 packet files it comes from, each with the SHA256 the round-7 `FILES.tsv` lists (checked by the extractor).

Reproduce from a checkout of the head:

```sh
python3 tb/verilator/ctrl_service_budget/receipt_regrade.py census-extract
```

- [proofs/extract.log](proofs/extract.log): the extractor regraded each of the 147 cases to its recorded grade.
- [proofs/extract-regrade.log](proofs/extract-regrade.log): 147/147 grades reproduced, cross-case PASS, worst pass 142775 cycles.
- [proofs/extract-control.log](proofs/extract-control.log): the extract without `srp-bound` is refused; #969's disposition names its own breach.
- [proofs/proof-comparison.json](proofs/proof-comparison.json) compares both runs against round 7's full-census runs ([proofs/round7-receipt-regrade.log](proofs/round7-receipt-regrade.log), [proofs/round7-receipt-regrade-control.log](proofs/round7-receipt-regrade-control.log)).
  The regrade is identical line for line; the full run's 13 timing lines are set aside, because the extract carries no timing reports.
  The control is identical apart from the regrader's own traceback frame line numbers.
- Why 1.43 GB is the floor for original lines: [extract-floor/filtertest.log](extract-floor/filtertest.log).
  Keeping only the read labels reproduces every grade. Dropping read-label lines outside work passes does not: the grades count every pass's polls, rounds and slices (for example 44025 polls passes, against 1122 inside work passes).

## No-disposition control derivation

[control-derivation/](control-derivation/): round 7's 147 traces, with every `srp-kept`/`srp-bound` record counted, on the same merged maxima.
[derive-no-disposition.json](control-derivation/derive-no-disposition.json): NO QUALIFIED MODEL. All 52 candidates fail an owner bound; the least last queued notice is 225.54 ms, against 140; load 0.6206.

## Paired step identity

[identity/paired-identity.md](identity/paired-identity.md) and [.json](identity/paired-identity.json) give each variant's native executable and firmware ELF, hashed from step 1's (`f7b90e3b7`) and step 2's (`74f942be5`) own files, side by side, with each case's stimulus.
For step 2 the stimulus is the script its own build's scenario writes. All identical.
`flash_image` is null at both steps: `build.build` writes a separate flash image only for an XIP core (`core.xip`, `xip_image`). The native census builds are not XIP, so the firmware is in the ROM init files the executable is built from.

## Post-route utilization

[route-utilization/](route-utilization/): `report_utilization` on the retained routed checkpoints (Design State `Physopt postRoute`), with no implementation step.

| Image | Routed checkpoint SHA256 | Bitstream SHA256 | Slice LUTs | Registers | Slices | BRAM tiles |
|---|---|---|---:|---:|---:|---:|
| Round 7 (`74f942be5`) | `1bbc99779c5de6ae18f6f8fd0c3a610e34eca148c7b9a44c2a584a1f5ca9233e` | `24a782c505c1ae4aea61d2abf1b1dd2e2cf0e5aa08e12a717e10cfddb37a871e` | 33015 | 40369 | 13791 | 78 |
| Round 6 (`49b534fc9`) | `6c82a59508c5ea2a1c932c498682b4800e3b2e1e9d65fce13d573796c6ddca5a` | `b5068ecb304b2fabfe5f46796b7ea9e333e4d699b482b90605b8e469cf354f43` | 33015 | 40369 | 13791 | 78 |

Routed-total LUT delta: 0, inside the ~50-LUT band.

## Gates at the head

[gates/](gates/gates8.rc): documentation, inventory, style, paths, gPTP docs, Python and C++ idiom, em-dash and TOC checks. Also the `rows_tiers`, `load_grade`, `egress_ledger`, `record_classes`, `arty_grade` and `kept_grade` self-tests, the `arty_grade` model, and the mutant fixtures' values identical across their comment change. All exit 0.
The split configuration's generated outputs are unchanged by its comment edits ([gates/builder-split.log](gates/builder-split.log)).

## Recipes

[recipes/](recipes/) holds the inventory, filter-test, packing and gate scripts, redacted.
