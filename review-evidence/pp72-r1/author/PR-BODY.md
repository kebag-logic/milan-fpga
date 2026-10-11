[A596] Requirement-to-test traceability: REQ tags in tb/ and a gate that fails an uncovered row

Relates to #72

Each check that verifies a row of the compliance matrix (`docs/00_MILAN_COMPLIANCE_REVIEW.md` §6)
now carries a tag statement on its own line directly above it. The tag names the row, the Ver
category of the check it labels, and the check's name as the check prints it:

```cpp
REQ_TAG("REQ-NOT-001", "STORM", "ST1b");
```

`scripts/check-req-tags.py` reads the tags out of `tb/` and the rows out of 00 §6; there is no
hand-kept list. This follows the lane owner's ruling on #72 (option 1): only a check of the row's
own Ver category traces the row. A row with no such check needs a waiver in 09 §8.10 that names one
of the row's own GAPs and gives a reason; otherwise the gate fails.

## What changes

- **The tag**: `tb/common/req_tag.hpp` (C++) and `tb/common/req_tag.py` (a Python test, at the head
  of the test method).
  - With `REQ_TAG_LOG` unset, which is every run but the gate's, a tag does nothing.
  - With it set, each tag that runs appends `suite file:line REQ CAT` to that file once.
- **The tags**: 225 in 18 suite sources, labelling the checks that verify 101 of the 109 rows whose
  Ver needs a check. The suites are `tb/pp_top`, `adp_engine`, `acmp_talker`, `acmp_listener`,
  `acmp_nvm`, `maap`, `srp_top`, `srp_decoder`, `srp_encoder`, `srp_stream_fsms`, `aecp_notify`,
  `originator`, and `desc_store` (the packer lint's tests). No check's condition, label or count
  changes.
- **The gate**: `scripts/check-req-tags.py`.
  - The static half runs in `make check` as `reqtags`, right after `matrix`, so also in the
    docs-gates job, which has no simulator. It checks that every row is traced, waived or needs no
    check; that tags are well formed, name a known REQ and category, and stand above a check that
    holds their name; that no waiver lacks a GAP of its own row or a reason, or is stale; and that
    the Cov column and the 09 §8.10 coverage table equal what it finds.
  - The executed half runs in the suites job, on that job's own `run_suites.sh` run made with
    `REQ_TAG_LOG`. Every tag's suite must PASS in that run and every tag must have run; an evidence
    line that no tag accounts for fails.
  - `--table` prints REQ, Ver, state, file:line and check name, in the order a reviewer samples them.
  - `--selftest` plants 29 faults in a scratch tree first and must see each one named.
- **The records**:
  - 00 §6: each Cov cell ends with the row's state (`traced`, `waived GAP-nn` or `no check`), and the
    column key says so;
  - 09 §8.10: the coverage table and the eight waivers;
  - 09 §2, §7 and §8 updated: REQ-ID coverage is no longer listed as future work;
  - F00.2 GAP-11 "Verified by", a GAP-11 landed note, and the REQ-VER-001 row.
- **CI** (`.github/workflows/hdl.yml`): the suites job keeps its `run_suites.sh` output and the
  evidence file, then runs the executed half.

## Coverage at head

| State | Rows |
|---|---|
| traced | 101 rows. RND: AEM-005 (`tb/originator` R), AEM-016 and NOT-002 (`tb/pp_top` RN). STORM: NOT-001 (ST1b), NOT-003 (ST2, ST2b, CS) |
| waived | AEM-019 (GAP-05), AEM-025 (GAP-06), MAAP-001 (GAP-04), MVU-003 (GAP-03), MVU-004 (GAP-03), NET-004 (GAP-05), NET-005 (GAP-04), SCP-001 (GAP-12) |
| no check | REU-001, REU-003, VER-001 (Ver —); REU-002, VER-002, DOC-001 (Ver lint) |

## Why "Relates to" rather than "Closes"

- **Acceptance 1** asks that every row with a dynamic Ver be linked to a check tag. Six of the waived
  rows carry no tag:
  - AEM-019 and NET-004: the integrator's counter banks;
  - NET-005: the integrator's AVTP discard;
  - MVU-003 and MVU-004: not implemented, under the October waiver;
  - SCP-001: a scoping statement.

  09 §8.10 gives each one's GAP and reason.
- **Acceptance 3** is replaced by the ruling. The RND and STORM rows are traced where a check of that
  category exists. Where none does (AEM-025, MAAP-001), the row is waived with its GAP. Neither case
  passes silently.

## Validation (base `2cbed0a9`; head `9540c34`, records also taken at `8b35915`; the same toolchain on both sides)

| Gate | rc base / head | Records |
|---|---|---|
| `./scripts/run_suites.sh` | 0 / 0 | byte-identical: 34 suites PASS, `suites: 1029620 checks total, 0 failing` |
| `REQ_TAG_LOG=<file> ./scripts/run_suites.sh`, then the executed half | – / 0, 0 | `run_suites.sh` output byte-identical to base; `req-tags executed: 225 evidence lines, 13 suites, OK` |
| `./scripts/lint_hdl.sh` | 0 / 0 | byte-identical |
| `make check` | 0 / 0 | every base line kept. Added: the two `reqtags` lines after `matrix`. Changed: `ids: 563 files` → `565 files` (the two new files under `tb/common`) |
| `python3 scripts/gen_matrix.py --check` | 0 / 0 | byte-identical |
| `python3 scripts/check-matrix.py` | 0 / 0 | byte-identical |
| `./syn/yosys/run.sh` | 0 / 0 | byte-identical |

- **Per-suite logs**: each suite's `make` was run with its log kept, from clean build directories, at
  base and at head. All 34 exit 0 on both sides, and every line a suite prints is identical. The only
  differences are build-tool output (compiler lines, Verilator's timing report) and one unittest
  duration.
- **Planted defects**: each was planted in the tree, gated, then restored.
  - a tag removed, so its row is uncovered → `UNCOVERED REQ-AEM-005 (RND)`;
  - a tag naming an unknown REQ → `UNKNOWN REQ REQ-ADP-099 tb/adp_engine/sim_main.cpp:964`;
  - a tag moved onto a check that never runs → passes the static half (as designed); the executed
    half then fails with `DEAD TAG REQ-FWX-001 tb/pp_top/sim_main.cpp:11078`, while that run's
    `run_suites.sh` output is identical to base;
  - a waiver without a GAP → `WAIVER WITHOUT GAP REQ-AEM-025`;
  - a REQ row added with no tag → `UNCOVERED REQ-AEM-027 (DIR)`.

  `make reqtags` exits 2 on each of the static four.
- **Mutation campaigns that build a changed file**: all 16 exit 0 at base and at head, with the same
  verdict for every arm. The four drivers that print verdicts in completion order give the same lines
  at both.
  - srp_top 137 PASS; maap 32; adp_engine 62; aecp 67; aecp_dispatch 44; ctr 18;
  - notify 93 of 93; d3 110 of 110; acmp 51 of 51 KILLED;
  - gsi 20; name_wr; name_state 16 of 16; srp_admission 12; acmp_talker retry 62; desc_store
    lint-suppression 56 of 56; desc_mem_guard.

  `tb/nvm_port`'s figures campaign builds no changed file and was not run.
- **Parent integration**: no adoption is proposed. The parent's gates that read processor files (its
  C++, Python and shell idiom, hygiene, TODO, test-evidence, control-flow, naming, fail-fast,
  submodule-docs and source-list gates) were run with its processor gitlink pointed at base and then
  at head (never committed).
  - Every gate gives the same rc at both.
  - Only population counts grow, by the three new files.
  - The three gates that fail do so identically at base: the documented pin, and one DUT-source
    reader, `tb/name_state/mutants.py`, that predates this change.
