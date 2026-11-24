STATUS: LOCAL VALIDATION COMPLETE

# [A837] REVIEW READY: PR #966, round 2 (R883-4-F1)

Commit: `0acf24d9b5060a263f725c02026446dde64c2574`, a single local commit on `44c566399002db32bf8a6ad3ce719488d418bcb0`.
Branch: `884-gptp-firmware`; PR base: `dev-soft-core-optimisation`. Not pushed. I make no PR edit or review verdict.

Subject: `Make the software gPTP AVB test fail when the datapath's AS_CAPABLE leaks through` (one line, no trailers).

## Delta from 44c56639

Tests only: `git diff --stat 44c56639 0acf24d9` touches two files, both under `sw/firmware/ctrl/test/` (+27/-15).
No product C, RTL, config, ratchet or doc file changed (`receipts/product-scope.txt`, `receipts/delta.diff`).

- `sw/firmware/ctrl/test/test_aecp.cpp`
  - `Far` gains `avb_flags` (default `0x7a`, the value the fixture answered before). `Far::word()` serves it as
    GET_AVB_INFO's flags byte (GSI kind 1, selector 1) instead of the literal `0x7a`. Every other test sees the
    same word as before.
  - `Face.SoftwareGptpAvbKeepsTheDatapathsLinkAndClass` now runs, on each interface, datapath bit 0 clear (`0x7a`)
    and set (`0x7b`) against the owner's asCapable true and false. So all four agree and disagree cases are covered,
    including the two R883-4-F1 names: datapath set with owner not capable, and datapath clear with owner capable.
  - The old single flags check is now two checks with separate words:
    - `flags & ~1` equals `0x7a`, words "software gPTP keeps the datapath's link flags" (unchanged).
    - `flags & 1` equals the owner's value, words "AS_CAPABLE is the software gPTP owner's, whatever the datapath's
      bit 0 (<bit>)" (new).
- `sw/firmware/ctrl/test/aecp_face_mutants.py`: the new row `face-software-gptp-keeps-datapath-capable` plants
  `out->flags | (as_capable ? 1u : 0u)` (mask dropped) in `aecp_face.c:212`. The campaign grades it on the AVB test
  with the words "AS_CAPABLE is the software gPTP owner's".

## The planted leak

| Run | Tests at | Result | Receipt |
|---|---|---|---|
| Leak planted, graded on any failure of the AVB test | `44c56639` | **ESCAPED**: `[ OK ]`, verdict PASS, as F1 reports | `plant-old.log`, `plant-old-leak.excerpt.log` |
| Leak planted, graded on the new words | `0acf24d9` | **caught**: 2 failures, both "AS_CAPABLE is the software gPTP owner's, whatever the datapath's bit 0 (1)", one per interface; 0 link-flag failures | `plant-new.log`, `plant-new-face-software-gptp-keeps-datapath-capable.excerpt.log` |
| `face-software-gptp-clears-link-flags` | `0acf24d9` | caught on its own words; 0 AS_CAPABLE failures | `plant-new-face-software-gptp-clears-link-flags.excerpt.log` |
| `face-software-gptp-ignores-path-refusal` | `0acf24d9` | caught on its own words | `plant-new.log` |
| Unplanted AVB test, 1 and 2 interfaces | `0acf24d9` | passes, rc 0 | `plant-new.log` |

The two existing face plants each fail one check only, and the leak fails the other check only. So each check is
graded by name and words, and neither check's words can stand in for the other's.

## Validation (all at `0acf24d9`, each firmware run in its own clean clone)

| Check | rc | Wall time | Receipt |
|---|---:|---|---|
| `fw_coverage.py --check --jobs 4` | 0 | 13:59 to 14:13 | `coverage-check.log`, `.rc` |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4` | 0 | 13:51 to 14:10 | `fw-shard-0.summary.log` |
| same, shard 1/4 (828 control plants, 0 escaped) | 0 | 13:48 to 15:30 | `fw-shard-1.summary.log` |
| same, shard 2/4 (AECP campaign incl. all three software-gPTP face rows, 0 escaped) | 0 | 13:48 to 14:27 | `fw-shard-2.summary.log` |
| same, shard 3/4 | 0 | 13:48 to 14:42 | `fw-shard-3.summary.log` |
| Plant proof (`plant_proof.py` old, then new) | 0 | 13:45 to 13:48 | `plant-*.log`, `plant-results.json` |
| `scripts/check_py_idiom.py` | 0 | | `py-idiom.log` |
| `git diff --check 44c56639 HEAD` | 0 | | `diff-check.log` |

Coverage figures are the same as at `44c56639`. `aecp_face.c` is 229/229 lines and 204/204 branches, `mbx.c`
384/384 and 202/202, `ctrl_plat.c` 224/226 and 110/116 raw, 100 % after exclusions, `gptp.h` 2/2 and 0/0, and `gptp.c`
665/704 and 346/437. The run reports `firmware coverage: PASS (42 files)`. `sw/firmware/gtest/coverage.ratchet` is
unchanged, so no recorded figure is lowered. The full AECP campaign's table-drift control ran inside the shards
with the new row in the table. Each shard summary records the full log's sha256 and the clone head.

## Not done or not claimed

- No push, PR comment, PR-body edit, hosted run, act replica or bench.
- R883-4-R1 to R3 (wording residue) and S1 are out of this round's scope and untouched.
- Boundary legs, docs workflow, Yosys and LiteX were not re-run. The delta changes only the two test files above,
  and those are read by the firmware gate and the AECP campaign, both of which ran here.

Open risks/questions: none.
